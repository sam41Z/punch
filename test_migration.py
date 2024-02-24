from unittest import TestCase

from sqlalchemy import delete, select

from database import TimeRecordRow
from migrate import Migration
from repository import Repository


class TestMigration(TestCase):
    migration: Migration
    repository: Repository

    @classmethod
    def setUpClass(cls):
        cls.repository = Repository.test()
        cls.migration = Migration(cls.repository)

    def tearDown(self):
        with self.repository.Session.begin() as session:
            query = delete(TimeRecordRow)
            session.execute(query)

    def test_migrate(self):
        self.migration.migrate(2023)

        with self.repository.Session.begin() as session:
            results = session.execute(select(TimeRecordRow)).scalars().all()
            self.assertEqual(1, len(results))
