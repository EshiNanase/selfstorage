# selfstorage

## Настройка переменных окружения

Для работы сайта необходимо определить 2 переменных:
```sh
DJANGO_SECRET_KEY = MY_KEY
DEBUG = True
```
Для отправки писем необходимо добавить еще 4 переменные:
```sh
EMAIL_NOTIFIER_LOGIN = login@email.ru
EMAIL_NOTIFIER_PASSWORD = password
EMAIL_NOTIFIER_SMTP_SERVER = 'smtp.mail.ru'
EMAIL_NOTIFIER_SMTP_SERVER_PORT = 465
```
