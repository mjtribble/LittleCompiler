from ASTNode import ASTNode 

# This class will traverse the AST Trees and create IR code objects for each node. 
# It will them combine all the code objects and print the resulting IR Code. 
class IRGenerate:
    
    global temp_number
    temp_number = 1
    
    def __init__(self, asslist_node, symbolTable, ast_stack):
        self.asslist_node = asslist_node
        self.symbolTable = symbolTable
        self.ast_stack = ast_stack
        
    def createRecord(self, record_type):
        temp = temp_number
        record_type = record_type
        record = IRRecord(temp_number, record_type)
        temp_number += 1
        
    def postorderTraversal(self):
        print("Traversing Stack in IR: ")
        print(self.ast_stack.size())
        self.ast_stack.pretty()
            
#     private void postOrder(Node localRoot)
# 	{
# 		if(localRoot != null)
# 		{
# 			postOrder(localRoot.leftChild);
# 			postOrder(localRoot.rightChild);
# 			System.out.print(localRoot.freq + " ");
# 		}
# 	}
   
    
    # def postorderTraversal(self, root):
    #     solution = []
    #     self.postorderTraversalRec(root, solution)
    #     return solution
    
    # def postorderTraversalRec(self, root, solution):
    #     if root == None:
    #         return
    #     self.postorderTraversalRec(root.left, solution)
    #     self.postorderTraversalRec(root.right, solution)
    #     solution.append(root.val)

# This class will hold the information about each operation as we traverse the tree,
# just like the exercise that we did in class
class IRRecord:
    
    def __init__(self, temp_number, record_type, code_object):
        self.code_object = code_object
        self.temp_number = temp_number
        self.record_type = record_type
        
    