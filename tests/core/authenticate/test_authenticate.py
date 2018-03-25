from datetime import datetime
from unittest import TestCase
import mock

from cheetahapi.core.authenticate import Authenticate


class TestAuthenticate(TestCase):
    """Tests for authenticate module."""

    exp_token = {"token": "foo-token", "date": "2018-03-24", "user_id": "1"}
    user_id = "1"
    user = "moe"
    pw = "pass"

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_token_has_valid_date(self, mock_get_today_date):
        """Test to check when the token has a valid date and it does not exceed the number of days when it's valid"""
        token_creation_date_string = "2018-03-23"
        auth = Authenticate()
        auth.set_token_days_valid(1)

        ret = auth.token_date_not_expired(token_creation_date_string)
        mock_get_today_date.assert_called_once()
        self.assertTrue(ret)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_token_has_not_valid_date(self, mock_get_today_date):
        """Test to check when the token has not a valid date and exceeds the number of days when it's valid"""
        token_creation_date_string = "2018-03-22"
        auth = Authenticate()
        auth.set_token_days_valid(1)

        ret = auth.token_date_not_expired(token_creation_date_string)
        mock_get_today_date.assert_called_once()
        self.assertFalse(ret)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_is_valid_token(self, mock_get_today_date):
        """Test a token is valid"""
        auth = Authenticate()
        auth.set_token_days_valid(1)
        exp_get_token_from_db = {"date": "2018-03-23"}
        with mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_from_db",
                        return_value=exp_get_token_from_db):
            is_valid = auth.is_valid_token(self.exp_token)
        mock_get_today_date.assert_called_once()
        self.assertTrue(is_valid)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_today_date",
                return_value=datetime.strptime("2018-03-24", "%Y-%m-%d"))
    def test_is_invalid_token(self, mock_get_today_date):
        """Test a token is not valid"""
        auth = Authenticate()
        auth.set_token_days_valid(1)
        exp_get_token_from_db = {"date": "2018-03-22"}
        with mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_from_db",
                        return_value=exp_get_token_from_db):
            is_valid = auth.is_valid_token(self.exp_token)
            mock_get_today_date.assert_called_once()
        self.assertFalse(is_valid)

    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token")
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=True)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id",
                return_value={"token": "foo-token", "date": "2018-03-24", "user_id": "1"})
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value={"user": "john", "id": "1"})
    def test_authenticate_ok(self, mock_get_user_from_db, mock_get_token_user_id,
                             mock_is_valid_token, mock_create_new_token):
        """Test to check authentication process is working"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        self.assertFalse(mock_create_new_token.called)
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(self.user_id)
        mock_is_valid_token.assert_called_once_with(self.exp_token["token"])
        self.assertEqual(self.exp_token["token"], token["token"])

    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token",
                return_value={"token": "foo-token", "date": "2018-03-24", "user_id": "1"})
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=True)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id", return_value=None)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value={"user": "john", "id": "1"})
    def test_authenticate_ok_create_new_token_from_none_token(self, mock_get_user_from_db, mock_get_token_user_id,
                                                              mock_is_valid_token, mock_create_new_token):
        """Test to check authentication process is working creating a new token because there was not previous token"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(self.user_id)
        mock_create_new_token.assert_called_once_with(self.user_id)
        self.assertFalse(mock_is_valid_token.called)
        self.assertEqual(self.exp_token["token"], token["token"])

    @mock.patch("cheetahapi.core.authenticate.Authenticate.create_new_token",
                return_value={"token": "foo-token", "date": "2018-03-24", "user_id": "1"})
    @mock.patch("cheetahapi.core.authenticate.Authenticate.is_valid_token",
                return_value=False)
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_token_user_id",
                return_value={"token": "foo-token", "date": "2018-03-24", "user_id": "1"})
    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value={"user": "john", "id": "1"})
    def test_authenticate_ok_create_new_token_from_invalid_token(self, mock_get_user_from_db, mock_get_token_user_id,
                                                                 mock_is_valid_token, mock_create_new_token):
        """Test to check authentication process is working creating a new token because previous token expired"""
        auth = Authenticate()

        token = auth.authenticate(self.user, self.pw)
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)
        mock_get_token_user_id.assert_called_once_with(self.user_id)
        mock_create_new_token.assert_called_once_with(self.user_id)
        mock_is_valid_token.assert_called_once_with(self.exp_token["token"])
        self.assertEqual(self.exp_token["token"], token["token"])

    @mock.patch("cheetahapi.core.authenticate.Authenticate.get_user_from_db",
                return_value=None)
    def test_authenticate_error_wrong_user_or_passwd(self, mock_get_user_from_db):
        auth = Authenticate()
        exp_token = token = 0
        try:
            token = auth.authenticate(self.user, self.pw)
            # To be sure that the exception is raised
            self.assertTrue(1 == 0)
        except Exception:
            self.assertEqual(exp_token, token)
        mock_get_user_from_db.assert_called_once_with(self.user, self.pw)


if __name__ == '__main__':
    unittest.main()
