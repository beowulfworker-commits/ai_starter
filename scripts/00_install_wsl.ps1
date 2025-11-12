# Запустите от имени администратора при необходимости установки WSL
wsl --install -d Ubuntu-24.04
wsl --set-default-version 2
wsl --update
wsl -l -v
