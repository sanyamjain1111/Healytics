
import argparse, pandas as pd
from backend.core.ai_orchestrator import AIOrchestrator

def main(split):
    df = pd.read_csv("data/joined_training_sample.csv")
    import asyncio
    res = asyncio.run(AIOrchestrator().process_dataset(df, {"specialty": "general"}))
    print("Analysis AUC keys:", [k for k in res["model_execution_results"].keys() if k != "note"])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-test", type=float, default=0.2)
    args = ap.parse_args()
    main(args.train_test)
