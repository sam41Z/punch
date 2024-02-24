from datetime import date, time
from unittest import TestCase

from sqlalchemy import delete, select

from database import TimeRecordRow
from model import TimeRecord
from repository import Repository


class TestRepository(TestCase):
    repository: Repository

    @classmethod
    def setUpClass(cls):
        cls.repository = Repository.test()

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        with self.repository.Session.begin() as session:
            query = delete(TimeRecordRow)
            session.execute(query)

    def test_emtpy(self):
        result = self.repository.get_by_year_and_week(2024, 8)
        self.assertEqual(len(result), 0)

    def test_no_overlap_after(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(11))
        second = TimeRecord.create(d, time(11), time(13))
        self.assert_no_overlap(first, second)

    def test_no_overlap_before(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(11))
        second = TimeRecord.create(d, time(7), time(9))
        self.assert_no_overlap(first, second)

    def test_overlap_after(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(12))
        second = TimeRecord.create(d, time(11), time(13))
        self.assert_overlap(first, second)

    def test_overlap_before(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(12))
        second = TimeRecord.create(d, time(8), time(10))
        self.assert_overlap(first, second)

    def test_overlap_within(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(12))
        second = TimeRecord.create(d, time(10), time(11))
        self.assert_overlap(first, second)

    def test_overlap_over(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(12))
        second = TimeRecord.create(d, time(8), time(13))
        self.assert_overlap(first, second)

    def test_overlap_exact(self):
        d = date(2024, 2, 24)
        first = TimeRecord.create(d, time(9), time(12))
        second = TimeRecord.create(d, time(9), time(12))
        self.assert_overlap(first, second)

    def test_in_weeks_range(self):
        week_start = date(2024, 2, 19)
        week_end = date(2024, 2, 25)

        first = TimeRecord.create(week_start, time(0), time(1))
        self.repository.create_record(first)
        last = TimeRecord.create(week_end, time(23), time(23, 59))
        self.repository.create_record(last)
        records = self.repository.get_by_year_and_week(week_start.year, week_start.isocalendar().week)
        self.assertEqual(2, len(records))

    def test_out_of_weeks_range(self):
        week_start = date(2024, 2, 19)

        first = TimeRecord.create(date(2024, 2, 18), time(23), time(23, 59))
        self.repository.create_record(first)
        last = TimeRecord.create(date(2024, 2, 26), time(0), time(1))
        self.repository.create_record(last)
        records = self.repository.get_by_year_and_week(week_start.year, week_start.isocalendar().week)
        self.assertEqual(0, len(records))

    def assert_no_overlap(self, first, second):
        self.repository.create_record(first)
        self.repository.create_record(second)
        with self.repository.Session.begin() as session:
            results = session.execute(select(TimeRecordRow)).scalars().all()
            self.assertEqual(2, len(results))
            first_result = results[0]
            self.assertEqual(first.starts_at, first_result.starts_at)
            self.assertEqual(first.ends_at, first_result.ends_at)
            second_result = results[1]
            self.assertEqual(second.starts_at, second_result.starts_at)
            self.assertEqual(second.ends_at, second_result.ends_at)

    def assert_overlap(self, first, second):
        self.repository.create_record(first)
        self.assertRaises(ValueError, self.repository.create_record, second)
        with self.repository.Session.begin() as session:
            results = session.execute(select(TimeRecordRow)).scalars().all()
            self.assertEqual(1, len(results))
            result = results[0]
            self.assertEqual(first.starts_at, result.starts_at)
            self.assertEqual(first.ends_at, result.ends_at)
