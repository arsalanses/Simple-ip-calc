import sys
import re

def verify(ip):
    ipv4 = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    return True if re.search(ipv4, ip) else False

def to_binary(ip):
    element = list(map(int, ip.split('.')))
    
    bin_num = []
    for item in element:
        bin_num.append(int(bin(item)[2:]))
    
    return "{:08d}.{:08d}.{:08d}.{:08d}".format(bin_num[0], bin_num[1], bin_num[2], bin_num[3])

def print_network(ip):
    print("Network: {} \t {}".format(ip, to_binary(ip)))

def print_netmask(ip, given_mask):
    ip_class = 'Undefined'
    binary_ip = to_binary(ip)

    if binary_ip[0] == '0':
        ip_class = 'A'
        given_mask = given_mask if given_mask != "NULL" else 8
    elif binary_ip[:2] == '10':
        ip_class = 'B'
        given_mask = given_mask if given_mask != "NULL" else 16
    elif binary_ip[:3] == '110':
        ip_class = 'C'
        given_mask = given_mask if given_mask != "NULL" else 24
    else:
        given_mask = given_mask if given_mask != "NULL" else 5

    mask = [0, 0, 0, 0]

    for item in range(int(given_mask)):
        mask[item // 8] += 1 << (7 - item % 8)

    print("Netmask: {} = {} \t {} (class {})".format('.'.join(map(str, mask)), given_mask, to_binary('.'.join(map(str, mask))), ip_class))
    
    return [mask, given_mask]

def print_broadcast(ip, netmask):
    element = list(map(int, ip.split('.')))
    res = []

    for not_netmask, ele in zip(netmask[0], element):
        res.append(ele + (255 - not_netmask))

    print("Broadcast: {} \t {}".format('.'.join(map(str, res)), to_binary('.'.join(map(str, res)))))
    
    return '.'.join(map(str, res))

def print_fist_host(ip):
    element = list(map(int, ip.split('.')))
    element[3] += 1

    print("FirstHost: {} \t {}".format('.'.join(map(str, element)), to_binary('.'.join(map(str, element)))))

def print_last_host(ip):
    element = list(map(int, ip.split('.')))
    element[3] -= 1

    print("LastHost: {} \t {}".format('.'.join(map(str, element)), to_binary('.'.join(map(str, element)))))

def print_hosts(mask):
    mask = int(mask) if mask != "NULL" else 5
    hosts = 2 ** (32 - mask) - 2
    print("Hosts: {}".format(hosts))

input_value = input("Enter ip address (ex. 127.0.0.1/24): ")

if '/' in input_value:
    ip, mask = input_value.split('/')
else:
    ip, mask = input_value, "NULL"

if not verify(ip):
    print("Invalid ip address")
    sys.exit(0)

print_network(ip)

netmask = print_netmask(ip, mask)

broadcast = print_broadcast(ip, netmask)

print_fist_host(ip)

print_last_host(broadcast)

print_hosts(netmask[1])
