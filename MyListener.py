# Generated from /home/ubuntu/Little.g4 by ANTLR 4.7.1
from antlr4 import *
from LittleListener import LittleListener
from my_stack import MyStack
import collections
from ASTNode import ASTNode
from node_enum import node_enum




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
        # print("added " + name + " to the symbol table and the stack.")
    
    # pops the current scope off the stack    
    def exitScope(self):
        if stack.isEmpty():
            # print("Stack is empty!")
            pass
        else:
            popped_scope = stack.pop()
            # print("popped " + popped_scope + " off of the stack.")
        

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
                    # print(values)
                    # for var_name, my_tuple in values:
                    for var_name in values:
                        if values[var_name][0] == "STRING":
                            print("name " + var_name + " type " + values[var_name][0] + " value " + values[var_name][1])
                        else:
                            print("name " + var_name + " type " + values[var_name][0])

    # getScopeName method to create numbered block names for conditionals
    def getScopeName(self):
        global block
        self.block += 1
        name = "BLOCK " + str(self.block)
        return name
        
    # Scope Declaration Functions
    def enterProg(self, ctx:LittleParser.ProgContext):
        # print("entered program with MyParser!")
        self.enterScope("GLOBAL")

    # Exit a parse tree produced by LittleParser#prog.
    def exitProg(self, ctx:LittleParser.ProgContext):
        self.exitScope()
    
     # Enter a parse tree produced by LittleParser#func_decl.
    def enterFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.enterScope(ctx.getChild(2).getText())
        
    # Exit a parse tree produced by LittleParser#func_decl.
    def exitFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.exitScope()
    
    # Enter a parse tree produced by LittleParser#if_stmt.
    def enterIf_stmt(self, ctx:LittleParser.If_stmtContext):
        name = self.getScopeName()
        self.enterScope(name)
        

    # Exit a parse tree produced by LittleParser#if_stmt.
    def exitIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.exitScope()
        

    # Enter a parse tree produced by LittleParser#else_part.
    def enterElse_part(self, ctx:LittleParser.Else_partContext):
        if ctx.getChildCount() == 0:
            pass
        else:
            name = self.getScopeName()
            self.enterScope(name)

    # Exit a parse tree produced by LittleParser#else_part.
    def exitElse_part(self, ctx:LittleParser.Else_partContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#while_stmt.
    def enterWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        name = self.getScopeName()
        self.enterScope(name)

    # Exit a parse tree produced by LittleParser#while_stmt.
    def exitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.exitScope()
    
    
     # Enter a parse tree produced by LittleParser#var_decl.
    def enterVar_decl(self, ctx:LittleParser.Var_declContext):
        v_type = ctx.getChild(0).getText()
        # print("v_type = " + v_type)
        name_list = ctx.getChild(1).getText().split(',')
        # print("Top of the stack: " + stack.peek())
        # scope = filter(stack.peek(), name_list)
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
        # print("enter addop")
        # print(ctx.getText())
        
    # Exit a parse tree produced by LittleParser#addop.
    def exitAddop(self, ctx:LittleParser.AddopContext):
        pass
        # print("exit addop")
    
    # Enter a parse tree produced by LittleParser#expr_prefix.
    def enterExpr_prefix(self, ctx:LittleParser.Expr_prefixContext):
        # pass
        # print("enter expression prefix")
        if ctx.getChildCount == 0:
            node = ASTNode(node_enum(0).name, "")
            ast_stack.push(node)
        
            
    # Exit a parse tree produced by LittleParser#expr_prefix.
    def exitExpr_prefix(self, ctx:LittleParser.Expr_prefixContext):
        # if not ast_stack.isEmpty():
        while ast_stack.size() > 0:
            node = ast_stack.pop()
            print("Popped " + "type " + node.node_type + "value " + node.value)
            # addop_node = ast_stack.pop()
            # factor_node = ast_stack.pop()
            # prefix_node = ast_stack.pop()
            
            # if prefix_node.node_type is node_enum.NULL:
            #     addop_node.leftChild = factor_node
            
            # else:
            #     prefix_node.rightChild = factor_node
            #     addop_node.leftChild = prefix_node
            
            # ast_stack.push(addop_node)    
        # pass
        # print("exit expression prefix")
    # Unused parse tree methods
    
    # Enter a parse tree produced by LittleParser#factor.
    def enterFactor(self, ctx:LittleParser.FactorContext):
        node = ASTNode(node_enum(3).name, ctx.getChild(0).getText())
        ast_stack.push(node)
        
        # print("enter factor")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#factor.
    def exitFactor(self, ctx:LittleParser.FactorContext):
        pass
        # print("exit factor")
    # Enter a parse tree produced by LittleParser#pgm_body.
    def enterPgm_body(self, ctx:LittleParser.Pgm_bodyContext):
        pass

    # Exit a parse tree produced by LittleParser#pgm_body.
    def exitPgm_body(self, ctx:LittleParser.Pgm_bodyContext):
        pass

    # Enter a parse tree produced by LittleParser#im.
    def enterIm(self, ctx:LittleParser.ImContext):
        pass
        # print("enter ID")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#im.
    def exitIm(self, ctx:LittleParser.ImContext):
        pass
        # print("exit ID")

    # Enter a parse tree produced by LittleParser#decl.
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

    # Enter a parse tree produced by LittleParser#stmt_list.
    def enterStmt_list(self, ctx:LittleParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by LittleParser#stmt_list.
    def exitStmt_list(self, ctx:LittleParser.Stmt_listContext):
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

    # Enter a parse tree produced by LittleParser#assign_stmt.
    def enterAssign_stmt(self, ctx:LittleParser.Assign_stmtContext):
        pass
        # print("enter assignment statement")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#assign_stmt.
    def exitAssign_stmt(self, ctx:LittleParser.Assign_stmtContext):
        pass
        # print("exit assignment statement")

    # Enter a parse tree produced by LittleParser#assign_expr.
    def enterAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        pass
        # print("enter assignment expression")
        # for c in ctx.getChildren():
            # print(c.getText())

    # Exit a parse tree produced by LittleParser#assign_expr.
    def exitAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        pass
        # print("exit assignment expression")

    # Enter a parse tree produced by LittleParser#read_stmt.
    def enterRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        pass
        # print("enter read statement")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#read_stmt.
    def exitRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        pass
        # print("exit read statement")

    # Enter a parse tree produced by LittleParser#write_stmt.
    def enterWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        pass
        # print("enter write statement")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#write_stmt.
    def exitWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        pass
        # print("exit write statement")

    # Enter a parse tree produced by LittleParser#return_stmt.
    def enterReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        pass
        # print("enter return statement")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#return_stmt.
    def exitReturn_stmt(self, ctx:LittleParser.Return_stmtContext):
        pass
        # print("exit return statement")

    # Enter a parse tree produced by LittleParser#expr.
    def enterExpr(self, ctx:LittleParser.ExprContext):
        pass
        # print("enter expression")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#expr.
    def exitExpr(self, ctx:LittleParser.ExprContext):
        node = ast_stack.peek()
        print("exiting expression " + node.node_type + node.value)
        # pass
        # print("exit expression")

    

    

    # Enter a parse tree produced by LittleParser#factor_prefix.
    def enterFactor_prefix(self, ctx:LittleParser.Factor_prefixContext):
        pass
        # print("enter factor prefix")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#factor_prefix.
    def exitFactor_prefix(self, ctx:LittleParser.Factor_prefixContext):
        pass
        # print("exit factor prefix")

    # Enter a parse tree produced by LittleParser#postfix_expr.
    def enterPostfix_expr(self, ctx:LittleParser.Postfix_exprContext):
        pass
        # print("enter postfix expression")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#postfix_expr.
    def exitPostfix_expr(self, ctx:LittleParser.Postfix_exprContext):
        pass
        # print("exit postfix expression")

    # Enter a parse tree produced by LittleParser#call_expr.
    def enterCall_expr(self, ctx:LittleParser.Call_exprContext):
        pass

    # Exit a parse tree produced by LittleParser#call_expr.
    def exitCall_expr(self, ctx:LittleParser.Call_exprContext):
        pass


    # Enter a parse tree produced by LittleParser#expr_list.
    def enterExpr_list(self, ctx:LittleParser.Expr_listContext):
        pass
        # print("enter expression list")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#expr_list.
    def exitExpr_list(self, ctx:LittleParser.Expr_listContext):
        pass
        # print("exit expression list")


    # Enter a parse tree produced by LittleParser#expr_list_tail.
    def enterExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#expr_list_tail.
    def exitExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        pass


    # Enter a parse tree produced by LittleParser#primary.
    def enterPrimary(self, ctx:LittleParser.PrimaryContext):
        pass
        # print("enter primary")
        print(ctx.getText())

    # Exit a parse tree produced by LittleParser#primary.
    def exitPrimary(self, ctx:LittleParser.PrimaryContext):
        pass
        # print("exit primary")

    # Enter a parse tree produced by LittleParser#mulop.
    def enterMulop(self, ctx:LittleParser.MulopContext):
        pass
        # print("enter mulop")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#mulop.
    def exitMulop(self, ctx:LittleParser.MulopContext):
        pass
        # print("exit mulop")


    # Enter a parse tree produced by LittleParser#cond.
    def enterCond(self, ctx:LittleParser.CondContext):
        pass
        # print("enter conditional")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#cond.
    def exitCond(self, ctx:LittleParser.CondContext):
        pass
        # print("exit conditional")


    # Enter a parse tree produced by LittleParser#compop.
    def enterCompop(self, ctx:LittleParser.CompopContext):
        pass
        # print("enter compop")
        # print(ctx.getText())

    # Exit a parse tree produced by LittleParser#compop.
    def exitCompop(self, ctx:LittleParser.CompopContext):
        pass
        # print("exit compop")
