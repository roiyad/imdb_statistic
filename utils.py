from copy import deepcopy

import pandas as pd

from conf import GROUP_BY_FIELDS_MAP
from enums.columns import Column
from imdb_handler import ImdbHandler


def add_missing_data_per_movie(movie, website):
    website_handler = ImdbHandler(movie[Column.URL])

    if Column.ACTOR_ID not in movie:
        actors = website_handler.get_top_cast()

        movie.update({Column.ACTOR: actors})
    if Column.DIRECTOR_ID not in movie:
        directors = website_handler.get_directors()

        movie.update({Column.DIRECTOR: directors})

    return movie


def get_df_by_key(df: pd.DataFrame, key):
    df = df.explode(column=key).reset_index()

    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)

    return df

def get_df_by_multiple_string_key(df: pd.DataFrame, key):

    df[key] = df[key].str.split(',').str.strip()
    df = df.explode(column=key).reset_index()

    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)

    return df


def get_df_by_key_id_and_name(df: pd.DataFrame, key):
    group_by_key = key + '_id'
    df = df.explode(column=group_by_key).reset_index()

    group_by_fields_map = deepcopy(GROUP_BY_FIELDS_MAP)
    group_by_fields_map.update({key + '_name': 'first'})

    df = df.groupby(by=group_by_key).agg(group_by_fields_map)

    return df
