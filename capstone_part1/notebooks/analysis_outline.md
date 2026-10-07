# Statistical and probability analysis outline

Create a reproducible notebook after selecting the observation/hourly policy.

1. Load the documented analysis table; show sample size, unique hours and coverage.
2. Compute mean, median, SD, variance and range of traffic volume. State `ddof` and interpret variability.
3. Compute temperature–volume correlation, plot it, and discuss time/season confounding and causality.
4. Define congestion `traffic_volume >5500`, clear `weather_main == Clear`, high temperature `temp >292`.
5. Compute P(congestion), P(clear), P(congestion AND clear), P(clear | congestion), P(high temperature | congestion). Show numerators and denominators.
6. Compare empirical joint probability with product of marginals and discuss independence, without equating approximate equality to proof.
7. Build the clear-vs-Clouds 2x2 congestion table; odds ratio = (clear congested * cloudy uncongested)/(clear uncongested * cloudy congested). Report exclusions and zero-cell handling.
8. Interpret annual and holiday queries with coverage caveats; select evidence for the 1–2 page report.
