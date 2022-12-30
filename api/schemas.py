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
        return schema

class RegisterSchema(AutoSchema):
    def get_tags(self, path, method):
        return ["Account"]
    def get_responses(self, path, method):
        return {
            '200': {
                'content': {
                    "application/json": {"schema": {
                                                    "properties": {
                                                    "user": {
                                                        "type": "object",
                                                        "properties": {
                                                        "username": {
                                                        "type": "string"},
                                                        "email": {
                                                        "type": "string"}}
                                                    },
                                                    "token": {
                                                        "type": "string"
                                                    }
                                                    }}}},
                'description': ""
            }}

class LoginSchema(AutoSchema):
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
                                                    "required": ["username","password"]}}}}
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

class NoteSchema(AutoSchema):

    def get_operation(self, path, method):
        customoperation = super(NoteSchema, self).get_operation(path, method)
        customoperation['security'] = []
        customoperation['security'].append( {"Authorization" : [], })
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
                                                        "required": ["id"]}}}}
        elif method == 'DELETE':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        }},
                                                        "required": ["id"]}}}}
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
                                                            }}}}                                                
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
                                                        "required": ["id"]}}}}
        elif method == 'DELETE':
            return {
                    'content': {
                        "application/json": {"schema": {
                                                        "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        }},
                                                        "required": ["id"]}}}}
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
                                                            }}}}                                                
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