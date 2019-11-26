import sys
import re

def verify(ip):
    res = re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip)
    if res:
        return True
    else:
        return False

def to_bin(ip):
    element = list(map(int, ip.split('.')))
    
    bin_num = []
    for item in element:
        bin_num.append(int(bin(item)[2:]))
    
    return "{:08d}.{:08d}.{:08d}.{:08d}".format(bin_num[0], bin_num[1], bin_num[2], bin_num[3])

def print_network(ip):
    print("Network: {} \t {}".format(ip, to_bin(ip)))

def print_netmask(ip, given_mask):
    ip_class = 'Undefined'
    if to_bin(ip)[0] == '0':
        ip_class = 'A'
    elif to_bin(ip)[:2] == '10':
        ip_class = 'B'
    elif to_bin(ip)[:3] == '110':
        ip_class = 'C'

    mask = [0, 0, 0, 0]

    for item in range(int(given_mask)):
        mask[item // 8] += 1 << (7 - item % 8)

    print("Netmask: {} \t {} (class {})".format('.'.join(map(str, mask)), to_bin('.'.join(map(str, mask))), ip_class))

# def print_broadcast(ip):
#     print("Broadcast: {} \t {}".format(ip, to_bin(ip)))

input_value = input("Enter ip address (ex. 127.0.0.1/24): ")

if '/' in input_value:
    ip, mask = input_value.split('/')
else:
    ip, mask = input_value, 16

if not verify(ip):
    print("Invalid ip address")
    sys.exit(0)

print_network(ip)

print_netmask(ip, mask)
