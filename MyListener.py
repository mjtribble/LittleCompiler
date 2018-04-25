# Generated from /home/ubuntu/Little.g4 by ANTLR 4.7.1
from antlr4 import *
from LittleListener import LittleListener
from MyStack import MyStack
import collections
from ASTNode import ASTNode, node_enum, AssignmentStmtList

if __name__ is not None and "." in __name__:
    from .LittleParser import LittleParser
else:
    from LittleParser import LittleParser

# This class defines a complete listener for a parse tree produced by LittleParser.
class MyListener(LittleListener):

    # Create a dictionary to hold the symbol table
    global symbolTable
    symbolTable = collections.OrderedDict()

    # Create a stack to keep track of which scope we are in
    global stack
    stack = MyStack()

    global ast_stack
    ast_stack = MyStack()

    global statements_node
    statements_node = AssignmentStmtList()

    # Global block variable to count Block scopes
    block = 0

    # Global flag variable to indicate declaration errors
    global flag
    flag = False

    # Global list to store repeated variable names
    # Currently only using the first entry in this list
    global errorNames
    errorNames = []



    # error method to set flag to true when an error is found
    def error(self):
        global flag
        flag = True

    # getError method to return error message as string
    def getError(self, name):
        return "DECLARATION ERROR " + name

    # creates a new symbol table scope
    def enterScope(self, name):
        scope_dict = collections.OrderedDict()

        symbolTable[name] = collections.OrderedDict()
        stack.push(name)

    # pops the current scope off the stack
    def exitScope(self):
        if stack.isEmpty():
            pass
        else:
            popped_scope = stack.pop()

    def getCurrentScope(self):
        return stack.peek()

    # Return the Symbol Table created
    def getTable(self):
        return symbolTable

    def printTable(self):
        # if there is a declaration error, return only the first error
        # we should probably figure out how to exit the listener if this
        # happens
        if flag:
            print(self.getError(errorNames[0]))
        else:
            for scope, values in symbolTable.items():

                print("Symbol table " + scope)
                if values:
                    for var_name in values:
                        if values[var_name][0] == "STRING":
                            print("name " + var_name + " type " + values[var_name][0] + " value " + values[var_name][1])
                        else:
                            print("name " + var_name + " type " + values[var_name][0])

    # getScopeNum method to create numbered block names for conditionals
    def getScopeNum(self):
        global block
        self.block += 1
        name = str(self.block)
        return name

    def getStatementList(self):
        return statements_node

    def getStack(self):
        return ast_stack

    # Scope Declaration Functions
    def enterProg(self, ctx:LittleParser.ProgContext):
        self.enterScope("GLOBAL")

    # Exit a parse tree produced by LittleParser#prog.
    def exitProg(self, ctx:LittleParser.ProgContext):
        self.exitScope()


     # Enter a parse tree produced by LittleParser#func_decl.
    def enterFunc_decl(self, ctx:LittleParser.Func_declContext):
        name = ctx.getChild(2).getText()
        self.enterScope(name)
        # statements_node.add('', ASTNode(node_enum(10).name, name))


    # Exit a parse tree produced by LittleParser#func_decl.
    def exitFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#if_stmt.
    def enterIf_stmt(self, ctx:LittleParser.If_stmtContext):
        num = self.getScopeNum()
        name = "BLOCK " + num
        self.enterScope(name)
        # statements_node.add('', ASTNode(node_enum(10).name, "label" + num))
        print("Enter If Statement")
        # for child in ctx.getChildren():
        #     print(child.getText())


    # Exit a parse tree produced by LittleParser#if_stmt.
    def exitIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.exitScope()


    # Enter a parse tree produced by LittleParser#else_part.
    def enterElse_part(self, ctx:LittleParser.Else_partContext):
        if ctx.getChildCount() == 0:
            pass
        else:
            num = self.getScopeNum()
            name = "BLOCK " + num
            self.enterScope(name)
            # statements_node.add('', ASTNode(node_enum(10).name, "label" + num))

    # Exit a parse tree produced by LittleParser#else_part.
    def exitElse_part(self, ctx:LittleParser.Else_partContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#while_stmt.
    def enterWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        num = self.getScopeNum()
        name = "BLOCK " + num
        self.enterScope(name)
        # statements_node.add('', ASTNode(node_enum(10).name, "label" + num))


    # Exit a parse tree produced by LittleParser#while_stmt.
    def exitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.exitScope()

     # Enter a parse tree produced by LittleParser#var_decl.
    def enterVar_decl(self, ctx:LittleParser.Var_declContext):
        v_type = ctx.getChild(0).getText()
        name_list = ctx.getChild(1).getText().split(',')
        scope = stack.peek()
        for n in name_list:
            if n in symbolTable[scope]:
                self.error()
                errorNames.append(n)
            else:
                symbolTable[scope][n] = (v_type, '')

    # Exit a parse tree produced by LittleParser#var_decl.
    def exitVar_decl(self, ctx:LittleParser.Var_declContext):
        pass

    # Enter a parse tree produced by LittleParser#string_decl.
    def enterString_decl(self, ctx:LittleParser.String_declContext):
        v_type = ctx.getChild(0).getText()
        name = ctx.getChild(1).getText()
        val = ctx.getChild(3).getText()
        scope = stack.peek()
        symbolTable[scope][name] = (v_type, val)

    # Exit a parse tree produced by LittleParser#string_decl.
    def exitString_decl(self, ctx:LittleParser.String_declContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl.
    def enterParam_decl(self, ctx:LittleParser.Param_declContext):
        v_type = ctx.getChild(0).getText()
        name = ctx.getChild(1).getText()
        if v_type == "STRING":
            val = ctx.getChild(3).getText()
        else:
            val = ''
        scope = stack.peek()
        symbolTable[scope][name] = (v_type, val)

    # Exit a parse tree produced by LittleParser#param_decl.
    def exitParam_decl(self, ctx:LittleParser.Param_declContext):
        pass



    ############ START OF AST TREE WALKING ##########################
    # Enter a parse tree produced by LittleParser#addop.
    def enterAddop(self, ctx:LittleParser.AddopContext):

        node = ASTNode(node_enum(1).name, ctx.getChild(0).getText())
        ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#addop.
    def exitAddop(self, ctx:LittleParser.AddopContext):
        pass

    # Enter a parse tree produced by LittleParser#expr_prefix.
    def enterExpr_prefix(self, ctx:LittleParser.Expr_prefixContext):
        # If the expr_prefix has no children(is NULL) add a Null node to the stack
        if ctx.getChildCount() != 0 and ctx.getChild(0).getChildCount()==0:
            node = ASTNode(node_enum(0).name, "") #NullNode
            ast_stack.push(node)
        elif ctx.getChildCount() == 0:
            node = ASTNode(node_enum(6).name, "" ) #Placeholder node
            ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#expr_prefix.
    def exitExpr_prefix(self, ctx:LittleParser.Expr_prefixContext):

        if ast_stack.peek().node_type == node_enum(6).name: # if a placeholder node
            ast_stack.pop()
        else:
            addop_node = ast_stack.pop()
            factor_node = ast_stack.pop()
            prefix_node = ast_stack.pop()

            if prefix_node.node_type == node_enum(0).name:
                addop_node.leftChild = factor_node

            else:
                prefix_node.rightChild = factor_node
                addop_node.leftChild = prefix_node

            ast_stack.push(addop_node)

    # Enter a parse tree produced by LittleParser#factor.
    def enterFactor(self, ctx:LittleParser.FactorContext):
        if ctx.getChild(0).getChildCount() == 0:
            ast_stack.push(ASTNode(node_enum(0).name, "")) #push

    # Exit a parse tree produced by LittleParser#factor.
    def exitFactor(self, ctx:LittleParser.FactorContext):
        postfix_node = ast_stack.pop()

        factor_prefix_node = ast_stack.pop()
        if factor_prefix_node.node_type == node_enum(0).name:
            ast_stack.push(postfix_node)

        else:
            # factor_prefix_node.pprint()
            factor_prefix_node.rightChild = postfix_node
            ast_stack.push(factor_prefix_node)

        # Enter a parse tree produced by LittleParser#assign_stmt.
    def enterAssign_stmt(self, ctx:LittleParser.Assign_stmtContext):
        pass
    # Exit a parse tree produced by LittleParser#assign_stmt.
    def exitAssign_stmt(self, ctx:LittleParser.Assign_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#factor_prefix.
    def enterFactor_prefix(self, ctx:LittleParser.Factor_prefixContext):

        # If the expr_prefix has no children(is NULL) add a Null node to the stack
        if ctx.getChildCount() != 0 and ctx.getChild(0).getChildCount()==0:
            node = ASTNode(node_enum(0).name, "") #NullNode
            ast_stack.push(node)
        elif ctx.getChildCount() == 0:
            node = ASTNode(node_enum(6).name, "" ) #Placeholder node
            ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#factor_prefix.
    def exitFactor_prefix(self, ctx:LittleParser.Factor_prefixContext):
        if ast_stack.peek().node_type == node_enum(6).name: # if a placeholder node
            ast_stack.pop()
        else:
            mulop_node = ast_stack.pop()
            postfix_node = ast_stack.pop()
            fact_prefix_node = ast_stack.pop()

            if fact_prefix_node.node_type == node_enum(0).name:
                mulop_node.leftChild = postfix_node

            else:
                fact_prefix_node.rightChild = postfix_node
                mulop_node.leftChild = fact_prefix_node

            ast_stack.push(mulop_node)

    # Enter a parse tree produced by LittleParser#assign_expr.
    def enterAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        print(";Enter Assignment")
        var1 = ctx.getChild(0).getText()
        var2 = ctx.getChild(1).getText()
        var_type = ""
        currentScope = self.getCurrentScope()

        # get the type for id_node, first check if its in the current scope else get it from global scope
        if var1 in symbolTable[currentScope]:
            var_type = symbolTable[currentScope][var1][0]
        elif var1 in symbolTable['GLOBAL']:
            var_type = symbolTable['GLOBAL'][var1][0]

        # create varref node
        id_node = ASTNode(node_enum(3).name, var1, var_type)
        ast_stack.push(id_node)

        # create assexp node
        node = ASTNode(node_enum(4).name, var2)
        ast_stack.push(node)

    # Instead of pushing onto the AST_stack here,
    # we will add the ass_exp tree to the statement_list node's list of assignments statments.
    # Exit a parse tree produced by LittleParser#assign_expr.
    def exitAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        print(";Exit Assignment")

        exp_node = ast_stack.pop()
        #pop assexp node
        assexp_node = ast_stack.pop()
        #pop id node as left child
        id_node = ast_stack.pop()

        assexp_node.rightChild = exp_node
        assexp_node.leftChild = id_node

        ast_stack.push(assexp_node)
        print(";Push ASSEXP node")
        assexp_node.pprint()

        # statements_node.add(id_node.value, assexp_node)
        # statements_node.assPrint()

    # Enter a parse tree produced by LittleParser#expr.
    def enterExpr(self, ctx:LittleParser.ExprContext):
        # pass
        if ctx.getChild(0).getChildCount() == 0:
            ast_stack.push(ASTNode(node_enum(0).name, "")) #push

    # Exit a parse tree produced by LittleParser#expr.
    def exitExpr(self, ctx:LittleParser.ExprContext):

        factor_node = ast_stack.pop()

        expr_prefix_node = ast_stack.pop()
        if expr_prefix_node.node_type == node_enum(0).name:
            ast_stack.push(factor_node)

        else:
            expr_prefix_node.rightChild = factor_node

            ast_stack.push(expr_prefix_node)

    # Enter a parse tree produced by LittleParser#postfix_expr.
    def enterPostfix_expr(self, ctx:LittleParser.Postfix_exprContext):
        pass
    # Exit a parse tree produced by LittleParser#postfix_expr.
    def exitPostfix_expr(self, ctx:LittleParser.Postfix_exprContext):
        pass

    # Enter a parse tree produced by LittleParser#read_stmt.
    def enterRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        print(";Enter Read Statement")
        i = 0
        # A read node's values will be a list of tuples [(variable, type), (var, type)]
        node = ASTNode(node_enum(7).name, [], "")
        while i < ctx.getChild(2).getChildCount():
            var = ctx.getChild(2).getChild(i).getText()
            var = var.strip(",")
            var_type = ""
            currentScope = self.getCurrentScope()

            # get the type for node, first check if its in the current scope else get it from global scope
            if var in symbolTable[currentScope]:
                var_type = symbolTable[currentScope][var][0]
            elif var in symbolTable['GLOBAL']:
                var_type = symbolTable['GLOBAL'][var][0]

            if var != "":
                node.value.append( (var, var_type) )
            # statements_node.add(node.value, node)
            i+=1

        ast_stack.push(node)
        print(";Pushed READ node")
        node.pprint()

    # Exit a parse tree produced by LittleParser#read_stmt.
    def exitRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        print(";Exit Read")
        # pass

    # Enter a parse tree produced by LittleParser#write_stmt.
    def enterWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        # print("; Enter write statment")
        currentScope = self.getCurrentScope()
        node = ASTNode(node_enum(8).name, [], "")
        i = 0
        while i < ctx.getChild(2).getChildCount():
            var = ctx.getChild(2).getChild(i).getText()
            var = var.split(",")
            if len(var) > 1:
                for v in var:
                    if(v != ""):
                        if v in symbolTable[currentScope]:
                            var_type = symbolTable[currentScope][v][0]
                        elif v in symbolTable['GLOBAL']:
                            var_type = symbolTable['GLOBAL'][v][0]
                        # statements_node.add("", node)
                        node.value.append((v, var_type))
            else:
                if(var != ""):
                # get the type for node, first check if its in the current scope else get it from global scope
                    if var[0] in symbolTable[currentScope]:
                        var_type = symbolTable[currentScope][var[0]][0]
                    elif var[0] in symbolTable['GLOBAL']:
                        var_type = symbolTable['GLOBAL'][var[0]][0]

                    node.value.append( (var[0], var_type) )
                    # statements_node.add("", node)
            i+=1

        ast_stack.push(node)
        print(";Pushed WRITE node")
        node.pprint()
    # Exit a parse tree produced by LittleParser#write_stmt.
    def exitWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        pass
        # print(";Exit Write")
    # Enter a parse tree produced by LittleParser#return_stmt.
    def enterReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        # pass
        print(";enter return statement")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#return_stmt.
    def exitReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        # pass
        print(";exit return statement")

    # Enter a parse tree produced by LittleParser#primary.
    def enterPrimary(self, ctx:LittleParser.PrimaryContext):
        if ctx.getChildCount() > 1:
            pass
        else:
            var = ctx.getChild(0).getText()
            var_type = ""
            currentScope = self.getCurrentScope()

            # get the type for id_node, first check if its in the current scope else get it from global scope
            if var in symbolTable[currentScope]:
                var_type = symbolTable[currentScope][var][0]
            elif var in symbolTable['GLOBAL']:
                var_type = symbolTable['GLOBAL'][var][0]

            node = ASTNode(node_enum(3).name, var, var_type)

            # check if there is an expression assignment for the variable
            # varexpr_node = statements_node.findVariable(node.value)

            # if varexpr_node != None:  # push the ASSEXP node instead of variable
            #     ast_stack.push(varexpr_node)
            # else:           # push the variable
            ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#primary.
    def exitPrimary(self, ctx:LittleParser.PrimaryContext):
        pass

    # Enter a parse tree produced by LittleParser#mulop.
    def enterMulop(self, ctx:LittleParser.MulopContext):
        node = ASTNode(node_enum(2).name, ctx.getChild(0).getText())
        ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#mulop.
    def exitMulop(self, ctx:LittleParser.MulopContext):
        pass


    # Enter a parse tree produced by LittleParser#cond.
    def enterCond(self, ctx:LittleParser.CondContext):
        # print(";enter cond")
        # node = ASTNode(node_enum.COMPOP.name, ctx.getChild(0).getText())
        # ast_stack.push(node)
        # print(Push compop onto stack)
        # print(node.pprint())
        pass

    # Exit a parse tree produced by LittleParser#cond.
    def exitCond(self, ctx:LittleParser.CondContext):
        # print(";exitCond start")

        exp2 = ast_stack.pop()
        # print("pop exp2")
        compop = ast_stack.pop()
        # print("pop compop")
        exp1 = ast_stack.pop()
        # print("pop exp2")

        compop.rightChild = exp2
        compop.leftChild = exp1
        # print("compop.rightChild = exp2")
        # print("compop.leftChild = exp1")

        ast_stack.push(compop)
        # print("Compop pushed")
        compop.pprint()
        # pass
        # print("exit conditional")


    # Enter a parse tree produced by LittleParser#compop.
    def enterCompop(self, ctx:LittleParser.CompopContext):
        # pass
        # print(";enter compop")
        node = ASTNode(node_enum(9).name, ctx.getText())
        ast_stack.push(node)
        # print("Compop pushed")
        # node.pprint()

    # Exit a parse tree produced by LittleParser#compop.
    def exitCompop(self, ctx:LittleParser.CompopContext):
        pass
        # print(";exit compop")


       # Enter a parse tree produced by LittleParser#stmt_list.
    def enterStmt_list(self, ctx:LittleParser.Stmt_listContext):
        print(";enter Stmt_list")
        # pass

    # Exit a parse tree produced by LittleParser#stmt_list.
    def exitStmt_list(self, ctx:LittleParser.Stmt_listContext):
        print(";exit Stmt_list")
        # pass





    ################# RULES WE MIGHT NEED ########################

    def enterDecl(self, ctx:LittleParser.DeclContext):
        pass

    # Exit a parse tree produced by LittleParser#decl.
    def exitDecl(self, ctx:LittleParser.DeclContext):
        pass

    # Enter a parse tree produced by LittleParser#st.
    def enterSt(self, ctx:LittleParser.StContext):
        pass

    # Exit a parse tree produced by LittleParser#st.
    def exitSt(self, ctx:LittleParser.StContext):
        pass

    # Enter a parse tree produced by LittleParser#var_type.
    def enterVar_type(self, ctx:LittleParser.Var_typeContext):
        pass

    # Exit a parse tree produced by LittleParser#var_type.
    def exitVar_type(self, ctx:LittleParser.Var_typeContext):
        pass

    # Enter a parse tree produced by LittleParser#any_type.
    def enterAny_type(self, ctx:LittleParser.Any_typeContext):
        pass

    # Exit a parse tree produced by LittleParser#any_type.
    def exitAny_type(self, ctx:LittleParser.Any_typeContext):
        pass

    # Enter a parse tree produced by LittleParser#func_declarations.
    def enterFunc_declarations(self, ctx:LittleParser.Func_declarationsContext):
        pass

    # Exit a parse tree produced by LittleParser#func_declarations.
    def exitFunc_declarations(self, ctx:LittleParser.Func_declarationsContext):
        pass

    # Enter a parse tree produced by LittleParser#func_body.
    def enterFunc_body(self, ctx:LittleParser.Func_bodyContext):
        pass

    # Exit a parse tree produced by LittleParser#func_body.
    def exitFunc_body(self, ctx:LittleParser.Func_bodyContext):
        pass

    # Enter a parse tree produced by LittleParser#stmt.
    def enterStmt(self, ctx:LittleParser.StmtContext):
        pass

    # Exit a parse tree produced by LittleParser#stmt.
    def exitStmt(self, ctx:LittleParser.StmtContext):
        pass

    # Enter a parse tree produced by LittleParser#base_stmt.
    def enterBase_stmt(self, ctx:LittleParser.Base_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#base_stmt.
    def exitBase_stmt(self, ctx:LittleParser.Base_stmtContext):
        pass


    ################# UNNEEDED RULES #############################


    # Enter a parse tree produced by LittleParser#pgm_body.
    def enterPgm_body(self, ctx:LittleParser.Pgm_bodyContext):
        pass

    # Exit a parse tree produced by LittleParser#pgm_body.
    def exitPgm_body(self, ctx:LittleParser.Pgm_bodyContext):
        pass

    # Enter a parse tree produced by LittleParser#im.
    def enterIm(self, ctx:LittleParser.ImContext):
        pass

    # Exit a parse tree produced by LittleParser#im.
    def exitIm(self, ctx:LittleParser.ImContext):
        pass
        # print("exit ID")

    # Enter a parse tree produced by LittleParser#expr_list_tail.
    def enterExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#expr_list_tail.
    def exitExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        pass
    # Enter a parse tree produced by LittleParser#call_expr.
    def enterCall_expr(self, ctx:LittleParser.Call_exprContext):
        pass

    # Exit a parse tree produced by LittleParser#call_expr.
    def exitCall_expr(self, ctx:LittleParser.Call_exprContext):
        pass
    # Enter a parse tree produced by LittleParser#id_list.
    def enterId_list(self, ctx:LittleParser.Id_listContext):
      #  print(ctx.getText())
      pass

    # Exit a parse tree produced by LittleParser#id_list.
    def exitId_list(self, ctx:LittleParser.Id_listContext):
        pass

    # Enter a parse tree produced by LittleParser#id_tail.
    def enterId_tail(self, ctx:LittleParser.Id_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#id_tail.
    def exitId_tail(self, ctx:LittleParser.Id_tailContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl_list.
    def enterParam_decl_list(self, ctx:LittleParser.Param_decl_listContext):
        pass

    # Exit a parse tree produced by LittleParser#param_decl_list.
    def exitParam_decl_list(self, ctx:LittleParser.Param_decl_listContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl_tail.
    def enterParam_decl_tail(self, ctx:LittleParser.Param_decl_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#param_decl_tail.
    def exitParam_decl_tail(self, ctx:LittleParser.Param_decl_tailContext):
        pass

    # Enter a parse tree produced by LittleParser#expr_list.
    def enterExpr_list(self, ctx:LittleParser.Expr_listContext):
        pass

    # Exit a parse tree produced by LittleParser#expr_list.
    def exitExpr_list(self, ctx:LittleParser.Expr_listContext):
        pass
