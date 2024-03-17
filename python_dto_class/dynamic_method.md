## dynamic class method Impl

### 목적 

- class는 하나 쓰는데, 특정 한개 method만 구현이 필요한 경우  
  - 예를 들면, data를 src에서 가져오는 과정은 같음
  - 그런데, 그 데이터를 preprocess 하는 method의 구현만 dynamic하게 해주고 싶은 경우 

### 방법 
일단 아래와 같이 구현되어 있는 class에서 process_rows 이걸 특정 경우에 따라 구현하는 것임.  
```python
class SampleClass:
    def __init__(self, idx_name):
        self.idx_name = idx_name

    def run(self):
        src_data = self.get_src_data()
        return self.process_rows(rows=src_data["data1"])

    @abstractmethod
    def process_rows(self, rows):
        pass
```
#### 1. 그냥 바로 assign 
```python
def process_a(self, rows):
    years = [a["year"] for a in rows]
    periods = [a["period"] for a in rows]
    values = [a["value"] for a in rows]
    return pd.DataFrame({"year": years, "periods": periods, self.idx_name: values})

test_instance.process_rows = process_a
```
- 이렇게 하면 되기는 함. 가장 간단. 
- 그런데 class내부 변수를 구현체에서 활용하지 못함.. 왜냐면 process_a라는 함수가 곧 process_rows인데, 이게 class내부에서는 self.를 또 주지는 않으니까.


#### 2. setattr로 해주기 
```python
def process_b(self, rows):
    years = [a["year"] for a in rows]
    values = [a["value"] for a in rows]
    return pd.DataFrame({"year": years, self.idx_name: values})

setattr(SampleClass, "process_rows", process_b)
```
- 이렇게하면 process_a 에 self를 param으로 받고, 내부에서 self를 통해서 class변수들을 활용할 수 잇다. 
- 근데 setattr을 class자체에만 가능한듯함.. instance에는 안되는듯.
  - 안되는건 아니지만, self를 인식못한다고함. 
  - object.attribute = value 와 같은 오류임 
- `object.attribute = value` 와 사실 같은 문법임 

#### 3. lambda로 주기 


## LazyInit of method 