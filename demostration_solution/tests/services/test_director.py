from unittest.mock import MagicMock

import pytest as pytest

from demostration_solution.dao.director import DirectorDAO
from demostration_solution.dao.model.director import Director
from demostration_solution.service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    director1 = Director(id=1, name='Tim Burton')
    director2 = Director(id=2, name='Darren Aronofsky')
    director3 = Director(id=3, name='Shonda Rhimes')

    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock()
    director_dao.partially_update = MagicMock()
    director_dao.delete = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "David Fincher"
        }
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Jim Jarmusch"
        }
        self.director_service.update(director_d)

    def test_partially_update(self):
        director_d = {
            "id": 3,
            "name": "Jim Jarmusch"
        }
        self.director_service.update(director_d)

    def test_delete(self):
        self.director_service.delete(1)


