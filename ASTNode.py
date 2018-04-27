from enum import Enum

class node_enum(Enum):
    NULL = 0
    ADDEXP = 1
    MULEXP = 2
    VARREF = 3
    ASSEXP = 4
    STMTLST = 5
    PLACEHOLDER = 6
    READ = 7
    WRITE = 8
    COMPOP = 9
    LABEL = 10
    RETURN = 11
    IF = 13
    WHILE = 14
    ELSE = 15
    END = 16
# Nodes have a node type, a value( =:, *, a, 1 etc), and a value type (int/float) if relevant.
class ASTNode:

    def __init__(self, node_type, value, val_type = ""):
        self.node_type = node_type
        self.value = value
        self.val_type = val_type
        self.leftChild = None
        self.rightChild = None
        self.code_object = None

    def __str__(self):
        str1 = ''.join(str(e) for e in self.value)
        return 'NODE: %s %s [ %s ] ' % (self.node_type, self.val_type, str1)

    def setRightChild(self, child):
        self.rightChild = child

    def setLeftChild(self, child):
        self.leftChild = child

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild
