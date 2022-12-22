from .utils import remove_parentheses, isNumber
from .ploc_tokens import Token, TokenType, OPERATORS, CONDITION_SEPARATOR
from .tree import Condition, Operator, Number


class PlocLexerException(Exception):
  ...


class PlocParserException(Exception):
  ...


class PlocInterpreterException(Exception):
  ...


class PlocLexer:
  def __init__(self):
    self.pos = 0
    self.text = ""
    self.current_char = ''

  def init_lexer(self, text: str):
    self.pos = 0
    self.text = text
    self.current_char = self.text[self.pos]

  def condition(self):
    result = []

    while self.current_char != '' and self.current_char in OPERATORS:
      result.append(self.current_char)
      self.forward()

    return "".join(result)

  def number(self):
    result = []

    while self.current_char != '' and isNumber(self.current_char):
      result.append(self.current_char)
      self.forward()

    return "".join(result)

  def forward(self):
    self.pos += 1
    if self.pos == len(self.text):
      self.current_char = ''
    else:
      self.current_char = self.text[self.pos]

  def skip(self):
    while self.current_char != '' and self.current_char.isspace():
      self.forward()

  def next(self) -> Token | None:
    while self.current_char != '':
      if self.current_char.isspace():
        self.skip()
        continue

      if self.current_char == "-":
        self.forward()
        return Token(TokenType.NUMBER, "-" + self.number())

      if isNumber(self.current_char):
        return Token(TokenType.NUMBER, self.number())

      if self.current_char in OPERATORS:
        return Token(TokenType.OPERATOR, self.condition())

      if self.current_char == CONDITION_SEPARATOR:
        token = Token(TokenType.CONDITION_SEPARATOR, self.current_char)
        self.forward()
        return token

      raise PlocLexerException(f"Unexpected token ({self.current_char})")


class PlocParser:
  def __init__(self):
    self.current_token: Token | None = None
    self.lexer = PlocLexer()
    self.conditions = [Condition()]
    self.current_condition_index = 0

  def check_type(self, type_: TokenType):
    if (self.current_token is None):
      raise PlocParserException("Current token is not defined")

    if self.current_token.type == type_:
      self.current_token = self.lexer.next()
      return

    raise PlocParserException(
        f"invalid token order. Expected {type_}, Received {self.current_token.type}")

  def factor(self):
    if (self.current_token is None):
      raise PlocParserException("Current token is not defined")

    token = self.current_token
    match token.type:
      case TokenType.OPERATOR:
        self.conditions[self.current_condition_index].operator = Operator(
            token)
        self.check_type(TokenType.OPERATOR)
        return
      case TokenType.NUMBER:
        self.conditions[self.current_condition_index].value = Number(token)
        self.check_type(TokenType.NUMBER)
        return
      case TokenType.CONDITION_SEPARATOR:
        self.current_condition_index += 1
        self.conditions.append(Condition())
        self.check_type(TokenType.CONDITION_SEPARATOR)
        return
      case _:
        raise PlocParserException("Invalid token")

  def generate_conditions(self):
    while self.current_token is not None:
      self.factor()

  def init_parser(self, text: str):
    self.lexer.init_lexer(text)
    self.current_token = self.lexer.next()
    self.conditions = [Condition()]
    self.current_condition_index = 0


class Ploc:
  def __init__(self, entries: dict):
    self._entries = entries
    self.parser = PlocParser()

  def __getitem__(self, key):
    if isinstance(key, str):
      key = remove_parentheses(key)
    return self.eval(key)

  def compare(self, condition: Condition, key: float) -> bool:
    operator = condition.operator.value.value
    value = float(condition.value.value.value)

    match operator:
      case ">=":
        return key >= value
      case "<=":
        return key <= value
      case "==":
        return key == value
      case ">":
        return key > value
      case "<":
        return key < value
      case "<>":
        return key != value
      case _:
        raise PlocInterpreterException(f"Invalid condition {condition}")

  def eval(self, text: str):
    self.parser.init_parser(text)
    self.parser.generate_conditions()

    match_conditions_entries = {}

    for entry in self._entries:
      splitted = remove_parentheses(entry).split(',')
      splitted = filter(lambda x: isNumber(x.strip()), splitted)
      splitted = [float(x) for x in splitted]

      if len(splitted) != len(self.parser.conditions):
        continue

      match_conditions_count = 0

      for i, condition in enumerate(self.parser.conditions):
        if self.compare(condition, splitted[i]):
          match_conditions_count += 1

      if match_conditions_count == len(splitted):
        match_conditions_entries[entry] = self._entries[entry]

    return match_conditions_entries
