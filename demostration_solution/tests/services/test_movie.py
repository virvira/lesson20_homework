from unittest.mock import MagicMock

import pytest as pytest

from demostration_solution.dao.movie import MovieDAO
from demostration_solution.dao.model.movie import Movie
from demostration_solution.dao.model.genre import Genre
from demostration_solution.dao.model.director import Director
from demostration_solution.service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    genre1 = Genre(id=1, name='Horror')
    director1 = Director(id=1, name='Tim Burton')

    movie1 = Movie(id=1, title='Мальчишник в Вегасе', description='Ребята много пьют', trailer='Ссылка на трейлер 1',
                   year=2015, rating=7.2, genre_id=1, director_id=2)
    movie2 = Movie(id=2, title='Анатомия Грей', description='Медицинская драма', trailer='Ссылка на трейлер 2',
                   year=2004, rating=9.9, genre_id=1, director_id=1)
    movie3 = Movie(id=3, title='Who am I?', description='Benjamin, a young German computer whiz',
                   trailer='Ссылка на трейлер 3', year=2015, rating=9.7, genre_id=2, director_id=1)

    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "Мальчишник в Вегасе",
            "description": "Ребята много пьют",
            "trailer": "Трейлер шикарный",
            "year": 2020,
            "rating": 7.2,
            "genre_id": 1,
            "director_id": 2,
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_update(self):
        movie_d = {
            "title": "Мальчишник в Вегасе",
            "description": "Ребята много пьют",
            "trailer": "Трейлер шикарный",
            "year": 2020,
            "rating": 7.2,
            "genre_id": 1,
            "director_id": 2,
        }
        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 1,
            "year": 2020
        }
        movie = self.movie_service.partially_update(movie_d)
        assert movie.year == movie_d.get("year")

    def test_delete(self):
        self.movie_service.delete(1)


