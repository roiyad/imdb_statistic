from copy import deepcopy

import pandas as pd

from conf import GROUP_BY_FIELDS_MAP, MINIMUM_CONTENT_FOR_SUMMARY
from enums.columns import Column
from enums.keys import Key
from imdb_handler import ImdbHandler


def add_missing_data_per_movie(movie):
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
    df = round_rating(df)
    df[key] = df[key].dropna()

    return df


def get_df_by_key_id_and_name(df: pd.DataFrame, key, **kwargs):
    df = df.explode(column=key).reset_index()

    key_df = pd.json_normalize(df[key])
    df = pd.concat([df, key_df], axis=1)

    group_by_fields_map = deepcopy(GROUP_BY_FIELDS_MAP)
    group_by_fields_map.update({key + '_name': 'first'})

    df = df.groupby(by=key + '_id', as_index=False).agg(group_by_fields_map)
    df = round_rating(df)

    return df


def get_df_by_multiple_string_key(df: pd.DataFrame, key, **kwargs):
    df[key] = df[key].str.strip().str.split(',')
    df = df.explode(column=key).reset_index()

    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)
    df = round_rating(df)


    return df


def get_df_by_key(df: pd.DataFrame, key, **kwargs):
    df = df.groupby(by=key, as_index=False).agg(GROUP_BY_FIELDS_MAP)
    df = round_rating(df)


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
    df = round_rating(df)

    return df


def build_runtime_data(df):
    total_runtime = df[Column.RUNTIME].sum()

    most_watched_genre_df = df[df[Column.RUNTIME] == df[Column.RUNTIME].max()]

    title = 'You watched a lot of content during your time ' if total_runtime > 80000 \
        else "You don't waste a lot of time watching so everything you wath is meaningfully "

    content = (f'You watched {int(total_runtime)} minutes of content well done \n '
               f'Your favourite genre is {most_watched_genre_df.iloc[0][Column.GENRES]} '
               f'and you watched {int(most_watched_genre_df[Column.RUNTIME].max())} minutes')

    slide_content = {'title': title,
                     'content': content}

    return slide_content


def build_full_slides_data(df, col_name):
    filtered_df = df[df[Column.NUM_OF_CONTENTS] >= MINIMUM_CONTENT_FOR_SUMMARY]

    entity_names = {
        'singular': 'actor' if col_name == 'actor' else 'director',
        'plural': 'actors' if col_name == 'actor' else 'directors'
    }

    df_sorted_by_user_ratings = filtered_df.sort_values(by=Column.USER_RATING, ascending=False)
    df_sorted_by_diff_ratings = filtered_df.sort_values(by=Column.DIFF_RATING, ascending=False)

    most_watched_item = filtered_df.loc[filtered_df[Column.RUNTIME].idxmax()]
    best_item = df_sorted_by_user_ratings.iloc[0]

    def get_top_n(df, column, n=5, condition=None):
        if condition:
            df = df[df[column] > condition]
        return df.iloc[:min(n, len(df))].to_dict('records')

    best_rating_by_user = get_top_n(df_sorted_by_user_ratings, Column.USER_RATING)
    best_diff_rating = get_top_n(df_sorted_by_diff_ratings, Column.DIFF_RATING, condition=0)

    def format_slide(title, content, left=None, right=None, slide_type=None):
        slide = {'title': title, 'content': content} if content else {'title': title, 'left_side_content': left,
                                                                      'right_side_content': right,
                                                                      'slide_type': slide_type}
        return slide

    best_actor_text = (
        f'You really liked {best_item[col_name]} with an average rating of {best_item[Column.USER_RATING]}\n'
        f'You watched a total of {int(best_item[Column.RUNTIME])} minutes'
    )

    best_rating_data = format_slide(f'Your favorite {entity_names["singular"]}', best_actor_text)

    top_five_user_data = format_slide(
        f'Some {entity_names["plural"]} you liked more than their average rating',
        None,
        left=f'{entity_names["plural"]} names\n ' + '\n '.join([row[col_name] for row in best_rating_by_user]),
        right='Average rating by user\n ' + '\n '.join([str(row[Column.USER_RATING]) for row in best_rating_by_user]),
        slide_type=3
    )

    top_five_diff_rating_data = format_slide(
        f'Some {entity_names["plural"]} you liked more than their average rating here they are',
        None,
        left='\n '.join([row[col_name] for row in best_diff_rating]),
        right='\n '.join([str(row[Column.DIFF_RATING]) for row in best_diff_rating]),
        slide_type=3
    )

    most_watched_data = format_slide(
        f'You saw one {entity_names["singular"]} more than the others',
        f'You watched {most_watched_item[col_name]} for a total of {most_watched_item[Column.RUNTIME]} minutes'
    )

    return best_rating_data, top_five_user_data, top_five_diff_rating_data, most_watched_data


def round_rating(df) -> pd.DataFrame:

    df[Column.USER_RATING] = df[Column.USER_RATING].round(2)
    df[Column.DIFF_RATING] = df[Column.DIFF_RATING].round(2)

    return df