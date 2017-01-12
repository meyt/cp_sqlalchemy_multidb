import cherrypy
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata


class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255))


class Root(object):
    
    @cherrypy.expose
    def index(self):
        db1 = cherrypy.request.db['db1']
        db2 = cherrypy.request.db['db2']
        
        t_user = User()
        t_user.username = 'DB One User'
        metadata.create_all(db1.bind)
        db1.add(t_user)
        
        t_user = User()
        t_user.username = 'DB Two User'
        metadata.create_all(db2.bind)
        db2.add(t_user)
        
        return "Done"
    
    
if __name__ == '__main__':
    
    import cp_sqlalchemy_multidb
    
    # Register plugin
    cp_sqlalchemy_multidb.Plugin(cherrypy.engine, {'db1': {'cs': 'sqlite:///db1.db',
                                                           'echo': True,
                                                           'autoflush': True,
                                                           'autocommit': True,
                                                           'expire_on_commit': True},
                                                   'db2': {'cs': 'sqlite:///db2.db',
                                                           'echo': True,
                                                           'autoflush': True,
                                                           'autocommit': True,
                                                           'expire_on_commit': True
                                                           }}).subscribe()

    # Register tool
    cherrypy.tools.db = cp_sqlalchemy_multidb.Tool()

    cherrypy.server.socket_port = 9091

    conf = {
        '/': {
            'tools.db.on': True
        }
    }
    cherrypy.quickstart(Root(), '/', conf)
