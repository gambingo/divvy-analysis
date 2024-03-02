import os

from sqlalchemy import create_engine


def upload_dataframe_to_database(df, table_name, if_exists="append"):
    engine = create_engine(database_uri())
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def database_uri():
    host = os.environ.get("HOST", "localhost")
    port = os.environ.get("PORT", 5432)
    db_name = os.environ["DATABASE_NAME"]
    db_uri = f"postgresql://@{host}:{port}/{db_name}"
    return db_uri