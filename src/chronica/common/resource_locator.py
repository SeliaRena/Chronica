from pathlib import Path
import src.chronica.common.paths as paths

class ResourceLocator:
    @staticmethod
    def character_asset(character_name: str, *parts: str) -> Path:
        return paths.CHARACTERS_DIR / character_name / "assets" / Path(*parts)
    
    @staticmethod
    def ui_asset(*parts: str) -> Path:
        return paths.UI_DIR / "assets" / Path(*parts)
    
    @staticmethod
    def ui_icon(*parts: str) -> Path:
        return ResourceLocator.ui_asset("icons") / Path(*parts)