import cattrs
from attr import define, field
import re


def return_test_data():
    sample = {
        "data1": [{'year': '2023', 'period': 'M12', 'periodName': 'December', 'value': '306.746', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M11', 'periodName': 'November', 'value': '307.051', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M10', 'periodName': 'October', 'value': '307.671', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M09', 'periodName': 'September', 'value': '307.789', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M08', 'periodName': 'August', 'value': '307.026', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M07', 'periodName': 'July', 'value': '305.691', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M06', 'periodName': 'June', 'value': '305.109', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M05', 'periodName': 'May', 'value': '304.127', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M04', 'periodName': 'April', 'value': '303.363', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M03', 'periodName': 'March', 'value': '301.836', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M02', 'periodName': 'February', 'value': '300.840', 'footnotes': [{}]},
                  {'year': '2023', 'period': 'M01', 'periodName': 'January', 'value': '299.170', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M12', 'periodName': 'December', 'value': '296.797', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M11', 'periodName': 'November', 'value': '297.711', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M10', 'periodName': 'October', 'value': '298.012', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M09', 'periodName': 'September', 'value': '296.808', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M08', 'periodName': 'August', 'value': '296.171', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M07', 'periodName': 'July', 'value': '296.276', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M06', 'periodName': 'June', 'value': '296.311', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M05', 'periodName': 'May', 'value': '292.296', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M04', 'periodName': 'April', 'value': '289.109', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M03', 'periodName': 'March', 'value': '287.504', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M02', 'periodName': 'February', 'value': '283.716', 'footnotes': [{}]},
                  {'year': '2022', 'period': 'M01', 'periodName': 'January', 'value': '281.148', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M12', 'periodName': 'December', 'value': '278.802', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M11', 'periodName': 'November', 'value': '277.948', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M10', 'periodName': 'October', 'value': '276.589', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M09', 'periodName': 'September', 'value': '274.310', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M08', 'periodName': 'August', 'value': '273.567', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M07', 'periodName': 'July', 'value': '273.003', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M06', 'periodName': 'June', 'value': '271.696', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M05', 'periodName': 'May', 'value': '269.195', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M04', 'periodName': 'April', 'value': '267.054', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M03', 'periodName': 'March', 'value': '264.877', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M02', 'periodName': 'February', 'value': '263.014', 'footnotes': [{}]},
                  {'year': '2021', 'period': 'M01', 'periodName': 'January', 'value': '261.582', 'footnotes': [{}]}]
        }

    return sample


@define
class MonthlyData:
    year = field(converter=int)
    period = field(converter=(lambda x: int(re.findall(r'\d+', x)[0])))
    value: float = field(converter=float)


@define
class Data1:
    data1: list[MonthlyData]


if __name__ == "__main__":
    sample_data = return_test_data()
    cattrs_converter = cattrs.Converter()
    d = cattrs_converter.structure(sample_data, Data1)
    print(d)
