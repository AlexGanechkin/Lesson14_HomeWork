import json
import sqlite3
from collections import Counter

title_rating = {
    'children': ('G', 'G'),
    'family': ('G', 'PG', 'PG-13'),
    'adult': ('R', 'NC-17')
}


def sql_request_by_title(title):
    """ Выбор фильма по его названию (по точному совпадению) с наиболее поздним годом выхода """

    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT title, country, release_year, listed_in, description "
                 "FROM netflix "
                 f"WHERE title LIKE '%{title}%' "
                 "AND type = 'Movie' "
                 "ORDER BY release_year DESC")

        executed_query = cursor.execute(query)
        data = executed_query.fetchone()

        result_in_dict = {
            'title': data[0],
            'country': data[1],
            'release_year': data[2],
            'genre': data[3],
            'description': data[4][:-1],
        }
        result_in_json = json.dumps(result_in_dict)
    return result_in_json


def sql_request_by_year(year1, year2):
    """ Выбор до 100 фильмов в диапазоне лет выхода """

    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT title, release_year "
                 "FROM netflix "
                 f"WHERE release_year BETWEEN {year1} AND {year2} "
                 "AND type = 'Movie' "
                 "LIMIT 100")

        executed_query = cursor.execute(query)
        data = executed_query.fetchall()

        result_list = []
        for row in data:
            result_in_dict = {'title': row[0], 'release_year': row[1]}
            result_list.append(result_in_dict)
            result_in_json = json.dumps(result_list)

    return result_in_json


def sql_request_by_category(title_category):
    """ Выбор по возрастным ограничениям (по группе рейтингов) """

    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        user_rating = title_rating[title_category]

        query = ("SELECT title, rating, description "
                 "FROM netflix "
                 f"WHERE rating IN {user_rating}")

        executed_query = cursor.execute(query)
        data = executed_query.fetchall()

        result_list = []
        for row in data:
            result_in_dict = {'title': row[0], 'rating': row[1], 'description': row[2][:-1]}
            result_list.append(result_in_dict)
            result_in_json = json.dumps(result_list)
    return result_in_json


def sql_request_by_genre(genre):
    """ Выбор 10 самых свежих фильмов в выбранном жанре """

    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT title, description "
                 "FROM netflix "
                 f"WHERE listed_in LIKE '%{genre}%' "
                 "AND type = 'Movie' "
                 "ORDER BY release_year DESC "
                 "LIMIT 10")

        executed_query = cursor.execute(query)
        data = executed_query.fetchall()

        result_list = []
        for row in data:
            result_in_dict = {'title': row[0], 'description': row[1][:-1]}
            result_list.append(result_in_dict)
        result_in_json = json.dumps(result_list)
    return result_in_json


def sql_request_by_actors(actor1, actor2):
    """ Выбор всех актеров, которые сыграли более 2 раз вместе с выбранными двумя актерами """

    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT `cast` "
                 "FROM netflix "
                 f"WHERE `cast` LIKE '%{actor1}%' "
                 f"AND `cast` LIKE '%{actor2}%' ")

        executed_query = cursor.execute(query)
        data = executed_query.fetchall()

        result_list = []
        requested_actors = []
        for row in data:
            actors_list = row[0].split(', ')
            result_list.extend(actors_list)
        actors = Counter(result_list)
        for name, number in actors.items():
            if number > 2 and name not in (actor1, actor2):
                requested_actors.append(name)
    return requested_actors


def sql_request_by_multi_parameters(title_type, title_year, title_genre):
    """ Выбор картин по типу картины, году выпуска и жанру """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT title, description "
                 "FROM netflix "
                 f"WHERE type = '{title_type}' "
                 f"AND release_year = {title_year} "
                 f"AND listed_in LIKE '%{title_genre}%'")

        executed_query = cursor.execute(query)
        data = executed_query.fetchall()

        result_list = []
        for row in data:
            result_in_dict = {'title': row[0], 'description': row[1][:-1]}
            result_list.append(result_in_dict)
        result_in_json = json.dumps(result_list)
    return result_in_json


"""
Для тестов
def sql_test_request():
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()

        query = ("SELECT * "
                 "FROM netflix "
                 "WHERE release_year = 1960 "
                 "LIMIT 50")

        executed_query = cursor.execute(query)
        result = executed_query.fetchall()

    return result



if __name__ == '__main__':
        #result = sql_request_by_actors('Rose McIver', 'Ben Lamb')
        #result = SQL_request_by_multi_parameters('Movie', 1960, 'Comedies')
        result = sql_request_by_title('love')
        #print(result)
        for item in result:
            print(item)
"""
