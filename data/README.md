# Dataset provenance

The supplied `Metro_Interstate_Traffic_Volume.csv` is used unchanged. Import it with `python scripts/import_data.py --source /path/to/Metro_Interstate_Traffic_Volume.csv`. Raw and generated data directories are ignored by Git, and the import script validates schema before copying.

- Raw observations: 48,204; columns: 9.
- Timestamp extent: 2012-10-02 09:00:00 to 2018-09-30 23:00:00.
- Unique timestamp strings: 40,575; exact duplicate rows: 17.
- Empty CSV cells: 0 across all columns. This does not establish that every value is valid.
- Temperature minimum: 0 K; rainfall maximum: 9831.3 mm. The cleaning pipeline handles these invalid weather readings with monthly median imputation; the raw CSV remains unchanged.
- Supplied file SHA-256: `749c90d720360a4215bb15345526073c079ba4cc95e3fa558796d083f85fce9e`.

Hogue, J. (2019). *Metro Interstate Traffic Volume*. UCI Machine Learning Repository. https://doi.org/10.24432/C5X60B. The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The project preserves the supplied raw file without modifications. Cleaning is documented in capstone_part2/reports/methodology_report.md and the checked-in pipeline.log; derived data retains this attribution.

To obtain the data independently, visit the [official dataset page](https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume), download it, extract the CSV (including gzip decompression if necessary), and run the same import script. Verify the checksum; document a differing version rather than silently replacing the original.
