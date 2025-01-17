from enums.columns import Column
from enums.keys import Key
from enums.reports import Report
from utils import get_df_by_key_id_and_name, get_df_by_key

PARAMS_BY_REPORT_NAME = {
    Report.RATING_BY_ACTOR: {
        Key.FUNC: get_df_by_key,
        Key.GROUP_BY_KEY: Column.ACTOR
    },
    Report.RATING_BY_DIRECTOR: {
        Key.FUNC: get_df_by_key,
        Key.GROUP_BY_KEY: Column.DIRECTOR
    }
}
