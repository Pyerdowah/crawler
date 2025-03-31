from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

class RobotsChecker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.parser = RobotFileParser()
        self.parser.set_url(urljoin(base_url, "/robots.txt"))
        self.parser.read()

    def can_fetch(self, url, user_agent='*'):
        return self.parser.can_fetch(user_agent, url)
