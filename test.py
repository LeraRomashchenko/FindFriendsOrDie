import unittest
import logging
from people_sqlite import PeopleSqlite


class FriendsAndImagesSqliteTestCase(unittest.TestCase):
    def setUp(self):
        self.db = PeopleSqlite(":memory:", logging.getLogger('test'))

    def test_no_unloaded_people_initially(self):
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [])

    def test_gets_added_unloaded_people(self):
        self.db.add_unloaded_person(123)
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [123])

    def test_marks_friends_of_loaded_person_unloaded(self):
        self.db.add_unloaded_person(1)
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }])
        res = list(self.db.get_unloaded_people_ids(10))
        self.assertListEqual(res, [2, 3])

    def test_images_of_loaded_person_unrecognized(self):
        self.db.add_unloaded_person(1)
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }])
        res = list(self.db.get_unrecognized_images(10))
        self.assertListEqual(res, [(1, "1.jpg")])

    def test_marks_unloaded_correctly_on_collisions(self):
        self.db.add_unloaded_person(1)
        self.db.add_unloaded_person(2)
        self.db.add_unloaded_person(3)
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
        self.db.add_unloaded_person(1)
        self.db.add_unloaded_person(2)
        self.db.add_unloaded_person(3)
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

    def test_added_faces_are_displayed_in_dump(self):
        self.db.load_people([{
            'id': 1,
            'friends': [2, 3],
            'images': ["1.jpg"]
        }])
        self.db.add_faces(1, [[1.0, 0.123], [-1.2, 0.0000001]])
        res = self.db.dump()["faces"]
        self.assertListEqual(res, [(1, "1,0.12"), (1, "-1.2,0")])


if __name__ == '__main__':
    unittest.main()
