from apps.collectors.base_http import HTTPCollectorPlugin


class ShodanPlugin(HTTPCollectorPlugin):
    name = "shodan"
    source_reputation = 80
