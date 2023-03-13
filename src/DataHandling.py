from sqlite3 import connect
from datetime import datetime
from TimeHandling import *
import logging
from winfw import UnbanIP

F2BLOGS = "C:/ProgramData/ssh/logs/Fail2Ban.log"    # path to Fail2Ban.log file (this service)

logging.basicConfig(filename=F2BLOGS,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

date_format = '%Y-%m-%d %H:%M:%S.%f'
TableName = "sshjail"
DbName = "Fail2Ban.db"

conn = connect(f"{DbName}")

def CreateTableIfNotExists(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {TableName} (host text, freedate text)")

def WriteToSQL(conn, host, freedate):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {TableName} VALUES ('{host}', '{freedate}')")
    conn.commit()

# WriteToSQL(conn, "192.168.1.228", "20.07.2023")

def RemoveFromSQL(conn, host, freedate):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {TableName} WHERE host=? AND freedate=?", (host, freedate))
    conn.commit()

# RemoveFromSQL(conn, "192.168.1.28", "20.07.2023")

    return dict

def GetSQLTableContent(conn, TableName):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TableName}")

    return cur.fetchall()

def CheckBanAge(conn, limit):
    try:
        TableContent = GetSQLTableContent(conn, TableName)
        for row in TableContent:
            timediff = GetDate() - StrToDate(row[1])

            if timediff.total_seconds() >= limit:
                UnbanIP(row[0])
                RemoveFromSQL(conn, row[0], row[1])
                logging.info(f"unbanning {row[0]}")

            else:
                logging.info(f"{row[0]} too young to unban (timediff = {timediff})")

    except Exception as e:
        logging.debug(e)
