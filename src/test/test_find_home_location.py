import unittest
from src import find_home
from .mocks.visit_data_has_home import visits as visits_has_home
from .mocks.visit_data_has_no_home import visits as visits_has_no_home


class FindHomeTestCase(unittest.TestCase):

    def test_home_found(self):
        """ The story is we're tracking a college kid named Bob
        He has two good nights of rest. Consecutively between
        8pm and 8 am (11:59 + 11:59 = 23:58 hrs).
        He comes home from class on Thursday and passes out early
        at 6pm waking at midnight to go to a party (18:00:00 to 00:00:00 is 4 hrs)
        He comes home from the party at 5am and heads out for a noon class (05:00:00 to 12:00:00 is 2:59 hrs)
        He spends 30:57 hrs total at this location.
        We know Bob's home.
                "latitude": 45.12345,
        "longitude": -118.12377,
        """
        expected = {'latitude': 45.123, 'longitude': -118.123}
        self.assertEqual(find_home(visits_has_home), expected)

    def test_home_not_found(self):
        """ The story is we're tracking a college kid named Bob in a parallel universe.
        He has two good nights of rest. Consecutively between
        8pm and 8 am (11:59 + 11:59 = 23:58 hrs).
        He comes home from class on Thursday and passes out early
        at 6pm waking at midnight to go to a party (18:00:00 to 00:00:00 is 4 hrs).
        He gets lucky at the party and never comes back to what we thought might be his home.
        He spends 27:58 hrs total at this location.
        We don't know Bob's home.
        """
        self.assertIsNone(find_home(visits_has_no_home))
