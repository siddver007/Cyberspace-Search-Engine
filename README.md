# Cyberspace Search Engine
This is a quick python project to search SHODAN, ZOOMEYE, CENSYS, and BINARYEDGE. Works with Python 3.x.x.

# usage:
```
usage: search.py [-h] [-qs "SEARCH STRING"] [-qz "SEARCH STRING"] [-qc "SEARCH STRING"] [-qb "SEARCH STRING"] [-ip]

Cyberspace Search Engine.

optional arguments:
  -h, --help           show this help message and exit
  -qs "SEARCH STRING"  Search string for Shodan
  -qz "SEARCH STRING"  Search string for ZoomEye
  -qc "SEARCH STRING"  Search string for Censys
  -qb "SEARCH STRING"  Search string for BinaryEdge
  -ip                  Modifier to return just unique SocketInfo for found Hosts IP:Port
```                        

# examples:
```
$ python search.py -qs "http.title:'Tesla PowerPack System'" -ip
```


just return socket information (IP:PORT): -
```
$ python search.py -qz "app:'{5}'" -ip
```
![picture](1.PNG)

# installation:
`pip install -r requirements.txt`


# update search.py:
```

SHODAN_API_KEY = 'SHODAN_API_KEY'
ZOOMEYE_CREDENTIALS = {'username': 'EMAIL', 'password': 'PASSWORD'}
CENSYS_API_ID = 'CENSYS_API_ID'
CENSYS_API_SECRET = 'CENSYS_API_SECRET'
BINARY_EDGE_API_KEY = 'BINARY_EDGE_API_KEY'

