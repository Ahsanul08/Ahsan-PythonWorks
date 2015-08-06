# ***************** How To Request with cURL **********************
#  for creating account :     curl -v -X POST http://127.0.0.1:8080/authenticate?username= <name>
#  for uploading file   :     curl -v -X PUT -T <file_to_upload> http://127.0.0.1:8080/<Auth_name>?filename=<ExpectedNameOfTheUploadedFile>
#  for downloading file :     curl -V -X GET http://127.0.0.1:8080/<Auth_name>?filename="fileToDownload" >> Acct_name/download/<expectedFileName>
#  *******************************************************************


import pprint,os
from cgi import parse_qs


def upDownLoad(environ,start_response):
    print "Hello"
    if environ["REQUEST_METHOD"]== "POST":
        return noAction(environ,start_response)

    if environ["REQUEST_METHOD"]== "GET":
        print "Before GET"
        result = downloadApp(environ,start_response)
        print "After GET"
        return  result
    print environ["REQUEST_METHOD"]
    if environ["REQUEST_METHOD"] == "PUT":
        print "Before PUT"
        result = uploadApp(environ,start_response)
        print "After PUT"
        return result


def noAction(environ,start_response):
    print "No action"
    status = "200 OK"
    response_header = [('Content-Type','text/plain')]
    start_response(status,response_header)
    query_string = parse_qs(environ['QUERY_STRING'])
    file_path = "Auth_%s" % query_string.get("username")[0]
    return ["Plz request with ",file_path, " to Upload and Download"]

def downloadApp(environ, start_response):
    print "____________________________________"
    pprint.pprint(environ)
    new_environ = environ.copy()
    state = True
    query_string = parse_qs(environ["QUERY_STRING"])
    fileToDownload = query_string.get("filename")[0]
    if os.path.exists(os.path.dirname(fileToDownload)):
        state = False
    else:
        if environ['PATH_INFO'] is not "INVALID":
            with open(fileToDownload, 'r') as f:
		        content = f.read()
            if state == False:
                content = "Requested file doesn't exist"
        else:
            content = "User doesn't exist"
    status = "200 OK"
    response_header = [('Content-Type','text/plain')]
    start_response(status,response_header)
    return content


def uploadApp(environ, start_response):
    print "_________________upload_______________________"
    pprint.pprint(environ)
    try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
		request_body_size = 0
    query_string = parse_qs(environ['QUERY_STRING'])
    file_path = environ['PATH_INFO'] + query_string.get("filename")[0]

    if not os.path.exists(os.path.dirname(file_path)):
		os.makedirs(os.path.dirname(file_path))

    request_body = environ['wsgi.input'].read(request_body_size)
    # print request_body
    with open(file_path, 'w') as f:
		f.write(request_body)

    status = "200 OK"
    body =['successfully uploaded\n']
    res_headers = [('Content-Type', 'text/plain')]
    start_response(status, res_headers)
    return body


if __name__ == "__main__":
    from paste import httpserver
    from auth_middleware import authMiddleware
    httpserver.serve(authMiddleware(upDownLoad), host="127.0.0.1", port='8080')