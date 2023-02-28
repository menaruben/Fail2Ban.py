import sqlite3
from datetime import datetime

date_format = '%Y-%m-%d %H:%M:%S.%f'
TableName = "sshjail"
DbName = "Fail2ban.db"

# conn = sqlite3.connect(f"{DbName}")
# cur.execute(f"CREATE TABLE IF NOT EXISTS {TableName} (host text, freedate text)")

def WriteToSQL(conn, host: str, freedate: str):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {TableName} VALUES ('{host}', '{freedate}')")
    conn.commit()

# WriteToSQL(conn, "192.168.1.228", "20.07.2023")


def RemoveFromSQL(conn, host: str, freedate: str):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {TableName} WHERE host=? AND freedate=?", (host, freedate))
    conn.commit()

# RemoveFromSQL(conn, "192.168.1.28", "20.07.2023")


def TableToDict(conn):
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM {TableName}")
    dict = {}
    for row in rows:
        dict[row[0]]= datetime.strptime(row[1], date_format)

    return dict

# testing
# for row in cur.execute(f'''SELECT * FROM {TableName}'''):
#     print(row[0], row[1])

