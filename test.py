import parse

my_list = parse.parse()
numfilm, film = parse.get_random_movie_of_genre_and_producer('семейный', 'Фрэнк Дарабонт', my_list)
print(film)