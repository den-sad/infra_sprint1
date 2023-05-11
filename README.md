# infra_sprint1

### Проект предназначен для отработки практических навыков развертывания приложений на удленном сервере

### Как запустить проект

Склонируйте репозитарий с проектом

```
git clone git@github.com:den-sad/infra_sprint1.git
cd ./infra_sprint1
```

Установите и настройте Nginx, файрвол, certbot

```
sudo apt install nginx -y
sudo cp ./infra/default /etc/nginx/sites-enabled/default
sudo mkdir /var/www/kittygram
sudo mkdir /var/www/kittygram/media
sudo chown -R <имя_пользователя> /var/www/kittygram/media/
sudo systemctl start nginx

sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

sudo apt install snapd
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Разверните и активируйте виртуальное окружение в папке проекта, установите зависимости

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте файл окружения для django с данными SECRET_KEY
```
nano ../backend/kittygram_backend/.env
SECRET_KEY = 'django-insecure-secret-key'
```

Выполните миграции и создайте супер пользователя

```
cd ../backend
python3 manage.py migrate
python3 manage.py createsuperuser
```

Соберите статику для backend

```
python3 manage.py collectstatic
sudo cp -r ./static_backend/. /var/www/kittygram/
```

Создайте демона для управления django приложением

```
cd ..
sudo cp ./infra/gunicorn_kittigram  /etc/systemd/system/gunicorn_kittygram.service
sudo systemctl start gunicorn_kittygram
sudo systemctl enable gunicorn_kittygram
```


Установите Node.js и необходимые пакеты

```
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
cd ./frontend/
npm i
```

Соберите статику для frontend и backend

```
npm run build
sudo cp -r ./build/. /var/www/kittygram/
```


Получите сертификат

```
sudo certbot --nginx
sudo systemctl reload nginx
```

### Примечание
Для перенастройки проекта на другой адрес необходимо:

```
Изменить ip и адрес сервера в файле конфигурации Nginx
sudo nano /etc/nginx/sites-enabled/default
и удалить из него настройки certbot

Изменить в файле настроек django значение константы ALLOWED_HOSTS
nano backend/kittygram_backend/settings.py

Получить сертификат и перезагрузить Nginx
sudo certbot --nginx
sudo systemctl reload nginx
```
# Автор
Денис