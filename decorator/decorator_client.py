
from decorator_define import *


@print_decorator
def test_function(tbl_name: str, db_name: str):
    return f"{db_name}.{tbl_name} good"


if __name__ == "__main__":
    print(test_function(tbl_name="youngjai", db_name="macro_db"))
    #print(test_function("test1", "test2"))