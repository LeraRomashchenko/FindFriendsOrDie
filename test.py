import unittest
import logging
from people_sqlite import PeopleSqlite


class FriendsAndImagesSqliteTestCase(unittest.TestCase):
    def setUp(self):
        self.db = PeopleSqlite(":memory:", logging.getLogger('test'))

    def test_no_unloaded_people_initially(self):
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [])

    def test_marks_friends_of_loaded_person_unloaded(self):
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }])
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [2, 3])

    def test_marks_unloaded_correctly_on_collisions(self):
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }, {
            'id': 2,
            'friends': [1, 3, 4],
            'images': ["2.jpg"]
        }, {
            'id': 3,
            'friends': [],
            'images': []
        }])
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [4])

    def test_marks_unloaded_correctly_on_collisions_when_loaded_one_by_one(self):
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }])
        self.db.load_people([{
            'id': 2,
            'friends': [1, 3, 4],
            'images': ["2.jpg"]
        }])
        self.db.load_people([{
            'id': 3,
            'friends': [],
            'images': []
        }])
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [4])


if __name__ == '__main__':
    unittest.main()
