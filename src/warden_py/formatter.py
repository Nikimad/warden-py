from warden_py.models import CheckResult


def format_result(result: CheckResult) -> str:
    parts = ["UP" if result.success else "DOWN", result.url]

    if result.status_code is not None:
        parts.append(str(result.status_code))
    if result.response_ms is not None:
        parts.append(f"{result.response_ms} ms")
    if result.error is not None:
        parts.append(result.error)

    return " | ".join(parts)
