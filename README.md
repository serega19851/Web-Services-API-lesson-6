# Web-Services-API-lesson-6

# Проект публикует комиксы в контакте 

### Файл main.py
При запуске создает внутри проекта каталог,
закачивает туда рандомный комикс из сайта (https://xkcd.com/353/) и публикует его на стене сообщества, 
после публикации удаляет комикс из каталога.

### Технологии
- Python 3.10
- requests 2.28.1
- python-dotenv 0.9.1

### Запуск проекта
- Зайдите по ссылки (https://github.com/serega19851/Web-Services-API-lesson-6), клонируйте проект к себе локально.
- Установите и активируйте виртуальное окружение внутри проекта
```
sudo apt install python3.10-venv
python3.10 -m venv venv
```
- Установите зависимости в активированном виртуальном окружении из файла requirements.txt
```
python3.10 -m pip install -r requirements.txt
```
- установку зависимостей можно проверить командой 
```
python3.10 -m pip list
```
### Создайте группу в контакте
Инструкция: https://vk.com/@tectgryppa-poshagovaya-instrukciya-po-sozdaniu-gruppy-v-vk

### Создайте приложение 
- Тип приложения standalone 
- Чтобы работать со своим приложением, надо знать его client_id

https://vk.com/dev

### Получите личный ключ
 Вам потребуются следующие права: photos, groups, wall и offline.

Инструкция: https://dev.vk.com/api/access-token/implicit-flow-user

Если в адресной строке появился code= вместо access_token=,
проверьте правильность параметра response_type.

### Создаем файл .env в папке проекта, командой в терминале.
```
touch .env
```
### В файл .env прописываем переменную.
```
VK_TOKEN=ваш токен 
```
### Команда запуска файла, производится в папке проекта.
```
python3.10 main.py 
```