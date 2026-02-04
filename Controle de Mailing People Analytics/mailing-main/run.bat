@echo off
cls

echo ==============================
echo   PEOPLE ANALYTICS - PIPELINE
echo ==============================
echo.
echo 1 - CLEAN (Limpeza + Divisao CSV)
echo 2 - COMPILAR EXCEL
echo.

set /p choice=Escolha uma opcao (1 ou 2): 

if "%choice%"=="1" (
    echo.
    echo Executando CLEAN...
    python src/clean.py
) else if "%choice%"=="2" (
    echo.
    echo Executando COMPILACAO DE EXCEL...
    python src/compila_excel.py
) else (
    echo Opcao invalida.
)

echo.
pause
