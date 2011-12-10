from django.conf import settings
import pycurl

def create_restcat_user(username, password, email, first_name, last_name,
                        mobile_phone_number=None, pin=None):
    
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=settings.RESTCAT_SERVER + str('accounts/create/')
    #build our RESTCat user dict
    attrs={'username':username,
           'password1':password,
           'password2':password,
           'email':email,
           'first_name': first_name,
           'last_name':last_name}
    if pin:
        attrs['pin']= pin    

    if mobile_phone_number:
        attrs['mobile_phone_number']= mobile_phone_number
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
    #c.setopt(c.WRITEDATA, f) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    return c