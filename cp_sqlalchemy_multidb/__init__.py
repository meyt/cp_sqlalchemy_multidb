# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.process import wspbus, plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Plugin', 'Tool']


class Plugin(plugins.SimplePlugin):
    def __init__(self, bus, connection_strings=None):
        plugins.SimplePlugin.__init__(self, bus)
        self.connections_conf = {}
        self.sessions = {}
        self.sa_engines = {}
        for idx, connection_string in connection_strings.items():
            self.sa_engines[idx] = None
            self.connections_conf[idx] = connection_string
            self.sessions[idx] = scoped_session(sessionmaker(autoflush=True,
                                                             autocommit=False))

    def start(self):
        for idx, connection in self.connections_conf.items():
            if isinstance(connection, str):
                connection = {'cs': connection, 'echo': False}
            self.bus.log('Starting up DB[%s] access' % idx)
            self.sa_engines[idx] = create_engine(connection['cs'], echo=connection['echo'])
        self.bus.subscribe("bind-session", self.bind)
        self.bus.subscribe("commit-session", self.commit)

    def stop(self):
        self.bus.unsubscribe("bind-session", self.bind)
        self.bus.unsubscribe("commit-session", self.commit)
        for idx, sa_engine in self.sa_engines.items():
            self.bus.log('Stopping down DB[%s] access' % idx)
            if self.sa_engines[idx]:
                self.sa_engines[idx].dispose()
                self.sa_engines[idx] = None

    def bind(self):
        for idx, session in self.sessions.items():
            self.sessions[idx].configure(bind=self.sa_engines[idx])
        return self.sessions

    def commit(self):
        for idx, session in self.sessions.items():
            try:
                self.sessions[idx].commit()
            except:
                self.sessions[idx].rollback()
                raise
            finally:
                self.sessions[idx].remove()


class Tool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=20)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.commit_transaction,
                                      priority=80)

    @staticmethod
    def bind_session():
        cherrypy.request.db = {}
        sessions = cherrypy.engine.publish('bind-session').pop()
        print(sessions, type(sessions), dir(sessions))
        for idx, session in sessions.items():
            cherrypy.request.db[idx] = session

    @staticmethod
    def commit_transaction():
        if not hasattr(cherrypy.request, 'db'):
            return
        cherrypy.request.db = {}
        cherrypy.engine.publish('commit-session')
