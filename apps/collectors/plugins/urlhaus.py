from apps.collectors.base_http import HTTPCollectorPlugin


class URLHausPlugin(HTTPCollectorPlugin):
    name = "urlhaus"
    source_reputation = 82
