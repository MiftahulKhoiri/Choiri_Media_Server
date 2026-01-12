import time

FAILED = {}
MAX_ATTEMPT = 5
BLOCK_TIME = 300  # 5 menit


def can_attempt(ip):
    entry = FAILED.get(ip)
    if not entry:
        return True

    count, last = entry
    if count >= MAX_ATTEMPT and time.time() - last < BLOCK_TIME:
        return False

    return True


def register_fail(ip):
    count, _ = FAILED.get(ip, (0, 0))
    FAILED[ip] = (count + 1, time.time())


def reset_fail(ip):
    FAILED.pop(ip, None)