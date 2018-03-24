from flask import Flask
from flask import jsonify
app = Flask(__name__)


@app.route("/ping")
def ping():
    return "cheeta-api version 1.0 up and running!"


def main():
    return 1


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
