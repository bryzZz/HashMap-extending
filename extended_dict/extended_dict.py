from .methods import Ploc
from .utils import remove_parentheses


class ExtendedDict:
  def __init__(self) -> None:
    self._entries = dict()
    self._ploc_instance = Ploc(self._entries)

  @property
  def iloc(self):
    return list({k: self._entries[k] for k in sorted(self._entries)}.values())

  @property
  def ploc(self):
    return self._ploc_instance

  def __getitem__(self, key):
    if isinstance(key, str):
      key = remove_parentheses(key)
    return self._entries[key]

  def __setitem__(self, key, value):
    val = self._entries[key] = value

    return val
