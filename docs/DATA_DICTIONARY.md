# Data dictionary

| Column | Meaning | Initial validation |
| --- | --- | --- |
| holiday | Holiday label, including regional holiday; `None` means no labelled holiday | Preserve as text; inspect label timing |
| temp | Average temperature in Kelvin | Numeric; investigate <=0; Celsius = Kelvin -273.15 |
| rain_1h | Hourly rainfall, mm | Numeric, nonnegative; investigate 9831.3 mm |
| snow_1h | Hourly snowfall, mm | Numeric, nonnegative |
| clouds_all | Cloud cover percentage | Numeric in [0,100] |
| weather_main | Short weather category | Strip whitespace; standardise using a reviewed mapping |
| weather_description | Detailed weather description | Strip whitespace; inspect multiple labels per hour |
| date_time | Supplied local CST timestamp | Parse, validate, audit coverage and repeats |
| traffic_volume | Hourly westbound I-94 count | Nonnegative integer; retain valid zero values |

Do not infer actual accidents, speeds, travel times, other corridors, or measured visibility from this schema.
