env_body = ('MAIL_SERVER=""\n'
            'MAIL_USERNAME=""\n'
            'MAIL_PASSWORD=""\n'
            'MAIL_PORT=""\n'
            'MONGO_URI=""\n'
            'MONGO_NAME=""\n'
            'REDIS_HOST=""\n'
            'REDIS_PORT=""\n'
            'REDIS_PASSWORD=""\n'
            'REDIS_PREFIX=""\n'
            'HCAPTCHA_SITE_KEY=""\n'
            'HCAPTCHA_SECRET_KEY=""\n')

with open("../../.env", "w") as file:
    file.write(env_body)
