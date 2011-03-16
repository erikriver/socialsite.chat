from socialsite.chat.models import DBSession
from socialsite.chat.models import Channels

def home(request):
    return {'project':'pyramid_chat'}

def chat(request):
    server_host = request['HTTP_HOST'].split(':')[0]
    username = request.params.get('username',None)
    request.session['username'] = username
    
    return {'username': username,
            'hookbox_server': 'http://'+server_host+':2974' }

def connect (request):
    # accept all connect requests and assume they are from 'guest'
    username = request.session.get('username', "Guest")
    return [ True, {"name":username} ]

def disconnect (self):
    return [ True, {} ]

def create_channel (self):
    # accept all create channel requests. in this example,
    # only one channel is ever created: 'chan1'
    return [ True, { "history_size" : 30, 
                        "reflective" : True, 
                        "presenceful" : True } ]

def subscribe (self):
    return [ True, {} ]

def unsubscribe (self):
    return [ True, {} ]

def publish (self):
    return [ True, {} ]

