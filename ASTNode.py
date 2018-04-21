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

# Most nodes will contain the type of the node (see node_enum above) and a value( =:, *, a, 1 etc).
# The STMTLST node's will use the stmt_list attribute and will hold a list assexp nodes in form:
# [ (variable, node/tree), (variable, node/tree)
# This will then be used by the IR generator to connect variable values to the end of a tree
class ASTNode:

    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.leftChild = None
        self.rightChild = None

    def pprint(self):
        print('Node: TYPE: %s VALUE: %s' % (self.node_type, self.value))

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
class AssignmentStmtNode:

    def __init__(self ):
        self.node_type = node_enum.STMTLST.name
        self.node_list = []

    # variable is the left hand side of the statment,
    # will be used to find a variables that may need in larger expressions.
    def add(self, var, node):
        print("Added " + var + " to the statement list")
        self.node_list.append((var, node))

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
            self.assPrint()
            print(stmt[0][0] +" is being removed from the statement list")
            print(stmt[0])

            # this removes the smt from the list since we've already used it
            self.node_list.remove(stmt[0])
            self.assPrint()
            # print("Find Variable is returning: ")
            # print(node)
            return node
        else:
            print("Find Variable is returning None ")
            return None
