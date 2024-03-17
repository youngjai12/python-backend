# Python DTO Class

## 목적
- 파이썬에서 데이터를 담는 여러 class들을 사용해본다.
- 다양한 class들 간의 아래의 성능들을 비교해본다.
  - 객체로 만드는 시간 
      - 특히 client의 resp를 객체화해야 작업하기가 편하니까 
  - 원하는 타입으로 변경하는 시간? (특정필드를 int로 바꾼다거나)
  - 필드에 대한 연산..?

## Performance Test 
#### 실험 대상 class
- python plain class
- cattrs + attrs 
- attrs 
- dataclass
- pydantic
- TypedDict

#### 실험결과: TypeConversion(특정 field의 타입)
- 결론 
  - nested한 경우가 아니라, 단순히 type변환 정도로 데이터를 담는거면 그냥 attrs쓰자.  
- TypedDictf : 500만개 타입변환해서 객체화: 0:00:01.616063
  - 이건 그냥 일반 dict랑 똑같음. 그래서 성능이 당연히 최상. 
  - 다만, pure python의 dict는 type을 강제할 수 없으니, 각 field에 대한 type을 좀 강제할 수 있다정도임
- cattrs : 0:00:09.241433
  - `cattrs_converter.structure(obj, [deserialize할 cattrs객체])` 을 이용해서 deserialize 
  - 원하는 형태로 바꿔주기는 함. 
- attrs : 0:00:06.942440