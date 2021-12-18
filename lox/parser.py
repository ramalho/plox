from enum import Enum
from typing import Final, Optional

import main

class TokenType(Enum):

    # Single-character tokens.
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'

    # One or two character tokens.
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literals.
    IDENTIFIER = '_IDENTIFIER_'
    STRING = '_STRING_'
    NUMBER = '_NUMBER_'

    # Keywords.
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

    EOF = '_EOF_'

    def iskeyword(self):
        # Only keyword TokenType values must be lowercase alpha strings.
        text = self.value
        return text.isalpha() and text.lower() == text

KEYWORDS = {tt.value: tt for tt in TokenType if tt.iskeyword()}


class Token:

    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int) -> None:
        self.type: Final = type
        self.lexeme: Final = lexeme
        self.literal: Final = literal
        self.line: Final = line

    def __str__(self):
        return f'{self.type} {self.lexeme} {self.literal}'


class Scanner:

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()

        if c == '(': self.add(TokenType.LEFT_PAREN)
        elif c == ')': self.add(TokenType.RIGHT_PAREN)
        elif c == '{': self.add(TokenType.LEFT_BRACE)
        elif c == '}': self.add(TokenType.RIGHT_BRACE)
        elif c == ',': self.add(TokenType.COMMA)
        elif c == '.': self.add(TokenType.DOT)
        elif c == '-': self.add(TokenType.MINUS)
        elif c == '+': self.add(TokenType.PLUS)
        elif c == ';': self.add(TokenType.SEMICOLON)
        elif c == '*': self.add(TokenType.STAR)
        elif c == '!':
            if self.match('='):
                self.add(TokenType.BANG_EQUAL)
            else:
                self.add(TokenType.BANG)
        elif c == '=':
            if self.match('='):
                self.add(TokenType.EQUAL_EQUAL)
            else:
                self.add(TokenType.EQUAL)
        elif c == '<':
            if self.match('='):
                self.add(TokenType.LESS_EQUAL)
            else:
                self.add(TokenType.LESS)
        elif c == '>':
            if self.match('='):
                self.add(TokenType.GREATER_EQUAL)
            else:
                self.add(TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                # A comment goes until the end of the line.
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add(TokenType.SLASH)
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha():
            self.identifier()
        elif c in ' \r\t':
            pass
        elif c == '\n':
            self.line += 1
        else:
            main.error(self.line, 'Unexpected character.')

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            main.error(self.line, 'Unterminated string.')
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add(TokenType.STRING, value)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.peek_next().isdigit():
            # consume the '.'
            self.advance()
            while self.peek().isdigit():
                self.advance()
        value = float(self.source[self.start:self.current])
        self.add(TokenType.NUMBER, value)

    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance() 

        text = self.source[self.start:self.current]
        type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add(type)

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected: str) -> bool:
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def add(self, type: TokenType, literal: Optional[object] = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
