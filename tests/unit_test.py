
import http.server
import socketserver
import unittest
import threading
import time
import http.client

class TestHTTPServer(unittest.TestCase):

   def setUp(self):
        # Create a temporary directory and add an index.html file
        self.temp_dir = TemporaryDirectory()
        with open(os.path.join(self.temp_dir.name, "index.html"), "w") as f:
            f.write("<html><body><h1>Test Index Page</h1></body></html>")

        # Start the server in a separate thread with a random available port
        self.handler = http.server.SimpleHTTPRequestHandler
        os.chdir(self.temp_dir.name)  # Change to the temp directory
        self.httpd = socketserver.TCPServer(("", 0), self.handler)  # Bind to a random available port
        self.PORT = self.httpd.server_address[1]  # Get the port assigned by the OS
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)  # Allow more time for the server to start

    def tearDown(self):
        # Shutdown the server and close the thread
        self.httpd.shutdown()
        self.server_thread.join()

    def test_server_start(self):
        self.assertTrue(self.server_thread.is_alive())

    def test_response_code(self):
        connection = http.client.HTTPConnection('127.0.0.1', self.PORT)  # Use 127.0.0.1 instead of localhost
        connection.request('GET', '/')
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        connection.close()

    def test_file_serving(self):
        connection = http.client.HTTPConnection('127.0.0.1', self.PORT)  # Use 127.0.0.1 instead of localhost
        connection.request('GET', '/index.html')  # Assuming index.html exists
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        connection.close()

    def test_404(self):
        connection = http.client.HTTPConnection('127.0.0.1', self.PORT)  # Use 127.0.0.1 instead of localhost
        connection.request('GET', '/non_existent_file')
        response = connection.getresponse()
        self.assertEqual(response.status, 404)
        connection.close()

    def test_server_shutdown(self):
        self.httpd.shutdown()
        self.assertFalse(self.server_thread.is_alive())
