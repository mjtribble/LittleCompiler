from ASTNode import ASTNode, node_enum 

# This class will traverse the AST Trees and create IR code objects for each node. 
# It will them combine all the code objects and print the resulting IR Code. 
class IRGenerate:
    
    global temp_number
    temp_number = -1
    
    global code_list
    code_list = None
    
    #created a new global to hold the objects in the order they are created
    global code_objects
    code_objects = []
    
    global tiny_list
    tiny_list = []
    
    def __init__(self, asslist_node, symbolTable):
        self.asslist_node = asslist_node
        self.symbolTable = symbolTable
        self.addGlobalVariables()
        self.getInstructions()
    
    def addGlobalVariables(self):
        tiny_list.append(";tiny code")
        for var in self.symbolTable['GLOBAL']:
            if self.symbolTable['GLOBAL'][var][0] == "STRING":
                tiny_code = 'str %s %s'% (var, self.symbolTable['GLOBAL'][var][1])
                tiny_list.append(tiny_code)
            else:
                tiny_code = 'var %s'% (var)
                tiny_list.append(tiny_code)
            
    def getInstructions(self):
        ast_list = self.asslist_node.node_list
        code_list = [] # this will hold the code object. 
        for treeTup in ast_list:
            code_list.append(self.postOrder(treeTup[1])) # because it is a tuple object we have to index to get the actual tree
        
    def postOrder(self, root):
        if root != None:
            left_obj = self.postOrder(root.leftChild)
            right_obj = self.postOrder(root.rightChild)
            
            tempLoc = ""
            tempType = ""
            current_code = []
            
            # if the root is a VARREF node and it does not have a type, it's a const. 
            # Create a temp, determine the type, store code in IRnode.
            if root.node_type == node_enum(3).name and root.val_type == "":
                tempLoc = self.getTemp() #gets a new temp value
                tempType = ""
                # determine if the const is an int or a float to get the correct instruction
                tempType = self.is_number(root.value)
                # get the correct instruction depending on the type
                op = self.returnOperator("STORE", tempType)
                node = IRNode(op, root.value, tempType, tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
            
            # if the root is a VARREF variable, store its value and type 
            # do we not create an ir node yet??
            elif root.node_type == node_enum(3).name:
                tempLoc = root.value
                tempType = root.val_type
            
            # **** Is there a reason we aren't storing the type here?
            # if the root is a READ node, create read code
            elif root.node_type == node_enum(7).name:
                tempLoc = root.value
                tempType = root.val_type
                #get the correct instruction depending on the type
                op = self.returnOperator("READ", tempType)
                node = IRNode(op, tempLoc, "", tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
            
            # if the root is an assignment statement, store the result from the right child
            # into the variable of the left child
            elif root.node_type == node_enum(4).name:
                tempLoc = root.leftChild.value
                tempType = left_obj.resType
                #get the correct instruction depending on the type
                op = self.returnOperator("STORE", tempType)
                node = IRNode(op, right_obj.resultLoc, "", tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
            
            # if the root is an ADDOP, add/subtract the memory locations together 
            # and store in a new temp
            elif root.node_type == node_enum(1).name:
                tempLoc = self.getTemp()
                tempType = left_obj.resType
                #get the correct instruction depending on the type
                op = self.returnOperator("ADD", tempType)
                node = IRNode(op, left_obj.resultLoc, right_obj.resultLoc, tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
            
            # if the root is a MULOP, multiply/divide the child memory locations together
            # and store in a new temp
            elif root.node_type == node_enum(2).name:
                tempLoc = self.getTemp()
                tempType = root.rightChild.val_type
                #get the correct instruction depending on the type
                op = self.returnOperator("MULT", tempType)
                node = IRNode(op, left_obj.resultLoc, right_obj.resultLoc, tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
                
            elif root.node_type == node_enum(8).name:
                tempLoc = root.value
                tempType = root.val_type
                op = self.returnOperator("WRITE", tempType)
                node = IRNode(op, "", "", tempLoc)
                tiny_list.append(node.operator_map[op](node))
                current_code.append(node)
                
            elif root.node_type == node_enum(10).name:
                node = IRNode("LABEL", '', '', root.value)
                tiny_list.append(node.operator_map["LABEL"](node))
                current_code.append(node)
                # print("Write node contents: " + root.val_type + " " + root.value)
            
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
        
    def getTinyList(self):
        return tiny_list

# This class will hold the information about each operation as we traverse the tree,
# just like the exercise that we did in class
class IRNode:
        
    def __init__(self, operation, op1, op2, result):
        self.operation = operation   #ADDI, SUBI, MULTI, DIVI, STORE, READ, WRITE
        self.result = result
        self.op1 = op1
        self.op2 = op2

    def printIR(self):
        if(self):
            print('IRNode: %s %s %s %s' % (self.operation, self.op1, self.op2, self.result))
        else:
            print("IR node is empty")
            
    def changeString(self, string):
        if string != "":
            if string[0] == "T":
                string = "r" + str(string[1:])
                return string
            else:
                return string
        else: 
            return string
    
    # function to map IR operators to tinycode instructions        
    def f(self, x):
        return {
            'READI': 'readi',
            'READF': 'readf',
            'WRITEI': 'writei',
            'WRITEF': 'writef',
            'WRITES': 'writes',
            'ADDI': 'addi',
            'ADDF': 'addf',
            'SUBI': 'subi',
            'SUBF': 'subf',
            'MULTI': 'muli',
            'MULTF': 'mulf',
            'DIVI': 'divi',
            'DIVF': 'divf',
            'LABEL': 'label',
        }[x]
   
   # functions below take IR code and return a string of correct tinycode instructions 
    def storei(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        tiny_code = 'move %s %s'% (self.op1, self.result)
        return tiny_code
     
    def storef(self):   
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        tiny_code = 'move %s %s'% (self.op1, self.result)
        return tiny_code
    
    def readi(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'sys %s %s'% (op, self.result)
        return tiny_code
    
    def readf(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'sys %s %s'% (op, self.result)
        return tiny_code
    
    def writei(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'sys %s %s'% (op, self.result)
        return tiny_code
    
    def writef(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'sys %s %s'% (op, self.result)
        return tiny_code
    
    def writes(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'sys %s %s'% (op, self.result)
        return tiny_code
    
    def addi(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def addf(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def subi(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def subf(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def muli(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def mulf(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def divi(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
    
    def divf(self):
        self.op1 = self.changeString(self.op1)
        self.op2 = self.changeString(self.op2)
        self.result = self.changeString(self.result)
        op = self.f(self.operation)
        tiny_code = 'move %s %s\n%s %s %s'% (self.op1, self.result, op, self.op2, self.result)
        return tiny_code
        
    def label(self):
        tiny_code = 'label %s' % (self.result)
        return tiny_code
    
    operator_map = {"STOREI": storei, 
        "STOREF": storef, 
        "READI": readi, 
        "READF": readf, 
        "WRITEI": writei, 
        "WRITEF": writef, 
        "WRITES": writes, 
        "ADDI": addi, 
        "ADDF": addf, 
        "SUBI": subi, 
        "SUBF": subf, 
        "MULTI": muli, 
        "MULTF": mulf, 
        "DIVI": divi, 
        "DIVF": divf, 
        'LABEL': label

    } 
        
# This class will hold the structure of 3 address code for the IR representation
class CodeObject:

    # Initializes a 3Address code list object, will be created at parent nodes(+ = *)
    # @param = codelist = send in all the code from the left hand side's children, then the right hand side.
    def __init__(self, codelist, resultLoc, resType):
        self.ir_nodes = []    # this will hold IR nodes containing the 3AC code
        self.resultLoc = resultLoc  # this will hold the Temp or variable containing the result of the expression.
        self.resType = resType            # int or float
        self.addCode(codelist)
        # self.printCO()

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


    