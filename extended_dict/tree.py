from abc import ABC
from .ploc_tokens import Token


class Node(ABC):
  ...


class Number(Node):
  def __init__(self, value: Token) -> None:
    self.value = value

  def __str__(self) -> str:
    return f"{self.__class__.__name__}({self.value})"


class Operator(Node):
  def __init__(self, value: Token) -> None:
    self.value = value

  def __str__(self) -> str:
    return f"{self.__class__.__name__}({self.value})"


class Condition(Node):
  def __init__(self) -> None:
    self.operator: Operator | None = None
    self.value: Number | None = None

  def __str__(self) -> str:
    return f"Condition {self.operator}, {self.value}"
