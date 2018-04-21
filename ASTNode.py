from enum import Enum

class ASTNode:

    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.leftChild = None
        self.rightChild = None
        self.stmt_list = []

    def pprint(self):
        print('Node: TYPE: %s VALUE: %s' % (self.node_type, self.value))

    # def setOperator(self, operator):
    #     self.operator = operator

    # def getOperator(self):
    #     return self.operator

    # def setVar(name, var_type):
    #     self.name = name;
    #     self.var_type = var_type

    # def setRightChild(self, child):
    #     self.rightChild = child

    # def setLeftChild(self, child):
    #     self.leftChild = child

    # def getRightChild(self):
    #     return self.rightChild

    # def getLeftChild(self):
    #     return self.leftChild
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



        
