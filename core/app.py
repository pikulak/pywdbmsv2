from flask import jsonify, render_template, make_response, request, Blueprint, abort
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.sql import select
from sqlalchemy import inspect

from pywdbms.core.database import db_session
from pywdbms.core.models import Server
from pywdbms.utils.db_utils import exists_row
from pywdbms.utils.view_utils import api_response, parse_url
from pywdbms.core.registers import SessionRegistry

blueprint = Blueprint('blueprint', __name__, template_folder="../templates")
registry = SessionRegistry()

@blueprint.route('/api/servers/', methods=['POST'])
def add_server():
    if request.method == "POST":
        properties = {
            'host': request.form['host'],
            'port': request.form['port'],
            'username': request.form['username'],
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
        if len(servers) > 0:
            return api_response(200, "success",
                         "Success! Returning servers's ipaddrs.", servers)
        else:
            return api_response(400, "error", "Servers doesn't exists.")

@blueprint.route('/api/servers/<string:server>/databases/', methods=['GET'])
def get_databases(server):
    session = registry.get(server)
    if session:
        query = session.execute('SELECT datname FROM pg_database')
        databases = []
        for database in query:
            databases.append(database[0])
        return api_response(200, "success", "Success! Returning server's databases.", databases)
    return api_response(404, "error", "Couldn't get session.")

@blueprint.route('/<path:path>')
def main(path):
    current_object = parse_url(path)
    print(current_object)
    return make_response(render_template(
                        'index.html',
                        current_object=current_object), 200)
