import unittest
from pyramid.config import Configurator
from pyramid import testing
from models import DBSession
from models import Users, Channels, Logs
from sqlalchemy import func


def _initTestingDB():
    from sqlalchemy import create_engine
    from socialsite.chat.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session

class TestModels(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        _initTestingDB()
        self.session = DBSession

    def tearDown(self):
        testing.tearDown()

    def test_users(self):
        user1 = Users(username=u'user1')
        self.session.add(user1)

        n = self.session.query(Users).filter(Users.username.like(u'%user1')).count()
        self.assertEqual(n,1)
        
        user2 = Users(username=u'user2')
        self.session.add(user2)

        n = self.session.query(Users).filter(Users.username.like(u'user%')).count()
        #self.assertEqual(n,2)

    def test_channels(self):
        chan1 = Channels(name=u'Channel1')
        self.session.add(chan1)
        self.assertEqual(chan1.name,u'Channel1') 

        chan2 = Channels(name=u'Channel2')
        chan3 = Channels(name=u'Channel3')
        chan4 = Channels(name=u'Channel4')
        self.session.add_all([chan2,chan3,chan4])

    def test_logs(self):
        user3 = Users(username=u'user3')
        chan5 = Channels(name=u'Channel5')
        self.session.add_all([user3,chan5])
        log = Logs(log=u'Lorem Ipsum', user=user3.id,channel=chan5.id)
        self.session.add(log)
        n = self.session.query(Logs.user).group_by(Logs.user).count()
        self.assertEqual(n,1)
        
class TestViews(unittest.TestCase):
    
    def test_home(self):
        from socialsite.chat.views import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'socialsite.chat')
        
    def test_chat(self):
        from socialsite.chat.views import chat
        request = testing.DummyRequest()
        info = chat(request)
        self.assertEqual(info['username'], None)
