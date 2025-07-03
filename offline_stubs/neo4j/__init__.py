class _Session:
    def run(self, query, parameters=None):
        return []


class _Driver:
    def session(self):
        return _Session()


class GraphDatabase:
    @staticmethod
    def driver(uri, auth=None):
        return _Driver()


__all__ = ["GraphDatabase"]
__version__ = "stub"
