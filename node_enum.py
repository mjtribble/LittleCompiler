from enum import Enum

class node_enum(Enum):
    NULL = 0
    ADDEXP = 1
    MULEXP = 2
    VARREF = 3
    ASSEXP = 4
    STMTLST = 5
    PLACEHOLDER = 6
    
    