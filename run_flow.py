from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from conf import RENAME_IMDB_COLS_MAP, MOVIES_DATA_NECESSARY_COLUMNS, MAX_THREAD_POOL_SIZE
from enums.reports import Report
from maps import PARAMS_BY_REPORT_NAME
from enums.columns import Column
from enums.keys import Key
from utils import add_missing_data_per_movie, build_runtime_data, build_actors_data


class MovieStatisticsFlow():

    def __init__(self, website):
        self.website = website

    def run_flow(self, file_name):
        movies_df = self.get_movies_df(file_name)

        reports = self.get_reports(movies_df)

        presentation_data = self.build_data_for_presentation(reports)

        return reports

    def get_movies_df(self, file) -> pd.DataFrame:
        movies_df = pd.read_csv(file)

        movies_df = movies_df.sample(100)

        movies_df = self.reshape_movies_df(movies_df)

        movies_df = self.add_missing_fields(movies_df)

        return movies_df

    def reshape_movies_df(self, movies_df) -> pd.DataFrame:
        rename_map = RENAME_IMDB_COLS_MAP

        movies_df = movies_df.rename(columns=rename_map)
        movies_df = movies_df[MOVIES_DATA_NECESSARY_COLUMNS]

        movies_df[Column.NUM_OF_CONTENTS] = 1
        movies_df[Column.DIFF_RATING] = movies_df[Column.USER_RATING] - movies_df[Column.WEBSITE_RATING]

        return movies_df

    def add_missing_fields(self, movies_df):
        movies_list = movies_df.to_dict('records')
        with ThreadPoolExecutor(max_workers=MAX_THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(add_missing_data_per_movie, movie, self.website)
                       for movie in movies_list]
            results = [future.result() for future in as_completed(futures)]

        movies_df = pd.DataFrame(results)

        return movies_df

    def get_reports(self, movies_df):
        reports_map = {}
        for report_name, params in PARAMS_BY_REPORT_NAME.items():
            function = params[Key.FUNC]
            key = params[Key.GROUP_BY_KEY]

            report_df = function(movies_df, key)

            reports_map[report_name] = report_df

        return reports_map

    def build_data_for_presentation(self, reports):

        runtime_data = build_runtime_data(reports[Report.TOTAL_RUNTIME])

        favorite_actor_data, best_five_actors, rational_best_actor = build_actors_data(reports[Report.RATING_BY_ACTOR])