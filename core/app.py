from flask import jsonify, render_template, make_response, request, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.sql import select

from pywdbms.core.database import db_session
from pywdbms.core.models import Server
from pywdbms.utils.db_utils import exists_row
from pywdbms.utils.view_utils import api_response
from pywdbms.core.registers import SessionRegistry

blueprint = Blueprint('blueprint', __name__, template_folder="../templates")
registry = SessionRegistry()

@blueprint.route('/')
def main():
    return make_response(render_template(
                        'index.html'), 200)

@blueprint.route('/api/servers/', methods=['POST'])
def add_server():
	if request.method == "POST":
		properties = {
			'host': request.form['host'],
			'port': request.form['port'],
			'database': request.form['database'],
			'user': request.form['username'],
			'password': request.form['password'],
			'drivername': request.form['drivername']}

		if exists_row(db_session, Server, "host", properties["host"]):
			return api_response(400, "error", "Server already exists!")

		server = Server(**properties)
		db_session.add(server)
		db_session.commit()
		return api_response(200, "success", "Successfully added server!")
	return api_response(400, "error", "Unexpected error.")

@blueprint.route('/api/servers/<string:server>/', methods=['DELETE'])
def delete_server(server):
	if request.method == "DELETE":
		if exists_row(db_session, Server, "host", server):
			Server.query.filter_by(host=server).delete()
			db_session.commit()
			return api_response(200, "success", "Successfully deleted specifed server!")
		else:
			return api_response(400, "error", "Specifed server doesn't exists!")
	return api_response(400, "error", "Unexpected error occured!")

@blueprint.route('/api/servers/', methods=['GET'])
def get_servers():
	if request.method == "GET":
		servers = []
		query = db_session.query(Server.host)
		for server in query:
			servers.append(server[0])
		return api_response(200, "success",
						 "Success! Returning servers's ipaddrs.", servers)

#@blueprint.route('/api/servers/<string:server>/databases/', methods=['GET'])
#def get_databases(server):
