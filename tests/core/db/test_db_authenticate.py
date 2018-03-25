from unittest import TestCase
import mock

from cheetahapi.core.db.db_authenticate import DbAuthenticate
from tests.factories.factory_fixtures import TokenFactory, session


class TestDbAuthenticate(TestCase):

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.load_db_session")
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.set_db_config_dict")
    def test_get_token(self, mock_set_db_config_dict, mock_load_db_session):
        # Add fake data
        token = TokenFactory()

        auth = DbAuthenticate({})
        # Add test session from factory_fixture (database in memory for testing)
        auth.set_session(session)

        token_obj = auth.get_token(token.token)

        self.assertEqual(token.token, token_obj.token)
        mock_set_db_config_dict.assert_called_once_with({})
        mock_load_db_session.assert_called_once()
