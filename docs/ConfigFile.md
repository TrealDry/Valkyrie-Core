Для начала создайте отдельный файл конфига, с расширением *.config.json* (или *.secret.config.json*, чтобы git не учитывал его)

```bash
cp ./configs/standard.config.json ./configs/example.config.json
```

Далее редактируйте на свой вкус!

Комментарии к стандартному шаблону конфига:
```json
{
  "server_setts": {
    "name": "Geometry Dash Example Server",  // название вашего приватного сервера
    "discord_link": "https://discord.com/",  // перекидывает на ваш дискорд сервер по ссылке ( https://example.com/discord )

    "domain": "https://example.com",  // http(s)://(домен или ip) (без / в конце)

    "path_to_api": "/api",  // https://example.com/api и так далее
    "path_to_song": "/song",
    "path_to_database": "/database/db",

    "command_prefix": "!",

    "max_content_length": 52428800
  },

  "secret_setts": {
    "mail": {
      "ip": "",  // работает только в режиме TLS
      "port": 0,
      "username": "",
      "password": ""
    },

    "mongo": {
      "uri": "mongodb://mongo:27017",
      "db_name": "vcore"
    },

    "redis": {
      "ip": "localhost",
      "port": 6379,
      "password": "",
      "prefix": "VCORE"
    },

    "hcaptcha": {
      "site_key": "",  // читайте HcaptchaGuide.md
      "secret_key": ""
    }

  },

  "security_setts": {
    "accounts_activation_via_mail": false,
    "dislike_bot_protection": false  // Включайте, если сервер наводнили дизлайк боты
  },

  "debug_setts": {
    "host": {
      "ip": "0.0.0.0",
      "port": 5000
    },

    "flask_debug": false
  }

}
```