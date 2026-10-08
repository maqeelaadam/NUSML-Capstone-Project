# Submission correction verification

Verified on 8 October 2026 in a temporary fresh copy of the repository, using the pinned Python 3.12 environment. No model was retrained during this check.

- Restored the committed artifact archive and verified every archived file checksum, all five original models, model aliases and MLflow artifact copies.
- Loaded all five model pipelines and produced predictions from an example input.
- Read all five original runs through MLflow; parameters and metrics exactly matched tracking_export.json, runs were FINISHED, model artifacts were accessible and file URIs pointed into the new checkout.
- Imported the supplied CSV and reran the primary SQLite analysis. Every result exactly matched the checked-in all_sql_results.json.
- Ran the Python pipeline and exercised all three application commands.
- All nine schema, leakage-boundary, CLI, API and monitoring acceptance checks passed.
- Rendered and visually inspected all nine pages of the four final PDFs: the Part 1 and Part 2 reports are two pages each, the final report is three pages, and the bias/fairness report is two pages. Optional references and report citations were removed as requested; dataset licensing/provenance information remains in the data documentation. Tables and text are readable without overlap or clipping.

The insights and final reports now identify raw CSV results as primary and hourly results as supplementary. Saved numerical model results and labels remain unchanged. The actual Power BI dashboard and course submission are still outstanding.
