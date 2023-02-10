from difflib import unified_diff # used to get difference between two files
from re import split

def GetContentDiff(lines1: list, lines2: list, file: str) -> list:
    FileContentDiff = list(set(lines2) - set(lines1))

    return FileContentDiff


def ReadFile(path: str) -> list:
    FileContent = []
    with open(path) as f:
        FileContent = f.readlines()
    f.close()

    return FileContent

def GetFailedLines(lines: list, findstr: str):
    FailedLines = []
    for line in lines:
        if findstr in line:
            FailedLines.append(line)

    return FailedLines

def SplitArray(line: str) -> list:
    fields = line.split()
    return fields

def RemoveDuplicates(arr: list):
    return list(set(arr))

def RemoveItem(arr: list, value):
    return [x for x in arr if x != value]