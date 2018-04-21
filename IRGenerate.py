from ASTNode import ASTNode

# This class will traverse the AST Trees and create IR code objects for each node.
# It will them combine all the code objects and print the resulting IR Code.
class IRGenerate:

    def __init__(self, asslist_node, symbolTable):
        self.asslist_node = asslist_node
        self.symbolTable = symbolTable

    def createRecord():
        pass

    def postOrderTraversal(ast_stack):
        pass

    #this is where the ascii logic should live
    #the node will be a VARREF and we need to see if its value is an int or a string
    def getRecordType(node):
        pass

    # this function will use postorder traversal to replace leaf node variables with ASSEXP nodes or READ nodes.
    def completeTree(self, node):
        pass
