import shlex
import re
from datetime import datetime
import numpy

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

# fileLocation = input("Enter file path: ")
# fileFormatInput = input("Enter format (comma separated): ")
# logFile = open(fileLocation, 'r')
logFile = open("logs/real.log")
# fileFormat = fileFormatInput.split(" ")

def append_2d_array(arr, term):
    if len(arr) < 1:
        arr.append([term, 1])
    else:
        found = False
        for sub_arr in arr:
            if term in sub_arr:
                sub_arr[1] += 1
                found = True
        if not found:
            arr.append([term, 1])

def append_2d_array_with_terms(term1, term2, arr):
    if len(arr) < 1:
        arr.append([term1, term2, 1])
    else:
        found = False
        for sub_arr in arr:
            if sub_arr[0] == term1 and sub_arr[1] == term2:
                sub_arr[2] += 1
                found = True
        if found == False:
            arr.append([term1, term2, 1])
            
# Requests with code
for line in logFile:
    
    tokens = shlex.split(line)
    
    for token in tokens:
        found = False
        for str in request_string:
            if str in token:
                req_url = token.replace(str, "").strip()
                found = True
                break
            if found:
                break
    
    if "GET" in line or "POST" in line or "PUT" in line or "DELETE" in line:
        requests += 1
    
    client_ip_match = re.search(r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3})', line)
    if client_ip_match:
        client_ip = client_ip_match.group(1)
    else:
        continue
        
    code_match = re.search(r'"[A-Z]+ [^"]+ HTTP/\d\.\d"\s+(\d{3})\s+\d+', line)
    if code_match:
        code = code_match.group(1)
    else:
        continue
    
    timestamp = (tokens[3] + tokens[4]).strip('[]')
    log_time_format = "%d/%b/%Y:%H:%M:%S%z"
    times.append(datetime.strptime(timestamp, log_time_format))
    
    if client_ip not in unique_ips_list:
        unique_ips_list.append(client_ip)
        unique_ips += 1
    
    append_2d_array(code_counts, code)
    append_2d_array(ip_addr_app_count, client_ip) 
    append_2d_array(ip_requests, client_ip) 
    append_2d_array(request_urls, req_url)
    append_2d_array_with_terms(client_ip, code, ip_addr_codes_count)  
    
total_time = max(times) - min(times)

ip_addr_app_count = sorted(ip_addr_app_count, key=lambda row: row[1], reverse=True)

print(ip_addr_app_count)
print(ip_addr_codes_count)