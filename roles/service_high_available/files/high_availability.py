from flask import Flask, jsonify
import requests
import redis
import json
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


def is_redis_available(rs):
    # Check Redis connection
    try:
        rs.get(None)  # getting None returns None or throws an exception
        logging.info("Redis connection successful")
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError) as err:
        logging.error(err)
        return False  # Return False if can't connect
    return True


def fetch_data():
    with open('config.json') as json_data:
        d = json.load(json_data)    # Loads configuration
        logging.info("confg loaded successfully %s" % (d))
        while True:
            try:        # Try except block to try connection until success
                resp = requests.get(    # Make request to api
                    d['date_endpoint'],
                    timeout=(float(d['timeout_conn']),
                             int(d['timeout_read'])))
                if resp.status_code == 200:
                    logging.info("Request Successful from URL %s"
                                 % (resp.status_code))
                    r = redis.StrictRedis(host='localhost',
                                          port=6379, db=0)
                    if is_redis_available(r):  # Check if redis is avail
                        r.set('date', resp.text)
                        logging.info
                        ("Response from redis %s" % (resp.text))
            except requests.exceptions.Timeout as err:
                logging.error(err)
                continue        # Continue back till receive success
            break
    return jsonify({"success": True})


@app.route('/', methods=["GET"])  # method api for storing in redis
def index():
    fetch_data()
    return jsonify({"success": True})


@app.route('/date', methods=["GET"])    # Get request for date querying
def get_date():                         # stored data in redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    if is_redis_available(r):       # Check if redis is available
        date = r.get('date')        # Get data from redis
        if date != "":
            logging.info("Get data successful %s" % (date))
        else:
            logging.erro("Date not available in redis")
    return date                     # return date to calling api


if __name__ == '__main__':
    logger = logging.getLogger()    # Impelement logger
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)   # set logger to info level
    fh = RotatingFileHandler(       # Log rotate
        '/usr/local/src/service/service.log',
        maxBytes=10000, backupCount=1)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    app.run(host='127.0.0.1', port=8081, debug=False)
