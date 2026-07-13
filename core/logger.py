import logging
import sys
from pathlib import Path

class ReportLogger:
    def __init__(self, report_id: str | None = None):
        self.logger = logging.getLogger(f"MetaReport.{report_id or 'default'}")
        self.logger.setLevel(logging.INFO)

        # === FORCE UTF-8 ON WINDOWS ===
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

        Path("logs").mkdir(exist_ok=True)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Console handler with safe encoding
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)

            # File handler (always UTF-8)
            if report_id:
                file = logging.FileHandler(
                    f"logs/report_{report_id}.log", encoding="utf-8"
                )
                file.setFormatter(formatter)
                self.logger.addHandler(file)

    def info(self, msg):
        if isinstance(msg, str):
            msg = msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
        self.logger.info(msg)

    def warning(self, msg):
        self.info(msg)

    def error(self, msg):
        self.info(msg)

    def exception(self, msg):
        if isinstance(msg, str):
            msg = msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
        self.logger.exception(msg)