@echo off
set LOG_DIR=C:\Users\Ekenair\Documents\Code Files\python\projects\trydjango\django_4.x_code\stock-startup\src\stockStartup
set DJANGO_PATH=C:\Users\Ekenair\Documents\Code Files\python\projects\trydjango\django_4.x_code\stock-startup\src\stockStartup
set UPDATE_STOCK_PRICES=update_stock_prices
set UPDATE_HISTORICAL_STOCK_PRICES=update_historical_stock_prices

cd %DJANGO_PATH%
python manage.py %UPDATE_STOCK_PRICES%
python manage.py %UPDATE_HISTORICAL_STOCK_PRICES%