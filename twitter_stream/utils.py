from datetime import datetime

class Utils(object):
    @staticmethod
    def parse_created_at(created_at, tz=None):
        return datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
