from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import argparse

from main import main


class Server(BaseHTTPRequestHandler):
    """
    Handles HTTP requests to the server.
    """

    def _set_response(self, code: int = 200, content_type: str = "text/html"):
        """
        Sets the response code and headers.

        Args:
            code (int): The response code.
            content_type (str): The content type for the response.
        """

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        """
        GET request handler.
        """

        data = main()

        # convert data to json
        json_data = json.dumps(data)

        self._set_response()
        self.wfile.write(json_data.encode("utf-8"))

    def do_POST(self):
        """
        POST request handler.
        """

        position = {"x": 1, "y": 2, "z": 3}

        self._set_response()
        self.wfile.write(str(position).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=Server, port: int = 8585):
    """
    Runs the server on the specified port.

    Args:
        server_class (HTTPServer): The server class.
        handler_class (Server): The handler class.
        port (int): The port to run the server on.
    """

    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)

    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server.")

    parser.add_argument(
        "-p", "--port", type=int, default=8585, help="Port to run the server on."
    )

    args = parser.parse_args()

    run(port=args.port)
