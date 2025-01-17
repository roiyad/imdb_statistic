import pytest
from imdb_handler import ImdbHandler

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