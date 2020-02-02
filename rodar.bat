@echo off
REM -----------------------------------------
REM    Mude a variável SILENCIAR para False
REM    (em marcador.py) para acompanhar ...
REM    todos os detalhes de cada turno do jogo
REM -----------------------------------------
python banco_imobiliario.py > teste.txt
start notepad teste.txt
