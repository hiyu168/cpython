import http.server
import socketserver
import unittest
import threading
import time
import http.client

class TestHTTPServer(unittest.TestCase):

    def setUp(self):
        # Start the server in a separate thread
        self.PORT = 8000
        self.handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", 0), self.handler)  # Bind to a random available port
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)  # Allow some time for the server to start

    def tearDown(self):
        # Shutdown the server and close the thread
        self.httpd.shutdown()
        self.server_thread.join()

    def test_server_start(self):
        self.assertTrue(self.server_thread.is_alive())

    def test_response_code(self):
        connection = http.client.HTTPConnection('localhost', self.PORT)
        connection.request('GET', '/')
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        connection.close()

    def test_file_serving(self):
        connection = http.client.HTTPConnection('localhost', self.PORT)
        connection.request('GET', '/index.html')  # Assuming index.html exists
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        connection.close()

    def test_404(self):
        connection = http.client.HTTPConnection('localhost', self.PORT)
        connection.request('GET', '/non_existent_file')
        response = connection.getresponse()
        self.assertEqual(response.status, 404)
        connection.close()

    def test_server_shutdown(self):
        # This test checks if the server can be shutdown properly.
        self.httpd.shutdown()
        self.assertFalse(self.server_thread.is_alive())
