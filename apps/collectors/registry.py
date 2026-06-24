import importlib
import inspect
import pkgutil

from core.interfaces.plugin import CollectorPlugin, PluginHealth


class PluginRegistry:
    def __init__(self, package: str = "apps.collectors.plugins") -> None:
        self.package = package
        self._plugins: dict[str, CollectorPlugin] = {}

    def discover(self) -> dict[str, CollectorPlugin]:
        package = importlib.import_module(self.package)
        for module_info in pkgutil.iter_modules(package.__path__, f"{self.package}."):
            module = importlib.import_module(module_info.name)
            for _, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(klass, CollectorPlugin) and klass is not CollectorPlugin:
                    plugin = klass()
                    self.register(plugin)
        return self._plugins

    def register(self, plugin: CollectorPlugin) -> None:
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> CollectorPlugin:
        return self._plugins[name]

    def all(self) -> list[CollectorPlugin]:
        if not self._plugins:
            self.discover()
        return list(self._plugins.values())

    async def health(self) -> dict[str, PluginHealth]:
        return {plugin.name: await plugin.health_check() for plugin in self.all()}
