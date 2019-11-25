import sys

def verify(ip):
    for item in ip.split('.'):
        if int(item) > 255:
            return False

ip = input("Address: ")

if not verify(ip):
    sys.exit(0)
