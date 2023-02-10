# better way to get diff

# old:
# def GetContentDiff(lines1: list, lines2: list, file: str) -> list:
#     FileContentDiff = []
#     for line in unified_diff(
#         lines1, lines2,
#         fromfile=file, tofile=file, lineterm=''):
#         FileContentDiff.append(line)

#     print(FileContentDiff)

# better:
# def get_difference_and_print(arr1, arr2):
#     diff = list(set(arr2) - set(arr1))
#     for elem in diff:
#         if "Failed password for" in elem:
#             print(elem)

# arr1 = ['1fafe', '21fafe', '31fafe']
# arr2 = ['1fafe', '21fafe', '31fafe', 'Failed password for']

# get_difference_and_print(arr1, arr2)

######################################

text = "16576 2022-12-21 14:35:01.622 Failed password for 50mer211 from 10.146.50.97 port 54422 ssh2"

components = text.split(" ")

event_id = components[0]
date_time = components[1] + " " + components[2]
failure_reason = " ".join(components[3:-4])
source_ip = components[-3]
source_port = components[-2]
protocol = components[-1]

print("Event ID:", event_id)
print("Date & Time:", date_time)
print("Failure Reason:", failure_reason)
print("Source IP:", source_ip)
print("Source Port:", source_port)
print("Protocol:", protocol)
