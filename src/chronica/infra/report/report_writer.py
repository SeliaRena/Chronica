import src.chronica.common.paths as paths
from datetime import datetime
from pathlib import Path

def write_report(content: str) -> None:
    report_dir = paths.REPORTS_DIR
    report_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"debug_report_{timestamp}.txt"
    report_path = report_dir / report_filename
    
    report_path.write_text(content, encoding="utf-8")