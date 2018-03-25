import six
if six.PY2:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser


class Config(object):
    """
    Represent the information contained in the configuration file
    """
    DEFAULT_CONFIG_FILE = '/etc/cheetah-api/config.conf'
    CONFIG_SECTIONS = {'general': 'GENERAL', 'database': 'DATABASE'}

    def __init__(self):
        """
        Constructor
        """
        self.config_parser = RawConfigParser()
        self.general = None
        self.database = None

    def get_parser(self):
        """
        Get the ConfigParser instance

        :return: ConfigParser instance
        """
        return self.config_parser

    def get_general(self):
        """
        Get the general information attribute

        :return: dict with data from GENERAL section
        """
        return self.general

    def get_database(self):
        """
        Get the database information attribute

        :return: dict with data from DATABASE section
        """
        return self.database

    def read_file(self, filename):
        """
        Open the given file and read it

        :param filename: Pathname of the file to be opened
        """
        with open(filename) as fp:
            self.read_data(fp)

    def read_data(self, file_handler):
        """
        Read the information (provided by the file handler) by the ConfigParser

        :param file_handler: File handler for the information to be read
        """
        self.config_parser.readfp(file_handler)

    def map_section(self, section, is_list=False):
        """
        Map a given config section into a dictionary

        :param section: Section to be mapped
        :param is_list: Defines whether the options of the section are a list of values
        :return: Dictionary with the options and values of the given section
        """
        section_dict = {}
        options = self.config_parser.options(section)
        for option in options:
            item = self.config_parser.get(section, option)
            section_dict[option] = self.get_list(item) if is_list else item
        return section_dict

    def read_general(self):
        """
        Get general data contained in the config file

        :return: Data object from GENERAL section in the config file
        """
        return self.map_section(self.CONFIG_SECTIONS['general'])

    def read_database(self):
        """
        Get database data contained in the config file

        :return: Data object from DATABASE section in the config file
        """
        ret = self.map_section(self.CONFIG_SECTIONS['database'])
        ret["db_port"] = int(ret["db_port"])
        return ret

    def load_config_data(self):
        """
        Load configuration data
        """
        self.general = self.read_general()
        self.database = self.read_database()

    def load_config_file(self, config_file=DEFAULT_CONFIG_FILE):
        """
        Load config file passed as an argument. There is a default config file

        :param config_file: Path file to configuration file to be read
        """
        self.read_file(config_file)
        self.load_config_data()

    def get_list(self, str_with_sep, sep=',', chars=None):
        """
        Return a list from a delimited string

        :param str_with_sep: String to be split into a list of values
        :param sep: Separator. Commas by default
        :param chars: Character stripped. Whitespaces by default
        :return: List of values extracted from the option
        """
        return [chunk.strip(chars) for chunk in str_with_sep.split(sep)]
