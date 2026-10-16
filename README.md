XSS Demo App
Учебное веб-приложение для демонстрации уязвимостей Reflected XSS и Stored XSS, а также их устранения.

Технологии
Python 3.11, Flask 3.0.3

SQLite

Docker, Docker Compose

Jinja2

Запуск
docker-compose up --build

Приложение будет доступно по адресу: http://localhost:5000

Страницы приложения
/ — главная страница

/search?q=... — поиск (уязвим к Reflected XSS)

/comments — комментарии с сохранением в SQLite (уязвим к Stored XSS)

Уязвимости
Reflected XSS
В файле templates/search.html используется фильтр safe, который отключает автоэкранирование Jinja2. Это позволяет внедрить произвольный JavaScript через параметр URL q.

Пример атаки:

http://localhost:5000/search?q=script alert XSS script

Stored XSS
В файле templates/comments.html комментарии выводятся через фильтр safe. Данные сохраняются в SQLite без санитизации, поэтому скрипт выполняется при каждом открытии страницы.

Пример атаки (в поле комментария):

img src=x onerror=alert(document.cookie)

Защита
Убрано использование фильтра safe в шаблонах. Jinja2 по умолчанию автоматически экранирует HTML-теги, что предотвращает выполнение JavaScript.

Структура проекта
xss-app/

app.py

requirements.txt

Dockerfile

docker-compose.yml

README.md

templates/

base.html

index.html

search.html

comments.html

Автор
[Верхозина Полина]