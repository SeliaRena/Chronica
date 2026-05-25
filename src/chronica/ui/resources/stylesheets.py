from src.chronica.common.resource_locator import ResourceLocator

class Stylesheets:
    @staticmethod
    def load(*path_parts: str) -> str:
        return ResourceLocator.stylesheet(*path_parts).read_text(encoding="utf-8")