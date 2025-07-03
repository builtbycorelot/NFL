class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class APIRouter:
    def __init__(self) -> None:
        self.routes = {"GET": {}, "POST": {}}

    def get(self, path: str):
        def decorator(func):
            self.routes["GET"][path] = func
            return func

        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes["POST"][path] = func
            return func

        return decorator


class FastAPI:
    def __init__(self, title: str | None = None) -> None:
        self.title = title or "FastAPI"
        self.routes = {"GET": {}, "POST": {}}
        self.event_handlers = {"startup": []}

    def include_router(self, router: APIRouter) -> None:
        for method in self.routes:
            self.routes[method].update(router.routes.get(method, {}))

    def get(self, path: str):
        def decorator(func):
            self.routes["GET"][path] = func
            return func

        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes["POST"][path] = func
            return func

        return decorator

    def on_event(self, event: str):
        def decorator(func):
            self.event_handlers.setdefault(event, []).append(func)
            return func

        return decorator

    def openapi(self):
        paths = {}
        for path in self.routes["GET"]:
            paths.setdefault(path, {})["get"] = {}
        for path in self.routes["POST"]:
            paths.setdefault(path, {})["post"] = {}
        return {"paths": paths, "title": self.title}

    def _call_route(self, method: str, path: str, json=None):
        handler = self.routes.get(method, {}).get(path)
        if handler is None:
            raise HTTPException(status_code=404, detail="Not Found")
        if json is not None:
            return handler(json)
        return handler()


__all__ = ["FastAPI", "APIRouter", "HTTPException"]
