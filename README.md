[![Flake8 + Black](https://github.com/TabarakoAkula/FaceRecognizerProject/actions/workflows/github-ci.yml/badge.svg)](https://github.com/TabarakoAkula/FaceRecognizerProject/actions/workflows/github-ci.yml)
# **FaceRecognizerProject**

<h2> Python version - 3.10 <br> BD - SQLite3</h2>

<details>
<summary><h2>Установка</h2></summary>

<h3>Клонирование проекта</h3>

```bash
git clone https://github.com/TabarakoAkula/FaceRecognizerProject
```
<h3>Обновление pip:</h3>

+ Windows:  
```bash
python -m pip install -U pip 
```

+ Linux:
  
```bash
pip install -U pip
```

---

<h3>Создание виртуального окружения:  </h3>

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

<h3>Установка зависимостей</h3>

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


<h3>Настройка .env файла:  </h3>

Заполните данные в файле ``.env.template`` и после переименуйте файл в ``.env``
</details>

<details>
<summary><h2>Первый запуск</h2></summary>
    
Запустите файл main.py без каких либо аргументов с помощью команды:
```bash
python main.py
```

<h3>Настройка</h3>

+   Первым делом вам необходимо создать файл базы данных и свою первую таблицу,
    для этого перейдите в ``Model --> Create table`` и введите название для
    таблицы c пользователями. После чего откройте ваш ``.env`` файл и запишите в переменную
    ``TABLE_NAME`` название своей таблицы.
+   Теперь вы можете добавлять информацию в свою базу данных. Для начала
    создайте своего первого пользователя, для этого перейдите в ``Model --> Add user``
    и введите имя для нового пользователя.
+ Для обучения модели на лицах нужно пройти несколько шагов:
  +   Создайте новые фотографии лица. Перейдите в ``Dataset --> Get New`` и введите ``id``
      пользователя, для которого вы хотите добавить фото. После чего выберите количество фотографий
      для обучения (рекомендуется указывать число 200).  
      Выберите: хотите ли вы видеть как вас снимает
      программа, указав ``Y`` или ``N`` в выборе. Теперь вам необходимо просто дождаться того, как все
      фотографии будут сделаны и обрезаны.  
      <br>
      **ВАЖНО:** Камере необходимо достаточно много света, иначе она будет медленно работать и может
      некорректно обрабатывать фотографии.  
      <br>
  +   Теперь нужно обучить модель на наших фото, для этого выберите в меню пункт ``Training`` (`Dataset --> Training`).  
      Выберите: хотите ли вы просматривать как работает программа, или нет с помощью `Y` и `N`.
      После завершения обучения программа укажет путь, по которому находиться ``.yml`` файл со всеми данными.
  +   Теперь можете запускать пункт ``Checker``(``Checker``, ``Dataset --> Checker``).  
      В течение 5 секунд программа будет собирать данные о лицах с камеры и после чего выведет в консоль 
      предполагаемое имя пользователя и процент совпадения с фотографиями из датасета.
</details>
<details>
<summary><h2>Тесты</h2></summary>

<h3>Проверка линтерами</h3>

Для проекта используются 2 линтера: ``flake8`` и ``black``. Чтобы проверить чистоту своего кода выполните следующее:
+ Установите зависимости для теста:
  ```bash
    pip install -r requirements/test.txt
    ```
+ Запустите ``flake8``:
    ```bash
    flake8 --verbose --max-line-length=79 --inline-quotes="double" --docstring-quotes="double" .
    ```
+ Запустите ``black``:
    ```bash
    black --check --verbose --diff --skip-string-normalization --line-length 79 --color .
    ```
Теперь вы можете просмотреть где можно улучшить свой код :) 
</details>
