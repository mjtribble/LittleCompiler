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
    ast_asslist = listener.getStatmentListNode()
    symbol_table = listener.getTable()

    # listener.printTable()
    ir = IRGenerate(ast_asslist, symbol_table )


if __name__ == '__main__':
    main(sys.argv)



    #for token in stream.tokens:
    #    print("Token Type:", lexer.symbolicNames[token.type])
    #    print("Value:", token.text)
