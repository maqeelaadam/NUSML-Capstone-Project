"""Save interpretable traffic figures using Matplotlib."""
import logging
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def save_figures(df, directory):
    directory.mkdir(parents=True, exist_ok=True)
    outputs = []
    def save(fig, name):
        path = directory / name
        fig.tight_layout()
        fig.savefig(path, dpi=130)
        plt.close(fig)
        logger.info("Saved figure to %s", path)
        outputs.append(path)
    hourly = df.groupby("hour").traffic_volume.mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    hourly.plot.bar(ax=ax, color="#24618a")
    ax.set(title="Average traffic by local hour", xlabel="Local hour", ylabel="Vehicles per hour")
    save(fig, "traffic_by_hour.png")
    day = df.groupby("is_weekend").traffic_volume.mean().rename(index={0:"Weekday",1:"Weekend"})
    fig, ax = plt.subplots(figsize=(6,4))
    day.plot.bar(ax=ax, color=["#24618a", "#d18b32"], rot=0)
    ax.set(title="Weekday and weekend traffic", ylabel="Vehicles per hour", xlabel="Day type")
    save(fig, "weekday_weekend.png")
    weather = df.groupby("weather_main").traffic_volume.mean().sort_values()
    fig, ax = plt.subplots(figsize=(8,4))
    weather.plot.barh(ax=ax, color="#24618a")
    ax.set(title="Average traffic by hourly weather category", xlabel="Vehicles per hour", ylabel="Weather")
    save(fig, "traffic_by_weather.png")
    fig, ax = plt.subplots(figsize=(8,4))
    sample = df.sample(min(5000,len(df)),random_state=42)
    ax.scatter(sample.temp_celsius,sample.traffic_volume,s=5,alpha=0.2,color="#24618a")
    ax.set(title="Temperature and traffic (reproducible sample)", xlabel="Temperature (°C)", ylabel="Vehicles per hour")
    save(fig,"temperature_traffic.png")
    text = f"""# Figure interpretations

Based on one record per observed hour after documented cleaning. Associations are descriptive, not causal.

- **Hourly demand:** mean traffic peaks at {hourly.idxmax():02d}:00 ({hourly.max():,.0f} vehicles/hour) and is lowest at {hourly.idxmin():02d}:00 ({hourly.min():,.0f}). Time of day should inform timing recommendations.
- **Day type:** weekdays average {day['Weekday']:,.0f} vehicles/hour and weekends {day['Weekend']:,.0f}; compare similar hours before assigning the difference to day type alone.
- **Weather:** {weather.idxmax()} has the highest observed mean ({weather.max():,.0f}) and {weather.idxmin()} the lowest ({weather.min():,.0f}). Rare-category sample sizes and conservative hourly category selection limit comparisons.
- **Temperature:** the sample scatter shows broad traffic variation at similar temperatures. Quantify correlation in Part 1 and consider time/season confounding.
"""
    (directory/"INTERPRETATIONS.md").write_text(text)
    logger.info("Saved figure interpretations to %s", directory/"INTERPRETATIONS.md")
    return outputs
