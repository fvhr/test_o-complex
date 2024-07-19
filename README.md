# Бейджи статус пайплайна CI/CD
[![pipeline Status](https://github.com/scolopendra2/test_o-complex/actions/workflows/main.yml/badge.svg)](https://github.com/scolopendra2/test_o-complex/actions/workflows/main.yml)

# Python
[![Python Version](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)

![Language stats](https://img.shields.io/badge/language_stats-python%3A72%25%20html%3A15%25%20javascript%3A7%25%20css%3A3%25%20makefile%3A2%25-brightgreen?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAAQCAYAAAC1HAwCAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAB7CAAAewgFu0HU+AAABNElEQVQ4T2NkYGBg5D3X/zAASkUgAaTgo7B5B5kXwD+MlC2S0MCwAzBDQMY3fT+OBkE+KMIHT4aF4yQ+G4vRm0E6AQNgYAxBAhT2AiBFENsGJHBpHDhysTKUBFkJqv2HQn8BNAsfwZQbF4C0QEmDzz4RJkCEWBNAFLuABca3UkAqPpSCS8HG0bPxjsVfFwWeCkIFZ4DZwA4GA1POwFgXk5Kihg7gBicS3vWMAeKwoFkgYGH7zTBjxkUfg7ApwJDWj0BRTBfFg8YWlPElMECA4n0dHAwQFyBi2AIApGWZAlxCwSwSAAyFgABxkE3xgC6HSJ2G0aQ4eEyL0CM8FE5zMQiBTh6QF5MAbgHieTTDsD7v9u4wM+AIlwMugjFTMtR5AKJrU8wL8OQA7B5GgA4AH2IEAI7Cz4tS0EBwBGOGiBBgANgC9A4CqOUyQq7Aqz+A4ErUYCpAEoHAAk9SFLsABBG2QA7iB0AF0BHAIhQAaQEwFg9TEUwgXIgBv8BE1gBdIg6Bm2CUqCF+eZA2Ma0wCxZ5wB+jAiABkRWoRBJgQ1Agh1E+BQkmw0Do4MksSKXwFFy4J4bVYfIBDJAVkNCRQN7ajBS+U0lGFFApAIAekpgJ5TQQBXQE8DzwZRmIuI2K0qMD0FAAKL0g8ZEAeKZkBAcKhCwA4gkAlA0V3gREbBAOGIAAWgABtQFgEgA8VgMCCP4A6h0yZAuM0Cd5HcQJ0JsyhOB7FvRAAAAD0QAvV5NTX2AAAAAElFTkSuQmCC)
# Добрый день из перечисленного было сделано
1. написаны тесты
2. сделаны автодополнение (подсказки) при вводе города
3. при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
4. будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город
# Не успел
1. Сохранение часто посещаемых городов в кэш(Redis)
2. Деплой на сервер(на localhost не праивльно работает автоопределение города)
# Технологии
1. Django - для самого сайта
2. DRF - API 
3. requests - Запросы к API Яндекса(не сможете получить API ключи предоставлю свои TG: @fv_hr)
# Как запустить
# Клонирование репозитория
git clone https://github.com/scolopendra2/test_o-complex

# Установка и запуск виртуального окружения
python -m venv venv

venv/Scripts/activate

# Установка зависимостей
pip install -r requirements/prod.txt

# Подстановка секретных переменных в окружение
DJANGO_SECRET_KEY=django-insecure-rqyfsc01-r27ovwi-fx*8_knf=(qe#!8wn8g$n2c7@cxz$ga@*

DJANGO_DEBUG=True

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

API_KEY_LOCATOR=КЛЮЧ ОТ АПИ ЯНДЕКС ЛОКАТОРА

API_KEY_GEOCODER=КЛЮЧ ОТ АПИ ЯНДЕКС ГЕОКОДЕРА

API_KEY_WEATHER=КЛЮЧ ОТ АПИ ЯНДЕКС ПОГОДЫ

MYSQL_USER=

MYSQL_PASSWORD=

MYSQL_HOST=

MYSQL_PORT=

# Создание миграций
make mig
# Загрузка городов
make load
# Запуск сервера
make run
