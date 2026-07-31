# Dogs Breed API

Учебный pet-проект на Django REST Framework: REST API для учёта собак и пород.

## Технологический стек

- **Python 3.13**
- **Django 6.0** + **Django REST Framework 3.17**
- **PostgreSQL 17**, драйвер — **psycopg 3**
- **Poetry** — пакетный менеджер
- **Docker / Docker Compose** — запуск и окружение
- **Ruff** — линтинг и форматирование, **pre-commit** — хуки на коммит
- **factory_boy** + **Faker** — генерация демо-данных

## Инструкция по установке и запуску

### Через Docker

Системное требование — установленные Docker и Docker Compose.

1. Склонируйте репозиторий и перейдите в его корень.
2. Создайте файл окружения на основе примера:
   ```bash
   cp .env.example .env
   ```
   Значения по умолчанию уже рабочие для локального запуска, но лучше замените `SECRET_KEY` и пароль Postgres на собственные.
3. Соберите и поднимите контейнеры:
   ```bash
   docker compose up --build -d
   ```
4. Примените миграции:
   ```bash
   docker compose run --rm web-app sh -c "python manage.py migrate"
   ```
5. (опционально) Наполните базу демо-данными:
   ```bash
   docker compose run --rm web-app sh -c "python manage.py insert_data"
   ```
   
Остановить проект: `docker compose down`

## Описание компонентов и архитектуры

### Структура проекта

```
.
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── poetry.lock
├── .env.example
├── .pre-commit-config.yaml
├── README.md
└── src/
    ├── manage.py
    ├── config/                 # конфигурация проекта
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── dogs/                   # доменное приложение
        ├── models.py
        ├── serializers.py
        ├── views.py
        ├── urls.py
        ├── admin.py
        ├── exceptions.py
        ├── speed_tester.py
        ├── factories.py
        ├── tests/
        ├── migrations/
        └── management/commands/insert_data.py
```

Проект состоит из одного Django-приложения `dogs`, содержащего всю доменную логику, и конфигурационного пакета `config` со стандартными Django-файлами.

### `config/settings.py`

- `SECRET_KEY` и `DEBUG` читаются из переменных окружения.
- `REST_FRAMEWORK` задаёт глобально для всех вьюсетов постраничную выдачу (`PageNumberPagination`, `PAGE_SIZE = 10`) и кастомный `EXCEPTION_HANDLER`).
- `LOGGING` настроен на вывод и в консоль.

### `dogs/models.py`

Две модели:

**`Breed`** — порода

**`Dog`** — собака

### `dogs/serializers.py`

- **`BreedSerializer` / `DogSerializer`** — «полное» представление (`fields = "__all__"`)
- **`BreedListSerializer` / `DogListSerializer` / `DogDetailSerializer`** — отдельные сериализаторы под конкретный action, добавляющие поля, которых нет в модели (`dogs_count`, `average_age`).
- **`DogWriteSerializer`** — отдельный сериализатор для `create`/`update`/`partial_update`. `breed`

### `dogs/views.py`

- **`BreedViewSet`** и **`DogViewSet`** — вьюсеты для работы с моделями Dog и Breed в бд

Модуль `dogs/speed_tester.py` замеряет число SQL-запросов и время выполнения для конкретного queryset

### `dogs/exceptions.py`

Кастомный `EXCEPTION_HANDLER` для DRF (удаление породы с привязанными собаками)

### `dogs/factories.py` и `management/commands/insert_data.py`

`factory_boy` — фабрики для генерации данных:

- `BreedFactory` — выбирает название из фиксированного списка `DOG_BREED_NAMES`.
- `DogFactory` — `breed` создаётся неявно через `SubFactory(BreedFactory)`. Остальные поля заполняются через `Faker`.

Команда `make insert_data` создаёт 20 собак за вызов

## Тесты

Тесты лежат в `dogs/tests/` (pytest + pytest-django, тестовые данные через фабрики из `factories.py`). Запуск:

   ```bash
make test
   ```

## Примеры использования API

| Метод | URL | Действие |
|---|---|---|
| GET | `/api/dogs/` | Список собак (постранично, `average_age` на породу) |
| POST | `/api/dogs/` | Создать собаку |
| GET | `/api/dogs/<id>/` | Одна собака (`dogs_count` по её породе) |
| PUT / PATCH | `/api/dogs/<id>/` | Обновить собаку (целиком / частично) |
| DELETE | `/api/dogs/<id>/` | Удалить собаку |
| GET | `/api/breeds/` | Список пород (постранично, `dogs_count` на породу) |
| POST | `/api/breeds/` | Создать породу |
| GET | `/api/breeds/<id>/` | Одна порода |
| PUT / PATCH | `/api/breeds/<id>/` | Обновить породу |
| DELETE | `/api/breeds/<id>/` | Удалить породу (`409`, если есть привязанные собаки) |