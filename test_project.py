import pytest
from imdb_handler import ImdbHandler
from run_flow import MovieStatisticsFlow


def test_get_actors():
    website_handler = ImdbHandler('https://www.imdb.com/title/tt0947798')
    actors = website_handler.get_top_cast()

    assert(isinstance(actors, list)) 

def test_get_genres():
    website_handler = ImdbHandler('https://www.imdb.com/title/tt0947798')
    genres = website_handler.get_genres()
    assert(isinstance(genres, list))

def test_get_writers():

    website_handler = ImdbHandler('https://www.imdb.com/title/tt0947798')

    writers = website_handler.get_writers()
    assert(isinstance(writers, list))

def test_get_directors():

    website_handler = ImdbHandler('https://www.imdb.com/title/tt0101414/')

    directors = website_handler.get_directors()
    assert (isinstance(directors, list))

def test_run_flow_start():
    run_flow = MovieStatisticsFlow('imdb')

    reports = run_flow.run_flow('roi_movies.csv')

def test_full_cast():
    website_handler = ImdbHandler('https://www.imdb.com/title/tt5537002')

    full_cast = website_handler.get_all_cast()