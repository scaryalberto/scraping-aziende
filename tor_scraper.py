
def start_tor(url):
    from torpy.http.requests import TorRequests
    with TorRequests() as tor_requests:
       with tor_requests.get_session() as sess:
           return sess.get(url).text


