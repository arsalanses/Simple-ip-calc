import sys

def verify(ip):
    for item in ip.split('.'):
        if int(item) > 255:
            return False

def to_bin(ip):
    element = list(map(int, ip.split('.')))
    
    bin_num = []
    for item in element:
        bin_num.append(int(bin(item)[2:]))
    
    return "{:08d}.{:08d}.{:08d}.{:08d}".format(bin_num[0], bin_num[1], bin_num[2], bin_num[3])

def print_address(ip):
    print("Network: {} \t {}".format(ip, to_bin(ip)))

ip = input("Enter ip address: ")

if not verify(ip):
    sys.exit(0)

print_address(ip)
