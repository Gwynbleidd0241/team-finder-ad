# TeamFinder (Вариант 1)

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/Gwynbleidd0241/team-finder-ad.git
cd team-finder-ad
```

---

### 2. Виртуальное окружение

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

---

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

### 4. Настройка переменных окружения

Создайте файл `.env` на основе примера:

```bash
cp .env_example .env
```

Пример содержимого `.env`:

```env
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=True

POSTGRES_DB=teamfinder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TASK_VERSION=1
```

---

### 5. Запуск базы данных (PostgreSQL)

```bash
docker compose up -d
```

Остановка контейнера:

```bash
docker compose down
```

---

### 6. Применение миграций

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

### 7. Создание суперпользователя

```bash
python3 manage.py createsuperuser
```

---

### 8. Создание тестовых данных

```bash
python3 manage.py seed_data
```

Будут созданы:
- тестовые пользователи
- проекты

---

### 9. Запуск сервера

```bash
python3 manage.py runserver
```

Открыть в браузере:

```
http://127.0.0.1:8000/
```

---

## Тесты

```bash
python3 manage.py test users.tests.test_views
python3 manage.py test projects.tests.test_views
```
