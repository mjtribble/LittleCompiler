class ASTNode:
    
    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.leftChild = None
        self.rightChild = None
        
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
        
            
        