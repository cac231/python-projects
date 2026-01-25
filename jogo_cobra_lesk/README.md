## Requisitos para executar o jogo

- Python 3.10 ou superior

### Módulo obrigatório

- Pygame ou Pygame-ce (dê preferência ao Pygame-ce)
pip install pygame-ce

### Módulo opcional (Windows)

- pywinstyles
pip install pywinstyles


## Como executar (Multiplataforma)

1. Usando o terminal:

* Pela pasta do jogo:
python jogo_cobra_lesk.py

* Pelo caminho completo do arquivo:
python "caminho do arquivo .py"


## Como executar no Windows (.exe)

1. Instale o PyInstaller
pip install pyinstaller

2. Gere o executável usando o arquivo .spec:

* Pela pasta do jogo
pyinstaller jogo_cobra_lesk.spec

* Pelo caminho completo do arquivo .spec
pyinstaller "caminho do arquivo .spec"

3. Após a conversão, o executável será gerado na pasta
dist/jogo_cobra_lesk.exe