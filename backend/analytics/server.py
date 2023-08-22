from flask import Flask, jsonify
import json
import time
import datetime
import random

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def get_data():
    data = {
        "routerId": "10.100.2.23",
        "userId": "192.168.1.4",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "usagePerSec": random.randint(0, 30000),
        "totalUsage": random.randint(30000, 300000),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
