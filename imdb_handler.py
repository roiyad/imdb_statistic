from bs4 import BeautifulSoup
import requests
import re


class ImdbHandler():
    def __init__(self, movie_link):

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'}
        response = requests.get(url=movie_link, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')


    def get_top_cast(self) -> list:

        cast_list = self.soup.find_all('a', {'data-testid': 'title-cast-item__actor'})
        top_cast = [actor.text.strip() for actor in cast_list]

        return top_cast

    def get_synopsis(self):

        synopsis = self.soup.find('span', {'data-testid': 'plot-xl'}).text.strip()

        return synopsis

    def get_genres(self):

        genre_div = self.soup.find("div", class_="ipc-chip-list__scroller")
        genres = []

        if genre_div:
            genre_elements = genre_div.find_all("span", class_="ipc-chip__text")
            # Extract and print the genres
            genres = [genre.text for genre in genre_elements]

        return genres


    def get_directors(self):

        directors = self.soup.find_all('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        final_directors = []
        is_director_section = False

        for director in directors:

            if 'Director' in director.previous.previous.previous.previous:
                is_director_section = True

            if 'Writer' in director.previous.previous.previous.previous:
                break

            if is_director_section:
                final_directors.append({'id': director['href'].split('/')[2],
                                      'name': director.text.strip()})

        return final_directors

    def get_writers(self):

        writers = self.soup.find_all('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        final_writers = []
        is_writer_section = False
        for writer in writers: 

            if 'Writer' in writer.previous.previous.previous.previous:
                is_writer_section = True
            
            if 'Star' in writer.previous.previous.previous.previous:
                break
            
            if is_writer_section:
                final_writers.append({'id': writer['href'].split('/')[2], 
                'name':writer.text.strip()})
        
        return final_writers
            