'''
Log Formats:
Common - %h %l %u %t \"%r\" %>s %b 
Combined - %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"
'''
import re
from datetime import datetime

ip_addr_app_count = [] # [IP Address, Appearence Count]
ip_addr_codes_count = [] # [IP Address, HTTP Code Number, Code Appearence Number]
unique_ips_list = [] # [IP Address]
code_counts = [] # [Code, Count]
request_urls_total = [] # [URL, Count]
request_urls_by_method = [] # [URL, Method, Count]
times_readable = [] # [Timestamp] (Formatted %Y-%m-%d %H:%M:%S %Z)
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
CLF_pattern = re.compile(
    r'(?P<ip>\S+) '                # %h: Remote host
    r'(?P<ident>\S+) '             # %l: RFC 1413 identity
    r'(?P<user>\S+) '              # %u: Authenticated user
    r'\[(?P<time>[^\]]+)\] '       # %t: Time
    r'"(?P<request>[^"]*)" '       # %r: Request line
    r'(?P<status>\d{3}) '          # %>s: Status code
    r'(?P<size>\S+)'               # %b: Response size
)
CombLF_pattern = re.compile(
    r'(?P<ip>\S+) '                # %h: Remote host
    r'(?P<ident>\S+) '             # %l: RFC 1413 identity
    r'(?P<user>\S+) '              # %u: Authenticated user
    r'\[(?P<time>[^\]]+)\] '       # %t: Time
    r'"(?P<request>[^"]*)" '       # %r: Request line
    r'(?P<status>\d{3}) '          # %>s: Status code
    r'(?P<size>\S+) '              # %b: Response size
    r'"(?P<referer>[^"]*)" '       # "%{Referer}i": Referring page
    r'"(?P<agent>[^"]*)"'          # "%{User-agent}i": User agent string
)

def parse_CLF(line):
    match = CLF_pattern.match(line)
    if not match:
        return None
    
    data = match.groupdict()
    
    # Clean and convert
    data["size"] = int(data["size"]) if data["size"].isdigit() else 0
    try:
        data["time"] = datetime.strptime(data["time"], "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        data["time"] = None
    
    return data

def increment_counter(arr, *keys):
    if not arr:
        arr.append([*keys, 1])
        return

    for entry in arr:
        if entry[:-1] == list(keys):
            entry[-1] += 1
            return

    arr.append([*keys, 1])

logFile = "logs/real.log"
logFormat = "Common" 

with open(logFile) as file:
    for line in file:
        entry = parse_CLF(line)
        #Skip malformed request lines
        if not entry:
            continue

        requests += 1

        if entry['ip'] not in unique_ips_list:
            unique_ips_list.append(entry['ip'])
        unique_ips = len(unique_ips_list)

        increment_counter(ip_addr_app_count, entry['ip'])
        increment_counter(ip_addr_codes_count, entry['ip'], entry['status'])
        increment_counter(code_counts, entry['status'])
        increment_counter(request_urls_total, entry['request'])
        increment_counter(request_urls_by_method, entry['request'], entry['request'].split()[0])

        times_readable.append(entry['time'].strftime("%Y-%m-%d %H:%M:%S %Z"))
        times.append(entry['time'])

total_elapsed_time = max(times) - min(times)