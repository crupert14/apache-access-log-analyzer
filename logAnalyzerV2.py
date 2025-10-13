# fileLocation = input("Enter file path: ")
# fileFormatInput = input("Enter format (comma separated): ")
# logFile = open(fileLocation, 'r')
# fileFormat = fileFormatInput.split(" ")

import shlex
import re
from datetime import datetime

'''
Completed:
- Total requests -> requests
- Unique IP List -> unique_ips_list
- Unique IP Count -> unique_ips
- Status Codes by IP -> ip_addr_codes_count
- Appearence of each code -> code_counts
- Implement status code count -> code_counts
- Implement request count by IP -> ip_requests
- Implement total time of log -> total_time
- Implement request count by appearence -> request_urls
'''

ip_addr_app_count = [] # [IP Address, Appearence Count]
ip_addr_codes_count = [] # [IP Address, HTTP Code Number, Code Appearence Number]
unique_ips_list = [] # [IP Address]
code_counts = [] # [Code, Count]
ip_requests = [] # [IP, Request Count]
request_urls = [] # [URL, Count]
times = [] # [Timestamp]
requests = 0
unique_ips = 0

request_string = ["GET", "POST", "PUT", "DELETE"]
existingCodes = [
    # 1xx Informational
    100, 101, 102, 103,
    # 2xx Success
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
    # 3xx Redirection
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    # 4xx Client Error
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 449, 450, 451, 499,
    # 5xx Server Error
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 532, 533, 535, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 598, 599
]

logFile = open("logs/real.log")
logFormat = "Common" #Common - %h %l %u %t \"%r\" %>s %b | Combined - %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"

def increment_counter(arr, *keys):
    if not arr:
        arr.append([*keys, 1])
        return

    for entry in arr:
        if entry[:-1] == list(keys):
            entry[-1] += 1
            return

    arr.append([*keys, 1])

"""
Ex:
increment_counter(code_counts, "200")
increment_counter(ip_addr_app_count, "192.168.0.1")
increment_counter(ip_addr_codes_count, "192.168.0.1", "404")
"""

for line in logFile:
    # tokens = shlex.split(line)
    # for token in tokens:
    #     found = False
    #     for str in request_string:
    #         if str in token:
    #             req_url = token.split(" ")
    #             found = True
    #             break
    #         if found:
    #             break

    """
    %h → Client IP
    %l → RFC 1413 identity (almost always -)
    %u → Authenticated username (if any)
    %t → Time of request
    %r → Request line ("GET /index.html HTTP/1.1")
    %>s → Response status code
    %b → Response size in bytes
    """

    client_ip = line[0:line.index(" ")] # %h
    # rfc_and_user = line[line.index(" "):line.index("[")].strip().split(" ") #RFC id and user combined
    rfc_id = line[line.index(" "):line.index(" ", line.index(" ")+1)] # %l
    user = line[line.index(" ", line.index(" ")+1):line.index("[")].strip() # %u
    time_of_request = line[line.index("[")+1:line.index("]")] # %t
    request_line = line[line.index("\"")+1:line.index("\"", line.index("\"")+1)] # %r
    response_status_code = line[line.index("\"", line.index("\"") + 1)+2:line.index(" ", line.index("\"", line.index("\"") + 1)+2)] # %>s
    response_size_bytes = line[line.index(" ", line.index("\"", line.index("\"") + 1)+2):]
    print(response_size_bytes)