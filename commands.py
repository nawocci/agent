from datetime import datetime

def get_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now().strftime(format)
