Обеспечение работы нового сайта
===============================

* nginx
* virtualenv + pip
* Git sudo apt update ssh root@your_server_ip adduser kvin usermod -aG sudo kvin

ufw app list 
ufw allow OpenSSH 
ufw enable 
ufw status

ssh kvin@your_server_ip sudo command_to_run rsync --archive --chown=kvin:kvin ~/.ssh /home/kvin ssh kvin@your_server_ip

sudo add-apt-repository ppa:fkrull/deadsnakes sudo apt install python3-pip python3-dev libpq-dev nginx curl

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com

## Служба Systemd

* см. gunicorn-systemd.template.service
* заменить SITENAME, например на staging.my-domain.com

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username

/home/username
-- sites
---- SITENAME
------- database
------- source
------- static
------- virtualenv