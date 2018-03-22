import sys
from antlr4 import *
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from MyListener import MyListener

def main(argv):
    input = FileStream(argv[1])
    lexer = LittleLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LittleParser(stream)
    tree = parser.prog()
    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    print(listener.getTable())


if __name__ == '__main__':
    main(sys.argv)



    #for token in stream.tokens:
    #    print("Token Type:", lexer.symbolicNames[token.type])
    #    print("Value:", token.text)
