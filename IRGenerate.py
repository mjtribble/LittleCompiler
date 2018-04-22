from ASTNode import ASTNode, node_enum 

# This class will traverse the AST Trees and create IR code objects for each node. 
# It will them combine all the code objects and print the resulting IR Code. 
class IRGenerate:
    
    global temp_number
    temp_number = 0
    
    global code_list
    code_list = None
    
    #created a new global to hold the objects in the order they are created
    global code_objects
    code_objects = []
    
    def __init__(self, asslist_node, symbolTable):
        self.asslist_node = asslist_node
        self.symbolTable = symbolTable
        self.getInstructions()
            
    def getInstructions(self):
        ast_list = self.asslist_node.node_list
        code_list = [] # this will hold the code object. 
        for treeTup in ast_list:
            code_list.append(self.postOrder(treeTup[1])) # because it is a tuple object we have to index to get the actual tree
        
    def postOrder(self, root):
        # code_objects = []
        if root != None:
            # print("ENTER root")
            # root.pprint()
            left_obj = self.postOrder(root.leftChild)
            # print("LEFT_OBJ: ")
            # print(left_obj)
            right_obj = self.postOrder(root.rightChild)
            # print("RIGHT_OBJ: ")
            # print(right_obj)
            
            
            tempLoc = ""
            tempType = ""
            current_code = []
            
            # if the root has a type if not, it's a const. and create a temp to store.
            if root.node_type == node_enum(3).name and root.val_type == "":
                tempLoc = self.getTemp() #gets a new temp value
                tempType = ""
                #determine if the const is an int or a float to get the correct instruction
                tempType = self.is_number(root.value)
                #get the correct instruction depending on the type
                op = self.returnOperator("STORE", tempType)
                current_code.append(IRNode(op, root.value, "", tempLoc))
            
            # if the root is a VARREF, store its value and type 
            elif root.node_type == node_enum(3).name:
                tempLoc = root.value
                tempType = root.val_type
                
            # if the root is a READ node, create read code
            elif root.node_type == node_enum(7).name:
                tempLoc = root.value
                tempType = root.val_type
                #get the correct instruction depending on the type
                op = self.returnOperator("READ", tempType)
                current_code.append(IRNode(op, tempLoc, "", tempLoc))
            
            # if the root is an assignment statement, store the result from the right child
            # into the variable of the left child
            elif root.node_type == node_enum(4).name:
                tempLoc = root.leftChild.value
                tempType = left_obj.resType
                #get the correct instruction depending on the type
                op = self.returnOperator("STORE", tempType)
                current_code.append(IRNode(op, right_obj.resultLoc, "", tempLoc))
            
            # if the root is an ADDOP, add/subtract the memory locations together 
            # and store in a new temp
            elif root.node_type == node_enum(1).name:
                tempLoc = self.getTemp()
                tempType = left_obj.resType
                #get the correct instruction depending on the type
                op = self.returnOperator("ADD", tempType)
                current_code.append(IRNode(op, left_obj.resultLoc, right_obj.resultLoc, tempLoc))
            
            # if the root is a MULOP, multiply/divide the child memory locations together
            # and store in a new temp
            elif root.node_type == node_enum(2).name:
                tempLoc = self.getTemp()
                tempType = root.rightChild.val_type
                #get the correct instruction depending on the type
                op = self.returnOperator("MULT", tempType)
                current_code.append(IRNode(op, left_obj.resultLoc, right_obj.resultLoc, tempLoc))
            
            # I commented this out because it ended up storing the instructions in the incorrect order
            # if root.leftChild:
            #     for code in left_obj.getCode():
            #         current_code.append(code)
            # if root.rightChild:
            #     for code in right_obj.getCode():
            #         current_code.append(code)
            
            # adding the code objects to the new list I created
            co = CodeObject(current_code, tempLoc, tempType)
            if co is not None:
                code_objects.append(co)
            return co
            
        # print("ROOT is None, return")
    
    # Annoying method that return the correct instruction based on the type that is being operated on
    def returnOperator(self, op, op_type):
        if op_type == "INT":
            if op == "ADD":
                return "ADDI"
            elif op == "SUB":
                return "SUBI"
            elif op == "MULT":
                return "MULTI"
            elif op == "DIV":
                return "DIVI"
            elif op == "READ":
                return "READI"
            elif op == "WRITE":
                return "WRITEI"
            elif op == "STORE":
                return "STOREI"
        elif op_type == "FLOAT":
            if op == "ADD":
                return "ADDF"
            elif op == "SUB":
                return "SUBF"
            elif op == "MUL":
                return "MULTF"
            elif op == "DIV":
                return "DIVF"
            elif op == "READ":
                return "READF"
            elif op == "WRITE":
                return "WRITEF"
            elif op == "STORE":
                return "STOREF"
        else:
            # the WRITE command is the only one that handles strings
            return "WRITES"
            
    def getTemp(self):
        global temp_number
        temp_number += 1
        return "T" + str(temp_number)
        
    # method to return the code_objects list to the driver    
    def getCodeObjects(self):
        return code_objects
        
    # method to test for a number and if it is an int or a float   
    def is_number(self, s):
        try:
            int(s) 
            return "INT"
        except ValueError:
            return "FLOAT"
        return False    

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
        self.addCode(codelist)
        self.printCO()

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


    