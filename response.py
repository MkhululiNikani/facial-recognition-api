# Flask has its own response but its not 
# design the way i want so I'm 
# writing my own and only call it's functions on
# return statements. 

import json

class Response:

    def __init__(self): 
        self.metadata = None
        self.set_metadata()

    # Success
    def created(self, data):
        response = {
            "data":data,
            "metadata": self.metadata
                    
        }
        return json.dumps(response)

    def ok(self, data):
        response = {
            "data": data,
            "metadata": self.metadata
                    
        }
        return json.dumps(response)


    # Errors
    def bad_request(self, msg):
        error = {
            "error": {
                "status_code": "400",
                "type": "Bad Request",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error)

    def unauthorized(self, msg):
        error = {
            "error": {
                "status_code": "401",
                "type": "Unauthorized",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error)

    def request_failed(self, msg):
        error = {
            "error": {
                "status_code": "402",
                "type": "Request Failed",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error)

    def forbidden(self, msg):
        error = {
            "error": {
                "status_code": "403",
                "type": "Forbidden",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error)

    def not_found(self, msg):
        error = {
            "error": {
                "status_code": "404",
                "type": "Not Found",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error)

    # Initialize metadata
    def set_metadata(self):
        self.metadata = {
            "description":"Facial Recognition API",
            "version": "0.0.1",
            "license": "Apache 2.0",
            "author": {
                "name": "Mkhululi Nikani",
                "email": "hello@mkhululi.net"
            }
        }