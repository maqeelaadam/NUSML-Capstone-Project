# Association rules

Descriptive full-data rules; support >=3%, confidence >=50%. Lift compares conditional frequency with the outcome's overall frequency, not a causal effect.

- When day_weekend AND time_overnight, congestion_Low occurs in 89.6% of matching hours; lift 3.59, support 6.4%.
- When time_overnight AND weather_Clouds, congestion_Low occurs in 86.0% of matching hours; lift 3.44, support 5.9%.
- When time_overnight AND weather_Clear, congestion_Low occurs in 85.7% of matching hours; lift 3.43, support 8.3%.
- When time_overnight, congestion_Low occurs in 85.3% of matching hours; lift 3.41, support 21.4%.
- When time_late_evening AND weather_Clouds, congestion_Medium occurs in 84.0% of matching hours; lift 3.36, support 5.1%.
