Для запуска выполнить:

```
docker-compose build
docker-compose up -d postgres
docker-compose up food-api
```

Спецификация API: ``http://0.0.0.0:49105/``

эндпоинт для API "блюда": ``http://0.0.0.0:49105/v1/food``

фильтрация: 
```
http://0.0.0.0:49105/v1/food?filter=["toppings.name","=","Киви"]
http://0.0.0.0:49105/v1/food?filter=["price", ">=", 100]
```

