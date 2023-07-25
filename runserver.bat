@echo off

pushd "C:\Users\rmizukosi\Desktop\Projetos_Lanmax\Web\django_lanmax\"
call ".\env\Scripts\activate.bat"
python manage.py runserver 192.168.10.42:8001