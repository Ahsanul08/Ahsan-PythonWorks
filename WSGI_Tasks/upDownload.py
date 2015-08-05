import pprint,os



def upDownLoad(environ,start_response):
    print "Hello"
    if environ["REQUEST_METHOD"]== "GET":
        print "Before GET"
        result = downloadApp(environ,start_response)
        print "After GET"
        return  result

    elif environ["REQUEST_METHOD"] == "PUT":
        print "Before PUT"
        result = uploadApp(environ,start_response)
        print "After PUT"
        return result


def downloadApp(environ, start_response):
    print "____________________________________"
    pprint.pprint(environ)
    new_environ = environ.copy()
    state = True
    print new_environ["REQUEST_METHOD"]
    pathToDownload = new_environ['PATH_INFO']
    file_path = 'downloaded/downloaded.txt'
    if new_environ["PATH_INFO"]:
        file_path = 'downloaded' + pathToDownload

    if not os.path.exists(os.path.dirname(file_path)):
		os.makedirs(os.path.dirname("fownloaded/"))

    with open(pathToDownload[1:], 'r') as f:
		content = f.read()
    status = "200 OK"
    response_header = [('Content-Type','text/plain')]
    start_response(status,response_header)
    if state == False:
        return ["Requested file doesn't exist"]
    return content


def uploadApp(environ, start_response):
    print "_________________upload_______________________"
    pprint.pprint(environ)
    try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
		request_body_size = 0

    path = environ['PATH_INFO']
    file_path = 'uploaded/uploaded.txt'
    if path:
		file_path = 'uploaded' + path

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
    httpserver.serve(upDownLoad, host="127.0.0.1", port='8080')