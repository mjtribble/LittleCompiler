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

    # Stack to track of which scope we are in for the symbol table
    global stack
    stack = MyStack()

    # Stack used to build the ast tree
    global ast_stack
    ast_stack = MyStack()

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

    # Pretty print for the symbol table
    def printTable(self):
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


    # Creates numbered block names for conditionals
    def getScopeNum(self):
        global block
        self.block += 1
        name = str(self.block)
        return name

    def getStack(self):
        return ast_stack

    # Scope Declaration Functions
    def enterProg(self, ctx:LittleParser.ProgContext):
        self.enterScope("GLOBAL")

    # Exit a parse tree produced by LittleParser#prog.
    def exitProg(self, ctx:LittleParser.ProgContext):
        self.exitScope()

    ############ START OF AST TREE WALKING ##########################

     # Enter a parse tree produced by LittleParser#func_decl.
    def enterFunc_decl(self, ctx:LittleParser.Func_declContext):
        name = ctx.getChild(2).getText()
        self.enterScope(name)
        ast_stack.push(ASTNode(node_enum(10).name, name))


    # Exit a parse tree produced by LittleParser#func_decl.
    def exitFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#if_stmt.
    def enterIf_stmt(self, ctx:LittleParser.If_stmtContext):
        num = self.getScopeNum()
        name = "BLOCK " + num
        self.enterScope(name)
        ast_stack.push(ASTNode(node_enum(10).name, "label" + num))


    # Exit a parse tree produced by LittleParser#if_stmt.
    def exitIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.exitScope()
        if_node = ASTNode(node_enum(13).name, [], "")
        end_node = ASTNode(node_enum(16).name, [])

        else_node = ast_stack.pop()
        sl_node = ast_stack.pop()
        comp_node = ast_stack.pop()

        if_label = ast_stack.pop()
        end_label = ASTNode(node_enum(10).name, "label" + self.getScopeNum())

        end_node.value.append(if_label)
        end_node.value.append(end_label)
        end_node.val_type = 'if'

        if_node.val_type = if_label
        if_node.value.append(comp_node)
        if_node.value.append(sl_node)

        # if not a placeholder node,
        # assign the else label to the cop_op node, add the end node to the else values
        # add else node to the end of if's value list
        if else_node.node_type != node_enum(6).name:
            eend_node = ASTNode(node_enum(16).name, [if_label, end_label])
            eend_node.val_type = 'else'
            else_label = else_node.val_type
            comp_node.val_type = else_label
            else_node.value.append(end_node)
            if_node.value.append(eend_node)
            if_node.value.append(else_node)
        else:
            comp_node.val_type = end_label

        if_node.value.append(end_node)
        ast_stack.push(if_node)

    # Enter a parse tree produced by LittleParser#else_part.
    def enterElse_part(self, ctx:LittleParser.Else_partContext):
        if ctx.getChildCount() == 0:
            node = ASTNode(node_enum(6).name, "" ) #Placeholder node
            ast_stack.push(node)
        else:
            num = self.getScopeNum()
            name = "BLOCK " + num
            self.enterScope(name)
            ast_stack.push(ASTNode(node_enum(10).name, "label" + num))

    # Exit a parse tree produced by LittleParser#else_part.
    def exitElse_part(self, ctx:LittleParser.Else_partContext):
        self.exitScope()
        if ast_stack.peek().node_type == node_enum(6).name:
            pass
        else:
            stmtList = ast_stack.pop()
            label = ast_stack.pop()
            node = ASTNode(node_enum(15).name, [stmtList], label)
            ast_stack.push(node)

    # Enter a parse tree produced by LittleParser#while_stmt.
    def enterWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        num = self.getScopeNum()
        name = "BLOCK " + num
        self.enterScope(name)
        ast_stack.push(ASTNode(node_enum(10).name, "label" + num))

    # Exit a parse tree produced by LittleParser#while_stmt.
    def exitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.exitScope()

        while_node = ASTNode(node_enum(14).name, [] )
        end_node = ASTNode(node_enum(16).name, [] )
        end_label = ASTNode(node_enum(10).name, "label" + self.getScopeNum())

        # grab nodes from the stack needed to create a WHILE node
        stmt_list = ast_stack.pop()
        comp_op = ast_stack.pop()        # add the end label to the comp-op node
        comp_op.val_type = end_label

        w_label = ast_stack.pop()

        # END node contains the while label and the endwhile label
        end_node.value.append(w_label)
        end_node.value.append(end_label)
        end_node.val_type = 'while'

        # WHILE.value = [comp_op, stmt_list, end]
        while_node.value.append(comp_op)
        while_node.value.append(stmt_list)
        while_node.value.append(end_node)
        while_node.val_type = w_label

        ast_stack.push(while_node)

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
        # print(";Enter Assignment")
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

    # Exit a parse tree produced by LittleParser#assign_expr.
    def exitAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        exp_node = ast_stack.pop()
        assexp_node = ast_stack.pop()
        id_node = ast_stack.pop()

        assexp_node.rightChild = exp_node
        assexp_node.leftChild = id_node

        ast_stack.push(assexp_node)

    # Enter a parse tree produced by LittleParser#expr.
    def enterExpr(self, ctx:LittleParser.ExprContext):
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
            i+=1

        ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#read_stmt.
    def exitRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#write_stmt.
    def enterWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
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
                        node.value.append((v, var_type))
            else:
                if(var[0] != ""):
                # get the type for node, first check if its in the current scope else get it from global scope
                    if var[0] in symbolTable[currentScope]:
                        var_type = symbolTable[currentScope][var[0]][0]
                    elif var[0] in symbolTable['GLOBAL']:
                        var_type = symbolTable['GLOBAL'][var[0]][0]

                    node.value.append( (var[0], var_type) )
                    # statements_node.add("", node)
            i+=1

        ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#write_stmt.
    def exitWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#return_stmt.
    def enterReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#return_stmt.
    def exitReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        pass

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
        pass

    # Exit a parse tree produced by LittleParser#cond.
    def exitCond(self, ctx:LittleParser.CondContext):

        exp2 = ast_stack.pop()
        compop = ast_stack.pop()
        exp1 = ast_stack.pop()

        compop.rightChild = exp2
        compop.leftChild = exp1

        ast_stack.push(compop)

    # Enter a parse tree produced by LittleParser#compop.
    def enterCompop(self, ctx:LittleParser.CompopContext):

        # The label to jump to will be added in the exit while and exit if functions as the val_type
        node = ASTNode(node_enum(9).name, ctx.getText())
        ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#compop.
    def exitCompop(self, ctx:LittleParser.CompopContext):
        pass

   # Enter a parse tree produced by LittleParser#stmt_list.
    def enterStmt_list(self, ctx:LittleParser.Stmt_listContext):

        if ctx.getChildCount() == 0:
            node = ASTNode(node_enum(6).name, [])
            ast_stack.push(node)

    # Exit a parse tree produced by LittleParser#stmt_list.
    def exitStmt_list(self, ctx:LittleParser.Stmt_listContext):

        # If node is a Placeholder
        if ast_stack.peek().node_type == node_enum(6).name:
            ast_stack.pop()
            node = ASTNode(node_enum(5).name, [])
            ast_stack.push(node)

        # add a statement to the statement list and push back on to stack
        else:
            sl = ast_stack.pop()
            stmt = ast_stack.pop()

            sl.value.insert(0, stmt)

            ast_stack.push(sl)

    ################# UNNEEDED RULES #############################

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
