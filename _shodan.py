# Shodan search
def shodan(q, SHODAN_API_KEY):
	from shodan import Shodan
	api = Shodan(SHODAN_API_KEY)
	results = []
	for banner in api.search_cursor(q, retries=10):
		results.append(banner)
	return results	

if __name__ == '__main__':
	shodan(q='search_string', SHODAN_API_KEY='api_key')		