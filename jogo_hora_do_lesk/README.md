## OBJETIVO

Jogo desenvolvido com Pygame que apresenta alta dificuldade e progressão de níveis, aumentando a velocidade do jogo a cada fase.

## REQUISITOS

- Python 3.10 ou superior
- Pygame ou Pygame-ce (recomendado)

```bash
pip install pygame-ce
```

### Dependência opcional (Windows)

Para recursos visuais exclusivos do Windows:

```bash
pip install pywinstyles
```

## ESTRUTURA DO PROJETO

Para funcionar corretamente, mantenha os seguintes arquivos e pastas na mesma estrutura do projeto:

- `hora_do_lesk.py`
- pasta `assets`

## EXECUÇÃO

Pelo terminal, na pasta do projeto:

```bash
python hora_do_lesk.py
```

Ou utilizando o caminho completo:

```bash
python "caminho/do/hora_do_lesk.py"
```

## EXECUTÁVEL (Windows)

Para gerar o executável:

### Instale o PyInstaller

```bash
pip install pyinstaller
```

### Gere o executável utilizando o arquivo `.spec`

Pela pasta do projeto:

```bash
pyinstaller hora_do_lesk.py.spec
```

Ou utilizando o caminho completo:

```bash
pyinstaller "caminho/do/hora_do_lesk.py.spec"
```

Após a compilação, o executável será gerado em:

```text
dist/Hora_do_Lesk.exe
```