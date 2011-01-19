from django.core.mail import send_mail
from datetime import datetime, timedelta
import os, uuid
import pycurl, json, StringIO
import settings
from operator import itemgetter, attrgetter

def RESTCatdt2pydt(in_string, tzo_string=None):
        """Convert a RESTCat datetime string into a python datetime object"""
        in_string=str(in_string)
        if (len(in_string)!=16):
            error_string = "Datime %s is Incorrect Length." % (in_string)
            return None
        
        if (in_string[15]!="z" and in_string[15]!="Z" and in_string[15]!="u" and in_string[15]!="U"):
            error_string = "Datime %s must end in 'z' or 'u' to explicitly denote UTC." % (in_string)
            return None
    
        year=str(in_string[0:4])
        if year.isdigit():
            year=int(year)
        else:
            return None
        
        month=in_string[4:6]
        if month.isdigit():
            month=int(month)
        else:
            return None
        
        
        day=in_string[6:8]
        if day.isdigit():
            day=int(day)
        else:
            return None
        
        hour=in_string[9:11]
        if hour.isdigit():
            hour=int(hour)
        else:
            return None
            
        minute=in_string[11:13]
        if minute.isdigit():
            minute=int(minute)
        else:
            return None
            
        second=in_string[13:15]
        if second.isdigit():
            second=int(second)
        else:
            return None
        dt=datetime(year, month, day, hour, minute, second)
        if tzo_string:
            if (-12 <= float(tzo_string) <=14 ) and int(tzo_string)!=0:
                dt = dt + timedelta(hours=float(tzo_string))
        return dt

def uploadFile2RESTCat(request, user, file_path):
    #build our RESTCat dict
    attrs={}
    now = datetime.utcnow()
    attrs['ev_dt']= datetime.strftime("%Y%m%d:%H%M%Sz")
    attrs['tx_dt']= datetime.strftime("%Y%m%d:%H%M%Sz")
    attrs['tx_tz']=-5 #US East Coast
    attrs['ev_tz']=-5 #US East Coast
    attrs['id']=str(uuid.uuid4())
    attrs['sndr']=str(user.email)
    attrs['rcvr']=str(user.email)
    attrs['subj']=str(user.email)
    attrs['ttype']=request.POST.ttype 
    #Guess mime type
    attrs['mime']="text"
    
    #Upload using Pycurl
    pf=[]
    for o in attrs:
        x=(str(o), str(post_dict[o]))
        pf.append(x)
    #print pf
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(c.WRITEDATA, f) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, userpass)
    c.perform()
    return c
    

def handle_uploaded_file(file, user):
    
    #create folder name for the api username
    dirname = '%s/%s' %(settings.MEDIA_ROOT, user.username)
    
    #create directory if it doesn't exist
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        
    myuuid=uuid.uuid4()
    current_time = str(datetime.utcnow())
    time_str=current_time.replace(" ", '_')
    
    #create file name by using current datetime
    new_file_name='%s_%s' %(myuuid,
                              file.name)
    try:
        #create the entire directory string
        file_name='%s%s' %(dirname, new_file_name)
    
        #open to write
        destination = open(file_name, 'wb')

        #write out in chunks
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        retval=file_name
    except:
        retval=None
        
    
    return retval


def query_restcat(URL, RESTCAT_SERVER=settings.RESTCAT_SERVER,
                  USERNAME=settings.RESTCAT_USER,
                  PASSWORD=settings.RESTCAT_PASS, CONVERT_DATES=True):
    """Query RESTCat"""
    response_dict={}
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=str(URL)
    ##print URL
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    json_string= b.getvalue()
    try:
        bodylist=list(json.loads(json_string))

        
        if CONVERT_DATES:
            for i in bodylist:
                if type(i)==dict:
                    i['ev_dt']=RESTCatdt2pydt(str(i['ev_dt']), str(i['ev_tz']))
                    i['tx_dt']=RESTCatdt2pydt(i['tx_dt'], i['tx_tz'])
        
        bodylist=sorted(bodylist, key=itemgetter('ev_dt'), reverse=True)
    
    except:
        bodylist=None
    
    response_dict['code'] = c.getinfo(c.HTTP_CODE)
    response_dict['bodylist'] = bodylist
    
    return response_dict


def sendmail_for_comment(username, text ,idr):
    URL="%sapi/transaction/get-by-txid/%s" % (settings.RESTCAT_SERVER, idr)
    r=query_restcat(URL)
    body="Just a heads up that %s just commented on your status.\n %s \n --Tweatwell" % (username, text)
    emailsubjectline="%s" % ("Tweatwell: Someone commented on your status.")
    send_mail(emailsubjectline, body, 'physique7@videntity.com',
                    [r['bodylist'][0]['subj']], fail_silently=False)
    

