import argparse
import os


def init(intervals):
    hosts = { i : 2**(32 - i) - 2  for i in range(*intervals) }

    masks = { i : 2**(32 - i) for i in range(*intervals)}

    last_available = 0    
    host_intervals = []
    
    return hosts, masks, last_available, host_intervals
    
def get_args():
    parser = argparse.ArgumentParser(description='IP creator', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-ip',
                        '--ip',
                        type=str,
                        help='The network prefix. ex. 192.168.0.0',
                        dest='prefix',
                        default='192.168.0.0')
    parser.add_argument('-m',
                        '--mask',
                        type=int,
                        help='Mask of subnet',
                        dest='mask_dec',
                        default=24)
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
    
def take_input(input_, sort, sep=','):
    rv = input_.replace('\n', '').split(sep=sep)
    if sort:
        return sorted(list(map(lambda x: int(x), rv)), reverse=True)
    return list(map(lambda x: int(x), rv))

def find_mask(host):
    return 32 - (host).bit_length()

def prepare_prefix(prefix):
    prefix = take_input(prefix, False, sep='.')
    rv = 0
    for element in prefix:
        rv <<= 8
        rv |= element
    return rv

def address_to_string(address):
    result = ''
    for i in reversed(range(4)):
        result += str((address >> (8 * i)) & (2**8 - 1))
        if i != 0:
            result += ('.')
    return result

def to_dotted_dec(number):
    output = ''
    for i in reversed(range(4)):
        output += str((number >> (8 * i)) & 2**8 - 1)
        if i != 0:
            output += '.'
    return output

def mask_repr(mask):
    mask = (2 ** 32 - 1) & (~(2**(32-mask) - 1))
    return to_dotted_dec(mask)

def process(prefix, mask_dec, n_hosts, filename, sort):
    hosts, masks, last_available, host_intervals = init((8,31))
    n_hosts = take_input(n_hosts, sort)
    prefix = prepare_prefix(prefix)
    max_addresses = 2 ** (32 - mask_dec)
    with open(filename, 'w') as file:
        file.write('First address is commonly used for default gateway and the last is broadcast\n')
        for host in n_hosts:
            mask_key = find_mask(host)
            if max_addresses - masks[mask_key] < 0:
                raise ValueError('Too many hosts for the given mask')

            addresses = (address_to_string(prefix + 1), address_to_string(prefix + masks[mask_key] - 1))
            prefix += masks[mask_key]
            max_addresses -= masks[mask_key]
            new_mask_dec = mask_repr(mask_key)
            file.write(f'{host}: {addresses[0]} ... {addresses[1]} mask: /{mask_key} | {new_mask_dec}\n')
    
    
if __name__ == "__main__":
    args = get_args()
    process(
        prefix=args.prefix,
        mask_dec=args.mask_dec,
        n_hosts=args.hosts,
        filename=args.filename,
        sort=args.sort
    )