from pathlib import Path
import src.chronica.common.paths as paths

class ResourceLocator:
    @staticmethod
    def character_asset(character_name: str, *parts: str) -> Path:
        return paths.CHARACTERS_DIR / character_name / "assets" / Path(*parts)