from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session_maker
from sqlalchemy.engine import url
from sqlalchemy.pool import NullPool

from pywdbms.core.models import Server


class SessionRegistry(object):
	_registry = {}

	def get(self, host, **kwargs):
		if host not in self._registry:
			server_params = Server.query.filter_by(host=host)
			_url = url.URL(**server_params)
			engine = create_engine(_url, poolclass=NullPool, **kwargs)
			Session = session_maker(bind=engine)
			session = scoped_session(Session)
			self._[host] = session
		return self._registry[url]

