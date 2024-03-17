# 아래 글 참고
# https://mgarod.medium.com/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6

from abc import abstractmethod

import pandas as pd


class SampleClass:
    def __init__(self, idx_name):
        self.idx_name = idx_name

    def run(self):
        src_data = self.get_src_data()
        return self.process_rows(rows=src_data["data1"])

    def process_rows(self, rows):
        pass

    def get_src_data(self):
        pass


def get_src_data_a():
    return {
        "data1": [
            {
                "year": "2023",
                "period": "M12",
                "periodName": "December",
                "value": "306.746",
                "footnotes": [{}],
            },
            {
                "year": "2023",
                "period": "M11",
                "periodName": "November",
                "value": "307.051",
                "footnotes": [{}],
            },
            {
                "year": "2023",
                "period": "M10",
                "periodName": "October",
                "value": "307.671",
                "footnotes": [{}],
            },
            {
                "year": "2023",
                "period": "M09",
                "periodName": "September",
                "value": "307.789",
                "footnotes": [{}],
            },
        ]
    }


def process_a(self, rows):
    years = [a["year"] for a in rows]
    periods = [a["period"] for a in rows]
    values = [a["value"] for a in rows]
    return pd.DataFrame({"year": years, "periods": periods, self.idx_name: values})


def process_b(rows):
    years = [a["year"] for a in rows]
    values = [a["value"] for a in rows]
    return pd.DataFrame({"year": years, "1-month-bond": values})


if __name__ == "__main__":
    test_instance = SampleClass(idx_name="wowow")
    # dynamic하게 assign하려는 함수에 class 내부 변수를 사용하지 않는 경우
    test_instance.get_src_data = get_src_data_a

    # process_a 라는 함수에 class 내부 변수가 필요한 경우
    # 그래서 구현체에 self를 넣으면 그게 없다고 에러남.
    # test_instance.process_rows = process_a

    # 이건 잘 working한다.
    setattr(SampleClass, "process_rows", process_a)

    test_instance2 = SampleClass(idx_name="test2")
    test_instance2.get_src_data = get_src_data_a
    test_instance2.process_rows = process_b
    #setattr(SampleClass, "process_rows", process_b)


    print(test_instance2.run())
