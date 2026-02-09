class LToken:
    ID = 1
    ASSIGN = 2
    SEMICOL = 3
    INT = 4
    PLUS = 5
    MINUS = 6
    MULT = 7
    LPAREN = 8
    RPAREN = 9
    PRINT = 10
    END = 11
    ERROR = 12

    _NAMES: dict[int, str] = {
        ID: "ID",
        ASSIGN: "ASSIGN",
        SEMICOL: "SEMICOL",
        INT: "INT",
        PLUS: "PLUS",
        MINUS: "MINUS",
        MULT: "MULT",
        LPAREN: "LPAREN",
        RPAREN: "RPAREN",
        PRINT: "PRINT",
        END: "END",
        ERROR: "ERROR",
    }

    def __init__(self, lexeme: str = "", token_code: int = 12) -> None:
        self.lexeme: str = lexeme
        self.token_code = int(token_code)

    @property
    def name(self) -> str:
        return self._NAMES.get(
            self.token_code, f"ERROR:UNKNOWN({self.token_code})"
        )

    def __repr__(self) -> str:
        return f"LToken({self.name}, {self.lexeme})"
