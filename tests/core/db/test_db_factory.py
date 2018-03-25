from unittest import TestCase

from cheetahapi.core.db.db_factory import DbFactory


class TestDbFactory(TestCase):

    def test_build_engine_connection_string(self):
        """Test get string connection to the database"""
        db_config_dict = {
            'db_driver': 'postgresql',
            'db_host': 'localhost',
            'db_port': 5432,
            'db_name': 'foo-database',
            'db_username': 'foo-username',
            'db_pwd': 'foo-pwd',
        }
        exp_string = '{0}://{1}:{2}@{3}:{4}/{5}'.format(db_config_dict['db_driver'],
                                                        db_config_dict['db_username'],
                                                        db_config_dict['db_pwd'],
                                                        db_config_dict['db_host'],
                                                        db_config_dict['db_port'],
                                                        db_config_dict['db_name'])
        db_factory = DbFactory()
        ret = db_factory.build_engine_connection_string(db_config_dict)
        self.assertEqual(exp_string, ret)

    def test_build_engine_connection_string_exception(self):
        """Test exception raised when there is no configuration data for the DB"""
        db_config_dict = {"db_driver": "foo-driver"}
        db_factory = DbFactory()
        try:
            db_factory.build_engine_connection_string(db_config_dict)
            self.assertTrue(1 == 0)
        except Exception as e:
            self.assertNotEqual(None, e)

    def test_get_engine_exception(self):
        """Test an exception is raised from get_engine method when there is no information about the driver"""
        db_factory = DbFactory()
        try:
            db_factory.build_engine_connection_string({})
            self.assertTrue(1 == 0)
        except Exception as e:
            self.assertNotEqual(None, e)

    def test_get_engine(self):
        """Test get the sqlalchemy engine built"""
        db_config_dict = {
            'db_driver': 'postgresql',
            'db_host': 'localhost',
            'db_port': 5432,
            'db_name': 'cheetah-api',
            'db_username': 'cheetah-api',
            'db_pwd': 'cheetah-api',
        }

        db_factory = DbFactory()
        engine = db_factory.get_engine(db_config_dict)
        self.assertNotEqual(None, engine)
