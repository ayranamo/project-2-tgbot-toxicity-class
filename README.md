# project-2-tgbot-toxicity-class
Проект для курса по организации процессов c DS и ML на Stepik.org

## Описание проекта

В рамках проекта необходимо реализовать бота для Telegram, который будет классифицировать тексты по уровню токсичности в виде вероятностной школы.

В блокноте dataset.txt находится модель для определения степени токсичности текстовых комментариев.

# Инструкция

Настроим бота для Telegram. Для этого необходимо создать бота с помощью @BotFather. После этого получим токен для доступа к HTTP API. Токен необходимо сохранить в переменной TOKEN. 

## Запуск

1. Убедитесь, что у вас установлены установщики Windows MacOS Unix 

2. Создайте виртуальное окружение и устанавливаем зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Создайте бота и получите telegram-токен:
- Напишите https://t.me/BotFather и введите команду /newbot
- Введите имя нового бота и его юзернейм
- Скопируйте и вставьте в ячейку ниже токен, который отправит вам BotFather. Это ключ от управления свежесозданным ботом.

4. Введите команду в командой строке:
~~~
export TOKEN="<Введите сюда свой telegram-токен>"
~~~

5. Запустите бота командой:
~~~
python3 main.py
~~~



### Благодарности в помощи в создании данного проекта:
1. Давиду Дале, NLP-исследователю https://daviddale.ru/
2. Байлак Монгуш, DevOps-инженеру https://github.com/npetrelli/
