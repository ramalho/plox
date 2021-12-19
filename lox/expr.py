from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

import parser

R = TypeVar('R')


class Visitor(ABC, Generic[R]):
    def visitBinaryExpr(self, expr: 'Binary') -> R:
        ...


class Expr(ABC, Generic[R]):
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        ...


@dataclass(frozen=True)
class Binary(Expr, Generic[R]):
    left: Expr
    operator: parser.Token
    right: Expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visitBinaryExpr(self)
