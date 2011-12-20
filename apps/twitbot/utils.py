import json, sys
import pycurl
import StringIO
import time
from datetime import datetime

def convert_twitter_date(date_str):
    """Convert string to datetime
    """
    time_struct = time.strptime(date_str, "%a, %d %b %Y %H:%M:%S +0000")#Tue, Apr 26 08:57:55 +0000 2011
    mydate= datetime.fromtimestamp(time.mktime(time_struct))
    return mydate


def twitbotsearch(query, since_id):
    URL="http://search.twitter.com/search.json?q=%s&since_id=%s" % (query, since_id)
    URL=str(URL)
    
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.perform()
    jsonstr= b.getvalue()
    
    d=json.loads(jsonstr)
    return d    



if __name__ == "__main__":
    
        try:
            query = sys.argv[1]
            since_id =   sys.argv[2]
            d=twitbotsearch(query, since_id)
            print d
        except:
                print "Error."
                print sys.exc_info()