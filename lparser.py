from ltoken import LToken
from llexer import LLexer


# The parser takes the tokens from the lexer and turns it into intermediate
# code.
class LParser:
    def __init__(self, lexer: LLexer) -> None:
        self.lexer: LLexer = lexer
        self.curr_token: LToken = LToken()

    # -----------------------↓Do not change↓-----------------------
    def parse(self) -> None:
        self.next_token()
        self.statements()
        print()  # Make sure the intermediate code ends with a newline

    def next_token(self) -> None:
        self.curr_token = self.lexer.get_next_token()
        if self.curr_token.token_code == LToken.ERROR:  # type: ignore
            self.error()

    # -----------------------↑Do not change↑-----------------------

    # Context-free grammar G for L is:
    #
    # Statements -> Statement ; Statements | end
    # Statement -> id = Expr | print id
    # Expr -> Term | Term + Expr | Term – Expr
    # Term -> Factor | Factor * Term
    # Factor -> int | id | ( Expr )
    #
    # Non-terminals are:
    # Statements (start symbol), Statement, Expr, Term, and Factor.
    #
    # Tokens/terminals are:
    # ; end id = print + - * int ( )
    #
    # The intermediate language consists of the following commands:
    # PUSH op : pushes the operand op onto the stack.
    # ADD : pops the two top elements from the stack, adds their values
    #       and pushes the result back onto the stack.
    # SUB : pops the two top elements from the stack, subtracts the first
    #       value retrieved from the second value,
    #       and pushes the result back onto the stack.
    # MULT : pops the two top elements from the stack, multiplies their
    #        values and pushes the result back onto the stack.
    # ASSIGN : pops the two top elements from the stack, assigns the first
    #          element (a value) to the second element (a variable).
    # PRINT : prints the value currently on top of the stack.

    def eat(self, expected: int) -> str:
        if self.curr_token.token_code != expected:
            self.error()  # Uhoh!
        lex: str = self.curr_token.lexeme  # The lexeme we wanna print
        self.next_token()  # Consume the token by advancing to the next token
        return lex  # Return the lexeme of the token we just consumed

    # statements() -> statement() LToken.SEMICOL statements()
    #               | LToken.END
    def statements(self):
        # Statements -> Statement ; Statements | end
        pass

    # statement() -> LToken.ID LToken.ASSIGN expr()
    #              | LToken.PRINT LToken.ID
    def statement(self):
        # Statement -> id = Expr | print id
        pass

    # expr() -> term()
    #         | term() LToken.PLUS expr()
    #         | term() LToken.MINUS expr()
    def expr(self):
        # Expr -> Term | Term + Expr | Term – Expr
        pass

    # term() -> factor()
    #         | factor() LToken.MULT term()
    def term(self):
        # Term -> Factor | Factor * Term
        pass

    # factor() -> LToken.INT
    #           | LToken.ID
    #           | LToken.RPAREN expr() LToken.LPAREN
    def factor(self):
        # Factor -> int | id | ( Expr )
        pass

    @staticmethod
    def error():
        raise Exception("Syntax error")
