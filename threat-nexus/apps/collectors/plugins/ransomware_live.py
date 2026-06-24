from apps.collectors.base_http import HTTPCollectorPlugin


class RansomwareLivePlugin(HTTPCollectorPlugin):
    name = "ransomware-live"
    source_reputation = 82
