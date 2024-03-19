from . import download
from . import data_processing
from src import database


def build_database():
    datasets = download.load_record_keeping_file()
    for filename in datasets.keys():
        # Download if not yet in database
        df = download.download_single_file(datasets, filename)

        if df is not None:
            # Clean
            df = data_processing.clean_and_transform_data(df)
            # print(df)

            # Upload and record
            table_name = "rides"
            database.upload_dataframe(df, table_name)
            download.record_flat_file_upload(datasets, filename)

            print(f"✓ {filename} – {df.shape[0]} trips added to database")