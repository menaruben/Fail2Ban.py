from datetime import datetime, timedelta # used to get dates
DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"

def GetDate():
    date = datetime.now() #iso format yyyy-mm-dd #.strftime("%H:%M:%S")
    return date

def GetFreeDate(mindelta):
    date = GetDate()
    FreeDate = date + timedelta(seconds=mindelta)
    return FreeDate

def StrToDate(dateStr):
    dateObj = datetime.strptime(dateStr, DATEFORMAT)
    
    return dateObj

def DateToStr(dateObj):
    dateStr =  datetime.strftime(dateObj, DATEFORMAT)

    return dateStr