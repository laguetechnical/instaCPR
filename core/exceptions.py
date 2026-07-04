class MetaReportError(Exception):
    pass

class OTPTimeoutError(MetaReportError):
    pass

class SeleniumActionError(MetaReportError):
    pass