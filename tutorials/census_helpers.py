"""Helper for the PGDW census tutorials. Built in Census Data in Python, Part 1."""

import os

import polars as pl
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")


def get_census(dataset, year, variables, geo_for, geo_in=None):
    """Request data from the Census API and return a clean Polars DataFrame.

    variables maps new column names to Census variable IDs, for example
    {"median_income": "B19013_001E"}.
    """
    url = f"https://api.census.gov/data/{year}/{dataset}"
    params = {
        "get": ",".join(["NAME", *variables.values()]),
        "for": geo_for,
        "key": API_KEY,
    }
    if geo_in is not None:
        params["in"] = geo_in

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError(f"Census API error: {response.text}")
    if response.url.endswith("_key.html"):
        raise ValueError(f"Problem with your API key. See {response.url}")

    rows = response.json()
    df = pl.DataFrame(rows[1:], schema=rows[0], orient="row")

    # Geography columns (state, county, tract, ...) come after the variables
    geo_cols = df.columns[len(variables) + 1:]
    new_names = list(variables.keys())

    return (
        df
        .rename(dict(zip(variables.values(), new_names)))
        .with_columns(
            pl.col(new_names).cast(pl.Float64),
            pl.concat_str(geo_cols).alias("GEOID"),
        )
        .with_columns(
            pl.when(pl.col(c) < 0).then(None).otherwise(pl.col(c)).alias(c)
            for c in new_names
        )
        .select("GEOID", "NAME", *new_names)
    )
