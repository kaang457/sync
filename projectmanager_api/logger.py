import logging

logger = logging.getLogger('django.request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()
        headers = dict(request.headers)
        cookies = request.COOKIES
        query_params = request.GET
        post_data = request.POST
        
        logger.info("Request: method=%s, path=%s, headers=%s,cookies=%s, query_params=%s,post_data=%s", method, path, headers, cookies, query_params, post_data)
        response = self.get_response(request)
        return response

