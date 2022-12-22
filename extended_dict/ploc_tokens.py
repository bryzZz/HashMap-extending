from enum import Enum, auto

OPERATORS = ['<', '>', '=']
CONDITION_SEPARATOR = ','


class TokenType(Enum):
  OPERATOR = auto()
  CONDITION_SEPARATOR = auto()
  NUMBER = auto()


class Token:
  def __init__(self, type, value) -> None:
    self.type = type
    self.value = value

  def __str__(self) -> str:
    return f"Token ({self.type}, {self.value})"
