__author__ = 'ahsanul'
from cgi import parse_qs
import os

def authMiddleware(app):

    def auth(environ, start_response):
        new_environ = environ.copy()
        if environ['REQUEST_METHOD'] == "POST":
            if environ['PATH_INFO'] == "/authenticate":
                 query_string = parse_qs(environ['QUERY_STRING'])
                 file_path = "Acct_%s" % query_string.get("username")[0]
                 upload_path = file_path+"/upload/hello"
                 download_path = file_path + "/download/hello"
                 check_path = file_path + "/"
                 if not os.path.exists(os.path.dirname(check_path)):
                    os.makedirs(os.path.dirname(upload_path))
                    os.makedirs(os.path.dirname(download_path))
                 else:
                    print "Account already exists"


        if environ['REQUEST_METHOD'] == "GET" or environ['REQUEST_METHOD']=="PUT":
            username = environ["PATH_INFO"][5:]
            storageID = "Acct" + username + "/"
            if not os.path.exists(os.path.dirname(storageID)):
                environ['PATH_INFO'] = "INVALID"
            else:
                environ['PATH_INFO'] = storageID + "upload/"

        return app(environ, start_response)

    return auth
