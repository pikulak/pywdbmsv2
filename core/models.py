from sqlalchemy import Column, Integer, String
from pywdbms.core.database import Base

class Server(Base):
	__tablename__ = 'servers'
	id = Column(Integer, primary_key=True)
	host = Column(String(15), unique=True)
	port = Column(Integer)
	username = Column(String(30))
	password = Column(String(50))
	drivername = Column(String(20))