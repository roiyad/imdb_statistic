from bs4 import BeautifulSoup
import requests

from conf import MAX_CAST_PER_CONTENT
from enums.columns import Column


class ImdbHandler():
    def __init__(self, movie_link):

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'}
        response = requests.get(url=movie_link, headers=headers)
        full_cast_response = requests.get(url=movie_link + '/fullcredits')
        self.metadata_soup = BeautifulSoup(response.text, 'html.parser')
        self.full_cast_soup = BeautifulSoup(full_cast_response.text, 'html.parser')

    def get_top_cast(self) -> list:

        cast_list = self.metadata_soup.find_all('a', {'data-testid': 'title-cast-item__actor'})
        top_cast = [actor.text.strip() for actor in cast_list]

        return top_cast

    def get_all_cast(self) -> list:
        start_sourceline = self.full_cast_soup.find('h4', id='cast').sourceline
        end_sourceline = self.full_cast_soup.find('td', text='Rest of cast listed alphabetically:')

        if not end_sourceline:
            end_sourceline = self.full_cast_soup.find('h4', id='producer')

        end_sourceline = end_sourceline.sourceline

        cast_list = self.full_cast_soup.find_all('a', href=lambda href: href and "/name/nm" in href, text=lambda t: t)
        cast_list = [actor.text.strip() for actor in cast_list
                     if start_sourceline < actor.sourceline < end_sourceline]
        cast_list = cast_list[:min(len(cast_list), MAX_CAST_PER_CONTENT)]

        return cast_list

    def get_synopsis(self):

        synopsis = self.metadata_soup.find('span', {'data-testid': 'plot-xl'}).text.strip()

        return synopsis

    def get_genres(self):

        genre_div = self.metadata_soup.find("div", class_="ipc-chip-list__scroller")
        genres = []

        if genre_div:
            genre_elements = genre_div.find_all("span", class_="ipc-chip__text")
            # Extract and print the genres
            genres = [genre.text for genre in genre_elements]

        return genres

    def get_directors(self):

        directors = self.metadata_soup.find_all('a',
                                                class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        final_directors = []
        is_director_section = False

        for director in directors:

            if 'Director' in director.previous.previous.previous.previous:
                is_director_section = True

            if 'Writer' in director.previous.previous.previous.previous:
                break

            if is_director_section:
                final_directors.append({Column.DIRECTOR_ID: director['href'].split('/')[2],
                                        Column.DIRECTOR_NAME: director.text.strip()})

        return final_directors

    def get_writers(self):

        writers = self.metadata_soup.find_all('a',
                                              class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        final_writers = []
        is_writer_section = False
        for writer in writers:

            if 'Writer' in writer.previous.previous.previous.previous:
                is_writer_section = True

            if 'Star' in writer.previous.previous.previous.previous:
                break

            if is_writer_section:
                final_writers.append({'id': writer['href'].split('/')[2],
                                      'name': writer.text.strip()})

        return final_writers
