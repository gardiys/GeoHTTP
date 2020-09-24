from server import HTTPServer

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000

    server = HTTPServer(host, port)

    try:
        server.run_forever()
    except KeyboardInterrupt:
        pass
