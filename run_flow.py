from conf import RENAME_IMDB_COLS_MAP, MOVIES_DATA_NECESSARY_COLUMNS, MAX_THREAD_POOL_SIZE
from imdb_handler import ImdbHandler
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import add_missing_data_per_movie


class MovieStatisticsFlow():

    def __init__(self, website):

        self.website = website

    def run_flow(self, file_name):
        movies_df = self.get_movies_df(file_name)

        reports = self.get_reports_df(movies_df)

    def get_movies_df(self, file) -> pd.Dataframe:

        movies_df = pd.read_csv(file)

        movies_df = self.reshape_movies_df(movies_df)

        movies_df = self.add_missing_fields(movies_df)

        return movies_df
    
    def reshape_movies_df(self, movies_df) -> pd.DataFrame:

        rename_map = RENAME_IMDB_COLS_MAP

        movies_df = movies_df.rename(rename_map)
        movies_df = movies_df[MOVIES_DATA_NECESSARY_COLUMNS]

        return movies_df

    def add_missing_fields(self, movies_df):
        movies_list = movies_df.to_records()
        with ThreadPoolExecutor(max_workers=MAX_THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(add_missing_data_per_movie, movie, self.website)
                       for movie in movies_list]
            results = [future.result() for future in as_completed(futures)]

