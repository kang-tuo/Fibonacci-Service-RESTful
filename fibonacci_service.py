from flask import Flask, jsonify, make_response
from redis import Redis
from redis import exceptions as redis_exceptions

import configparser
import pickle
import logging

from generator import Generator

config = configparser.ConfigParser()
config.read("config/config.ini")

app = Flask(__name__)
try:
    port = config["REDIS"]["port"]
    host = config["REDIS"]["host"]
except KeyError:
    host = "redis"
    port = 6379

redis = Redis(host=host, port=port)


@app.route("/fib/<number>", methods=["GET"])
def get_fib_combinations(number):
    f1 = 2
    if number < f1 or not isinstance(number, int):
        msg = "input should be an integer which is larger than 2"
        raise ValueError("invalid input: {0}".format(msg))
    else:
        number = int(number)
    try:
        combinations = redis.get(number)
    except (redis_exceptions.ConnectionError, ValueError, NameError):
        logging.warning("No connection to cache")
        combinations_generator = Generator()
        combinations = combinations_generator.generate_combinations(number)
        return make_response(jsonify(combinations), 200)

    if combinations:
        combinations = pickle.loads(combinations)
        return make_response(jsonify(combinations), 200)
    else:
        # if there is a connection, but no such value in cache
        combinations_generator = Generator()
        combinations = combinations_generator.generate_combinations(number)
        redis.set(number, pickle.dumps(combinations))

        return make_response(jsonify(combinations), 200)


@app.route("/health", methods=["GET"])
def health():
    response = jsonify(success=True)
    return response


if __name__ == "__main__":
    try:
        debug = bool(config["FIBO_APP"]["port"])
        host = config["FIBO_APP"]["host"]
    except KeyError:
        debug = False
        host = "0.0.0.0"
    app.run(debug=debug, host=host)
