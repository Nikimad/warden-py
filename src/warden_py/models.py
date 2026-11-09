from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CheckResult:
    url: str
    checked_at: datetime
    success: bool
    response_ms: int | None = None
    status_code: int | None = None
    error: str | None = None
