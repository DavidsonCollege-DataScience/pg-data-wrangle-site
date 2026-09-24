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
- **Archive.** Earlier years' pages, such as workshop tutorials, live in `_archive/<year>/`. The `render` globs in `_quarto.yml` exclude that folder. `_freeze/` holds frozen execution results (`freeze: auto`).
- **Output.** `docs/` is build output and is committed. Don't hand-edit it.

## Deployment

On every push to `main`, `.github/workflows/main.yaml` renders the site and then rsyncs `docs/` into `datawrangle/` in the `DavidsonCollege-DataScience/datasci-hub` repo, using the `HUB_REPO_PUSH_TOKEN` secret. Only the hub repo deploys to the shared Azure Static Web App, because each Azure deploy replaces all of the app's content. Never deploy to Azure directly from this repo.
