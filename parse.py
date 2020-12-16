from os.path import basename

import requests
from bs4 import BeautifulSoup
import random


def parse():
    url = ['https://www.kinoafisha.info/rating/movies/?page=0' ,
           'https://www.kinoafisha.info/rating/movies/?page=1' ,
           'https://www.kinoafisha.info/rating/movies/?page=2' ,
           'https://www.kinoafisha.info/rating/movies/?page=3' ,
           'https://www.kinoafisha.info/rating/movies/?page=4' ,
           'https://www.kinoafisha.info/rating/movies/?page=5' ,
           'https://www.kinoafisha.info/rating/movies/?page=6' ,
           'https://www.kinoafisha.info/rating/movies/?page=7' ,
           'https://www.kinoafisha.info/rating/movies/?page=8' ,
           'https://www.kinoafisha.info/rating/movies/?page=9']
    k = 0
    pages = 9
    id_films = 1
    film_list = []
    while k <= pages:
        response = requests.get(url[k])
        soup = BeautifulSoup(response.text , 'lxml')
        films = soup.find_all('div' , class_='films_content')

        for i in range(0 , len(films)):
            j = 0
            prod = ''
            film_names = films[i].find('a' , class_='films_name ref')
            ratings = films[i].find('span' , class_='rating_num')
            films_info = films[i].find_all('span' , class_='films_info')
            producers = films[i].find_all('a' , class_='films_info_link')

            for producer in producers:
                prod += producer.get_text()
                if len(producers) > 1 and producer != producers[-1]:
                    prod += ', '

            film_dict = {
                "ID": id_films ,
                "Name": film_names.text ,
                "Ratings": ratings.text ,
                "Genre": films_info[j + 1].text ,
                "Info": films_info[j].text ,
                "Producer": prod
            }
            film_list.append(film_dict)
            id_films += 1

        k += 1
    return film_list


def get_random_movie(lst):
    res1 = random.choice(lst)
    num = str(res1["ID"])
    name = res1["Name"]
    ratings = res1["Ratings"]
    genre = res1["Genre"]
    info = res1["Info"]
    producer = res1["Producer"]
    result = ('Номер фильма: ' + num + '\n' +
              'Название фильма: ' + name + '\n' +
              'Оценка фильма: ' + ratings + '\n' +
              'Жанр: ' + genre + '\n' +
              'Информация о фильме: ' + info + '\n' +
              'Режиссер/ы: ' + producer)
    return num , result


def get_random_movie_of_genre(genre , lst):
    genre_lst = []
    for i in range(0 , len(lst)):
        if lst[i]["Genre"].startswith(genre) or lst[i]["Genre"].endswith(genre):
            genre_lst.append(lst[i])
    num , result = get_random_movie(genre_lst)
    return num , result


def get_random_movie_of_producer(producer , lst):
    producer_lst = []
    for i in range(0 , len(lst)):
        if lst[i]["Producer"].startswith(producer) or lst[i]["Producer"].endswith(producer):
            producer_lst.append(lst[i])
    num , result = get_random_movie(producer_lst)
    return num , result


def get_random_movie_of_genre_and_producer(genre , producer , lst):
    genre_lst = []
    producer_lst = []
    for i in range(0 , len(lst)):
        if lst[i]["Genre"].startswith(genre) or lst[i]["Genre"].endswith(genre):
            genre_lst.append(lst[i])
    if len(genre_lst) != 0:
        for i in range(0 , len(genre_lst)):
            if genre_lst[i]["Producer"].startswith(producer) or genre_lst[i]["Producer"].endswith(producer):
                producer_lst.append(genre_lst[i])
    if len(producer_lst) != 0:
        num , result = get_random_movie(producer_lst)
        return num , result
    if len(genre_lst) != 0 or len(producer_lst) != 0:
        return None, None
