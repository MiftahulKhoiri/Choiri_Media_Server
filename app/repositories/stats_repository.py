from app.repositories.db import get_db

def user_stats():
    conn = _get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
    active = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE is_active = 0")
    locked = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "active": active,
        "locked": locked,
    }