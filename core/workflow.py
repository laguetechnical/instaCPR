from typing import Callable
from utils.otp import get_otp
from .config import OTP_TIMEOUT

class Workflow:
    def __init__(
        self,
        driver,
        report,
        retry_func: Callable,
        progress_callback: Callable,
        logger,
        otp_handler=get_otp,           # injectable
    ):
        self.driver = driver
        self.report = report
        self.retry = retry_func
        self.progress = progress_callback
        self.logger = logger
        self.get_otp = otp_handler

    def execute(self, cfg: dict):
        """Full automation workflow - owns everything"""
        actions = cfg["actions"]
        url = cfg["url"]

        self.progress("Opening copyright form...")
        self.retry(lambda: self.driver.get(url))

        # Form filling steps
        steps = [
            ("Select Owner",      actions["owner"],      None),
            ("Enter Name",        actions["name1"],      self.report.fullname),
            ("Enter Email",       actions["email1"],     self.report.email),
            ("Confirm Email",     actions["email2"],     self.report.email),
            ("Select Country",    actions["country"],    self.report.country),
            ("Content Type",      actions["copiedtype"], self.report.copied_type),
            ("Owner Name",        actions["name2"],      self.report.fullname),
            ("Copied URL",        actions["copiedurl"],  self.report.copied_url),
            ("Copied Description",actions["copieddesc"], None),
            ("Target Type",       actions["targettype"], None),
            ("Target URL",        actions["targeturl"],  self.report.target_url),
            ("Target Description",actions["targetdesc"], self.report.description),
            ("Signature",         actions["name3"],      self.report.fullname),
            ("Submit Form 1",     actions["submit1"],    None),
        ]

        for step_name, action_obj, arg in steps:
            self.progress(f"→ {step_name}")
            try:
                if arg is None:
                    self.retry(lambda: action_obj.performaction(self.driver))
                else:
                    self.retry(lambda: action_obj.performaction(self.driver, arg))
            except Exception as e:
                self.logger.exception(f"{step_name} failed")
                raise
        # OTP Phase
        MAX_OTP_RESENDS = 3

        for resend in range(MAX_OTP_RESENDS + 1):

            self.progress("⏳ Waiting for Meta OTP...")

            try:
                otp = self.get_otp(
                    self.report.email,
                    timeout=OTP_TIMEOUT,
                )

                self.progress(f"✅ OTP received: {otp}")

                self.retry(
                    lambda: actions["otp"].performaction(
                        self.driver,
                        otp,
                    )
                )

                self.retry(
                    lambda: actions["submit2"].performaction(
                        self.driver,
                    )
                )

                self.progress("🎉 Final submission completed!")
                return

            except TimeoutError:

                if resend >= MAX_OTP_RESENDS:
                    self.logger.exception(
                        "OTP / Final submit failed"
                    )
                    raise TimeoutError(
                        "Meta never sent an OTP."
                    )

                self.progress(
                    f"⚠️ OTP timeout. Re-requesting OTP ({resend + 1}/{MAX_OTP_RESENDS})..."
                )

                # Close current OTP popup
                self.retry(
                    lambda: actions["resendotp"].performaction(
                        self.driver
                    )
                )

                # Submit form again to request a fresh OTP
                self.retry(
                    lambda: actions["submit1"].performaction(
                        self.driver
                    )
                )

            except Exception:
                self.logger.exception(
                    "OTP / Final submit failed"
                )
                raise

        # # OTP Phase
        # self.progress("⏳ Waiting for Meta OTP...")
        # try:
        #     otp = self.get_otp(self.report.email, timeout=OTP_TIMEOUT)
        #     self.progress(f"✅ OTP received: {otp}")

        #     self.retry(lambda: actions["otp"].performaction(self.driver, otp))
        #     self.retry(lambda: actions["submit2"].performaction(self.driver))
        #     self.progress("🎉 Final submission completed!")
        # except Exception as e:
        #     self.logger.exception("OTP / Final submit failed")
        #     raise