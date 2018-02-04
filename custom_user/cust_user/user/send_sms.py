import urllib.request
import urllib.parse
import json
from django.conf import settings

apikey = settings.SMS_API_KEY

def sendSMS(number=None, message=None):

    if number is None or message is None:
        return -1

    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': number,
                                   'message': message, 'sender': 'TXTLCL'})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    c = fr.decode('utf-8')
    d = json.loads(c)
    return (d)


