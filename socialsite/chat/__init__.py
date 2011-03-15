from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from socialsite.chat.models import initialize_sql

from pyramid.session import UnencryptedCookieSessionFactoryConfig
my_session_factory = UnencryptedCookieSessionFactoryConfig('pyramid_s3cr3t')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.add_static_view('static', 'socialsite.chat:static')
    config.add_route('home', '/', view='socialsite.chat.views.home',
                    view_renderer='templates/home.pt')
    config.add_route('chat', '/chat', view='socialsite.chat.views.chat',
                    view_renderer='templates/chat.pt')


    config.add_view('socialsite.chat.views.connect',
                    name='connect',
                    renderer='json')
    config.add_view('socialsite.chat.views.disconnect',
                    name='disconnect',
                    renderer='json')
    config.add_view('socialsite.chat.views.create_channel',
                    name='create_channel',
                    renderer='json')
    config.add_view('socialsite.chat.views.subscribe',
                    name='subscribe',
                    renderer='json')    
    config.add_view('socialsite.chat.views.unsubscribe',
                    name='unsubscribe',
                    renderer='json')    
    config.add_view('socialsite.chat.views.publish',
                    name='publish',
                    renderer='json')    
    
    return config.make_wsgi_app()
