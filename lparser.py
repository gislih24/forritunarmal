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

    # One function for each of these:
    # - Statements (start_symbol)
    # - Statement
    # - Expr
    # - Term
    # - Factor
    # I *think* they should be here:
    def statements(self):
        pass

    def statement(self):
        pass

    def expr(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def error(self):
        raise Exception("Syntax error")
