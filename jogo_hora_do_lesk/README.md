## Requisitos

- Python 3.10 ou superior

### Dependência obrigatória

Instale **Pygame** ou **Pygame-ce** (recomendado):

```bash
pip install pygame-ce
```

### Dependência opcional (Windows)

Para recursos visuais exclusivos do Windows:

```bash
pip install pywinstyles
```

---

## Executando o jogo

### Pelo terminal

Na pasta do projeto:

```bash
python hora_do_lesk.py
```

Ou utilizando o caminho completo do arquivo:

```bash
python "caminho/do/hora_do_lesk.py"
```

---

## Gerando um executável (Windows)

### 1. Instale o PyInstaller

```bash
pip install pyinstaller
```

### 2. Gere o executável

Na pasta do projeto:

```bash
pyinstaller hora_do_lesk.py.spec
```

Ou utilizando o caminho completo do arquivo `.spec`:

```bash
pyinstaller "caminho/do/hora_do_lesk.py.spec"
```

### 3. Localize o executável

Após a compilação, o executável será criado em:

```text
dist/Hora_do_Lesk.exe
```
```