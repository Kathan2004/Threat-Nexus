from apps.collectors.base_http import HTTPCollectorPlugin


class BleepingComputerPlugin(HTTPCollectorPlugin):
    name = "bleepingcomputer"
    source_reputation = 72


class TheHackerNewsPlugin(HTTPCollectorPlugin):
    name = "the-hacker-news"
    source_reputation = 70


class SecurityWeekPlugin(HTTPCollectorPlugin):
    name = "securityweek"
    source_reputation = 70
