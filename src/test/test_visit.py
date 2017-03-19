from unittest import TestCase
from src import Visit
import datetime


class VisitTestCase(TestCase):


    def test_full_window(self):
        twelve_hours = 43200
        visit = Visit(None, None, '3/17/2017 20:00:00', '3/18/2017 08:00:00')
        self.assertEqual(visit.get_applicable_duration(), twelve_hours)

    def test_beginning_window_edge(self):
        one_second = 1
        visit = Visit(None, None, '3/17/2017 12:00:00', '3/17/2017 20:00:01')
        self.assertEqual(visit.get_applicable_duration(), one_second)

    def test_before_beginning_window(self):
        no_seconds = 0
        visit = Visit(None, None, '3/18/2017 18:00:00', '3/18/2017 20:00:00')
        self.assertEqual(visit.get_applicable_duration(), no_seconds)

    def test_end_window_edge(self):
        no_seconds = 0
        visit = Visit(None, None, '3/18/2017 8:00:00', '3/18/2017 12:00:00')
        self.assertEqual(visit.get_applicable_duration(), no_seconds)

    def test_before_end_window_edge(self):
        one_second = 1
        visit = Visit(None, None, '3/18/2017 7:59:59', '3/18/2017 12:00:00')
        self.assertEqual(visit.get_applicable_duration(), one_second)

    def test_partial_beginning_window(self):
        one_hour = 3600
        visit = Visit(None, None, '3/18/2017 18:00:00', '3/18/2017 21:00:01')
        self.assertEqual(visit.get_applicable_duration(), one_hour)


    def test_partial_end_window(self):
        three_hours = 10800
        visit = Visit(None, None, '3/18/2017 5:00:00', '3/18/2017 10:00:00')
        self.assertEqual(visit.get_applicable_duration(), three_hours)



    def test_parse_timestring(self):
        visit = Visit(None, None, '3/17/2017 20:42:43', '3/17/2017 20:42:43')
        self.assertEqual(
            visit._parse_time('3/17/2017 20:42:43'),
            datetime.datetime(2017, 3, 17, 20, 42, 43)
        )
        pass
