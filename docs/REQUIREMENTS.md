# Capstone requirements and acceptance evidence

Source: supplied `NUSSOC_AMLDS_Capstone Project Instructions.docx` and `NUSSOC_AMLDS_Guide to GitHub for Capstone.docx`. These are course requirements; the implementation choices in DECISIONS.md are proposed project decisions. No analysis task is marked complete by this framework.

| Task | Required acceptance evidence | Planned location | Status |
| --- | --- | --- | --- |
| 1.1 SQL loading | SQLite import and verification; annual totals and changes for 2012–2017; at least two observations; holiday temperatures for New Year's Day and Labor Day in 2015–2017 | capstone_part1/sql/, notebooks/, reports/ | Starter queries only |
| 1.2 Statistics | Mean, median, SD, variance, range; temperature–volume correlation; interpretation and causality limits | capstone_part1/notebooks/, reports/ | Pending |
| 1.3 Probability | Congestion >5500; P(congestion), P(clear), joint and conditional probabilities; high temperature >292 K; independence check; odds ratio clear vs cloudy | capstone_part1/notebooks/, reports/ | Pending |
| 1.4 Dashboard | Power Query quality audit, hour, Celsius, fixed categories; daily means 2015–2017; hourly means 2017; weather extremes and difference; scatter; 3 KPI cards and 3 slicers | capstone_part1/powerbi/ | Specification only |
| 1 deliverables | SQL/database, statistical and probability analysis, Power BI dashboard, 1–2 page insights report | capstone_part1/ | Pending |
| 2.1 Pipeline | pipeline.py; CSV exception handling; schema validation first; category/time cleaning; missing values, exact duplicates, outliers; justified imputation; explicit conditionals and loops | capstone_part2/pipeline.py, cleaning.py | Input validation only |
| 2.1 Logging | Named module loggers; entry-point console+file handlers; timestamp/level/module/message; INFO loaded shape; separate cleaning logs; WARNING change counts/reasons; graceful ERROR with exception details | capstone_part2/, pipeline.log | Starter configuration and validation sample |
| 2.2 Features | Hour, weekday, weekend, cyclical feature; encoded weather and useful indicators; >=2 scaled continuous fields; documented data-driven congestion categories; before/after INFO shapes and DEBUG thresholds | capstone_part2/feature_engineering.py | Calendar helper only |
| 2.3 Figures | >=3 Matplotlib figures, interpretations, INFO save paths | capstone_part2/visualizations.py, figures/ | Pending |
| 2.4 Application | >=3 queries; INFO command and arguments; invalid input produces clear ERROR | capstone_part2/mini_app/ | Command plan only |
| 2.5 Reproducibility | Incremental task commits, README, logging documentation, 1–2 page methodology/findings report, final sample log | capstone_part2/ | Framework only |
| 3.1 Supervised | >=2 algorithms per regression/classification task; common time/weather/holiday/cyclical features; regression MAE/R²; classification accuracy/precision/recall/F1/ROC AUC | capstone_part3/supervised/ | Pending |
| 3.2 Unsupervised | Interpreted K-means traffic clusters; congestion association rules ranked by lift with plain-language meaning | capstone_part3/unsupervised/ | Pending |
| 3.3 Deep learning | One neural network/LSTM/CNN; SHAP or LIME, or explained comparable-model choice | capstone_part3/deep_learning/, explainability/ | Pending |
| 3.4 Advanced AI | At least one advanced technique, rationale, implementation, value, limitations; MLflow proposed | capstone_part3/experiments/, reports/ | Pending |
| 3.5 Recommendations | Low-traffic windows considering day type/weather; plain-language timing advice for this corridor | capstone_part3/recommendations/ | Pending |
| 3.6 MLOps | Versioned model performance; MLflow params/metrics/versions/experiments; FastAPI/Flask prediction; drift simulation; PASS/ALERT mechanism | capstone_part3/deployment/, monitoring/, experiments/ | Pending |
| 3.7 Responsible AI | Coverage limitations, proxy-label risk, errors by conditions/time, oversight, resource/environmental trade-offs | capstone_part3/reports/ | Outline only |
| 3 deliverables | Models/notebooks/scripts, MLflow records, API simulation, recommendations, final report across tasks, fairness report, README stating proxy vs real accidents | capstone_part3/ | Pending |
| Final submission | One portfolio for all parts; required outputs, reproducible instructions, incremental history, grader access, Canvas repository URL | Root README and all parts | Pending |

Part 1 traffic categories: Low <4500; Medium 4500–5500 inclusive; High >5500. Part 2/3 quartiles: Low <=Q1; Medium <=Q2; High <=Q3; Severe >Q3. Keep these definitions separately named.
