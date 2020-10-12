# Censys search
# Different IPV4_FIELDS can be set - 
# see data definitions here - https://censys.io/ipv4/help/definitions
# also number of max_records can be changed too
def censys(q, api_id, api_secret):
	import censys.ipv4
	c = censys.ipv4.CensysIPv4(api_id=api_id, api_secret=api_secret)
	IPV4_FIELDS = ['ip',
					'protocols',
					'80.http.get.body',
					'443.https.get.body'
					]
	data = list(c.search(q, IPV4_FIELDS, max_records=200))		 
	return data

if __name__ == '__main__':
	censys(q='search_string', api_id='api_id', api_secret='api_secret')    