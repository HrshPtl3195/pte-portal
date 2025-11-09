from enum import Enum




class Role(str, Enum):
    ADMIN = "admin"
    EVALUATOR = "evaluator"
    STUDENT = "student"




class SessionState(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"