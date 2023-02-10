from datetime import datetime, timedelta # used to get dates

def GetDate():
    date = datetime.now() #iso format yyyy-mm-dd #.strftime("%H:%M:%S")
    return date

def GetFreeDate(mindelta):
    date = GetDate()
    FreeDate = date + timedelta(seconds=mindelta)
    return FreeDate
