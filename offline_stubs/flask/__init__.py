class _Request:
    def __init__(self):
        self.json = None


request = _Request()


class Response:
    def __init__(self, data, status=200):
        self.data = data
        self.status_code = status

    def get_json(self):
        return self.data


def jsonify(obj):
    if isinstance(obj, Response):
        return obj
    return Response(obj)


class Flask:
    def __init__(self, name, static_folder=None, static_url_path=None):
        self.routes = {}
        self.static_folder = static_folder
        self.static_url_path = static_url_path

    def route(self, path, methods=["GET"]):
        def decorator(func):
            for m in methods:
                self.routes[(path, m)] = func
            return func

        return decorator

    def test_client(self):
        app = self

        class Client:
            def open(self, path, method="GET", json=None):
                request.json = json
                func = app.routes.get((path, method))
                if func is None:
                    return Response({"error": "not found"}, 404)
                res = func()
                if isinstance(res, tuple):
                    res, status = res
                    if not isinstance(res, Response):
                        res = Response(res, status)
                    else:
                        res.status_code = status
                    return res
                if isinstance(res, Response):
                    return res
                return Response(res)

            def get(self, path):
                return self.open(path, "GET")

            def post(self, path, json=None):
                return self.open(path, "POST", json=json)

        return Client()

    def send_static_file(self, filename):
        return Response({"file": filename})


__version__ = "stub"


def send_from_directory(directory, filename):
    return Response({"file": filename})
