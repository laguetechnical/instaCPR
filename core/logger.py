import logging
from pathlib import Path


class ReportLogger:

    def __init__(self, report_id: str | None = None):

        self.logger = logging.getLogger(
            f"MetaReport.{report_id or 'default'}"
        )

        self.logger.setLevel(logging.INFO)

        Path("logs").mkdir(exist_ok=True)

        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)

            if report_id:
                file = logging.FileHandler(
                    f"logs/report_{report_id}.log"
                )
                file.setFormatter(formatter)
                self.logger.addHandler(file)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def exception(self, msg):
        self.logger.exception(msg)