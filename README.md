# ДЗ 3

Упаковка в docker приложения `app/`

## Запуск

```sh
cp .env.example .env
docker compose up -d --build
docker compose down
```

## Настройки для docker compose

| Переменная | Значение по умолчанию | За что отвечает |
| --- | --- | --- |
| `APP_PORT` | `8080` | локальный порт сервиса |
| `GREETING` | `Hello, Docker!` | приветствие, которое возвращает сервис |