from datetime import datetime
from unittest import TestCase
import mock

from cheetahapi.core.authenticate import Authenticate
from cheetahapi.core.db.model import Token

from tests.factories.factory_fixtures import UserFactory
from tests.factories.factory_fixtures import TokenFactory

exp_token = TokenFactory()
exp_user = UserFactory()

class TestAuthenticate(TestCase):
    """Tests for authenticate module."""

    user_id = "1"
    user = "moe"
    pw = "pass"

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_token_has_valid_date(self, mock_get_today_date):
        """Test to check when the token has a valid date and it does not exceed the number of days when it's valid"""
        token_creation_date_string = "2018-03-23 00:00:01.377000"
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        auth.set_token_days_valid(1)

        ret = auth.token_date_not_expired(token_creation_date_string)
        mock_get_today_date.assert_called_once()
        self.assertTrue(ret)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f"))
    def test_token_has_not_valid_date(self, mock_get_today_date):
        """Test to check when the token has not a valid date and exceeds the number of days when it's valid"""
        token_creation_date_string = "2018-03-22 00:00:00.0"
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        auth.set_token_days_valid(1)

        ret = auth.token_date_not_expired(token_creation_date_string)
        mock_get_today_date.assert_called_once()
        self.assertFalse(ret)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_is_valid_token(self, mock_get_today_date):
        """Test a token is valid"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        auth.set_token_days_valid(1)
        exp_get_token_from_db = Token()
        exp_get_token_from_db.created = "2018-03-23 00:00:01.377000"
        with mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_from_db",
                        return_value=exp_get_token_from_db):
            is_valid = auth.is_valid_token(exp_token)
        mock_get_today_date.assert_called_once()
        self.assertTrue(is_valid)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f"))
    def test_is_invalid_token(self, mock_get_today_date):
        """Test a token is not valid"""
        auth = Authenticate()
        auth.set_token_days_valid(1)
        exp_get_token_from_db = Token()
        exp_get_token_from_db.created = "2018-03-22 00:00:00.0"
        with mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_from_db",
                        return_value=exp_get_token_from_db):
            is_valid = auth.is_valid_token(exp_token)
            mock_get_today_date.assert_called_once()
        self.assertFalse(is_valid)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=True)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id",
                return_value=exp_token.token)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value=exp_user)
    def test_authenticate_ok(self, mock_get_user_from_db, mock_get_token_user_id,
                             mock_is_valid_token, mock_create_new_token, mock_load_db_manager):
        """Test to check authentication process is working"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        self.assertFalse(mock_create_new_token.called)
        mock_load_db_manager.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(0)
        mock_is_valid_token.assert_called_once_with("token-0")
        self.assertEqual("token-0", token)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token",
                return_value=exp_token)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=True)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id", return_value=None)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value=exp_user)
    def test_authenticate_ok_create_new_token_from_none_token(self, mock_get_user_from_db, mock_get_token_user_id,
                                                              mock_is_valid_token, mock_create_new_token,
                                                              mock_load_db_manager):
        """Test to check authentication process is working creating a new token because there was not previous token"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        mock_load_db_manager.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(exp_user.id)
        mock_create_new_token.assert_called_once_with(exp_user.id)
        self.assertFalse(mock_is_valid_token.called)
        self.assertEqual(exp_token.token, token.token)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token",
                return_value=exp_token)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=False)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id",
                return_value=exp_token.token)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value=exp_user)
    def test_authenticate_ok_create_new_token_from_invalid_token(self, mock_get_user_from_db, mock_get_token_user_id,
                                                                 mock_is_valid_token, mock_create_new_token,
                                                                 mock_load_db_manager):
        """Test to check authentication process is working creating a new token because previous token expired"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        mock_load_db_manager.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(exp_user.id)
        mock_create_new_token.assert_called_once_with(exp_user.id)
        mock_is_valid_token.assert_called_once_with(exp_token.token)
        self.assertEqual(exp_token.token, token.token)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value=None)
    def test_authenticate_error_wrong_user_or_passwd(self, mock_get_user_from_db, mock_load_db_manager):
        auth = Authenticate()
        try:
            auth.authenticate(self.user, self.pw)
            # To be sure that the exception is raised
            self.assertTrue(1 == 0)
        except Exception:
            self.assertTrue(1 == 1)
        mock_load_db_manager.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_get_token_from_db(self, mock_db_init):
        """Test get token from database filtering by token string, which is unique"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        with mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.get_token", return_value=exp_token)\
                as mock_get_token:
            ret = auth.get_token_from_db(exp_token.token)
            self.assertEqual(exp_token.token, ret.token)
            mock_get_token.assert_called_once_with(exp_token.token)
            mock_db_init.assert_called_once()

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.get_user_from_db", return_value=exp_user)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_get_user_from_db(self, mock_db_init, mock_get_user_from_db):
        """Test to get a user from the database using username and password"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        user_ret = auth.get_user_from_db(exp_user.username, exp_user.pw)
        self.assertEqual(exp_user.username, user_ret.username)
        mock_db_init.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(exp_user.username, exp_user.pw)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.get_user_from_db", return_value=None)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_get_user_from_db_not_found(self, mock_db_init, mock_get_user_from_db):
        """Test return None user when the username or password is wrong"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        username = "foo"
        pw = "bar"
        user_ret = auth.get_user_from_db(username, pw)
        self.assertEqual(None, user_ret)
        mock_db_init.assert_called_once()
        mock_get_user_from_db.assert_called_once_with(username, pw)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.get_token_user_id", return_value=exp_token)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_get_token_user_id(self, mock_db_init, mock_get_token_user_id):
        """Test get token from a user id that has token"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        token_ret = auth.get_token_user_id(exp_user.id)
        self.assertEqual(exp_token.token, token_ret.token)
        mock_db_init.assert_called_once()
        mock_get_token_user_id.assert_called_once_with(exp_user.id)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.get_token_user_id", return_value=None)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_get_token_user_id_not_found(self, mock_db_init, mock_get_token_user_id):
        """Test None token from a user id that has NOT token"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        user_id = 99999
        token_ret = auth.get_token_user_id(user_id)
        self.assertEqual(None, token_ret)
        mock_db_init.assert_called_once()
        mock_get_token_user_id.assert_called_once_with(user_id)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.create_new_token", return_value=exp_token.token)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_create_new_token(self, mock_db_init, mock_create_new_token):
        """Test get token from a user id that has token"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        token_ret = auth.create_new_token(exp_user.id)
        self.assertEqual(exp_token.token, token_ret)
        mock_db_init.assert_called_once()
        mock_create_new_token.assert_called_once_with(exp_user.id)

    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.create_new_token", return_value=None)
    @mock.patch("cheetahapi.core.db.db_authenticate.DbAuthenticate.__init__", return_value=None)
    def test_create_new_token_not_found(self, mock_db_init, mock_create_new_token):
        """Test get token from a user id that has token"""
        with mock.patch("cheetahapi.core.authenticate.Authenticate.load_db_manager"):
            auth = Authenticate()
        user_id = 99999
        token_ret = auth.create_new_token(user_id)
        self.assertEqual(None, token_ret)
        mock_db_init.assert_called_once()
        mock_create_new_token.assert_called_once_with(user_id)


if __name__ == '__main__':
    unittest.main()
