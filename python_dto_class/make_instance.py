import random
from typing import TypedDict

from attr import define, dataclass, field
import cattrs
from datetime import datetime

@define(kw_only=True)
class CattrsClass:
    a1: int
    a2: int
    a3: int
    a4: int
    a5: int
    a6: int
    a7: str


@define(kw_only=True)
class AttrsClass:
    a1: int = field(converter=int)
    a2: int = field(converter=int)
    a3: int = field(converter=int)
    a4: int = field(converter=int)
    a5: int = field(converter=int)
    a6: int = field(converter=int)
    a7: str = field(converter=str)

class TypedDictClass(TypedDict):
    a1: int
    a2: int
    a3: int
    a4: int
    a5: int
    a6: int
    a7: str

def convert_typedict(obj: dict) -> TypedDictClass:
    to_return={}
    for field_name in obj.keys():
        if field_name == "a7":
            to_return[field_name] = obj[field_name]
        else:
            to_return[field_name] = int(obj[field_name])
    return to_return


def generate_sample_data(cnt):
    rand_nums = random.choices(range(1, 100), k=6*cnt)
    tot = []
    for i in range(cnt):
        data = {
            "a1": str(rand_nums[i+0]),
            "a2": str(rand_nums[i + 1]),
            "a3": str(rand_nums[i + 2]),
            "a4": str(rand_nums[i + 3]),
            "a5": str(rand_nums[i + 4]),
            "a6": str(rand_nums[i + 5]),
            "a7": "34d"
        }
        tot.append(data)
    return tot

if __name__ == "__main__":
    dd = generate_sample_data(5000000)
    cattrs_converter = cattrs.Converter()

    st1 = datetime.now()
    cattrs_converted = [cattrs_converter.structure(e, CattrsClass) for e in dd]
    ed1 = datetime.now()
    typed_dict_results = [convert_typedict(e) for e in dd]
    ed2 = datetime.now()
    attrs_results = [
        AttrsClass(
            a1=e["a1"], a2=e["a2"], a3=e["a3"], a4=e["a4"], a5=e["a5"],
            a6=e["a6"], a7=e["a7"]
        )
        for e in dd
    ]
    ed3 = datetime.now()

    print(f"cattrs: {ed1 - st1}")
    print(f"typeddict: {ed2 - ed1}")
    print(f"attrs: {ed3 - ed2}")

    print(f"typeddict : access 3rd a1: {typed_dict_results[3]['a1']} type({type(typed_dict_results[3]['a1'])})\n")
    print(f"cattrs access 3rd a1: {cattrs_converted[3].a1} type({type(cattrs_converted[3].a1)})\n")
    print(f"attrs access 3rd a1: {attrs_results[3].a1} type({type(attrs_results[3].a1)})")

