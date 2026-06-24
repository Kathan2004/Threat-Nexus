from apps.collectors.base_http import HTTPCollectorPlugin


class RedditPlugin(HTTPCollectorPlugin):
    name = "reddit"
    source_reputation = 55
