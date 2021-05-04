# Foodgram, Сайт рецептов
[![Actions Status](https://github.com/BazhanovD/foodgram-project/workflows/Foodgram/badge.svg)](https://github.com/BazhanovD/foodgram/actions)

Проект Foodgram создан для хранения рецептов пользователей, сформированных на основе списка ингридиеентов. Каждый из рецептов имеет своё описание, в т.ч. время готовки и предпочитаемое время употребления - завтрак, обед и ужин. Можно добавлять каждый из рецептов в свой список покупок чтобы потом скачать полный список ингридиентов в удобном формате.

Посмотреть на работу проекта можно по этому адресу: [http://84.252.133.33](http://84.252.133.33)

# Установка
Клонируйте репозиторий.
```
git clone https://github.com/BazhanovD/yamdb_final
```
Команда для запуска терминала внутри контейнера:
```
docker-compose exec web bash
```
Чтобы сделать миграцию бд, выполните следующую команду:
```
python manage.py migrate
```
Для создания администратора Django:
```
python manage.py createsuperuser
```
Чтобы загрузить в БД данные ингридиентов, выполните:
```
python manage.py loaddata fixtures.json
```
Команда для остановки контейнеров:
```
docker-compose down
```
Команда для повторного запуска:
```
docker-compose up -d
```

