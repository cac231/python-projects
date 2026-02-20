## Requisitos para executar o jogo

- Python 3.10 ou superior

### Módulo obrigatório
- Pygame ou Pygame-ce (dê preferência ao Pygame-ce) 
```bash
pip install pygame-ce
```

### Módulo opcional (Windows)
- pywinstyles
```bash
pip install pywinstyles
```

## Como executar (Multiplataforma)

### 1. Usando o terminal
* Pela pasta do jogo
```bash
python hora_do_lesk.py
```

* Pelo caminho completo do arquivo
```bash
python "caminho_do_arquivo.py"
```

## Como executar no Windows (.exe)

### 1. Instale o PyInstaller
```bash
pip install pyinstaller
```

### 2. Gere o executável usando o arquivo .spec
* Pela pasta do jogo
```bash
pyinstaller hora_do_lesk.py.spec
```

* Pelo caminho completo do arquivo .spec
```bash
pyinstaller "caminho_do_arquivo.spec"
```

### 3. Após a conversão, o executável será gerado na pasta
```bash
dist/Hora_do_Lesk.py.exe
```