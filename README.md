# 📚 Wallet Database API

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)
![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![Alembic](https://img.shields.io/badge/Alembic-✓-yellow)

REST API для управления кошельками с поддержкой операций DEPOSIT и WITHDRAW. Система обеспечивает безопасную обработку параллельных операций через оптимистичную блокировку.

---

## 🏗 Архитектура

```
wallet-api/
├── api/
│ ├── endpoints/ # Роутеры API
│ ├── schemas/ # Pydantic модели и SQLAlchemy модели
│ └── services/ # Бизнес-логика
├── core/ # Конфигурация и подключение к БД
├── migrations/ # Миграции Alembic
├── tests/ # Тесты
├── main.py # Точка входа FastAPI
├── docker-compose.yml # Docker конфигурация
├── Dockerfile # Dockerfile для API
├── pyproject.toml # Зависимости проекта (uv)
└── .env # Переменные окружения

```
---

## 🚀 Быстрый старт

### Запуск через Docker Compose (рекомендуется)

Клонируйте репозиторий
```bash
git clone git@github.com:IvalexAnna/wallet-api
```
Перейдите в корневую директорию проекта

```bash
cd wallet-api
```

Скопируйте переменные окружения
```bash
cp .env.example .env
```
Запустите приложение
```bash
docker-compose up --build -d
```
```bash
Приложение: http://localhost:8000
Документация: http://localhost:8000/docs
PostgreSQL: localhost:5432
```
### Локальный запуск
Установите uv
```bash
pip install uv
```
Альтернативный вариант:

На Windows через PowerShell:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
На macOS и Linux через curl:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Создайте виртуальное окружение 
```bash
uv python -m venv venv
```
Установите зависимости
На Linux/macOS:
```bash
source .venv/bin/activate
```
На Windows PowerShell:
```bash
.venv\Scripts\activate
```
Чтобы синхронизировать зависимости из pyproject.toml:
```bash
uv sync
```
Применение миграций Alembic:
```bash
alembic upgrade head
```
Запустите приложение локально
```bash
uv run uvicorn main:app --reload
```

Соберите контейнеры и запутсите их 
```bash
docker compose up --build
```

---

## ⚙️ Конфигурация

Файл `.env` в корне проекта. Образец — `.env.example`.
```bash

POSTGRES_DB=book_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
Переменная `PYTHONPATH` настраивается в Compose и Dockerfile.

---

## 📡 API Endpoints

### 👛 Кошельки

#### Получить все кошельки
```bash
curl -X GET "http://localhost:8000/api/v1/wallets"
```

#### Создать кошелек
```bash
curl -X POST "http://localhost:8000/api/v1/wallets"
-H "Content-Type: application/json"
-d '{"user_id": "uuid-user"}'
```

---

### Получить баланс кошелька
```bash
curl -X GET "http://localhost:8000/api/v1/wallets/<wallet_id>/balance"
```

#### Выполнить операцию (DEPOSIT/WITHDRAW)
# DEPOSIT
```bash
curl -X POST "http://localhost:8000/api/v1/wallets/<wallet_id>/operations"
-H "Content-Type: application/json"
-d '{"operation_type": "DEPOSIT", "amount": 1000}'
```
# WITHDRAW
```bash
curl -X POST "http://localhost:8000/api/v1/wallets/<wallet_id>/operations"
-H "Content-Type: application/json"
-d '{"operation_type": "WITHDRAW", "amount": 500}'
```
```bash
Ответ:
{
  "wallet_id": "bb83d0fe-a404-4f28-bddd-a41e9e7ce9a4",
  "operation_type": "DEPOSIT",
  "amount": 1000.0,
  "new_balance": 1000.0,
  "success": true
}
```


### 🩺 Health Check
```bash
curl -X GET "http://localhost:8000/health"

Ответ:

{"status": "healthy"}
```

---
## 🗄 Структура базы данных

### Таблица `wallets`

| Поле         | Тип         | Ограничения               | Описание                          |
|--------------|-------------|---------------------------|-----------------------------------|
| `id`         | UUID        | PRIMARY KEY               | Уникальный идентификатор кошелька |
| `balance`    | NUMERIC(10,2)| NOT NULL, DEFAULT 0.0     | Баланс кошелька                  |            |
| `version`    | INTEGER     | NOT NULL, DEFAULT 1       | Версия для оптимистичной блокировки |
| `created_at` | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Время создания                   |
| `updated_at` | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Время последнего обновления   

---


---

## 🧪 Тесты

- Основные тесты: `uv run pytest tests/tests.py`, `docker-compose exec web python -m pytest tests/tests.py -v`

---

## 👩‍💻 Автор

**Анна Иванова**

Разработано в рамках тестового задания для ITK Academy. 🚀


[![Email](https://img.shields.io/badge/Email-ivalex.anna@gmail.com-red?logo=gmail)](mailto:ivalex.anna@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-@IvalexAnna-blue?logo=telegram)](https://t.me/IvalexAnna)
[![GitHub](https://img.shields.io/badge/GitHub-IvalexAnna-black?logo=github)](https://github.com/IvalexAnna)
