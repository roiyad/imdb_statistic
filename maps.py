from enums.columns import Column
from enums.keys import Key
from enums.reports import Report
from utils import get_df_by_key_id_and_name, get_df_by_list_key, get_df_by_multiple_string_key, get_df_by_multiple_keys, \
    get_df_by_key

PARAMS_BY_REPORT_NAME = {
    Report.RATING_BY_ACTOR: {
        Key.FUNC: get_df_by_list_key,
        Key.GROUP_BY_KEY: Column.ACTOR
    },
    Report.RATING_BY_DIRECTOR: {
        Key.FUNC: get_df_by_key_id_and_name,
        Key.GROUP_BY_KEY: Column.DIRECTOR
    },
    Report.RATING_BY_GENRE: {
        Key.FUNC: get_df_by_multiple_string_key,
        Key.GROUP_BY_KEY: Column.GENRES
    },
    Report.RATING_BY_TYPE_AND_ACTOR: {
        Key.FUNC: get_df_by_multiple_keys,
        Key.GROUP_BY_KEY: {
            Column.ACTOR: {
                Key.GROUP_BY_ID: False,
                Key.INSTANCE: 'list'
            },
            Column.TYPE: {
                Key.GROUP_BY_ID: False,
                Key.INSTANCE: 'str'
            }
        }
    },
    Report.RATING_BY_RELEASE_YEAR: {
        Key.FUNC: get_df_by_key,
        Key.GROUP_BY_KEY: Column.YEAR
    }
}
