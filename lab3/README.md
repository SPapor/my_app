# Лабораторная №3

**Вариант 2:** Пользовательские категории  


---

## Требования

- **Docker**  
- **Python ≥ 3.11** 

---

## Запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/SPapor/my_app.git
cd lab_3

```
### 2. Настройка конфигурации
Создайте файл .env.docker в корне папки lab_3 и вставьте следующие настройки:

```bash 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DATABASE_URL=postgresql://postgres:my_secret_password@db:5432/expense_db
```
### 3. Docker Compose: Сборка и Запуск
Эта команда соберет образы и запустит базу данных
``` bash
docker compose up --build -d
```

### 4. Применение миграций
Необходимо создать таблицы

``` bash
docker compose exec app alembic upgrade head
```
