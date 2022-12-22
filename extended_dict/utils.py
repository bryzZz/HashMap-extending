def isNumber(char: str):
  return char.isdigit() or char == '.'


def remove_parentheses(str: str):
  return str.strip('(').strip(')')
