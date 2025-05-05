from enum import Enum

class AuditStatus(str, Enum):
    """
    Enum for content audit status
    """
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected' 