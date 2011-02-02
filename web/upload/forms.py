from django import forms
from tweatwell import settings
import pycurl, StringIO
from omhe.core.parseomhe import parseomhe
from django.contrib.auth.models import User
from tweatwell.web.upload.models import fruit_list, veg_list

file_types_choices=(("pdf","pdf"),
                  ("ccr","ccr"),
                  ("ccd","ccd"),
                  ("indivo","indivo"),
                  ("hdata","hdata"),
                  ("png", "png"),
                  ("jpg","jpg"),
                  ("bmp", "bmp"),
                  ("tiff", "tiff"),
                  ("png", "png"),
                  ("jpeg200", "jpeg200"),
                  ("word_doc", "word_doc"),
                  ("text","text"),
                  ("tweet","tweet"),
                  ("snomedct", "snomedct"),
                  ("hl7v2", "hl7v2"),
                  ("hl7v3", "hl7v3"),
                  ("unk","unk"),
                  ("icd9","icd9"),
                  ("icd10","icd10"),
                  ("cpt","cpt"),
                  ("hicpcs","hicps"),
                  ("loinc","loinc"),
                  ("lab","lab"),
                  ("rx","rx"),
                  ("rxnorm","rxnorm"),
                  ("diacom_image", "diacom_image"),
                  ("diacom_structured_report","diacom_structured_report"),
                  ("x10","x10"),
                  ("idc", "idc"),)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, label="Name for this File")
    file  = forms.FileField()
    type =forms.TypedChoiceField(choices=file_types_choices,
                   widget=forms.RadioSelect, label="File Type")
    tags  = forms.CharField(required=False, max_length=50, label="Tags (Seperated by commas)")
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your password'})
    
class PickFruitForm(forms.Form):
    fruit = forms.TypedChoiceField(choices=fruit_list, label="Fruit")

class PickVeggieForm(forms.Form):
    vegetable = forms.TypedChoiceField(choices=veg_list, label="Vegetable")

class BPUploadForm(forms.Form):
    
    where_choices=(
        ('home','home'),
        ('work','work'),
        ("doctor's office","doctor's office"),
        ("other","other"),
        
    )
    
    syst = forms.IntegerField(max_value=999, label="Systolic")
    dia = forms.IntegerField(max_value=999, label="Diastolic")
    pulse = forms.IntegerField(max_value=999, required=False, label="Pulse")
    where= forms.TypedChoiceField(required=False,
                   choices=where_choices,
                   widget=forms.RadioSelect, label="Where did you take the reading?")
       
    def save(self, user):
        syst=self.cleaned_data['syst']
        dia=self.cleaned_data['dia']
        pulse=self.cleaned_data['pulse']
        where=self.cleaned_data['where']
        
        omhe_str="bp=%s/%sp%s" % (syst, dia, pulse)
        if where:
            omhe_str="%s#%s"% (omhe_str, where)
        
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)

        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 2)        
        code = result.getinfo(result.HTTP_CODE)
        
        return code
    
    
class WTUploadForm(forms.Form):
    wt = forms.FloatField(max_value=2000, label="Weight in Pounds (lbs.)")
     
    def save(self, user):
        wt=self.cleaned_data['wt']
        
        omhe_str="wt=%sl" % (wt)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER_EMAIL,
                                  user_email, 2)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
    
class AJAXWTUploadForm(forms.Form):
    wt = forms.FloatField(max_value=2000, label="Weight in Pounds (lbs.)")
     
    def save(self, user):
        
        responsedict={}
        wt=self.cleaned_data['wt']
        
        omhe_str="wt=%sl" % (wt)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)
        responsedict=uploadOMHE2restcatdict(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER_EMAIL,
                                  user_email, 2)
        #print responsedict
        
        return responsedict
    
class AJAXOMHEUploadForm(forms.Form):
    
    texti = forms.CharField(label="texti")
     
    def save(self, user):
        responsedict={}
        omhe_str=self.cleaned_data['texti']
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)
        responsedict=uploadOMHE2restcatdict(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER_EMAIL,
                                  user_email, 2)
        print responsedict
        
        return responsedict
    
class AJAXCIUploadForm(forms.Form):
    ci = forms.CharField(label="Your Comment")
     
    def save(self, user):
        ci=self.cleaned_data['ci']
        
        omhe_str="ci=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        responsedict=uploadOMHE2restcatdict(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER_EMAIL,
                                  user_email, 2)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)

        return responsedict
    
class FFMUploadForm(forms.Form):
    ffm = forms.FloatField(max_value=2000, label="Free Fat Mass in Pounds (lbs.)")
      
    def save(self, user):
        ffm=self.cleaned_data['ffm']
        
        omhe_str="ffm=%sl" % (ffm)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 2)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
class FMUploadForm(forms.Form):
    fm = forms.FloatField(max_value=2000, label="Fat Mass in Pounds (lbs.)")
     
    def save(self, user):
        fm=self.cleaned_data['fm']
        
        omhe_str="fm=%sl" % (fm)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 2)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code  
    
    
class PBFUploadForm(forms.Form):
    pbf = forms.FloatField(max_value=2000, label="Percent Body Fat")
    
    def save(self, user):
        pbf=self.cleaned_data['pbf']
        
        omhe_str="pbf=%s" % (pbf)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 2)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code  
    
class CIUploadForm(forms.Form):
    ci = forms.CharField(label="Comment")
    
    def save(self, user):
        ci=self.cleaned_data['ci']
        
        omhe_str="ci=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        responsedict=uploadOMHE2restcatdict(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        return responsedict



class OMHEUploadForm(forms.Form):
    texti = forms.CharField(label="texti")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str= texti
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        responsedict=uploadOMHE2restcatdict(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        return responsedict


class TextiUploadForm(forms.Form):
    texti = forms.CharField(label="Texti")
    
    def save(self, user, omhe_prefix):
        texti=self.cleaned_data['texti']
        
        omhe_str="%s=%s" % (omhe_prefix, texti)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code

  
class VeggieUploadForm(forms.Form):
    texti = forms.CharField(label="Veggie")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="veg=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
    
class FruitUploadForm(forms.Form):
    texti = forms.CharField(label="Fruit")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="fruit=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
class BeerUploadForm(forms.Form):
    texti = forms.CharField(label="Beer")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="alc=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
class WaterUploadForm(forms.Form):
    texti = forms.CharField(label="Water")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="alc=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
class JunkUploadForm(forms.Form):
    texti = forms.CharField(label="Water")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="junk=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
class EatUploadForm(forms.Form):
    texti = forms.CharField(label="Eat")
    
    def save(self, user):
        texti=self.cleaned_data['texti']
        
        omhe_str="eat=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code
    
class CommentUploadForm(forms.Form):
    ci  = forms.CharField(label="Comment")
    idr = forms.CharField(label="ID Reference")
    
    def save(self, user):
        ci=self.cleaned_data['ci']
        idr =self.cleaned_data['idr']
        omhe_str="ci=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3, idr, str(u.username) )
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code

    
class TwitBotCIUploadForm(forms.Form):
    ci = forms.CharField(label="Comment")
    
    def save(self, user, text):
        ci=text
        omhe_str="ci=%s" % (ci)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code  
 
    
class STUploadForm(forms.Form):
    st = forms.IntegerField(max_value=2000, label="Steps Per Day")
     
    def save(self, user):
        st=self.cleaned_data['st']
        
        omhe_str="st=%s" % (st)
        """ Instantiate an instance of the OMHE class"""
        o = parseomhe()
        """Parse it if valid, otherwise raise the appropriate  error"""
        d=o.parse(omhe_str)
        u=User.objects.get(username=user)
        user_email=str(u.email)

        result=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS, user_email,
                                  settings.RESTCAT_USER,
                                  user_email, 3)
        #print "HTTP Response Code=%s" % (result.getinfo(result.HTTP_CODE),)
        code = result.getinfo(result.HTTP_CODE)
        return code



def uploadOMHE2restcat(omhe_dict, username, password, 
                        sndr, rcvr, subj, 
                        security=3, idr=None, commenter_display_name=None):

    URL="%sapi/transaction/create/" % (settings.RESTCAT_SERVER)
    URL=str(URL)
    user_and_pass="%s:%s" % (username, password)
    user_and_pass=str(user_and_pass)
    pf=[]
    routing={'sndr':sndr,
        'rcvr':settings.RESTCAT_USER_EMAIL,
        'subj':sndr,
         'sec':security,}
    post_dict={}
    if idr:
        post_dict['idr']=idr
        if commenter_display_name:
            post_dict['texti']="@"+ commenter_display_name + omhe_dict['texti']
    post_dict['ttype']='omhe'
    post_dict.update(routing)
    post_dict['tx_dt']=omhe_dict['tx_dt']
    post_dict['tx_tz']=settings.DEFAULT_TRANSACTION_TIMEZONE_OFFSET
    post_dict['ev_dt']=omhe_dict['ev_dt']
    post_dict['ev_tz']=settings.DEFAULT_TRANSACTION_TIMEZONE_OFFSET
    post_dict['id']=omhe_dict['id']
    post_dict['texti']=omhe_dict['texti']
    
    #print post_dict
    
    #f = open("out.txt", "wb")
    for o in post_dict:
        x=(str(o), str(post_dict[o]))
        pf.append(x)   
    
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    #c.setopt(c.WRITEDATA, f)
    
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    #f.close() 
    
    
    return c
def uploadOMHE2restcatdict(omhe_dict, username, password, 
                        sndr, rcvr, subj, 
                        security=3, idr=None, commenter_display_name=None):
    """returns a dict instead of the handle"""
    
    URL="%sapi/transaction/create/" % (settings.RESTCAT_SERVER)
    URL=str(URL)
    user_and_pass="%s:%s" % (username, password)
    user_and_pass=str(user_and_pass)
    pf=[]
    routing={'sndr':sndr,
        'rcvr':settings.RESTCAT_USER_EMAIL,
        'subj':sndr,
         'sec':security,}
    post_dict={}
    if idr:
        post_dict['idr']=idr
        if commenter_display_name:
            post_dict['texti']="@"+ commenter_display_name + omhe_dict['texti']
    post_dict['ttype']='omhe'
    post_dict.update(routing)
    post_dict['tx_dt']=omhe_dict['tx_dt']
    post_dict['tx_tz']=settings.DEFAULT_TRANSACTION_TIMEZONE_OFFSET
    post_dict['ev_dt']=omhe_dict['ev_dt']
    post_dict['ev_tz']=settings.DEFAULT_TRANSACTION_TIMEZONE_OFFSET
    post_dict['id']=omhe_dict['id']
    post_dict['texti']=omhe_dict['texti']
    
    #print post_dict
    
    #f = open("out.txt", "wb")
    for o in post_dict:
        x=(str(o), str(post_dict[o]))
        pf.append(x)   
    
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform() 
    responsedict={}
    responsedict['code']=c.getinfo(c.HTTP_CODE)
    responsedict['body']=b.getvalue()
    return responsedict