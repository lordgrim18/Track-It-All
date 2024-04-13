import enum

class Bug_Status(enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    VERIFIED = 'Verified'
    CLOSED = 'Closed'

class Bug_Priority(enum.Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'