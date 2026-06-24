from apps.collectors.base_http import HTTPCollectorPlugin


class NVDPlugin(HTTPCollectorPlugin):
    name = "nvd"
    endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    source_reputation = 90
