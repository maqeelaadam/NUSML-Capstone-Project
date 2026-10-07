"""Discover traffic clusters and interpretable congestion association rules."""
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from mlxtend.frequent_patterns import apriori,association_rules
from capstone_part2.feature_engineering import add_calendar,quartile_categories
from capstone_part2.cleaning import WEATHER_SEVERITY

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]


def main():
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/unsupervised.log",encoding="utf-8")],force=True)
        df=add_calendar(pd.read_csv(ROOT/"data/processed/hourly_traffic.csv",keep_default_na=False,parse_dates=["date_time"]))
        # Descriptive discovery uses all observed hours; it is not supervised holdout evaluation.
        variables=df[["hour_sin","hour_cos","traffic_volume"]].copy()
        variables["weather_severity"]=df.weather_main.map(WEATHER_SEVERITY).fillna(2)
        scaled=StandardScaler().fit_transform(variables)
        model=KMeans(n_clusters=4,n_init=10,random_state=42)
        df["cluster"]=model.fit_predict(scaled)
        means=df.groupby("cluster").agg(hours=("traffic_volume","size"),mean_traffic=("traffic_volume","mean"),mean_hour=("hour","mean"),mean_temperature_c=("temp_celsius","mean"),low_visibility_fraction=("is_low_visibility","mean"))
        means.to_csv(ROOT/"capstone_part3/results/cluster_profiles.csv")
        sample=np.random.default_rng(42).choice(len(df),size=min(2000,len(df)),replace=False)
        score=silhouette_score(scaled[sample],df.cluster.iloc[sample])
        (ROOT/"capstone_part3/results/clustering.json").write_text(json.dumps({"k":4,"sampled_silhouette":float(score),"sample_size":len(sample),"interpretation":"Describe each profile using volume, cyclic time and weather; arithmetic mean hour alone can conceal midnight wraparound."},indent=2)+"\n")
        quartiles=df.traffic_volume.quantile([.25,.5,.75]).to_numpy()
        transactions=pd.DataFrame({"time":pd.cut(df.hour,[-1,5,9,15,19,23],labels=["overnight","morning","midday","evening","late_evening"]),"day":np.where(df.is_weekend,"weekend","weekday"),"weather":df.weather_main,"congestion":quartile_categories(df.traffic_volume,quartiles)})
        basket=pd.get_dummies(transactions,prefix=transactions.columns,dtype=bool)
        itemsets=apriori(basket,min_support=0.03,use_colnames=True,max_len=3)
        rules=association_rules(itemsets,metric="confidence",min_threshold=0.5)
        rules=rules.loc[rules.consequents.map(lambda s:len(s)==1 and all(x.startswith("congestion_") for x in s)) & rules.antecedents.map(lambda s:all(not x.startswith("congestion_") for x in s))].sort_values(["lift","support"],ascending=False)
        for column in ["antecedents","consequents"]:
            rules[column]=rules[column].map(lambda s:" AND ".join(sorted(s)))
        rules[["antecedents","consequents","support","confidence","lift"]].head(30).to_csv(ROOT/"capstone_part3/results/association_rules.csv",index=False)
        lines=["# Association rules", "", "Descriptive full-data rules; support >=3%, confidence >=50%. Lift compares conditional frequency with the outcome's overall frequency, not a causal effect.", ""]
        for _,r in rules.head(5).iterrows():
            lines.append(f"- When {r.antecedents}, {r.consequents} occurs in {r.confidence:.1%} of matching hours; lift {r.lift:.2f}, support {r.support:.1%}.")
        (ROOT/"capstone_part3/results/association_interpretations.md").write_text("\n".join(lines)+"\n")
        logger.info("Saved four cluster profiles and %d eligible association rules",len(rules));return 0
    except (OSError,ValueError,KeyError,RuntimeError) as exc:
        logger.error("Unsupervised analysis failed: %s",exc,exc_info=True);return 1


if __name__=="__main__":raise SystemExit(main())
