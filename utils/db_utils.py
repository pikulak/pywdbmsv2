from sqlalchemy.sql import exists

def exists_row(session, model, where, value):
	return session.query(exists().where(getattr(model, where) == value)).scalar()

#def get_databases()