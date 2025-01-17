from enums.columns import Column
from enums.imdb_columns import IMDbColumn

MOVIES_DATA_NECESSARY_COLUMNS = [Column.ID, Column.USER_RATING, Column.WEBSITE_RATING, Column.TITLE, Column.DATE_RATED,
                                 Column.TYPE, Column.RUNTIME, Column.YEAR, Column.GENRES, Column.NUM_OF_VOTES,
                                 Column.RELEASE_DATE,
                                 ]

RENAME_IMDB_COLS_MAP = {
    IMDbColumn.TITLE: Column.TITLE,
    IMDbColumn.RUNTIME: Column.RUNTIME,
    IMDbColumn.NUM_VOTES: Column.NUM_OF_VOTES,
    IMDbColumn.DIRECTORS: Column.DIRECTORS,
    IMDbColumn.TITLE_TYPE: Column.TYPE,
    IMDbColumn.CONST: Column.ID,
    IMDbColumn.URL: Column.URL,
    IMDbColumn.GENRES: Column.GENRES,
    IMDbColumn.IMDB_RATING: Column.WEBSITE_RATING,
    IMDbColumn.YOUR_RATING: Column.USER_RATING
}

GROUP_BY_FIELDS_MAP = {
    Column.USER_RATING: 'avg',
    Column.WEBSITE_RATING: 'avg',
    Column.RUNTIME: 'sum',

}

MAX_THREAD_POOL_SIZE = 10
