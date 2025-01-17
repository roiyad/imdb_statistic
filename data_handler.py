from copy import deepcopy

import pandas as pd

from conf import GROUP_BY_FIELDS_MAP


class StatisticDataHelper():

    def __init__(self):
        pass

    def get_df_by_key(self, df: pd.DataFrame, key):

        df[key] = df[key].str.split(',').str.strip()
        df = df.explode(column=key).drop(index=True)

        df = df.groupby(by=key).aggregate(GROUP_BY_FIELDS_MAP)

        return df

    def get_df_by_key_id_and_name(self, df:pd.DataFrame, key):

       group_by_key = key + '_id'
       df = df.explode(column=group_by_key).drop(index=True)

       group_by_fields_map = deepcopy(GROUP_BY_FIELDS_MAP)
       group_by_fields_map.update({key + '_name': 'first'})

       df = df.groupby(by=group_by_key).aggregate(group_by_fields_map)

       return df