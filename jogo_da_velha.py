import random
import time
from colorama import init, Fore

init()
cor = {
   "blueUP": Fore.LIGHTBLUE_EX,
   "cyan": Fore.CYAN,
   "red": Fore.RED,
   "redUP": Fore.LIGHTRED_EX,
   "yellow": Fore.YELLOW,
   "green": Fore.GREEN,
   "reset": Fore.RESET,
}


numJogo = [0, 1, 2, 3, 4, 5, 6, 7, 8]

simbolo_O = f"{cor['redUP']}O{cor['reset']}"
simbolo_X = f"{cor['green']}X{cor['reset']}"
simbolo_O = f"O"
simbolo_X = f"X"

jogo = [
    0, 1, 2, 
    3, 4, 5, 
    6, 7, 8
]
def desenho(jogo):
    jogo = rf"""
 {jogo[0]} | {jogo[1]} | {jogo[2]}
---|---|---
 {jogo[3]} | {jogo[4]} | {jogo[5]}
---|---|---  
 {jogo[6]} | {jogo[7]} | {jogo[8]}
"""
    return jogo

vitoria = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 6],
    [0, 4, 8], [6, 4, 2]
]

def isVitoria(simbolo):
    for combinacao in vitoria:
        if (jogo[combinacao[0]] == simbolo and 
            jogo[combinacao[1]] == simbolo and 
            jogo[combinacao[2]] == simbolo):
            return True
    return False

def getJogadaCPU(array):
    jogada = [i for i, x in enumerate(jogo) if x in array]
    return random.choice(jogada)
    
jogoCANTO = [0, 2, 6, 8]
jogoMEIO = [1, 3, 5, 7]

def getCpuInteligente(round, pri): 
    cantoDISPONIVEL = [i for i in jogoCANTO if i in numJogo]
    
    if round == 1 and pri == 2:
        return jogo[random.choice(cantoDISPONIVEL)]
    
    if round == 2 and pri == 1:
        for i in jogoCANTO:
            posição = [z for z in jogo[i]]
            if posição.count(simbolo_X) != 0:
                return 4
            
    
    for combinacao in vitoria:
        posição = [jogo[i] for i in combinacao]

        if posição.count(simbolo_O) == 2 and posição.count(simbolo_X) == 0: # BOT PARA GANHAR
            for i in [0, 1, 2]:
                if combinacao[i] in jogo:
                    return combinacao[i]
                
        if posição.count(simbolo_X) == 2 and posição.count(simbolo_O) == 0: # BOT PARA BLOQUEAR
            for i in [0, 1, 2]:
                if combinacao[i] in jogo:
                    return combinacao[i]
    
    return getJogadaCPU(numJogo)






    
    
    
    




while True:

    jogo = [
    0, 1, 2, 
    3, 4, 5, 
    6, 7, 8
]
    def desenho(jogo):
        jogo = rf"""
 {jogo[0]} | {jogo[1]} | {jogo[2]}
---|---|---
 {jogo[3]} | {jogo[4]} | {jogo[5]}
---|---|---  
 {jogo[6]} | {jogo[7]} | {jogo[8]}
"""
        return jogo
    
    print(
f"""{cor['blueUP']}
===========# JOGO DA VELHA - YEAH #===========

(1) - Comece o insano jogo com um robô...
(0) - Sair do jogo com o cu da mão de medo

==============================================
{cor['reset']}""")
    
    escolha = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

    if escolha == "1":
        print(
f"""{cor['blueUP']}
================# DIFICULDADE #================

(1) - Burro -> jogo com um burro
(0) - Inteligente -> jogue com um inteligente

===============================================
{cor['reset']}""")
        
        dificuldade = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

        if dificuldade == "1":
            print("BURRO")
            print(desenho(jogo))
            primeiroJOGAR = random.randint(1, 2)

            if primeiroJOGAR == 2:
                print("\n# O robô vai começar...")
                jogo[getJogadaCPU()] = simbolo_O
                print(desenho(jogo))

            while True:
                try:
                    escolhaX = int(input(f"\n{cor['cyan']}Quer marcar o seu X onde? {cor['reset']}"))

                    if jogo[escolhaX] in [simbolo_O, simbolo_X]:
                        print("\n# Já tem algo marcado ai burro")
                        continue
                    else:
                        jogo[escolhaX] = simbolo_X
                    print(desenho(jogo))

                    if isVitoria(simbolo_X) == True:
                        print("\n# VOCÊ GANHOU HAHAH mas era o burro então lol")
                        break
                    
                    jogo[getJogadaCPU(numJogo)] = simbolo_O
                    print(desenho(jogo))
                    if isVitoria(simbolo_O) == True:
                        print("\n# VOCÊ PERDEUKKKKKKKKKKKKKK ok")
                        break

                except IndexError:
                    print(f"\n{cor['red']}# Digite um número entre 0 a 9 mn{cor['reset']}")

        if dificuldade == "0":
            print("INTELIGENTE")
            print(desenho(jogo))
            primeiroJOGAR = random.randint(1, 2)

            round = 1
            
            if primeiroJOGAR == 2:
                print("\n# O robô vai começar...")
                jogo[getCpuInteligente(round, primeiroJOGAR)] = simbolo_O
                print(desenho(jogo))
                round += 1

            while True:
                try:
                    escolhaX = int(input(f"\n{cor['cyan']}Quer marcar o seu X onde? {cor['reset']}"))
                    round += 1
                except IndexError:
                    print(f"\n{cor['red']}# Digite um número entre 0 a 9 mn{cor['reset']}")
                    continue

                if jogo[escolhaX] in [simbolo_O, simbolo_X]:
                    print("\n# Já tem algo marcado ai burro")
                    continue
                else:
                    jogo[escolhaX] = simbolo_X
                print(desenho(jogo))

                if isVitoria(simbolo_X) == True:
                    print("\n# VOCÊ GANHOU HAHAH mas era o burro então lol")
                    break

                if sum(1 for x in numJogo if x in jogo) == 0:
                    print("EMPATE")
                    break
                
                jogo[getCpuInteligente(round, primeiroJOGAR)] = simbolo_O
                round += 1
                
                print(desenho(jogo))
                
                if isVitoria(simbolo_O) == True:
                    print("\n# VOCÊ PERDEUKKKKKKKKKKKKKK ok")
                    break

                if sum(1 for x in numJogo if x in jogo) == 0:
                    print("EMPATE")
                    break

                    

                










    
    
    
    
    
    
    
    
    
    elif escolha == "0":
        print("\n# Tchau ahh")
        break

    else:
        print("\n# Digita certo mano kkkk 1 ou 0")