import sys
from ltoken import LToken


class LLexer:
    def __init__(self) -> None:
        # Single-character pushback buffer (1-char lookahead).
        self.curr_char: str = ""
        self.lookahead_char: str | None = None
        self.TOKEN_SINGLE_CHARACTER: dict[str, int] = {
            ";": LToken.SEMICOL,
            "=": LToken.ASSIGN,
            "+": LToken.PLUS,
            "-": LToken.MINUS,
            "*": LToken.MULT,
            "(": LToken.LPAREN,
            ")": LToken.RPAREN,
        }

    def _read_next_char(self) -> None:
        """Read one character from stdin (or the lookahead char)."""
        if self.lookahead_char is not None:
            self.curr_char = self.lookahead_char
            self.lookahead_char = None
        else:
            self.curr_char = sys.stdin.read(1)

    def _backup_cur_char(self) -> None:
        """Save cur_char to the lookahead_char"""
        self.lookahead_char = self.curr_char

    def _read_chars_while(self, method_to_use) -> str:
        """Helper funtion that reads and appends characters to a list, so long
        as each character satisfies the given function.

        Args:
            method_to_use (Callable[[str], bool]): The string method which each
            character must satisfy (function returns True when char is passed
            to it).

        Returns:
            str: The string formed by concatenating the characters read.
        """
        lexeme_chars: list[str] = []
        lexeme_chars.append(self.curr_char)
        self._read_next_char()
        while self.curr_char != "" and method_to_use(self.curr_char):
            lexeme_chars.append(self.curr_char)
            self._read_next_char()
        # If we stopped, and the current character isn't the EOF
        if self.curr_char != "":
            # Backup cur_char since it's a character of another type
            self._backup_cur_char()

        lexeme: str = "".join(lexeme_chars)
        return lexeme

    def get_next_token(self) -> LToken:
        """_summary_

        Returns:
            LToken: _description_
        """
        lexeme: str = ""
        token_code: int = 0

        # Skip whitespace.
        self._read_next_char()
        while self.curr_char != "" and self.curr_char.isspace():
            self._read_next_char()

        # When we reach EOF: treat it as an error so the parser prints "Syntax
        # error" instead of crashing if the input ends unexpectedly.
        if self.curr_char == "":
            lexeme = ""
            token_code = LToken.ERROR

        # If it starts with [A-Za-z]+: token_code is PRINT, END, or ID
        elif self.curr_char.isalpha():
            lexeme: str = self._read_chars_while(str.isalpha)

            if lexeme == "print":
                token_code = LToken.PRINT
            elif lexeme == "end":
                token_code = LToken.END
            else:
                token_code = LToken.ID

        # If it starts with [0-9]+: token_code is INT
        elif self.curr_char.isdigit():
            lexeme: str = self._read_chars_while(str.isdigit)
            token_code = LToken.INT

        # If it's a single-character token
        elif self.curr_char in self.TOKEN_SINGLE_CHARACTER:
            lexeme = self.curr_char
            token_code = self.TOKEN_SINGLE_CHARACTER[lexeme]

        # Everything else is illegal.
        else:
            lexeme = self.curr_char
            token_code = LToken.ERROR

        self.curr_char = ""  # Reset cur_char
        return LToken(lexeme, token_code)  # Return the token
