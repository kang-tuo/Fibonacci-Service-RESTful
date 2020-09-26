from flask import Flask, jsonify, make_response
from redis import Redis
from redis import exceptions as redis_exceptions
from combi_finder import CombiFinder

import configparser
import pickle
import logging

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


@app.route("/", methods=["GET"])
def welcome():
    return f"Welcome to Fibonacci app."


@app.route("/fib/<number>", methods=["GET"])
def fib(number):
    # TODO(charlie): add negative number exception handling
    number = int(number)
    try:
        combinations = redis.get(number)
    except (redis_exceptions.ConnectionError, ValueError, NameError):
        # exception if no redis attached or config is wrong
        logging.warning("No connection to cache")
        combi_finder = CombiFinder()
        combinations = combi_finder.find_combinations(number)
        return make_response(jsonify(combinations), 200)

    if combinations:
        # if there is a connection, and value is cached
        combinations = pickle.loads(combinations)
        return make_response(jsonify(combinations), 200)
    else:
        # if there is a connection, but now such value in cache
        combi_finder = CombiFinder()
        combinations = combi_finder.find_combinations(number)
        redis.set(number, pickle.dumps(combinations))

        return make_response(jsonify(combinations), 200)


@app.route("/health", methods=["GET"])
def heartbeat():
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


