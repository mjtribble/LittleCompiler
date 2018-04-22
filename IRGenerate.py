from ASTNode import ASTNode, node_enum 

# This class will traverse the AST Trees and create IR code objects for each node. 
# It will them combine all the code objects and print the resulting IR Code. 
class IRGenerate:
    
    global temp_number
    temp_number = 0
    
    global code_list
    code_list = None
    
    def __init__(self, asslist_node, symbolTable):
        self.asslist_node = asslist_node
        self.symbolTable = symbolTable
        self.getInstructions()
            
    def getInstructions(self):
        ast_list = self.asslist_node.node_list
        code_list = [] # this will hold the code object. 
        for treeTup in ast_list:
            code_list.append(self.postOrder(treeTup[1])) # because it is a tuple object we have to index to get the acctual tree

    def createRecord(self, record_type):
        temp = temp_number
        record_type = record_type
        record = IRNode(temp_number, record_type)
        temp_number += 1
        
    def postOrder(self, root):
        if root != None:
            print("ENTER root")
            root.pprint()
            left_obj = self.postOrder(root.leftChild)
            print("LEFT_OBJ: ")
            print(left_obj)
            right_obj = self.postOrder(root.rightChild)
            print("RIGHT_OBJ: ")
            print(right_obj)
            
            
            tempLoc = ""
            tempType = ""
            current_code = []
            
            # if the root has a type if not, it's a const. and create a temp to store.
            if root.node_type == node_enum(3).name and root.val_type == "":
                tempLoc = self.getTemp() #gets a new temp value
                tempType = ""
                print("Ready to append IR Node")
                current_code.append(IRNode("STORE", root.value, "", tempLoc))
            elif root.node_type == node_enum(3).name:
                tempLoc = root.value
                tempType = root.val_type

            if root.leftChild:
                for code in left_obj.getCode():
                    current_code.append(code)
            if root.rightChild:
                for code in right_obj.getCode():
                    current_code.append(code)
            
            return CodeObject(current_code, tempLoc, tempType)
            #if root has type, check if its node_type is VARREF
                # IRNode "LOAD"
        print("ROOT is None, return")
    

    def getTemp(self):
        global temp_number
        temp_number += 1
        return "T" + str(temp_number)

# This class will hold the information about each operation as we traverse the tree,
# just like the exercise that we did in class
class IRNode:

    def __init__(self, operation, op1, op2, result):
        self.operation = operation   #ADDI, SUBI, MULTI, DIVI, STORE, READ, WRITE
        self.result = result
        self.op1 = op1
        self.op2 = op2

    def printIR(self):
        print("IRNode: " + self.operation + " " + self.op1 + " " + self.op2 + " " + self.result)
        
# This class will hold the structure of 3 address code for the IR representation
class CodeObject:

    # Initializes a 3Address code list object, will be created at parent nodes(+ = *)
    # @param = codelist = send in all the code from the left hand side's children, then the right hand side.
    def __init__(self, codelist, resultLoc, resType):
        self.ir_nodes = []    # this will hold IR nodes containing the 3AC code
        self.resultLoc = resultLoc  # this will hold the Temp or variable containing the result of the expression.
        self.resType = resType            # int or float
        self.printCO()
        self.addCode(codelist)

    def printCO(self):
        print("Code Object:")
        i = 0
        while i < len(self.ir_nodes):
            self.ir_nodes[i].printIR()
            i += 1
        print("Result Location: " + self.resultLoc)
        print("Result Type: " + self.resType) 
        
    def getCode(self):
        return self.ir_nodes

    def addCode(self, codelist):
        for code in codelist:
            self.ir_nodes.append(code)

    def getResultLoc(self):
        return self.resultLoc

    def setResultLoc(self, loc):
        self.resultLoc = loc

    def getType(self):
        return self.resType

    def setResultLoc(self, tp):
        self.resType = tp


    