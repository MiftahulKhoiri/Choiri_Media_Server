import sqlite3
from core.cms_bash_folder import DB_PATH

def get_db():
    return sqlite3.connect(DB_PATH)