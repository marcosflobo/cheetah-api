from unittest import TestCase
import mock
import uuid

from cheetahapi.core.db.db_authenticate import DbAuthenticate
from tests.factories.factory_fixtures import TokenFactory, session, UserFactory

exp_token = TokenFactory()
exp_user = UserFactory()

class TestDbAuthenticate(TestCase):

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_token(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_obj = auth.get_token(exp_token.token)

        self.assertEqual(exp_token.token, token_obj.token)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_token_not_found(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_obj = auth.get_token("foo")

        self.assertEqual(None, token_obj)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_user_from_db(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        user_obj = auth.get_user_from_db(exp_user.username, exp_user.pw)

        self.assertEqual(exp_user.username, user_obj.username)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_user_from_db_not_found(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        user_obj = auth.get_user_from_db("foo", "bar")

        self.assertEqual(None, user_obj)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_token_user_id(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_string = auth.get_token_user_id(exp_user.id)

        self.assertEqual(exp_token.token, token_string)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_token_user_id_not_found(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_string = auth.get_token_user_id("9999")

        self.assertEqual(None, token_string)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_create_new_token(self, mock_set_db_config_dict, mock_load_db_session):
        auth = DbAuthenticate()
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_string = auth.create_new_token(uuid.uuid4().hex)

        self.assertNotEqual(None, token_string)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()