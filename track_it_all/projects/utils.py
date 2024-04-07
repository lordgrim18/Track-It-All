import enum

class Project_Roles(enum.Enum):
    MANAGER = 'Manager'
    DEVELOPER = 'Developer'
    TESTER = 'Tester'
    DESIGNER = 'Designer'

class Bug_Status(enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    VERIFIED = 'Verified'
    CLOSED = 'Closed'