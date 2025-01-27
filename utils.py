from copy import deepcopy

import pandas as pd

from conf import GROUP_BY_FIELDS_MAP
from enums.columns import Column
from enums.keys import Key
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


def get_df_by_list_key(df: pd.DataFrame, key, **kwargs):
    df = df.explode(column=key).reset_index()

    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)
    df[key] = df[key].dropna()

    return df


def get_df_by_key_id_and_name(df: pd.DataFrame, key, **kwargs):
    df = df.explode(column=key).reset_index()

    key_df = pd.json_normalize(df[key])
    df = pd.concat([df, key_df], axis=1)

    group_by_fields_map = deepcopy(GROUP_BY_FIELDS_MAP)
    group_by_fields_map.update({key + '_name': 'first'})

    df = df.groupby(by=key + '_id', as_index=False).agg(group_by_fields_map)

    return df


def get_df_by_multiple_string_key(df: pd.DataFrame, key, **kwargs):
    df[key] = df[key].str.strip().str.split(',')
    df = df.explode(column=key).reset_index()

    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)

    return df


def get_df_by_key(df: pd.DataFrame, key, **kwargs):
    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)

    return df


def get_df_by_multiple_keys(df: pd.DataFrame, keys, **kwargs):
    """

    :param df:
    :param keys:
    :param kwargs:
    :return:
    """

    group_by_map = deepcopy(GROUP_BY_FIELDS_MAP)
    group_by_keys_list = []

    for key, settings in keys.items():
        if settings['instance'] == 'list':
            df = df.explode(column=key).reset_index()

        elif settings['instance'] == 'string_list':
            df[key] = df[key].str.strip().str.split(',')

        reshaped_key = key
        if settings['group_by_id']:
            key_df = pd.json_normalize(df[key])
            df = pd.concat([df, key_df], axis=1)
            group_by_map.update({key + '_name': 'first'})
            reshaped_key = key + '_id'

        group_by_keys_list.append(reshaped_key)

    df.groupby(by=group_by_keys_list, as_index=False).agg(GROUP_BY_FIELDS_MAP)

    return df


def build_runtime_data(df):
    total_runtime = df[Column.RUNTIME].sum()

    is_movie = df[Column.TYPE] == 'Movie'

    most_watched_genre_df = df[df[Column.RUNTIME] == df[Column.RUNTIME].max()]

    title = 'You watched a lot of content during your time ' if total_runtime > 80000 \
        else "You don't waste a lot of time watching so everything you wath is meaningfully "

    content = (f'You watched {total_runtime} minutes of content well done \n '
               f'Your favourite genre is {most_watched_genre_df.iloc[0][Column.GENRES]} '
               f'and you watched {most_watched_genre_df[Column.RUNTIME].max()}')

    slide_content = {'title': title,
                     'content': content}


def build_actors_data(df):
    df_sorted_by_user_ratings = df.sort_values(by=Column.USER_RATING, ascending=False)
    df_sorted_by_diff_ratings = df.sort_values(by=Column.DIFF_RATING, ascending=False)

    top_five_user = df_sorted_by_user_ratings.iloc[:min(5, len(df))].to_dict()
    best_actor = df_sorted_by_user_ratings.iloc[0].to_dict()
    top_five_diff = df_sorted_by_diff_ratings[df_sorted_by_diff_ratings[Column.DIFF_RATING] > 0].iloc[
                    :min(5, len(df))].to_dict()

    best_actor_text = (
        f'You really liked {best_actor[Column.ACTOR_NAME]} with an average rating of {best_actor[Column.USER_RATING]}\n'
        f'You watched him total of {best_actor[Column.RUNTIME]}')

    best_actor_dict = {'title': 'Your favorite actor',
                       'text': best_actor_text}

    top_five_diff_text = '\n'.join(
        [f'{row[Column.ACTOR_NAME]}:         {row[Column.DIFF_RATING]}' for row in df_sorted_by_diff_ratings])
    top_five_diff_title = 'Some actors you liked more then their average rating those are the actors'

    top_five_diff_text = '\n'.join(
        [f'{row[Column.ACTOR_NAME]}:         {row[Column.USER_RATING]}' for row in df_sorted_by_user_ratings])
    top_five_user_title = 'time to reveal your favorite actors and their rating'

    top_five_user_dict = {'title': top_five_user_title,
                          'text': top_five_user_title}

    top_five_diff_dict = {'title': top_five_user_dict,
                          'text': top_five_diff_text}

    return best_actor_dict, top_five_user_dict, top_five_diff_dict