from useragents import search_strings
from flask import request, g
from functools import wraps

def is_mobile():
    return is_mobile_request(request)

def is_mobile_request(request):
    if hasattr(g, "mobile"):
        return g.mobile

    if request is None or not hasattr(request, 'headers'):
        return False

    if 'X-Operamini-Features' in request.headers:
        # Then it's running opera mini. 'Nuff said.
        # Reference from:
        #  http://dev.opera.com/articles/view/opera-mini-request-headers/
        g.mobile = True
        return True


    if 'Accept' in request.headers:
        s = request.headers['Accept'].lower()
        if 'application/vnd.wap.xhtml+xml' in s:
            # Then it's a wap browser
            g.mobile = True
            return True

    if 'User-Agent' in request.headers:
        # This takes the most processing. Surprisingly enough, when I
        # Experimented on my own machine, this was the most efficient
        # algorithm. Certainly more so than regexes.
        # Also, Caching didn't help much, with real-world caches.
        s = request.headers['User-Agent'].lower()
        for ua in search_strings:
            if ua in s:
                g.mobile = True
                return True

    g.mobile = False
    return False


def detect_mobile(view):
    """View Decorator that adds a "mobile" attribute to the request which is
       True or False depending on whether the request should be considered
       to come from a small-screen device such as a phone or a PDA"""

    @wraps(view)
    def detected(*args, **kwargs):
        request.mobile = is_mobile_request(request)
        return view(*args, **kwargs)
    detected.__doc__ = "%s\n[Wrapped by detect_mobile which detects if the request is from a phone]" % view.__doc__
    return detected


__all__ = ['detect_mobile']
