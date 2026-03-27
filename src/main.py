from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from extract   import extract_all
from transform import transform_all
from validate  import run_validation
from load      import load_all

def run_pipeline() -> None:
    start = datetime.now()
    print("\n" + "=" * 50)
    print("  OLIST ETL PIPELINE")
    print(f"  {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")

    datasets   = extract_all()
    df         = transform_all(datasets)
    validation = run_validation(df)
    load_all(df, validation, start)

    duration = (datetime.now() - start).total_seconds()
    print(f"\nPipeline completed in {duration:.1f} seconds\n")


if __name__ == "__main__":
    run_pipeline()