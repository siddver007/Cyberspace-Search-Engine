##################################################################################
## Python 3.x.x
##################################################################################
## search.py: currently supports Shodan, Censys, ZoomEye, and BinaryEdge
##################################################################################
## Usage: python search.py -h
## Usage: python search.py -qs "http.title:'Tesla PowerPack System'" -ip
##################################################################################
## Author: Siddhant Verma
##################################################################################

import _shodan, _zoomeye, _censys, _binaryedge
import sys, traceback, argparse, pprint, requests, time, json

SHODAN_API_KEY = 'SHODAN_API_KEY'
ZOOMEYE_CREDENTIALS = {
						'username': 'EMAIL', 
						'password': 'PASSWORD'
					}
CENSYS_API_ID = 'CENSYS_API_ID'
CENSYS_API_SECRET = 'CENSYS_API_SECRET'
BINARY_EDGE_API_KEY = 'BINARY_EDGE_API_KEY'

# Shodan search 
def search_shodan(q, api_key):
	sockets = _shodan.shodan(q, SHODAN_API_KEY)
	return sockets

# Zoomeye search 
def search_zoomeye(q, creds):
	sockets = _zoomeye.zoomeye(q, ZOOMEYE_CREDENTIALS)
	return sockets

# Censys search
def search_censys(q, api_id, api_key):
	sockets = _censys.censys(q, api_id, api_key)
	return sockets	

# BinaryEdge search 
def search_binary_edge(q, api_key):
	sockets = _binaryedge.binary_edge(q, api_key)
	return sockets	

if __name__ == '__main__':		 
	try:
		p = argparse.ArgumentParser(description='Cyberspace Search Engine.')
		p.add_argument('-qs', metavar='"SEARCH STRING"',
									help='Search string for Shodan')
		p.add_argument('-qz', metavar='"SEARCH STRING"',
									help='Search string for ZoomEye')
		p.add_argument('-qc', metavar='"SEARCH STRING"',
									help='Search string for Censys')
		p.add_argument('-qb', metavar='"SEARCH STRING"',
									help='Search string for BinaryEdge')
		p.add_argument('-ip', help='Modifier to return just unique ' +
									'SocketInfo for found Hosts IP:Port',
								action='store_true')
		args = p.parse_args()
		qs = args.qs
		qz = args.qz
		qc = args.qc
		qb = args.qb
		only_socks = args.ip
		if not (qs or qz or qc or qb) and only_socks:
			print('-ip modifier cannot be used alone.\n\n'+ 
					'For help - python search.py -h')
			sys.exit()
		if not (qs or qz or qc or qb):
			print('Atleast one argument required.\n\n'+ 
					'For help - python search.py -h')
			sys.exit()
		results_qs = None
		res_qs_sockets = []
		results_qz = None
		res_qz_sockets = []
		results_qc = None
		res_qc_sockets = []
		results_qb = None
		res_qb_sockets = []	
		results_all = {}	
		if qs:
			try:
				results_qs = search_shodan(qs, SHODAN_API_KEY)
				results_all['SHODAN_RESULTS'] = results_qs
				if only_socks:
					for r in results_qs:
						ip, port = (str(r['ip_str']).strip(),
							str(r['port']).strip())
						res_qs_sockets.append({
								'ip': ip,
								'ports': port
							})
			except Exception as e:
				print('[+] EXCEPTION OCCURRED IN Shodan SEARCH + %s\n'
												%(traceback.format_exc()))
				# even if exception occurs in one, continue to next one
				pass
		if qz:
			try:
				for timeout in [2, 4, 6, 8]:
					try:
						results_qz = search_zoomeye(qz, ZOOMEYE_CREDENTIALS)
						results_all['ZOOMEYE_RESULTS'] = results_qz
						if only_socks:
							for r in results_qz:
								for rr in r['matches']:
									ip, port = (str(rr['ip']).strip(),
										str(rr['portinfo']['port']).strip())
									res_qz_sockets.append({
											'ip': ip,
											'ports': port
										})
						break
					except requests.exceptions.ConnectionError as e:
						time.sleep(timeout)
						continue
					except KeyError as e:
						time.sleep(timeout)
						continue
					except json.decoder.JSONDecodeError as e:
						time.sleep(timeout)
						continue			
			except Exception as e:
				print('[+] EXCEPTION OCCURRED IN ZoomEye SEARCH + %s\n'
												%(traceback.format_exc()))
				# even if exception occurs in one, continue to next one
				pass									
		if qc:
			try:
				results_qc = search_censys(qc, CENSYS_API_ID,
													CENSYS_API_SECRET)
				results_all['CENSYS_RESULTS'] = results_qc
				if only_socks:
					for r in results_qc:
						ip = str(r['ip']).strip()
						ports = []
						for p in r['protocols']:
							ports.append(str(p).split('/')[0].strip())
						res_qc_sockets.append({
								'ip': ip,
								'ports': ports
							})
			except Exception as e:
				print('[+] EXCEPTION OCCURRED IN Censys SEARCH + %s\n'
												%(traceback.format_exc()))
				# even if exception occurs in one, continue to next one
				pass										
		if qb:
			try:
				results_qb = []
				results_qb.append(search_binary_edge(qb, BINARY_EDGE_API_KEY))
				results_all['BINARY_EDGE_RESULTS'] = results_qb
				if only_socks:
					for r in results_qb:
						for rr in r['events']:
							ip, port = (rr['target']['ip'].strip(), 
											str(rr['target']['port']).strip())
							res_qb_sockets.append({
									'ip': ip,
									'ports': port
								})
			except Exception as e:
				print('[+] EXCEPTION OCCURRED IN BinaryEdge SEARCH + %s\n'
												%(traceback.format_exc()))									
		# you can play with results_qs, results_qz, results_qc, 
		## results_qb objects independently - these contain search results for
		## Shodan, ZoomEye, Censys, BinaryEdge resp.
		# OR you can play with results_all, which contains
		## all search results from all 4 search engines
		## under dictionary keys - SHODAN_RESULTS, ZOOMEYE_RESULTS,
		## CENSYS_RESULTS, and BINARY_EDGE_RESULTS
		# i haven't parsed any data here because it's upto the user
		## now whatever he/she wants to parse. But in the original
		## script, I had parsed this data to obtain IP Addresses
		
		# to only return hosts/sockets/ip:port values
		## to get SHODAN IP:PORT, use just_socket_info['SHODAN_RESULTS']
		## to get SHODAN IP:PORT, use just_socket_info['ZOOMEYE_RESULTS']
		## to get SHODAN IP:PORT, use just_socket_info['CENSYS_RESULTS']
		## to get SHODAN IP:PORT, use just_socket_info['BINARY_EDGE_RESULTS']		
		if only_socks:
			just_socket_info = {}		
			just_socket_info['SHODAN_RESULTS'] = res_qs_sockets
			just_socket_info['ZOOMEYE_RESULTS'] = res_qz_sockets
			just_socket_info['CENSYS_RESULTS'] = res_qc_sockets
			just_socket_info['BINARY_EDGE_RESULTS'] = res_qb_sockets
			print(json.dumps(just_socket_info, indent=1))
	except Exception as e:
		print('[+] EXCEPTION OCCURRED IN MAIN + %s\n'
												%(traceback.format_exc()))
	

