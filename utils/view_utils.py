from flask import jsonify
from ipaddress import ip_address

def api_response(http_status, status, message, data=""):
	prepare = {"status": status,
			   "message": message}
	if len(data) > 0:
		prepare["data"] = data
	return jsonify(prepare, http_status)

def parse_url(url):
	current_object = {"server": "",
					  "database": "",
					  "table": ""}
	url = url.split("/")
	url = list(filter(None, url))
	if len(url) >= 2 and url[0] == "servers":
		print("ta")
		try:
			host = ip_address(url[1])
			current_object["server"] = url[1]
		except ValueError:
			pass
	if len(url) >= 4 and url[2] == "databases":
		current_object["databases"] = url[3]
	if len(url) >= 6 and url[4] == "table":
		current_object["tables"] = url[5]
	return current_object
