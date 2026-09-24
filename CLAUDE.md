# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Quarto website for the Public Good Data Wrangle (PGDW), a one-day data science hackathon for Davidson College students run by the Department of Data Science and the Institute for Public Good. It's published at https://datasci.davidson.edu/datawrangle.

## Commands

- `quarto preview`: local dev server with live reload
- `quarto render`: full build into `docs/`
- CI runs `quarto render --profile release --cache-refresh` in the `rocker/verse` container. There's no `_quarto-release.yml`, so the profile currently changes nothing.

The repo has no tests and no linter.

## Architecture

- **Mostly one page.** `index.qmd` holds the whole site. The navbar in `_quarto.yml` links to anchors in it (`#about`, `#location`, `#schedule`, `#faq`, `#sponsors`). If you rename or add a section, update the navbar anchors too.
- **Page structure.** The hero section uses Quarto's `about` template (`jolla`), which targets the `#hero-heading` div. The FAQ is defined as YAML in the `accordion:` front-matter key and rendered with `{{< accordion faq >}}`, using the `royfrancis/accordion` extension. To change the FAQ, edit the YAML, not the page body. A countdown uses FlipDown, loaded from a CDN in `include-in-header`. `_extensions/` also includes a carousel extension.
- **Event variables.** `_variables.yml` stores per-year values (`pgdw.date`, `pgdw.term`), which pages read with `{{< var pgdw.* >}}`. The countdown script reads `pgdw.iso_date` (shortcodes do expand inside the raw `{=html}` block) and looks up the America/New_York offset at runtime. The hero `links` date in `index.qmd` is still hard-coded. Check those when rolling the site over to a new year.
- **Styling.** The theme is `materia` plus `styles.scss`, with Atkinson Hyperlegible as the main font. The goal is to look like the DataFest site.
- **Code windows.** The `mcanouil/code-window` extension draws window chrome around code blocks, and by design it also frames blocks that have no language. Two project filters keep executed cell output plain. `_filters/plain-cell-output.lua` runs before `code-window` and opts output blocks out. `_filters/plain-cell-output-cleanup.lua` runs after it and strips the `default` label the extension still adds. Keep the three entries in `_quarto.yml` in that order. They need separate files because Quarto ignores a filter path listed twice.
- **Archive.** Earlier years' pages, such as workshop tutorials, live in `_archive/<year>/`. The `render` globs in `_quarto.yml` exclude that folder. `_freeze/` holds frozen execution results (`freeze: auto`).
- **Output.** `docs/` is build output and is committed. Don't hand-edit it.

## Tutorials

`tutorials/` holds census data tutorials (Census 101, then R and Python tracks of two parts each), listed by `tutorials/index.qmd` and linked from the navbar. Their code cells execute and call the live Census API, so they can only be rendered locally.

- **CI never executes them.** It relies on the committed `_freeze/tutorials/` results. After changing a tutorial's code, re-render it locally and commit `_freeze/` along with `docs/`.
- **Rendering locally needs:**
  - `CENSUS_API_KEY` in the environment. R reads the key from there. Python's `load_dotenv()` also finds `tutorials/.env`, which is gitignored.
  - `QUARTO_R` pointing at the per-user R install. It isn't on PATH, and its location is in the `HKCU:\SOFTWARE\R-core\R` registry value `InstallPath`.
  - `QUARTO_PYTHON` pointing at `.venv/Scripts/python.exe`. The gitignored `.venv` has the tutorial packages plus `jupyter` and `jupyter-cache`. The site-wide `cache: true` requires `jupyter-cache`.
- **Hidden cells.** Cells that install packages, set or print the API key, or read and write files use `#| eval: false`. Never let a cell print the key.
- **No mapview.** Use leaflet (or tmap) for interactive maps in R, not mapview.
- **Setup chunks and the cache.** The site-wide `cache: true` skips cached chunks entirely on later renders, so side effects like `options()` never run. Any R setup chunk that sets options needs `#| cache: false`. R Part 2's setup chunk sets `tigris_use_cache`, and without that line tigris re-downloads shapes and prints long progress bars. tigris has no global switch for those bars, so a chunk that may download shapes and prints nothing else can use `#| results: hide`.
- **Render errors.** A running `quarto preview` re-renders a file as soon as it changes, which can collide with a manual render (`mediabag` or `quarto-session-temp` "file not found" errors). Retry the render. If knitr then fails with `readLines ... cannot open the connection`, delete `tutorials/<page>_cache/` and render again.
- **census_helpers.py.** `tutorials/census_helpers.py` copies the setup cell and `get_census()` from Python Part 1. Python Part 2 imports it, so keep the two in sync.

## Deployment

On every push to `main`, `.github/workflows/main.yaml` renders the site and then rsyncs `docs/` into `datawrangle/` in the `DavidsonCollege-DataScience/datasci-hub` repo, using the `HUB_REPO_PUSH_TOKEN` secret. Only the hub repo deploys to the shared Azure Static Web App, because each Azure deploy replaces all of the app's content. Never deploy to Azure directly from this repo.
