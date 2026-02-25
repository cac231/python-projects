lista_1 = []
lista_2 = []
intersecao = []
exclusivo_1 = []
exclusivo_2 = []
uniao = []
subconjuntos = {}

def limpar_tudo():
    lista_1.clear()
    lista_2.clear()
    intersecao.clear()
    exclusivo_1.clear()
    exclusivo_2.clear()
    uniao.clear()
    subconjuntos.clear()

def esta_preenchida():
    if not lista_1 or not lista_2:
        print("\n -- Erro: Não preencheu as listas (opção: 2)")
        return False
    return True

def confirmar_limpar_listas(frase):
    if len(lista_1) != 0 or len(lista_2) != 0:
        print(frase)
        while True:
            resposta = input(f"\n -- Digite 's' ou 'n': ")
            if resposta == "s":
                return True
            elif resposta == "n":
                return False
            else:
                print("\n -- Erro: Resposta inválida")
    return True

def preencher_listas(array, array_numero):
    while True:
        try:
            quantidade = int(input(f"\n -- Quantos números terá a lista {array_numero}? "))
            if quantidade <= 0:
                print("\n -- Erro: Digite uma quantidade positiva...")
                continue
            print()    
            for i in range(quantidade):
                while True:
                    try:
                        numero = int(input(f"Digite um número ({i+1}/{quantidade}): "))
                        array.append(numero)
                        break
                    except ValueError:
                        print("\n -- Erro: Digite um número válido...\n")
            return True
        except ValueError:
            print("\n -- Erro: Digite uma quantidade válida...")

def gerar_intersecao():
    return [el for el in lista_1 if el in lista_2 and el not in intersecao]

def gerar_diferenca(lista_1, lista_2, exclusivo):
    return [i for i in lista_1 if i not in lista_2 and i not in exclusivo]

def gerar_uniao():
    uniao_temp = []
    for el in lista_1:
        if el not in lista_2:
            uniao_temp.append(el)
    uniao_temp += lista_2
    return uniao_temp

def gerar_subconjuntos():
    subconjuntos["lista_1"] = 2 ** len(lista_1)
    subconjuntos["lista_2"] = 2 ** len(lista_2)

def retirar_repeticao(array):
    resultado = []
    for el in array:
        if el not in resultado:
            resultado.append(el)
    array.clear()
    array.extend(resultado)

menu = f"""\n\n
{" Menu ":-^40}
1 -> Limpar as listas

2 -> Preencher as duas listas
3 -> Mostrar as listas
4 -> intersecao entre as listas
5 -> Diferença entre as listas
6 -> União entre as listas
7 -> Subconjuntos das duas listas separadamente

0 -> SAIR
{"-" * 40}"""

print(menu)

while True:
    escolha = input("\n -- Escolha uma opção: ").strip()
    
    if escolha == "2":
        if confirmar_limpar_listas("\n -- Quer mesmo preencher novamente?"):
            limpar_tudo()
            print("\n -- Preenchendo a lista 1")
            if preencher_listas(lista_1, 1):
                print("\n -- Preenchendo a lista 2")
                preencher_listas(lista_2, 2)
            retirar_repeticao(lista_1)
            retirar_repeticao(lista_2)
            print("\n -- Preenchimento concluído...")
        print(menu)
        
    elif escolha == "3":
        print(f"\n\n\n{" Operações ":-^40}")
        print(f"Lista_1: {lista_1}")
        print(f"Lista_2: {lista_2}")
        print(f"\ninterseção: {intersecao}")
        print(f"\nDiferença da 1: {exclusivo_1}")
        print(f"Diferença da 2: {exclusivo_2}")
        print(f"\nUnião: {uniao}")
        print(f"\nSubconjunto: {subconjuntos}")
        print("" + "-" * 40)
        print(menu)

    elif escolha == "4":
        if esta_preenchida():
            intersecao.clear()
            intersecao = gerar_intersecao()
            print("\n -- interseção concluída...")

    elif escolha == "5":
        if esta_preenchida():
            exclusivo_1.clear()
            exclusivo_2.clear()
            exclusivo_1 = gerar_diferenca(lista_1, lista_2, exclusivo_1)
            exclusivo_2 = gerar_diferenca(lista_2, lista_1, exclusivo_2)
            print("\n -- Diferenças concluídas...")

    elif escolha == "6":
        if esta_preenchida():
            intersecao_temp = gerar_intersecao()
            uniao.clear()
            uniao = gerar_uniao()
            print("\n -- União concluída...")
    
    elif escolha == "7":
        if esta_preenchida():
            subconjuntos.clear()
            gerar_subconjuntos()
            print("\n -- Subconjuntos concluídos...")
                    
    elif escolha == "1":
        if confirmar_limpar_listas("\n -- Quer mesmo limpar as listas?"):
            limpar_tudo()
            print("\n -- Listas limpas...")
        print(menu)

    elif escolha == "0":
        print("\n -- Saindo...")
        break

    else:
        print("\n -- Erro: Opção inválida")