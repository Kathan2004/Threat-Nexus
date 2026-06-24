# Plugin Development Guide

Create a Python module in `apps/collectors/plugins/` containing a class that inherits `CollectorPlugin` or `HTTPCollectorPlugin`.

Required methods:

- `collect()`: fetch raw intelligence.
- `normalize(raw)`: convert one raw item into a `ThreatEvent`.
- `validate(event)`: reject malformed normalized intelligence.
- `health_check()`: report plugin health and dependency status.

Plugins are discovered automatically by `PluginRegistry` using package inspection. Do not add source-specific logic to collector runners.
