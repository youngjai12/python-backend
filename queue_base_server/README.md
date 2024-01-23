# Queue Base Server 

## 역할 
- 비동기로 모델 inference 요청같은 것들이 몰려올때 처리하는 서버. 

## 구조 
- RabbitMQ 큐가 Event bus 역할 
- kombu, Celery 라이브러리 통해서 이벤트 consume한다. 