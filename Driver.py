import sys
from antlr4 import *
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from MyListener import MyListener
from IRGenerate import IRGenerate


def main(argv):
    input = FileStream(argv[1])
    lexer = LittleLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LittleParser(stream)
    tree = parser.prog()
    listener = MyListener()
    walker = ParseTreeWalker()

    # creates the symbol table, and the ast tree
    walker.walk(listener, tree)

    symbol_table = listener.getTable()
    ast_stack = listener.getStack()

    #generate IR code using the AST stack and the symbol table
    ir = IRGenerate(ast_stack, symbol_table)

   # print tiny code
    print(";Printing Tiny Code from Driver")
    for tiny in ir.getTinyList():
        print(tiny)
    print("sys halt")

if __name__ == '__main__':
    main(sys.argv)
