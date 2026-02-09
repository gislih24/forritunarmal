from llexer import LLexer
from lparser import LParser

if __name__ == "__main__":
    lexer = LLexer()
    parser = LParser(lexer)
    parser.parse()
