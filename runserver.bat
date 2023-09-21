@echo off

pushd "C:\Users\rmizukosi\Desktop\Projetos_Lanmax\Web\django_lanmax\"
call ".\env\Scripts\activate.bat"
waitress-serve --port=8001 django_lanmax.wsgi:application