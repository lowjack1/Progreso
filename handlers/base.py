from tornado.web import HTTPError, RequestHandler


class BaseHandler(RequestHandler):
    def write_api_response(self, data, status=True, msg="", code=None):
        '''
        Function to generate a standard response for API calls
        '''
        status = True if status == True else False 
        if code is None:
            code = 200 if status else 400
        resp = {
            "status": status,
            "code": code,
            "msg": msg,
            "result": {'data': data} if status else None
        }
        self.write(resp)
