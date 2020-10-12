# BinaryEdge search
def binary_edge(q, BINARY_EDGE_API_KEY):
	import requests
	uri = 'https://api.binaryedge.io/v2/query/search?query=%s' %(q)
	headers = {'X-Key': BINARY_EDGE_API_KEY}
	q = q.replace('\'', '"')
	res_json = requests.get(uri, headers=headers).json()
	results = res_json
	return results	

if __name__ == '__main__':
	be = binary_edge(q='search_string', BINARY_EDGE_API_KEY='API_KEY')