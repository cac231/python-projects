import random
import time
from colorama import init, Fore

init()
cor = {
   "blueUP": Fore.LIGHTBLUE_EX,
   "cyan": Fore.CYAN,
   "redUP": Fore.LIGHTRED_EX,
   "yellow": Fore.YELLOW,
   "green": Fore.GREEN,
   "black": Fore.LIGHTBLACK_EX,
   "reset": Fore.RESET,
}

simbolo_O = f"{cor['redUP']}O{cor['reset']}{cor['black']}"
simbolo_X = f"{cor['green']}X{cor['reset']}{cor['black']}"

jogo = [
    0, 1, 2, 
    3, 4, 5, 
    6, 7, 8
]

def desenho(jogo):
    jogo = rf"""{cor['black']}
 {jogo[0]} | {jogo[1]} | {jogo[2]}
---|---|---
 {jogo[3]} | {jogo[4]} | {jogo[5]}
---|---|---
 {jogo[6]} | {jogo[7]} | {jogo[8]}
{cor['reset']}"""
    return jogo

vitoria = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [6, 4, 2]
]

def isVitoria(simbolo):
    for combinacao in vitoria:
        if (jogo[combinacao[0]] == simbolo and 
            jogo[combinacao[1]] == simbolo and 
            jogo[combinacao[2]] == simbolo):
            return True
    return False

def isEmpate():
    return len([i for i in jogo if i not in [simbolo_O, simbolo_X]]) == 0

def getRandomCPU():
    aleatorio = [i for i in jogo if i not in [simbolo_O, simbolo_X]]
    return random.choice(aleatorio)

def getInteligenteCPU():
    for combinacao in vitoria:
        posicao = [jogo[i] for i in combinacao]
        if posicao.count(simbolo_O) == 2 and posicao.count(simbolo_X) == 0: # BOT PARA GANHAR
            for i in [0, 1, 2]:
                if combinacao[i] in jogo:
                    return combinacao[i]
    
    for combinacao in vitoria:
        posicao = [jogo[i] for i in combinacao]            
        if posicao.count(simbolo_X) == 2 and posicao.count(simbolo_O) == 0: # BOT PARA BLOQUEAR
            for i in [0, 1, 2]:
                if combinacao[i] in jogo:
                    return combinacao[i]
                
    cantos = [0, 2, 6, 8]
    meios = [1, 3, 5, 7]
    
    cantosLivres = [i for i in cantos if jogo[i] not in [simbolo_O, simbolo_X]]
    meiosLivres = [i for i in meios if jogo[i] not in [simbolo_O, simbolo_X]]

    centro = jogo[4] not in [simbolo_O, simbolo_X]

    posicaoJogo = lambda parte, simbolo: [jogo[i] for i in parte].count(simbolo)

    if posicaoJogo(cantos, simbolo_X) != 0 and centro:
        return 4

    if posicaoJogo(meios, simbolo_X) != 0:
        
        if posicaoJogo(cantos, simbolo_O) != 0:
            return random.choice(cantosLivres)
        
        elif posicaoJogo(meios, simbolo_X) != 0 and centro:
            return 4

    if jogo[4] == simbolo_X:
        return random.choice(cantosLivres)
    
    return getRandomCPU()

while True:

    jogo = [
    0, 1, 2, 
    3, 4, 5, 
    6, 7, 8
]
    
    time.sleep(0.6)
    print(
f"""\n{cor['blueUP']}
==============# JOGO DA VELHA - YEAH #==============

(Digite 1) - Comece o insano jogo com um robô...
(Digite 2) - Sair do jogo (tá com medo?)

====================================================
{cor['reset']}""")
    
    menu_escolha = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

    if menu_escolha == "1":
        
        time.sleep(0.6)
        print(
f"""{cor['blueUP']}
===================# DIFICULDADE #===================

(Digite 1) - Jogue com um burro
(Digite 2) - Jogue com um inteligente, diff de vc

=====================================================
{cor['reset']}""")
        
        difc = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

        time.sleep(0.6)
        if difc == "1":
            print(f"\n{cor['blueUP']}MODO: BURRO{cor['reset']}")
        elif difc == "2":
            print(f"\n{cor['blueUP']}MODO: INTELIGENTE{cor['reset']}")
        else:
            print(f"\n{cor['yellow']}# Cara, você não consegue digitar 2? Nem me fala que cê ia apertar no 1...{cor['reset']}")
            continue

        primeiroJOGAR = random.randint(1, 2)

        if primeiroJOGAR == 2:
            time.sleep(0.4)
            print(f"\n{cor['blueUP']}# O robô vai começar...{cor['reset']}")
            
            if difc == "1":
                jogo[getRandomCPU()] = simbolo_O
            elif difc == "2":
                jogo[getInteligenteCPU()] = simbolo_O
            
            time.sleep(0.6)
            print(f"\n{cor['blueUP']}# O robô JOGOU!{cor['reset']}")
            print(desenho(jogo))
        
        else:
            print(desenho(jogo))

        while True:
            try:
                jogada = int(input(f"\n{cor['cyan']}Quer marcar o seu X onde? {cor['reset']}"))    

                if jogo[jogada] in [simbolo_O, simbolo_X]:
                    print(f"\n{cor['yellow']}# Já está marcado nesse espaço burro{cor['reset']}")
                    continue
                else:
                    jogo[jogada] = simbolo_X
                    print(desenho(jogo))
            
            except (IndexError, ValueError):
                print(f"\n{cor['yellow']}# Digite um número entre 0 a 9 mn{cor['reset']}")
                continue
            
            if isVitoria(simbolo_X):
                if difc == "1":
                    print(f"\n{cor['green']}# VOCÊ GANHOU! Mas era o modo burro...{cor['reset']}")
                elif difc == "2":
                    print(f"\n{cor['green']}# VOCÊ GANHOU! Mas era o modo bur-... Ah, acho que eu errei em alguma coisa rs{cor['reset']}")
                time.sleep(0.6)
                break

            if isEmpate():
                print(f"\n{cor['yellow']}# EMPATE{cor['reset']}")
                break

            if difc == "1":
                jogo[getRandomCPU()] = simbolo_O
            elif difc == "2":
                jogo[getInteligenteCPU()] = simbolo_O
            
            time.sleep(0.6)
            print(f"\n{cor['blueUP']}# O robô JOGOU!{cor['reset']}")
            print(desenho(jogo))
            
            if isVitoria(simbolo_O):
                print(f"\n{cor['redUP']}# VOCÊ PERDEUKKK Ok...{cor['reset']}")
                time.sleep(0.6)
                break

            if isEmpate():
                print(f"\n{cor['yellow']}# EMPATE{cor['reset']}")
                time.sleep(0.6)
                break
                    
    elif menu_escolha == "2":
        print(f"\n{cor['yellow']}# Tchau ahh covarde{cor['reset']}")
        time.sleep(1)
        break

    else:
        print(f"\n{cor['yellow']}# Digite certo mano kkkk 1 ou 2{cor['reset']}")