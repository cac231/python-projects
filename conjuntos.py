array1 = []
array2 = []
interseção = []
exclusivo_1 = []
exclusivo_2 = []
uniao = []

while True:
    print("""
Menu
----
"S" -> Começar a preencher as arrays
"P" -> Printar as arrays
"I" -> Interseção entre as arrays
"D" -> Diferença entre as arrays
"U" -> União entre as arrays

"C" -> Limpar as arrays
"X" -> SAIR
""")
    
    def getInterseção():
        interseção.clear()
        # x = 0
        # y = 0
        # quantasVezes = len(array2)
        # while x != len(array1):
        #     while quantasVezes > 0:
        #         if array1[x] == array2[y] and array1[x] not in interseção:
        #             interseção.append(array1[x])
        #         y += 1 
        #         quantasVezes -= 1
        #     x += 1
        #     y = 0
        #     quantasVezes = len(array2)
        for el in array1:
            if el in array2 and el not in interseção:
                interseção.append(el)
    
    def getCompararArrays(lista_1, lista_2, exclusivo):
        return [i for i in lista_1 if i not in lista_2 and i not in exclusivo]

    def getLimparTudo():
        array1.clear()
        array2.clear()
        interseção.clear()
        exclusivo_1.clear()
        exclusivo_2.clear()
        uniao.clear()

    def getPreencherArrays(array, array_numero):
        while True:
            try:
                quantidade = int(input(f"\n -- Quantos números terá a array {array_numero}? "))
                
                if quantidade <= 0:
                    print("\n -- Erro: Digite uma quantidade positiva...")
                    continue

                for i in range(quantidade):
                    while True:
                        try:
                            numeros_array = int(input(f"Digite um número ({i+1}/{quantidade}): "))
                            array.append(numeros_array)
                            break
                        except ValueError:
                            print("\n -- Erro: Digite um número válido...")
                return True
            
            except ValueError:
                print("\n -- Erro: Digite uma quantidade válida...")
    
    def isPreenchida():
        if not array1 or not array2:
            print("\n -- Erro: Preencha as duas arrays primeiro (opção \"S\")")
            return False
        return True
    
    def getRepetição(array):
        resultado = []
        for el in array:
            if el not in resultado:
                resultado.append(el)
        array.clear()
        array.extend(resultado)

    escolha = input("\n -- Escolha uma opção: ").strip().lower()
    
    if escolha == "s":
        getLimparTudo()
        print("\n -- Preenchendo a array 1")
        if getPreencherArrays(array1, 1):
            print("\n -- Preenchendo a array 2")
            getPreencherArrays(array2, 2)
        getRepetição(array1)
        getRepetição(array2)
    
    elif escolha == "p":
        print(f"Array 1: {sorted(array1)}")
        print(f"Array 2: {sorted(array2)}")
        print(f"Interseção: {sorted(interseção)}")
        print(f"Diferença da 1: {sorted(exclusivo_1)}")
        print(f"Diferença da 2: {sorted(exclusivo_2)}")
        print(f"União: {sorted(uniao)}")

    elif escolha == "i":
        if isPreenchida():
            getInterseção()
            print("\n -- Interseção concluída...")

    elif escolha == "d":
        if isPreenchida():
            getInterseção()
            exclusivo_1.clear()
            exclusivo_2.clear()
            exclusivo_1 = getCompararArrays(array1, array2, exclusivo_1)
            exclusivo_2 = getCompararArrays(array2, array1, exclusivo_2)
            print("\n -- Diferenças concluídas...")

    elif escolha == "u":
        if isPreenchida():
            uniao.clear()
            interseção.clear()
            getInterseção()
            
            for el in array1:
                if el not in interseção:
                    uniao.append(el)
            for el in array2:
                uniao.append(el)

            print("\n -- União concluída...")   
        
    elif escolha == "c":
        getLimparTudo()
        print("\n -- Limpas...")

    elif escolha == "x":
        print("\n -- Saindo...")
        break

    else:
        print("\n\n -- Erro: Opção inválida")