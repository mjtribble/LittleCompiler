import sys
from antlr4 import *
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from MyListener import MyListener
# from LittleListener import LittleListener
from IRGenerate import IRGenerate

def main(argv):
    input = FileStream(argv[1])
    lexer = LittleLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LittleParser(stream)
    tree = parser.prog()
    # listener = LittleListener()
    listener = MyListener()
    walker = ParseTreeWalker()

    # creates the symbol table, and the ast tree
    walker.walk(listener, tree)

    # get a node containing a list of assignment statements
    ast_asslist = listener.getStatementList()
    # print("Printing AssList")
    # for item in ast_asslist.node_list:
    #     print(item[1].value)
    symbol_table = listener.getTable()
    ast_stack = listener.getStack()

    # for s in listener.get_s_list():
    #     print(";" + s)
    # print(";End of S List")
    # print("Traversing Stack in Driver: ")
    # ast_stack.pretty()

    # listener.printTable()
    # print("Printing Code Objects from Driver")
    # objects = ir.getCodeObjects()
    # for obj in objects:
    #     obj.printCO()

    ir = IRGenerate(ast_asslist, symbol_table)

    print(";Printing Tiny Code from Driver")
    for tiny in ir.getTinyList():
        print(tiny)
    print("sys halt")

if __name__ == '__main__':
    main(sys.argv)



    #for token in stream.tokens:
    #    print("Token Type:", lexer.symbolicNames[token.type])
    #    print("Value:", token.text)
