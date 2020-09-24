import socket
import json

from email.parser import Parser

from request import Request
from storage import Storage
from translate import transliterate

MAX_LINE = 2**16
MAX_HEADERS = 100


class HTTPServer:
    """HTTP single stream server"""
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._cities = Storage()

    def run_forever(self):
        """Method for run server and listen socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            sock.bind((self._host, self._port))
            sock.listen()

            while True:
                conn, _ = sock.accept()
                try:
                    self.server_client(conn)
                except Exception as e:
                    print("client failed", e)
        finally:
            sock.close()

    def server_client(self, conn):
        """Method for connection with client and transport info"""
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        """
        Method for parsing income requests
        (connection) -> Request
        """
        file = conn.makefile('rb')
        method, target, ver = self.parse_request_line(file)
        headers = self.parse_headers(file)
        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        return Request(method, target, ver, headers, file)


    def parse_request_line(self, file):
        """Method for parsing request line for method name, target and HTTP version
        (binary file) -> str, str, str"""
        raw = file.readline(MAX_LINE+1)
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad request',
                            'Request line is too long')

        words = str(raw, 'iso-8859-1').split()

        if len(words) != 3:
            raise HTTPError(400, 'Bad request',
                            'Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')
        return method, target, ver

    def parse_headers(self, file):
        """Method for parsing headers
        (binary file) -> <class 'email.message.Message'>
        """

        headers = []
        while True:
            line = file.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')

        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)


    def handle_request(self, req):
        """Routing method for handling requests
        (Request) -> Response"""
        if req.path.startswith("/cities/"):
            city_id = req.path[len("/cities/"):]
            if city_id.isdigit():
                return self.handle_get_city(req, city_id)

        if req.path.startswith("/citylist"):
            return self.handle_get_citylist(req)

        if req.path.startswith("/citycompare"):
            return self.handle_city_compare(req)

        raise Exception("Not found")

    def handle_city_compare(self,req):
        """Challenge #3: City comparing to find what city is north
         and the difference between their timezones
         (Request) -> Response"""
        def _get_timezone_difference(long1, long2):

            return long2 / 15 - long1 / 15

        def _search_city(city1, city2,city1_trans,city2_trans):
            value1 = ""
            value2 = ""

            for key, value in self._cities.data.items():
                if value["name"].lower() == city1_trans \
                        or value["asciiname"].lower() == city1_trans \
                        or city1 in [i.lower() for i in value["alternatenames"]]:
                    if value1 != "" and value["population"] > value1["population"]:
                        value1 = value
                    elif value1 == "":
                        value1 = value
                if value["name"].lower() == city2_trans \
                        or value["asciiname"].lower() == city2_trans \
                        or city2 in [i.lower() for i in value["alternatenames"]]:
                    if value2 != "" and value["population"] > value2["population"]:
                        value2 = value
                    elif value2 == "":
                        value2 = value
            return value1, value2

        try:
            city1 = req.query["city1"][0]
            city1_trans = transliterate(city1)
            city2 = req.query["city2"][0]
            city2_trans = transliterate(city2)
        except Exception:
            raise HTTPError(400,"Bad Request")

        value1, value2 = _search_city(city1.lower(), city2.lower(),
                                      city1_trans.lower(), city2_trans.lower())

        north = city1.capitalize() if value1['latitude'] > value2['latitude'] else city2.capitalize()
        timezone = 'Одинаковая' if value1['timezone'] == value2['timezone'] else 'Разная'
        time_difference = _get_timezone_difference(value1['longitude'],value2['longitude'])

        data_json = {
            city1.capitalize(): value1,
            city2.capitalize(): value2,
            "north": north,
            "timezone": timezone,
            "time_diff": time_difference
        }

        data_html = f"<p>Город {city1.capitalize()}: {value1}</p>" \
                    f"<p>Город {city2.capitalize()}: {value2}</p>" \
                    f"<p>Севернее находится город: {north}</p>" \
                    f"<p>Временная зона: {timezone}</p>" \
                    f"<p>Разница во времени: {time_difference}</p>"

        return self.form_response(req, data_html, data_json)

    def handle_get_citylist(self,req):
        """Challenge #2: Method for getting a list of cities with paging
        (Request) -> Response"""
        page_id = req.query["page"][0]
        number_of_cities = req.query["number"][0]
        if not(page_id.isdigit() and number_of_cities.isdigit()):
            raise HTTPError(400,"Bad Request")

        page_id = int(page_id)
        number_of_cities = int(number_of_cities)

        if page_id * number_of_cities > len(self._cities.data_list) or \
            page_id * number_of_cities <= 0:
            raise HTTPError(404, "Not found")

        i = page_id * number_of_cities
        data_html = "<ol>"
        data_json = {"number": number_of_cities,
                     "page":page_id,
                     "cities":[]}

        k = i

        while i < len(self._cities.data_list) and i < (k+number_of_cities):
            cities = self._cities.get(self._cities.data_list[i])
            data_html += "<li>" + str(cities) + "</li>"
            data_json["cities"].append(cities)
            i += 1
        data_html += "</ol>"
        return self.form_response(req,data_html,data_json)

    def handle_get_city(self,req, city_id):
        """Challenge #1: Method for getting city by id
        (Request) -> Response"""
        city = self._cities.get(int(city_id))
        if city is None:
            raise HTTPError(404, "Not found")

        return self.form_response(req, city, city)

    def form_response(self,req, text_html, json_data):
        """Method for forming responses"""
        accept = req.headers.get("Accept")
        if "text/html" in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'{text_html}'
            body += '</body></html>'
        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(json_data)
        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)


    def send_response(self, conn, resp):
        """Method for sending responses"""
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        """Method for sending errors"""
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)

class HTTPError(Exception):
    """Custom error"""
    def __init__(self, status, reason, body=None):

        super()
        self.status = status
        self.reason = reason
        self.body = body

class Response:
    """Response class"""
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
