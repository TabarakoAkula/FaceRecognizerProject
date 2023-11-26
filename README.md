# FaceRecognizerProject

### Python version - 3.10

### BD - SQLite3
---
## Клонирование проекта
```bash
git clone https://github.com/TabarakoAkula/FaceRecognizerProject
```
## Обновление pip:  
+ Windows:
```bash
python -m pip install -U pip 
```

+ Linux:
```bash
pip install -U pip
```

---

## Создание виртуального окружения:  
+ Windows:
```cmd
python -m venv venv
venv\Scripts\activate.bat 
```

+ Linux: 
```bash
python3 -m venv venv
source venv/bin/activate 
```

---

## Установка зависимостей
+ Для работы приложения:
```bash
pip install -r requirements/prod.txt
```
Дополнительно:
+ Для дебага ошибок: 
```bash
pip install -r requirements/test.txt
```

---


## Настройка .env файла:  
Заполните данные в файле ``.env.template`` и после переименуйте файл в ``.env``

---

## Запуск  
Запустите файл main.py без каких либо аргументов с помощью команды:
```bash
python main.py
```