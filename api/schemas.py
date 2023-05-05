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
            {"name" : "Account",
             "description" : "User operations"
            },
            {"name" : "Quiz",
             "description" : "Operations for quiz app"
            },
            {"name" : "Notes",
             "description" : "Operations for notes app"
            },
            {"name" : "Tasks",
             "description" : "Operations for tasks app"
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
            },
            '400': {'description': 'Error: Bad Request'}
                }

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
            },
            '400': {'description': 'Error: Bad Request'}
            }
    
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
            customoperation['summary'] = "Return user's notes"
        elif method == 'POST':
            customoperation['summary'] = "Add a note"
        elif method == 'DELETE':
            customoperation['summary'] = "Delete an existing note"
        elif method == 'PUT':
            customoperation['summary'] = "Update an existing note"
        return customoperation

    def get_tags(self, path, method):
        return ["Notes"]
    
    def get_filter_parameters(self, path, method):
        if method == 'GET':
            return [
            {
                "name": "id",
                "in": "query",
                "description": "Optional query parameter {?id} used to return a specific note by its ID.",
                "required": False,
                "schema": {
                "type": "integer"
                }
            }
            ]
        else:
            return super(NoteSchema, self).get_filter_parameters(path, method)

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
        customresponse = super(NoteSchema, self).get_responses(path, method)
        if method == 'POST':
            return {
                '200': {
                    'description': "Note added"
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'Request body Error!'
                }
        }
        elif method == 'GET':
            customresponse["401"] = {
                    'description': "Not authorized!"
                }
            return customresponse
        elif method == 'DELETE':
            return {
                '200': {
                    'description': 'Note deleted'
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'ID Error!'
                }
            } 
        elif method == 'PUT':
            return {
                '200': {
                    'description': 'Note updated'
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'Request body Error!'
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
            customoperation['summary'] = "Return user's tasks"
        elif method == 'POST':
            customoperation['summary'] = "Add a task"
        elif method == 'DELETE':
            customoperation['summary'] = "Delete an existing task"
        elif method == 'PUT':
            customoperation['summary'] = "Update an existing task"
        return customoperation

    def get_tags(self, path, method):
        return ["Tasks"]
    
    def get_filter_parameters(self, path, method):
        if method == "GET":
            return [
            {
                "name": "id",
                "in": "query",
                "description": "Optional query parameter {?id} used to return a specific task by its ID.",
                "required": False,
                "schema": {
                "type": "integer"
                }
            }
            ]
        else:
            return super(TaskSchema, self).get_filter_parameters(path, method)

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
        customresponse = super(TaskSchema, self).get_responses(path, method)
        if method == 'POST':
            return {
                '200': {
                    'description': "Task added"
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'Request body Error!'
                }
        }
        elif method == 'GET':
            customresponse["401"] = {
                    'description': "Not authorized!"
                }
            return customresponse
        elif method == 'DELETE':
            return {
                '200': {
                    'description': 'Task deleted'
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'ID Error!'
                }
            } 
        elif method == 'PUT':
            return {
                '200': {
                    'description': 'Task updated'
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'Request body Error!'
                }
            }
        else:
            return super(TaskSchema, self).get_responses(path, method)
        
class QuizSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(QuizSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        if method == 'GET':
            customoperation['summary'] = "Return user's quizzes"
        elif method == 'POST':
            customoperation['summary'] = "Create a quiz"
        elif method == 'DELETE':
            customoperation['summary'] = "Delete an existing quiz"
        return customoperation

    def get_tags(self, path, method):
        return ["Quiz"]
    
    def get_request_body(self, path, method):
        if method == 'POST':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "name": {"type": "string"},
                                                        "questions": {
                                                            "type": "array",
                                                            "items": { 
                                                               "properties": {
                                                                "question": {"type": "string"},
                                                                "answers": {
                                                                    "type": "array",
                                                                    "items": {  
                                                                        "answer": {"type": "string"},}},
                                                                "correct_answer" :{"type": "string"}}
                                                                    }}},}}},
                "required" : True}
        elif method == 'DELETE':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "string"
                                                        }},}}},
                "required" : True}
                                             
    def get_responses(self, path, method):
        customresponse = super(QuizSchema, self).get_responses(path, method)
        if method == 'POST':
            return {
                '200': {
                    'description': "Quiz added"
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'Request body Error!'
                }
        }
        elif method == 'GET':
            customresponse["401"] = {
                    'description': "Not authorized!"
                }
            return customresponse
        elif method == 'DELETE':
            return {
                '200': {
                    'description': 'Quiz deleted'
                },
                '401': {
                    'description': 'Not authorized!'
                },
                '400': {
                    'description': 'ID Error!'
                }
            } 
        else:
            return super(QuizSchema, self).get_responses(path, method)
        
class QuizDetailsSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(QuizDetailsSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
        if method == 'GET':
            customoperation['summary'] = "Return a quiz's details"
        return customoperation

    def get_tags(self, path, method):
        return ["Quiz"]
                                   
    def get_responses(self, path, method):
        if method == 'GET':
            return {
                    "200": { 'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "name": {"type": "string"},
                                                        "id": {"type": "string"},
                                                        "questions": {
                                                            "type": "array",
                                                            "items": { 
                                                               "properties": {
                                                                "question": {"type": "string"},
                                                                "answers": {
                                                                    "type": "array",
                                                                    "items": {
                                                                        "properties": {
                                                                            "answer": {"type": "string"},
                                                                            "correct": {"type": "boolean"}}}}}}},
                                                        "results": {
                                                            "type": "array",
                                                            "items": { 
                                                               "properties": {
                                                                "taker_name": {"type": "string"},
                                                                "score": {"type": "integer"},
                                                                "date": {"type": "string"}}}}},}}},
                "required" : True}}
        else:
            return super(QuizDetailsSchema, self).get_responses(path, method)
        
class QuizPageSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(QuizPageSchema, self).get_operation(path, method)
        if method == 'GET':
            customoperation['summary'] = "Return a quiz's questions and answers"
        elif method == 'POST':
            customoperation['summary'] = "Submit a quiz answers"
        return customoperation

    def get_tags(self, path, method):
        return ["Quiz"]

    def get_request_body(self, path, method):
        if method == 'POST':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "taker_name": {"type": "string"},
                                                        "answers": {
                                                            "type": "array",
                                                            "items": { 
                                                                "answer": {"type": "string"}
                                                               }}},}}},
                "required" : True}
                                    
    def get_responses(self, path, method):
        if method == 'GET':
            return {
                    "200": { 'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "name": {"type": "string"},
                                                        "id": {"type": "string"},
                                                        "QA": {
                                                            "type": "array",
                                                            "items": { 
                                                               "properties": {
                                                                "question": {"type": "string"},
                                                                "answers": {
                                                                    "type": "array",
                                                                    "items": {
                                                                            "answer": {"type": "string"}}}}}},
                                                        },}}},
                "required" : True}}
        elif method == 'POST':
            return {
                    "200": { 'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "score": {"type": "integer"},
                                                        },}}},
                "required" : True}}
        else:
            return super(QuizPageSchema, self).get_responses(path, method)