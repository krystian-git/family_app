from typing import List
import requests
from bs4 import BeautifulSoup


class MovieFilmweb():
    def __init__(self, title, rate, image, plot, link):
        self.title = title
        self. rate = rate
        self.image = image
        self.plot = plot
        self.link = link


class Filmweb:
    """Scrapping 'Movies of the Day' from Filmweb and returning as list of MovieFilmweb objects"""
    def __init__(self):
        pass
    def movie_filmweb(self, limit:int) -> List:
        try:
            url = 'https://www.filmweb.pl'                 # Source of data/movies
            movie_list = []                                # List of Movie objects
            filmweb_page = requests.get(url=url+'/films')  # Download movies
            soup = BeautifulSoup(filmweb_page.text, 'lxml')# Transform requests -> BeautifulSoup
            movie_list_links = []                          # list of movie links/sections of Filmweb
            # Making list of movie links    
            for link in soup.find_all('div', class_='simplePoster__poster', limit=limit):
                movie_list_links.append(url+link.a['href'])

            for movie in movie_list_links:
                movie_url = requests.get(url=movie)
                movie_soup = BeautifulSoup(movie_url.text, 'lxml')
                movie_dir = MovieFilmweb(
                    title=movie_soup.find('h1'),
                    rate = movie_soup.find('span', class_='filmRating__rateValue'),
                    image = movie_soup.find('div', class_='filmPosterSection__poster'),
                    plot = movie_soup.find('div', class_='filmPosterSection__plot'),
                    link = movie
                    )
                movie_list.append(movie_dir)

        except:
            return None

        return movie_list