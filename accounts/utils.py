from registration.models import RegistrationProfile, SHA1_RE
from tweatwell import settings
import pycurl
import StringIO

def verify(verification_key):
    if SHA1_RE.search(verification_key):
        try:
            profile = RegistrationProfile.objects.get(activation_key=verification_key)
        except RegistrationProfile.DoesNotExist:
            return False
        if not profile.activation_key_expired():
            user = profile.user
            user.save()
            profile.activation_key = 'EMAIL_VERIFIED'
            profile.save()
            return user
    return False

def create_restcat_user(username, password, first_name, last_name, email, height_in,
                        weight_goal, gender, pin, birthdate, 
                        mobile_phone_number, twitter):
    
    URL="%sapi/accounts/create/" % (settings.RESTCAT_SERVER)
    URL=str(URL)
    
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    user_and_pass=str(user_and_pass)
    
    pf=[]
    
    post_dict={}
    post_dict['username']=username
    post_dict['password']=password
    post_dict['first_name']=first_name
    post_dict['last_name']=last_name
    post_dict['email']=email
    post_dict['height_in']=height_in
    post_dict['weight_goal']=weight_goal
    post_dict['gender']=gender
    post_dict['pin']=pin
    post_dict['birthdate']=birthdate
    post_dict['mobile_phone_number']=mobile_phone_number
    post_dict['twitter']=twitter


    #print post_dict
    
    for o in post_dict:
        x=(str(o), str(post_dict[o]))
        pf.append(x)   
    
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    message= str(b.getvalue())
    #print message
    ret = {'code': str(c.getinfo(c.HTTP_CODE)), 'message' : message}
    return ret

def update_restcat_user(username, first_name, last_name, email, height_in,
                        weight_goal, gender, pin, birthdate, steps_per_day_goal,
                        phone_number, mobile_phone_number, twitter):
    
    URL="%sapi/accounts/create/" % (settings.RESTCAT_SERVER)
    URL=str(URL)
    
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    user_and_pass=str(user_and_pass)
    pf=[]

    post_dict={}
    post_dict['username']=username
    post_dict['first_name']=first_name
    post_dict['last_name']=last_name
    post_dict['email']=email
    post_dict['height_in']=height_in
    post_dict['weight_goal']=weight_goal
    post_dict['steps_per_day_goal']=steps_per_day_goal
    post_dict['gender']=gender
    post_dict['pin']=pin
    post_dict['birthdate']=birthdate


    #print post_dict
    
    for o in post_dict:
        x=(str(o), str(post_dict[o]))
        pf.append(x)   
    
    
    
    
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)    
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    return c
