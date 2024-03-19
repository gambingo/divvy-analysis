import os
import warnings

from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd



load_dotenv()
pd.options.mode.chained_assignment = None
warnings.simplefilter(action='ignore', category=UserWarning)
"""I worry this is too greedy, but I just want to supress the timedelta
    conversion warning"""


def upload_dataframe(df, table_name, if_exists="append"):
    engine = create_engine(database_uri())
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def database_uri():
    host = os.environ.get("HOST", "localhost")
    port = os.environ.get("PORT", 5432)
    db_name = os.environ["DATABASE_NAME"]
    db_uri = f"postgresql://@{host}:{port}/{db_name}"
    return db_uri