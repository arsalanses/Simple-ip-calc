import sys

def verify(ip):
    for item in ip.split('.'):
        if int(item) > 255:
            print("Invalid ip address")
            return False
    
    return True

def to_bin(ip):
    element = list(map(int, ip.split('.')))
    
    bin_num = []
    for item in element:
        bin_num.append(int(bin(item)[2:]))
    
    return "{:08d}.{:08d}.{:08d}.{:08d}".format(bin_num[0], bin_num[1], bin_num[2], bin_num[3])

def print_network(ip):
    print("Network: {} \t {}".format(ip, to_bin(ip)))

def print_netmask(ip):
    element = list(map(int, ip.split('.')))
    
    ip_class = 'Undefined'
    if element[0] < 126:
        ip_class = 'A'
    elif element[0] < 191:
        ip_class = 'B'
    elif element[0] < 223:
        ip_class = 'C'

    snm = "{}.{}.{}.{}".format(255, 255 if ip_class == 'B' else 0, 255 if ip_class == 'C' else 0, 0)

    print("Netmask: {} \t {}(class {})".format(snm, to_bin(snm), ip_class))

def print_broadcast(ip):
    print("Network: {} \t {}".format(ip, to_bin(ip)))

input_value = input("Enter ip address: (ex. 127.0.0.1/24)")

ip, mask = input_value.split('/')

if not verify(ip):
    sys.exit(0)

print_network(ip)

print_netmask(ip)
