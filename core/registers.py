from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import url
from sqlalchemy.pool import NullPool

from pywdbms.core.models import Server


class SessionRegistry(object):
	_registry = {}

	def get(self, host, **kwargs):
		if host not in self._registry:
			try:
				server_params = Server.query.filter_by(host=host).all()[0]
			except IndexError:
				return False
				
			prepare_url = {'host': server_params.host,
						   'port': server_params.port,
						   'username': server_params.username,
						   'drivername': server_params.drivername,
						   'password': server_params.password}
			_url = url.URL(**prepare_url)
			engine = create_engine(_url, poolclass=NullPool, **kwargs)
			Session = sessionmaker(bind=engine)
			session = scoped_session(Session)
			self._registry[host] = session
		return self._registry[host]

