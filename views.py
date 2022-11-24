from flask import Flask
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>')
def by_title(title):
    result = sql_request_by_title(title)
    return result


@app.route('/movie/<year1>/to/<year2>')
def by_year(year1, year2):
    result = sql_request_by_year(year1, year2)
    return result


@app.route('/rating/<title_category>')
def by_title_category(title_category):
    result = sql_request_by_category(title_category)
    return result


@app.route('/genre/<genre>')
def by_title_genre(genre):
    result = sql_request_by_genre(genre)
    return result


if __name__ == '__main__':
    app.run()
