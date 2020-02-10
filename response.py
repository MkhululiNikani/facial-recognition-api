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
        return json.dumps(response), 201

    def ok(self, data):
        response = {
            "data": data,
            "metadata": self.metadata
                    
        }
        return json.dumps(response), 200


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
        return json.dumps(error), 400

    def unauthorized(self, msg):
        error = {
            "error": {
                "status_code": "401",
                "type": "Unauthorized",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error), 401

    def request_failed(self, msg):
        error = {
            "error": {
                "status_code": "402",
                "type": "Request Failed",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error), 402

    def forbidden(self, msg):
        error = {
            "error": {
                "status_code": "403",
                "type": "Forbidden",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error), 403

    def not_found(self, msg):
        error = {
            "error": {
                "status_code": "404",
                "type": "Not Found",
                "message": msg
            },
            "metadata": self.metadata
        }
        return json.dumps(error), 404

    # Initialize metadata
    def set_metadata(self):
        self.metadata = {
            "description":"Facial Recognition API",
            "version": "1.0",
            "license": "Apache 2.0",
            "author": {
                "name": "Mkhululi Nikani",
                "email": "hello@mkhululi.net"
            }
        }