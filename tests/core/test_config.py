from cheetahapi.core.config import Config
import six
if six.PY2:
    from ConfigParser import RawConfigParser, MissingSectionHeaderError, NoSectionError
else:
    from configparser import RawConfigParser, MissingSectionHeaderError, NoSectionError
import io
import os
import tempfile
from unittest import TestCase


general_data = '''[GENERAL]
log_format = %(whateverformat)s
log_file = /var/log/cheetah-api/cheetah-api.log
log_level=CRITICAL'''

database_data = '''[DATABASE]
db_driver = postgresql
db_host = localhost
db_port = 5432
db_name = cheetah-api
db_username = cheetah-api
db_pwd = 1234'''


def io_bytesio(bytes_string):
    """
    Makes compatibility Py2/Py3
    :param bytes_string:
    :return:
    """
    if six.PY2:
        return bytes_string
    return bytes(bytes_string, 'utf8')


class TestConfig(TestCase):

    def setUp(self):
        self.cr = Config()

    def test_get_parser_returns_correct_object(self):
        """Test get_parser returns proper ConfigParser instance"""
        parser = self.cr.get_parser()

        self.assertIsInstance(parser, RawConfigParser)

    def test_read_data_raises_exception_when_no_sections_found(self):
        """Test read_data raises exception when no sections are found"""
        fh = io.BytesIO(io_bytesio('Some test data without sections'))

        with self.assertRaises(MissingSectionHeaderError):
            self.cr.read_data(fh)

    def test_read_data_with_iostream_reads_correctly(self):
        """Test read_data handles iostream inputs properly"""
        expected_section = ['GENERAL']
        fh = io.BytesIO(io_bytesio(general_data))

        self.cr.read_data(fh)
        parser = self.cr.get_parser()
        section = parser.sections()

        self.assertEqual(expected_section, section)
        self.assertEqual(1, len(section))

    def test_read_data_with_temporary_file_reads_correctly(self):
        """Test read_data handles file inputs properly"""
        expected_section = ['GENERAL']

        with tempfile.TemporaryFile() as fh:
            fh.write(general_data)
            fh.seek(0)
            self.cr.read_data(fh)
        parser = self.cr.get_parser()
        section = parser.sections()

        self.assertEqual(expected_section, section)
        self.assertEqual(1, len(section))

    def test_read_file_raises_exception_when_wrong_number_of_arguments(self):
        """Test read_file raises exception when called with wrong number of arguments"""
        with self.assertRaises(TypeError):
            self.cr.read_file()

    def test_read_file_raises_exception_when_wrong_filename(self):
        """Test read_file raises exception when called with wrong filename"""
        with self.assertRaises(IOError):
            self.cr.read_file('non_existing_file.ini')

    def test_read_file_with_temporary_file_opens_correctly(self):
        """Test read_file opens file properly"""
        expected_section = ['GENERAL']

        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(general_data)
        self.cr.read_file(fh.name)
        os.remove(fh.name)
        parser = self.cr.get_parser()
        section = parser.sections()

        self.assertEqual(expected_section, section)
        self.assertEqual(1, len(section))

    def test_map_section_raises_exception_when_not_found(self):
        """Test map_section raises exception when section not found"""
        fh = io.BytesIO(io_bytesio('[NON_DESIRED_SECTION]\ndata = some test data without desired section'))
        self.cr.read_data(fh)

        with self.assertRaises(NoSectionError):
            self.cr.map_section('GENERAL')

    def test_read_general_returns_correct_object(self):
        """Test read_general returns correct General data dict"""
        expected_log_format = '%(whateverformat)s'
        expected_log_file = '/var/log/cheetah-api/cheetah-api.log'
        expected_log_level = 'CRITICAL'
        fh = io.BytesIO(io_bytesio(general_data))
        self.cr.read_data(fh)

        general_obj = self.cr.read_general()

        self.assertEqual(expected_log_format, general_obj["log_format"])
        self.assertEqual(expected_log_file, general_obj["log_file"])
        self.assertEqual(expected_log_level, general_obj["log_level"])

    def test_read_database_returns_correct_object(self):
        """Test read_database returns correct DATABASE data dict"""
        exp_db_driver = 'postgresql'
        exp_db_host = 'localhost'
        exp_db_port = 5432
        exp_db_name = 'cheetah-api'
        exp_db_username = 'cheetah-api'
        exp_db_pwd = '1234'
        fh = io.BytesIO(io_bytesio(database_data))
        self.cr.read_data(fh)

        database_obj = self.cr.read_database()

        self.assertEqual(exp_db_driver, database_obj["db_driver"])
        self.assertEqual(exp_db_host, database_obj["db_host"])
        self.assertEqual(exp_db_port, database_obj["db_port"])
        self.assertEqual(exp_db_name, database_obj["db_name"])
        self.assertEqual(exp_db_username, database_obj["db_username"])
        self.assertEqual(exp_db_pwd, database_obj["db_pwd"])

    def tearDown(self):
        self.cr = None

if __name__ == '__main__':
    unittest.main()
