# ML-Сервис для проверки ответов

## Proto файл
Proto файл можно найти [здесь](https://github.com/danyatalent/protos/blob/main/proto/answer/answer.proto)

## Установка зависимостей
```bash
make req
```

## Запуск

Для запуска
```bash
make start
```


## Пример

Используя gRPC в формате запрос на localhost:50051 в формате:

```bash
{
    "userAnswer": "ведущая скрипка",
    "correctAnswer": "первая скрипка"
}
```

Ожидаемый ответ:
```bash
{
    "isCorrect": true
}
```

## TODO
* Logging Interceptor