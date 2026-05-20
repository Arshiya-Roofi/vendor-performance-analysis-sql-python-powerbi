import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Create logs folder if it does not exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Create SQLite database connection
engine = create_engine('sqlite:///inventory.db')


# INSERT CSV DATA INTO DATABASE TABLE USING CHUNKS
def ingest_db(file_path, table_name, engine):

    first_chunk = True

    for chunk in pd.read_csv(file_path, chunksize=100000):

        chunk.to_sql(
            table_name,
            con=engine,
            if_exists='replace' if first_chunk else 'append',
            index=False
        )

        first_chunk = False


def load_raw_data():

    '''Load CSV files and ingest into SQLite database'''

    start = time.time()

    for file in os.listdir('data/raw'):

        if file.endswith('.csv'):

            try:

                full_path = os.path.join('data/raw', file)

                logging.info(f'Ingesting {file} into database')

                print(f'Loading: {file}')

                ingest_db(full_path, file[:-4], engine)

                print(f'Successfully ingested: {file}')

            except Exception as e:

                logging.error(f'Error ingesting {file}: {e}')

                print(f'Failed: {file}')
                print(e)

    end = time.time()

    total_time = (end - start) / 60

    logging.info('------------ Ingestion Complete ------------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

    print(f'\nTotal Time Taken: {total_time:.2f} minutes')


if __name__ == '__main__':

    load_raw_data()