"""Run the complete implemented portfolio with failure-aware stage logging."""
import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[1]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,help="Optional supplied CSV to import first")
    args=parser.parse_args(argv)
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"reproduction.log",encoding="utf-8")],force=True)
        stages=[]
        if args.source:stages.append([str(ROOT/"scripts/import_data.py"),"--source",str(args.source.resolve())])
        modules=["capstone_part2.pipeline","capstone_part1.run_requested_sql","capstone_part1.analyze","capstone_part3.train","capstone_part3.unsupervised.analyze","capstone_part3.explainability.explain","capstone_part3.monitoring.check","capstone_part3.recommendations.engine"]
        stages.extend([["-m",module] for module in modules])
        stages.append(["-m","unittest","discover","-s","tests","-v"])
        env=os.environ.copy()
        env.setdefault("MPLCONFIGDIR",str(ROOT/".mplconfig"))
        env.setdefault("OPENBLAS_NUM_THREADS","2");env.setdefault("OMP_NUM_THREADS","2")
        env.setdefault("MLFLOW_DISABLE_AGENT_HINT","1")
        for stage in stages:
            logger.info("Running stage %s",stage)
            subprocess.run([sys.executable,*stage],cwd=ROOT,env=env,check=True)
        logger.info("All implemented stages and acceptance checks completed; Power BI still requires authoring")
        return 0
    except (OSError,subprocess.CalledProcessError) as exc:
        logger.error("Reproduction stopped at failed stage: %s",exc,exc_info=True);return 1


if __name__=="__main__":raise SystemExit(main())
