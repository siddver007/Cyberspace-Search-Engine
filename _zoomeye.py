# Zoomeye search
def zoomeye(q, creds):
	import requests
	url = 'https://api.zoomeye.org/user/login'
	res = requests.post(url, json=creds).json()
	b_token = 'JWT ' + res['access_token']
	q = q.replace('\'', '"')
	res2 = requests.get('https://api.zoomeye.org/host/search?query=%s'
						%(q), headers={'Authorization': b_token}).json()
	total = res2['total']
	available = res2['available']
	results = []
	for page in range(1, int(int(total)/int(available)) + 2):
		res3 = requests.get('https://api.zoomeye.org/host/search?query=' +
								'%s&page=%s' %(q, str(page)),
								headers={'Authorization': b_token}).json()
		results.append(res3)
	return results  

if __name__ == '__main__':
	zoomeye(q='search_string', creds='credentials')   



