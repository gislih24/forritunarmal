from ltoken import LToken
from llexer import LLexer


# The parser takes the tokens from the lexer and turns it into intermediate
# code.
class LParser:
    def __init__(self, lexer: LLexer) -> None:
        self.lexer: LLexer = lexer
        self.curr_token: LToken = LToken()
        self.ret_str = ""

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

    # statements() -> statement() LToken.SEMICOL statements() | LToken.END
    def statements(self):
        # Statements -> Statement ; Statements | end
        if self.curr_token.token_code == LToken.END:
            return
        elif self.curr_token.token_code in (LToken.ID, LToken.PRINT):
            # Parse a single statement, then expect ';' and continue.
            self.statement()
            if self.curr_token.token_code != LToken.SEMICOL:
                self.error()
            # consume ';'
            self.next_token()
            self.statements()
        else:
            self.error()
        print(self.ret_str)

    # statement() -> LToken.ID LToken.ASSIGN expr() | LToken.PRINT LToken.ID
    def statement(self):
        # Statement -> id = Expr | print id
        if self.curr_token.token_code == LToken.PRINT:
            # consume 'print'
            self.next_token()
            if self.curr_token.token_code != LToken.ID:
                self.error()
            self.ret_str += f"PUSH {self.curr_token.lexeme}\n"
            self.ret_str += "PRINT\n"
            # consume identifier
            self.next_token()
            return
        elif self.curr_token.token_code == LToken.ID:
            # assignment: id = Expr
            var_name = self.curr_token.lexeme
            # push the variable first so it's beneath the value on the stack
            self.ret_str += f"PUSH {var_name}\n"
            # consume 'id'
            self.next_token()
            # expect '='
            if self.curr_token.token_code != LToken.ASSIGN:
                self.error()
            # consume '='
            self.next_token()
            # parse the expression (produces the value on top of stack)
            self.expr()
            # perform assignment: pop value, then variable
            self.ret_str += "ASSIGN\n"
            return
        else:
            self.error()

    # expr() -> term() | term() LToken.PLUS expr() | term() LToken.MINUS expr()
    def expr(self):
        # Expr -> Term | Term + Expr | Term – Expr
        # Minimal implementation: just a Term for now
        self.term()
        while self.curr_token.token_code in (LToken.PLUS, LToken.MINUS):
            op = self.curr_token.token_code
            self.next_token()  # consume '+' or '-'
            self.term()
            self.ret_str += "ADD\n" if op == LToken.PLUS else "SUB\n"

    # term() -> factor() | factor() LToken.MULT term()
    def term(self):
        # Term -> Factor | Factor * Term
        self.factor()
        if self.curr_token.token_code == LToken.MULT:
            self.next_token()
            self.term()
            self.ret_str += "MULT\n"

    # factor() -> LToken.INT | LToken.ID | LToken.RPAREN expr() LToken.LPAREN
    def factor(self):
        if self.curr_token.token_code == LToken.LPAREN:
            # consume '('
            self.next_token()

            # parse expression
            self.expr()

            # require and consume ')'
            if self.curr_token.token_code != LToken.RPAREN:
                self.error()
            self.next_token()
            return
        # int
        if self.curr_token.token_code == LToken.INT:
            self.ret_str += f"PUSH {self.curr_token.lexeme}\n"
            self.next_token()
            return

        # id
        if self.curr_token.token_code == LToken.ID:
            self.ret_str += f"PUSH {self.curr_token.lexeme}\n"
            self.next_token()
            return
        self.error()

    @staticmethod
    def error():
        raise Exception("Syntax error")
