import argparse
import os

hosts = { i : 2**(32 - i) - 2  for i in range(16, 31) }

mask = { i : 2**(32 - i) for i in range(16, 31) }

last_available = 0    
host_intervals = []
    
def get_args():
    parser = argparse.ArgumentParser(description='IP creator', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-ip',
                        '--ip',
                        type=str,
                        help='The network prefix. ex. 192.168.0.0',
                        dest='prefix',
                        default='192.168.0.0')
    parser.add_argument('-n',
                        '--noctet',
                        type=int,
                        help='Number of octets to fill, 1 or 2',
                        dest='n_octets',
                        default=1)
    parser.add_argument('-ho',
                        '--hosts',
                        type=str,
                        help='List of hosts separated with commas',
                        dest='hosts')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Filename where output should be placed',
                        dest='filename',
                        default='result.txt')
    parser.add_argument('-s',
                        '--sort',
                        type=int,
                        help='input is sorted by descending order',
                        dest='sort',
                        default=0)
    return parser.parse_args()
    
def take_input(input_, sort):
    rv = input_.replace('\n', '').split(sep=',')
    if sort:
        return sorted(list(map(lambda x: int(x), rv)), reverse=True)
    return list(map(lambda x: int(x), rv))

def find_closest(n_hosts):
    global hosts
    closest = 24
    for key, value in hosts.items():
        if value - n_hosts >= 0 and value - n_hosts < hosts[closest]:
            closest = key
    return closest 

def take_and_divide(n_hosts):
    global last_available
    closest = find_closest(n_hosts)
    host_intervals.append([last_available + 1, last_available + 1 + hosts[closest], closest])
    last_available +=  mask[closest]
    
def create_ip_addresses(prefix, filename, hosts, n_octets):
    global host_intervals
    if n_octets == 2:
        prefix = prefix.split('.')[:2]
        with open(os.path.join(os.path.dirname(__file__), filename), 'w') as file:
            file.write('First address is a default-gateway and the last is a broadcast address\n')
            for (left, right, mask), host in zip(host_intervals, hosts):
                left, right = to_dotted_decimal(left), to_dotted_decimal(right)
                file.write(f'hosts: {host} -> {prefix[0]}.{prefix[1]}.{left} ... {prefix[0]}.{prefix[1]}.{right} mask: /{mask} ')     
                mask = mask_repr(mask)
                file.write(f'{mask}\n')
                
    elif n_octets == 1:
        prefix = prefix.split('.')[:3]
        with open(os.path.join(os.path.dirname(__file__), filename), 'w') as file:
            file.write('First address is a default-gateway and the last is a broadcast address\n')
            for (left, right, mask), host in zip(host_intervals, hosts):
                file.write(f'hosts: {host} -> {prefix[0]}.{prefix[1]}.{prefix[2]}.{left} ... {prefix[0]}.{prefix[1]}.{prefix[2]}.{right} mask: /{mask} ')  
                mask = mask_repr(mask)
                file.write(f'{mask}\n')

def to_dotted_decimal(number, length=3):
    output = ''
    for i in reversed(range(length)):
        output += str((number >> (8 * i)) & 2**8 - 1)
        if i != 0:
            output += '.'
    return output

def mask_repr(mask):
    mask = (2 ** 32 - 1) & (~(2**(32-mask) - 1))
    return to_dotted_decimal(mask, 4)

def process(prefix, n_octets, hosts, filename, sort):
    hosts = take_input(hosts, sort)
    if n_octets == 1:
        assert sum(hosts) < 254 and sum(hosts) > 0, 'Coś za dużo tych hostów'
    for input_ in hosts:
        take_and_divide(input_)
    create_ip_addresses(prefix, filename, hosts, n_octets)

if __name__ == "__main__":
    args = get_args()
    process(
        prefix=args.prefix,
        n_octets=args.n_octets,
        hosts=args.hosts,
        filename=args.filename,
        sort=args.sort
    )