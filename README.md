Для запуска выполнить:

```
docker-compose build
docker-compose up -d postgre
docker-compose up food-api
```

Спецификация API: ``http://0.0.0.0:49105/``

эндпоинт для API "блюда": ``http://0.0.0.0:49105/v1/food``