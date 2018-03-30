from flask import Flask, request, abort, jsonify

import sys
import getopt


from core.config import Config
from dispacher import Dispacher

app = Flask(__name__)


def parse_arguments(args):
    """
    Parses command-line arguments passed to the main program

    :param args: List with command-line parameters passed to the main
    :return: Dictionary with general configuration
             {"-c": "..."}
    :raise GetoptError: if error when parsing arguments
    """
    optlist, args = getopt.getopt(args, "c:")

    parameters = {"-c": Config.DEFAULT_CONFIG_FILE}

    for o, v in optlist:
        parameters[o] = v

    return parameters


def read_configuration(config_file_path):
    """
    Reads configuration and loads it into a Config object

    :param config_file_path: String with general configuration file path
    :return: Config object
    :raise Exception: if there is an error during the reading
    """
    config_obj = Config()
    config_obj.load_config_file(config_file_path)
    return config_obj


"""
Usage:
    main.py [-c <conf_file>]

:return 0: Application was executed and successfully stopped after a while
:return -1: Wrong input parameters
:return -2: Error when reading the configuration
"""
# parse command-line arguments
try:
    params = parse_arguments(sys.argv[1:])
except getopt.GetoptError:
    print("\nUsage:\n\tmain.py [-c <conf_file>]\n")
    sys.exit(-1)

config = read_configuration(params["-c"])


def get_json_response(response):
    return jsonify(response.to_json())


@app.route("/v1/authenticate", methods = ['POST'])
def authenticate():
    if not request.is_json:
        abort(400)
    dispacher = Dispacher(config)
    response = dispacher.authenticate(request.get_json())
    print request.get_json()
    return get_json_response(response)


@app.route("/ping")
def ping():
    return "cheetah-api version {0} up and running!".format(config.get_general()["version"])


if __name__ == "__main__":
    app.run(host=config.get_general()["host"], port=int(config.get_general()["port"]))
