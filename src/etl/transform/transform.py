import sys
from pathlib import Path
from src.etl.transform.schema import pp_schema
from src.etl.transform.validate import simple_report
from src.etl.transform.format import format_to_parquet
from src.etl.transform.marts import fact_avg_monthly_ptype, fact_avg_monthly_district, write_partitioned, last_5_yrs_window, bounds_years, write_single
from src.etl.transform.clean import standardize_data, remove_bad_rows, drop_duplicates
from src.utils.state_utils import read_state
from src.utils.read_utils import read_input
from src.utils.date_utils import last_month_ym
from src.utils.pyspark_utils import create_spark
from config.transform_config import (RAW_DIR, FULL_CSV, MONTHLY_FILENAME, TRANS_DIR, STATE_FILE)
from config.transform_config import (TRANS_DIR, MART_FACT_BY_TYPE, MART_FACT_BY_DISTRICT, MART_BOUNDS_5Y)
from src.utils.logging_utils import setup_logger

# Initialize logger
logger = setup_logger(name="transform", log_file="transform.log")

def transform() -> int:
    """Transform raw CSV to partitioned Parquet with basic cleaning.
    Add data marts for better performance of Streamlit application"""
    
    spark = None
    
    try:
        logger.info("=== TRANSFORM STARTED ===")
        
        # Load info from state JSON file
        state = read_state(STATE_FILE)
        
        # Decide which CSV to transform:
        full_import_done = state.get("full_import_done", False)
        last_month = state.get("last_month_fetched")  # None until first monthly fetch
        use_full_csv = full_import_done and (last_month is None)

        if use_full_csv:
            csv_path = Path(FULL_CSV)
            first_load = True                      # overwrite entire Parquet dataset
            logger.info(f"Mode=FULL (first_load={first_load}); csv_path={csv_path}")
        else:
            ym = last_month or last_month_ym()     # fallback to computed last month if missing
            csv_path = RAW_DIR / ym / MONTHLY_FILENAME
            first_load = False                     # dynamic partition overwrite (only that month)
            logger.info(f"Mode=MONTHLY (first_load={first_load}); ym={ym}; csv_path={csv_path}")

        # Check that input exists
        if not csv_path.exists():
            logger.error(f"Input CSV not found: {csv_path}")
            return 1
        
        # Spark + schema
        spark = create_spark()
        spark.sparkContext.setLogLevel("ERROR")     # Turn off all unnecessary console messages
        schema = pp_schema()
        logger.info("Spark session created and schema loaded.")
        
        # Read CSV
        df = (spark.read
              .option("header", "false")
              .option("mode", "PERMISSIVE")
              .option("quote", '"')
              .option("escape", '"')
              .option("multiLine", "false")
              .schema(schema)
              .csv(str(csv_path)))
        
        logger.info(f"Read from CSV complete.")
        
        # Transform
        df = standardize_data(df)
        before = simple_report(df)
        
        df = remove_bad_rows(df)
        df = drop_duplicates(df)
        after = simple_report(df)
        
        # Write parquet
        logger.info(f"Writing Parquet to {TRANS_DIR} (first_load={first_load})...")
        format_to_parquet(df, TRANS_DIR, first_load=first_load)
        logger.info("Write complete.")

        logger.info(f"Data (before): {before}")
        logger.info(f"Data (after): {after}")
        
        # Create data marts
        logger.info(f"[marts] Reading cleaned dataset from: {TRANS_DIR}")
        df = read_input(engine="spark", spark=spark) # Use read_input, send engine and also spark instance

        # FACT: monthly by (district, property_type)
        print("[marts] Building fact_monthly_prices …")
        fact_by_type = fact_avg_monthly_ptype(df)
        write_partitioned(fact_by_type, MART_FACT_BY_TYPE)
        logger.info(f"[marts] Wrote: {MART_FACT_BY_TYPE}")

        # FACT: monthly by district
        print("[marts] Building fact_monthly_prices_district …")
        fact_by_dist = fact_avg_monthly_district(df)
        write_partitioned(fact_by_dist, MART_FACT_BY_DISTRICT)
        logger.info(f"[marts] Wrote: {MART_FACT_BY_DISTRICT}")

        # AGG: min/max in last 5 years (for UI sliders, prediction bounds)
        print("[marts] Building agg_bounds_5y …")
        df5 = last_5_yrs_window(df)
        bounds = bounds_years(df5)
        write_single(bounds, MART_BOUNDS_5Y)
        logger.info(f"[marts] Wrote: {MART_BOUNDS_5Y}")
        
        logger.info("[marts] DONE")
        
        return 0
    
    except Exception as e:
        print(f"[transform] FAILED: {e}")
        return 1
    
    finally:
        if spark is not None:
            try:
                spark.stop()
                logger.info("Spark session stopped.")
                logger.info("=== TRANSFORM COMPLETED ===")
            except Exception:
                logger.warning("Spark session stop raised, continuing.", exc_info=True)
        
if __name__ == "__main__":
    sys.exit(transform())