# selfstorage

## Настройка переменных окружения

Для работы геокодера необходима 1 переменная:
```sh
YANDEX_API_TOKEN =
```

Для работы сайта необходимо определить 2 переменных:
```sh
DJANGO_SECRET_KEY = MY_KEY
DEBUG = True
```

Для работы Stripe необходимы следующие 3 переменные:
```sh
STRIPE_PUBLIC_KEY =
STRIPE_SECRET_KEY =
STRIPE_WEBHOOK_SECRET =
BOX_STRIPE_ID =
```

Для отправки писем необходимо добавить еще 4 переменные:
```sh
EMAIL_NOTIFIER_LOGIN = login@email.ru
EMAIL_NOTIFIER_PASSWORD = password
EMAIL_NOTIFIER_SMTP_SERVER = 'smtp.mail.ru'
EMAIL_NOTIFIER_SMTP_SERVER_PORT = 465
```
