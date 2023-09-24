# FaceRecognizerProject

### Python version - 3.10

### BD - PostgreSQL 16.0
---

## Создание базы данных:

1) Установите PostgreSQL:

+ Windows:

    + Скачайте и установите PostgreSQL с официального
      сайта ([Скачать можно тут](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads "Переход на официальный сайт"))
    + Откройте папку, в которую была произведена установка и перейдите в директорию bin (C:\Program
      Files\PostgreSQL\16\bin).
    + Откройте из данной папки терминал

+ Linux:
    + Введите в терминал:  
      `sudo apt-get install postgresql`
    + Произведите установку

---

2) Откройте терминал
3) Введите команду
   `psql -U postgres`
   и после пароль, который вы задали ранее
3) После ввода пароля создайте базу данных с таблицей, для этого введите в терминал

``` sql 
CREATE DATABASE my_db;
```  

``` sql
CREATE TABLE users  
                                  (id INT PRIMARY KEY     NOT NULL,  
                                  name           TEXT    NOT NULL,  
                                  profile_photo_address         TEXT NOT NULL);
```

4) Проверьте, создалась ли база данных с указанным именем, введя в терминал команду
   `\l`

5) Если все успешно, можете переходить к запуску программы

---