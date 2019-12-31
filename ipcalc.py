import re


def verify(ip):
    ipv4 = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    return True if re.search(ipv4, ip) else False


def to_binary(ip):
    element = list(map(int, ip.split('.')))

    bin_num = []
    for item in element:
        bin_num.append(int(bin(item)[2:]))

    return "{:08d}.{:08d}.{:08d}.{:08d}".format(bin_num[0], bin_num[1], bin_num[2], bin_num[3])


def to_decimal(bin):
    element = bin.split('.')

    dec_num = []
    for item in element:
        dec_num.append(int(item, 2))

    return "{}.{}.{}.{}".format(dec_num[0], dec_num[1], dec_num[2], dec_num[3])


def verify_mask(ip, mask):
    binary_ip = to_binary(ip)

    if mask == "NULL":
        if binary_ip[0] == '0':
            return 8
        elif binary_ip[:2] == '10':
            return 16
        elif binary_ip[:3] == '110':
            return 24
        else:
            return 5
    else:
        return mask if int(mask) < 32 else False


def print_netmask(ip, mask):
    ip_class = 'Undefined'
    binary_ip = to_binary(ip)

    if binary_ip[0] == '0':
        ip_class = 'A'
    elif binary_ip[:2] == '10':
        ip_class = 'B'
    elif binary_ip[:3] == '110':
        ip_class = 'C'

    netmask = [0, 0, 0, 0]

    for item in range(int(mask)):
        netmask[item // 8] += 1 << (7 - item % 8)

    print("Netmask: {} = {} \t {} (class {})".format('.'.join(map(str, netmask)), mask, to_binary('.'.join(map(str, netmask))), ip_class))


def formatter(my_str, group=8, char='.'):
    my_str = str(my_str)
    return char.join(my_str[i:i+group] for i in range(0, len(my_str), group))


def print_network(ip, mask):
    binary_ip = to_binary(ip)
    binary_ip = binary_ip.replace('.', '')
    binary_ip = binary_ip[:int(mask)] + binary_ip[int(mask):].replace('1', '0')
    binary_ip = formatter(binary_ip)
    print("Network: {} \t {}".format(to_decimal(binary_ip), binary_ip))


def print_broadcast(ip, mask):
    binary_ip = to_binary(ip)
    binary_ip = binary_ip.replace('.', '')
    binary_ip = binary_ip[:int(mask)] + binary_ip[int(mask):].replace('0', '1')
    binary_ip = formatter(binary_ip)
    print('Broadcast: {} \t {}'.format(to_decimal(binary_ip), binary_ip))
    return to_decimal(binary_ip)


def print_fist_host(ip):
    element = list(map(int, ip.split('.')))
    element[3] += 1
    print("FirstHost: {} \t {}".format('.'.join(map(str, element)), to_binary('.'.join(map(str, element)))))


def print_last_host(ip):
    element = list(map(int, ip.split('.')))
    element[3] -= 1
    print("LastHost: {} \t {}".format('.'.join(map(str, element)), to_binary('.'.join(map(str, element)))))


def print_hosts(mask):
    hosts = 2 ** (32 - int(mask)) - 2
    print("Hosts: {}".format(hosts))


input_value = input("Enter ip address (ex. 127.0.0.1/24): ")

if '/' in input_value:
    ip, mask = input_value.split('/')
else:
    ip, mask = input_value, "NULL"

if not verify(ip):
    print("Invalid ip address")
    exit()

if not verify_mask(ip, mask):
    print("Invalid mask value")
    exit()
else:
    mask = verify_mask(ip, mask)

print_network(ip, mask)
print_netmask(ip, mask)
broadcast = print_broadcast(ip, mask)
print_fist_host(ip)
print_last_host(broadcast)
print_hosts(mask)
