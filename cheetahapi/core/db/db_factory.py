from sqlalchemy import create_engine


class DbFactory(object):

    """The driver list"""
    db_driver_list = ["postgresql"]

    def get_engine(self, db_config_dict):
        """
        Method to return the database engine built and ready to be connected for the driver indicated in db_config_dict

        :param db_config_dict: Dict with all configuration values for database connection
        :return: DB Engine to be connected
        """
        if "db_driver" not in db_config_dict:
            raise Exception("Parameter 'db_driver' must be configured in configuration file")
        return create_engine(self.build_engine_connection_string(db_config_dict))

    def build_engine_connection_string(self, db_config_dict):
        """
        Build the string connection from configuration parameters

        :param db_config_dict: Dict with all configuration values for database connection
        :raise Exception: When the driver is not found in the implementation
        :return: String
        """
        if db_config_dict["db_driver"] not in self.db_driver_list:
            raise Exception("Database driver {0} not allowed".format(db_config_dict["db_driver"]))
        driver = db_config_dict["db_driver"]
        username = db_config_dict["db_username"]
        pwd = db_config_dict["db_pwd"]
        host = db_config_dict["db_host"]
        port = db_config_dict["db_port"]
        db_name = db_config_dict["db_name"]
        return '{0}://{1}:{2}@{3}:{4}/{5}'.format(driver, username, pwd, host, port, db_name)
