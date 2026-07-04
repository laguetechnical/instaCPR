from pathlib import Path
import time
import json
from datetime import datetime
from .models import ReportData
from .driver import DriverManager
from .workflow import Workflow
from .logger import ReportLogger
from .exceptions import OTPTimeoutError
from utils.mailgen import generate_temp_email
from utils.post2user import post_to_username
from utils.otp import get_otp
from .config import INSTAGRAM_FORM_URL, FACEBOOK_FORM_URL, OTP_TIMEOUT
from .platforms import get_platform_config

class MetaReporter:
    def __init__(self, report_data: ReportData, proxy_config=None, headless=False, progress_callback=None):
        self.report = report_data
        self.proxy_config = proxy_config
        self.headless = headless
        self.progress_callback = progress_callback
        self.logger = ReportLogger(report_id=str(int(time.time())))
        self.driver_manager: DriverManager = None
        self.start_time = datetime.utcnow()
    def progress(self, message: str):
            self.logger.info(message)
            if self.progress_callback:
                self.progress_callback(message)

    def build_report_data(self):
        # TODO: Later → ReportBuilder
        self.report.email = generate_temp_email(self.report.fullname)
        self.report.target_username = post_to_username(self.report.target_url)
        self.report.description = f"I am {self.report.fullname}..."  # full text

    def run(self):
        try:
            self.progress(f"🚀 Starting {self.report.platform} report")

            self.driver_manager = DriverManager(
                headless=self.headless, 
                proxy_address=self.proxy_config
            )
            driver = self.driver_manager.create()

            self.build_report_data()

            cfg = get_platform_config(self.report.platform)

            workflow = Workflow(
                driver=driver,
                report=self.report,
                retry_func=self.driver_manager.retry,
                progress_callback=self.progress,
                logger=self.logger,
            )

            workflow.execute(cfg)                    # ← One call does everything

            self.report.status = "success"
            self.save_report()
            self.progress("🎉 Report completed successfully!")

        except Exception as e:
            self.report.status = "failed"
            if self.driver_manager:
                self.driver_manager.screenshot("failure")
            self.logger.exception(f"Report failed: {e}")
            raise
        finally:
            if self.driver_manager:
                self.driver_manager.close()

    def save_report(self):
        # Your improved JSON structure
        data = {
            "status": self.report.status,
            "started_at": self.start_time.isoformat(),
            "finished_at": datetime.utcnow().isoformat(),
            "duration_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "platform": self.report.platform,
            "email": self.report.email,
            "target_url": self.report.target_url,
            "proxy_used": bool(self.proxy_config),
            "id": int(time.time()),
            "fullname": self.report.fullname,
            "country": self.report.country,
            "copied_url": self.report.copied_url,
        }
        Path("reports").mkdir(exist_ok=True)
        with open(f"reports/report_{int(time.time())}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)