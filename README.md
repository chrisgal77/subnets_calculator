# subnets_calculator
Project provides a script to calculate subnets of a given prefix and other specs.

```
subnets.py [-h] [-ip PREFIX] [-n N_OCTETS] [-ho HOSTS] [-o FILENAME] [-s SORT]
```

```
IP creator

optional arguments:
  -h, --help            show this help message and exit
  -ip PREFIX, --ip PREFIX
                        The network prefix. ex. 192.168.0.0 (default: 192.168.0.0)
  -n N_OCTETS, --noctet N_OCTETS
                        Number of octets to fill, 1 or 2 (default: 1)
  -ho HOSTS, --hosts HOSTS
                        List of hosts separated with commas (default: None)
  -o FILENAME, --output FILENAME
                        Filename where output should be placed (default: result.txt)
  -s SORT, --sort SORT  input is sorted by descending order (default: 0)
```
