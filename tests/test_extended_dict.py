from extended_dict.extended_dict import ExtendedDict
import pytest


class TestExtendedDict:
  def test_iloc(self):
    extended_dict = ExtendedDict()
    extended_dict["value1"] = 1
    extended_dict["value2"] = 2
    extended_dict["value3"] = 3
    extended_dict["1"] = 10
    extended_dict["2"] = 20
    extended_dict["3"] = 30
    extended_dict["1, 5"] = 100
    extended_dict["5, 5"] = 200
    extended_dict["10, 5"] = 300

    assert extended_dict.iloc[0] == 10
    assert extended_dict.iloc[2] == 300
    assert extended_dict.iloc[5] == 200
    assert extended_dict.iloc[8] == 3

  def test_ploc(self):
    extended_dict = ExtendedDict()
    extended_dict["value1"] = 1
    extended_dict["value2"] = 2
    extended_dict["value3"] = 3
    extended_dict["1"] = 10
    extended_dict["2"] = 20
    extended_dict["3"] = 30
    extended_dict["(1, 5)"] = 100
    extended_dict["(5, 5)"] = 200
    extended_dict["(10, 5)"] = 300
    extended_dict["(1, 5, 3)"] = 400
    extended_dict["(5, 5, 4)"] = 500
    extended_dict["(10, 5, 5)"] = 600

    assert extended_dict.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
    assert extended_dict.ploc["<3"] == {"1": 10, "2": 20}
    assert extended_dict.ploc[">0, >0"] == {
        "(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
    assert extended_dict.ploc[">=10, >0"] == {"(10, 5)": 300}
    assert extended_dict.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}
