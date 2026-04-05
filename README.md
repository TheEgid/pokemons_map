# Карта покемонов

![sample text](https://i.ibb.co/tXD20G6/image.jpg)

### Предметная область

Сайт для помощи по игре [Pokemon GO](https://www.pokemongo.com/en-us/). Это игра про ловлю [покемонов](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BA%D0%B5%D0%BC%D0%BE%D0%BD).

Суть игры в том, что на карте периодически появляются покемоны, на определённый промежуток времени. Каждый игрок может поймать себе покемона, и пополнить свою личную коллекцию.

### Технологии

- Python 3.12+
- Django 5.2+
- Folium (интерактивные карты)
- Pydantic (валидация данных)
- Bootstrap 5.3 (UI)

### Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта:
```env
DEBUG=true
SECRET_KEY=your-secret-key-here
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер:
```bash
python manage.py runserver
```

### Запуск

- Главная страница: http://localhost:8000
- Админка: http://localhost:8000/admin

Заполните данные покемонов через админку.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
