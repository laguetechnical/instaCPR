from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class ReportData:
    platform: str
    fullname: str
    copied_url: str
    target_url: str
    email: Optional[str] = None
    copied_type: str = "Video"
    country: str = "India"
    target_username: Optional[str] = None
    description: Optional[str] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)