@echo off
cd /d C:\ibkr-trading\TradingSystems\laughing-spoon

echo ================================
echo CURRENT GIT STATUS
echo ================================
git status

echo ================================
echo SWITCHING TO CLEAN BUILD BRANCH
echo ================================
git fetch origin
git switch clean-build-ml-scanner 2>NUL || git switch -c clean-build-ml-scanner

echo ================================
echo CREATING CLEAN BUILD FOLDERS
echo ================================
if not exist app mkdir app
if not exist app\broker mkdir app\broker
if not exist app\data mkdir app\data
if not exist app\strategies mkdir app\strategies
if not exist app\scanner mkdir app\scanner
if not exist app\risk mkdir app\risk
if not exist app\execution mkdir app\execution
if not exist app\ml mkdir app\ml
if not exist app\monitoring mkdir app\monitoring
if not exist tests mkdir tests
if not exist docs mkdir docs

echo ================================
echo COPYING ORIGINAL BOT FILES
echo ================================
if exist 01_connect.py copy /Y 01_connect.py app\broker\ibkr_client.py
if exist 02_strategy.py copy /Y 02_strategy.py app\strategies\moving_average.py
if exist 03_order_execution.py copy /Y 03_order_execution.py app\execution\order_manager.py
if exist 04_risk_management.py copy /Y 04_risk_management.py app\risk\risk_limits.py
if exist 05_live_bot.py copy /Y 05_live_bot.py app\main.py
if exist 06_backtest.py copy /Y 06_backtest.py tests\backtest_single_asset.py
if exist 07_backtest_multi_assets.py copy /Y 07_backtest_multi_assets.py tests\backtest_multi_asset.py
if exist 08_live_multi_asset_bot.py copy /Y 08_live_multi_asset_bot.py app\main_multi_asset.py
if exist 09_live_multi_asset_bot.py copy /Y 09_live_multi_asset_bot.py app\main_multi_asset_v2.py
if exist 10_live_multi_asset_bot.py copy /Y 10_live_multi_asset_bot.py app\main_live.py
if exist ib_ma_multi.py copy /Y ib_ma_multi.py app\strategies\ib_ma_multi.py
if exist ib_ma_30_test.py copy /Y ib_ma_30_test.py tests\test_ib_ma_30.py
if exist Data\tickers_us_clean.txt copy /Y Data\tickers_us_clean.txt app\data\tickers_us_clean.txt
if exist strategies\macross_bt.py copy /Y strategies\macross_bt.py app\strategies\macross_bt.py

echo ================================
echo CREATING PYTHON PACKAGE FILES
echo ================================
type nul > app\__init__.py
type nul > app\broker\__init__.py
type nul > app\data\__init__.py
type nul > app\strategies\__init__.py
type nul > app\scanner\__init__.py
type nul > app\risk\__init__.py
type nul > app\execution\__init__.py
type nul > app\ml\__init__.py
type nul > app\monitoring\__init__.py
type nul > tests\__init__.py

echo ================================
echo GIT ADD / COMMIT / PUSH
echo ================================
git status
git add .
git commit -m "Create clean build structure from original bot scripts"
git push -u origin clean-build-ml-scanner

echo ================================
echo DONE
echo ================================
git status
pause