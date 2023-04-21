from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator

class CustomMainSchema(SchemaGenerator):
    
    def get_schema(self, request, public):
        schema = super().get_schema(request, public)
        schema['components']['securitySchemes'] = {
                'Authorization': {
                    'type': 'http',
                    'in': 'header',
                    'name': 'Authorization',
                    'description': 'Obtian a token using the login API',
                    'scheme': 'bearer'
                },}
        schema['servers'] = [{
            "url": "https://ubade.pythonanywhere.com/api"
        },]
        schema["tags"] = [
            {"name" : "Notes",
             "description" : "Operations for notes app"
            },
            {"name" : "Tasks",
             "description" : "Operations for tasks app"
            },
            {"name" : "Account",
             "description" : "User operations"
            }
        ]
        return schema

class RegisterSchema(AutoSchema):
    
    def get_operation(self, path, method):
        customoperation = super(RegisterSchema, self).get_operation(path, method)
        customoperation['summary'] = "Register a new user"
        return customoperation
    
    def get_tags(self, path, method):
        return ["Account"]
    
    def get_request_body(self, path, method):
        return {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "username": {
                                                        "type": "string"
                                                    },
                                                    "password": {
                                                        "type": "string"
                                                    }},
                                                    "required": ["username","password"]}}},
                "required" : True}
    
    def get_responses(self, path, method):
        return {
            '200': {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "username": {
                                                        "type": "string"},
                                                    "token": {
                                                        "type": "string"
                                                    }
                                                    }}}},
                'description': ""
            }}

class LoginSchema(AutoSchema):
    
    def get_operation(self, path, method):
        customoperation = super(LoginSchema, self).get_operation(path, method)
        customoperation['summary'] = "Login a registered user"
        return customoperation
    
    def get_tags(self, path, method):
        return ["Account"]
    
    def get_request_body(self, path, method):
        return {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "username": {
                                                        "type": "string"
                                                    },
                                                    "password": {
                                                        "type": "string"
                                                    }},
                                                    "required": ["username","password"]}}},
                "required" : True}
   
    def get_responses(self, path, method):
        return {
            '200': {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "expiry": {
                                                        "type": "string"
                                                    },
                                                    "token": {
                                                        "type": "string"
                                                    },
                                                    "username": {
                                                        "type": "string"
                                                    },
                                                    }}}},
                'description': ""
            }}
    
class LogoutSchema(AutoSchema):
   
    def get_operation(self, path, method):
        customoperation = super(LogoutSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        customoperation['summary'] = "Remove a user's authentication token"
        return customoperation
    
    def get_tags(self, path, method):
        return ["Account"]
   
    def get_request_body(self, path, method):
        return {'content': {}}
    
    def get_responses(self, path, method):
        return {
            '204': {}}
    
class GuestLoginSchema(AutoSchema):
    
    def get_operation(self, path, method):
        customoperation = super(GuestLoginSchema, self).get_operation(path, method)
        customoperation['summary'] = "Create and login as a guest user"
        return customoperation
    
    def get_tags(self, path, method):
        return ["Account"]
    
    def get_request_body(self, path, method):
        return {'content': {}}
    
    def get_responses(self, path, method):
        return {
            '200': {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "expiry": {
                                                        "type": "string"
                                                    },
                                                    "token": {
                                                        "type": "string"
                                                    }
                                                    }}}},
                'description': ""
            }}
    
class ConvertGuestSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(ConvertGuestSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        customoperation['summary'] = "Convert a guest user to an ordinary user"
        return customoperation
    
    def get_tags(self, path, method):
        return ["Account"]
    
    def get_request_body(self, path, method):
        return {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "username": {
                                                        "type": "string"
                                                    },
                                                    "password": {
                                                        "type": "string"
                                                    }},
                                                    "required": ["username","password"]}}},
                "required" : True}
    
    def get_responses(self, path, method):
        return {
            '200': {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "username": {
                                                        "type": "string"}
                                                    }}}},
                'description': ""
            },
            '400': {
                    'description': 'Data Error!'
                }}


class NoteSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(NoteSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        if method == 'GET':
            customoperation['summary'] = "Return all available notes"
        elif method == 'POST':
            customoperation['summary'] = "Add a note"
        elif method == 'DELETE':
            customoperation['summary'] = "Delete an existing note"
        elif method == 'PUT':
            customoperation['summary'] = "Update an existing note"
        return customoperation

    def get_tags(self, path, method):
        return ["Notes"]

    def get_request_body(self, path, method):
        if method == 'PUT':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        },
                                                        "title": {
                                                            "type": "string"
                                                        },
                                                        "body": {
                                                            "type": "string"
                                                        },
                                                        "color": {
                                                            "type": "string"
                                                        }},
                                                        "required": ["id"]}}},
                "required" : True}
        elif method == 'DELETE':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        }},
                                                        "required": ["id"]}}},
                "required" : True}
        elif method == 'POST':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "title": {
                                                            "type": "string"
                                                        },
                                                        "body": {
                                                            "type": "string"
                                                        },
                                                        "color": {
                                                            "type": "string"
                                                        }},
                                                            }}},
                "required" : True}       
                                                 
    def get_responses(self, path, method):
        if method == 'POST':
            return {
            '200': {
                'description': "Note added"
            }
        }
        elif method == 'DELETE':
            return {
                '200': {
                    'description': 'Note deleted'
                }
            } 
        elif method == 'PUT':
            return {
                '200': {
                    'description': 'Note updated'
                }
            }
        else:
            return super(NoteSchema, self).get_responses(path, method)


class TaskSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(TaskSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        if method == 'GET':
            customoperation['summary'] = "Return all available tasks"
        elif method == 'POST':
            customoperation['summary'] = "Add a task"
        elif method == 'DELETE':
            customoperation['summary'] = "Delete an existing task"
        elif method == 'PUT':
            customoperation['summary'] = "Update an existing task"
        return customoperation

    def get_tags(self, path, method):
        return ["Tasks"]

    def get_request_body(self, path, method):
        if method == 'PUT':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        },
                                                        "title": {
                                                            "type": "string"
                                                        },
                                                        "description": {
                                                            "type": "string"
                                                        },
                                                        "complete": {
                                                            "type": "boolean"
                                                        }},
                                                        "required": ["id"]}}},
                "required" : True}
        elif method == 'DELETE':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        }},
                                                        "required": ["id"]}}},
                "required" : True}
        elif method == 'POST':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "title": {
                                                            "type": "string"
                                                        },
                                                        "description": {
                                                            "type": "string"
                                                        }},
                                                            }}},
                "required" : True}       
                                                 
    def get_responses(self, path, method):
        if method == 'POST':
            return {
            '200': {
                'description': "Task added"
            }
        }
        elif method == 'DELETE':
            return {
                '200': {
                    'description': 'Task deleted'
                }
            }
        elif method == 'PUT':
            return {
                '200': {
                    'description': 'Task updated'
                }
            }
        else:
            return super(TaskSchema, self).get_responses(path, method)