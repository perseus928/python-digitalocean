import requests

class BaseAPI(object):
    """
        Basic api class for
    """
    token = ""
    call_response = None

    def __init__(self):
        super(BaseAPI, self).__init__()

    def __perform_get(self, url, headers=dict(), params=dict()):
        return requests.get(url, headers=headers, params=params)

    def __perform_post(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/json'
        return requests.post(url, headers=headers, params=params)

    def __perform_put(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/json'
        return requests.put(url, headers=headers, params=params)

    def __perform_delete(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/x-www-form-urlencoded'
        return requests.delete(url, headers=headers, params=params)

    def __perform_request(self, url, type='GET', params=dict()):
        """
            This method will perform the real request,
            in this way we can customize only the "output" of the API call by
            using self.__call_api method.
            This method will return the request object.
        """
        headers = {'Authorization':'Bearer ' + self.token}
        if type == 'POST':
            r = self.__perform_request(url, headers=headers, params=params)
        elif type == 'PUT':
            r = self.__perform_put(url, headers=headers, params=params)
        elif type == 'DELETE':
            r = self.__perform_delete(url, headers=headers, params=params)
        else:
            r = self.__perform_get(url, headers=headers, params=params)
        return r

    def get_data(self, url, type="GET", params=dict()):
        """
            This method is a basic implementation of __call_api that checks
            errors too.
        """
        req = self.__perform_request(url, type, params)
        if req.status_code != requests.codes.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise Exception(msg)
        return req

    def call_api(self, *args, **kargs):
        """
            exposes any api entry
            useful when working with new API calls that are not yet implemented by Droplet class
        """
        return self.__call_api(*args, **kargs)
