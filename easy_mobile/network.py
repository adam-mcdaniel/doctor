# import urllib
# from kivy.network.urlrequest import UrlRequest

# def println(s):
#     print(s)

# params = urllib.urlencode({'chatroom':1, 'username':"adamthekiwi"})
# headers = {'Content-type': 'application/x-www-form-urlencoded',
#           'Accept': 'text/plain'}

# req = UrlRequest('https://httpbin.org/headers', on_success=(lambda a: println("post successful")), req_body=params,
#         req_headers=headers)
        
# def got_json(req, result):
#     for key, value in result['headers'].items():
#         print('{}: {}'.format(key, value))

# req = UrlRequest('https://httpbin.org/headers', got_json)