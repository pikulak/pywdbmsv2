from flask import jsonify

def api_response(http_status, status, message, data=""):
	prepare = {"status": status,
			   "message": message}
	if len(data) > 0:
		prepare["data"] = data
	return jsonify(prepare, http_status)