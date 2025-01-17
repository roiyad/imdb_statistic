from enums.columns import Column
from imdb_handler import ImdbHandler


def add_missing_data_per_movie(movie, website):

    website_handler = ImdbHandler(movie[Column.URL])

    if Column.ACTOR_ID not in movie:

        actors = website_handler.get_top_cast()
        actor_ids = [actor[Column.ID] for actor in actors]
        actor_names = [actor[Column.NAME] for actor in actors]

        movie.update({Column.ACTOR_ID: actor_ids, Column.ACTOR_NAME: actor_names})

    if Column.DIRECTOR_ID not in movie:

        directors = website_handler.get_directors()
        director_ids = [director[Column.ID] for director in directors]
        director_names = [director[Column.NAME] for director in directors]

        movie.update({Column.DIRECTOR_ID: director_ids, Column.DIRECTOR_NAME: director_names})


    return movie


