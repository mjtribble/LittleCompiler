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
# Nodes have a node type, a value( =:, *, a, 1 etc), and a value type (int/float) if relevant.
class ASTNode:

    def __init__(self, node_type, value, val_type = ""):
        self.node_type = node_type
        self.value = value
        self.val_type = val_type
        self.leftChild = None
        self.rightChild = None
        self.code_object = None

    def pprint(self):
        if self.node_type == node_enum(5).name:
            print('; Node: TYPE: %s VALUE: list' % (self.node_type))
        else:
            print('; Node: TYPE: %s VALUE: %s %s' % (self.node_type, self.val_type, self.value))
        # print('Code Object: %s' % self.code_object)

    def setRightChild(self, child):
        self.rightChild = child

    def setLeftChild(self, child):
        self.leftChild = child

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

#  This is a special node that holds all assignment statment ast trees.
#  It is of type STMTLST
class AssignmentStmtList:

    def __init__(self ):
        self.node_type = node_enum(5).name
        self.node_list = []
        self.add("PLACEHOLDER", ASTNode(node_enum(6).name, ""))

    # variable is the left hand side of the statment,
    # will be used to find a variables that may need in larger expressions.
    def add(self, var, node):
        # print("Added " + var + " to the statement list")
        self.node_list.append((var, node))

    def remove(self):
        self.node_list.pop()

    def assPrint(self):
        print("Available Assignment Variables:")
        for node in self.node_list:
            print("var = " + node[0])

    # This will find a variable and return the assignment tree root node or None if it doesn't exist
    def findVariable(self, var):
        # this returns the tuple in list form [(var, node)] if found or an empty list if not.
        stmt = [item for item in self.node_list if item[0] == var]
        if stmt:
            # this pulls the node out of the list->tuple obj
            node = stmt[0][1]
            # self.assPrint()
            # print(stmt[0][0] +" is being removed from the statement list")
            # print(stmt[0])

            # this removes the smt from the list since we've already used it
            self.node_list.remove(stmt[0])
            # self.assPrint()
            # print("Find Variable is returning: ")
            # print(node)
            return node
        else:
            # print("Find Variable is returning None ")
            return None
