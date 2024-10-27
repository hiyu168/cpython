import http.server
import socketserver
import unittest

class TestHTTPServer(unittest.TestCase):

    def test_server_start(self):
        PORT = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            self.assertIsInstance(httpd, socketserver.TCPServer)

    def test_response_code(self):
        PORT = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            response = http.client.HTTPConnection('localhost', PORT)
            response.request('GET', '/')
            res = response.getresponse()
            self.assertEqual(res.status, 200)

    def test_file_serving(self):
        # Assuming the server serves files from the current directory
        PORT = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            response = http.client.HTTPConnection('localhost', PORT)
            response.request('GET', '/index.html')
            res = response.getresponse()
            self.assertEqual(res.status, 200)

    def test_404(self):
        PORT = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            response = http.client.HTTPConnection('localhost', PORT)
            response.request('GET', '/non_existent_file')
            res = response.getresponse()
            self.assertEqual(res.status, 404)

    def test_server_shutdown(self):
        PORT = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            self.assertIsNone(httpd.shutdown())
