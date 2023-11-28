from flask import Flask, jsonify
import json_tricks as json
import argparse
from main import main

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_data() -> str:
    """
    Get the data from the main function and return it as a JSON object.
    """

    data = main()
    json_data = json.dumps(data, indent=4, sort_keys=True)
    return json_data


@app.route("/position", methods=["POST"])
def post_position() -> str:
    """
    Post the position of the robot to the server.
    """

    position = {"x": 1, "y": 2, "z": 3}
    return jsonify(position)


def run_flask_app(port):
    """
    Run the Flask app.
    """

    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Flask HTTP server.")
    parser.add_argument(
        "-p", "--port", type=int, default=8585, help="Port to run the server on."
    )
    args = parser.parse_args()
    run_flask_app(args.port)
