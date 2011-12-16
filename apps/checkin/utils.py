from django.conf import settings
import pycurl
from datetime import datetime, timedelta
import os


def update_filename(instance, filename):
    path = "freggie-pics/"
    format = instance.user.username + "-" + filename
    return os.path.join(path, format)
    



def save_to_restcat(attrs):
    print attrs
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=settings.RESTCAT_SERVER + str('transaction/create/')
    #Upload using Pycurl
    pf=[]
    for o in attrs:
        x=(str(o), str(attrs[o]))
        pf.append(x)
    #print pf
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    return c
