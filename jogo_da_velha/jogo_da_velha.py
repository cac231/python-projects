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

def verificar_vitoria(simbolo):
    for combinacao in vitoria:
        if (jogo[combinacao[0]] == simbolo and 
            jogo[combinacao[1]] == simbolo and 
            jogo[combinacao[2]] == simbolo):
            return True
    return False

def verificar_empate():
    return len([i for i in jogo if i not in [simbolo_O, simbolo_X]]) == 0

def gerar_escolha_aleatoria_CPU():
    aleatorio = [i for i in jogo if i not in [simbolo_O, simbolo_X]]
    return random.choice(aleatorio)

def verificar_vitoria_ou_defesa(simbolo_nao_precisa, simbolo_precisa_dois):
    for combinacao in vitoria:
        posicao = [jogo[i] for i in combinacao]
        if posicao.count(simbolo_precisa_dois) == 2 and posicao.count(simbolo_nao_precisa) == 0:
            for i in [0, 1, 2]:
                if combinacao[i] in jogo:
                    return (True, combinacao[i])
    return (False, 0)

def gerar_escolha_inteligente_CPU():
    verificao_vitoria = verificar_vitoria_ou_defesa(simbolo_O, simbolo_X)
    if verificao_vitoria[0] == True:
        return verificao_vitoria[1]
    
    verificao_defesa = verificar_vitoria_ou_defesa(simbolo_X, simbolo_O)
    if verificao_defesa[0] == True:
        return verificao_defesa[1]
                
    cantos = [0, 2, 6, 8]
    meios = [1, 3, 5, 7]
    
    cantos_livres = [i for i in cantos if jogo[i] not in [simbolo_O, simbolo_X]]
    meios_livres = [i for i in meios if jogo[i] not in [simbolo_O, simbolo_X]]

    centro = jogo[4] not in [simbolo_O, simbolo_X]

    posicao_jogo = lambda parte, simbolo: [jogo[i] for i in parte].count(simbolo)

    if posicao_jogo(cantos, simbolo_X) != 0 and centro:
        return 4

    if posicao_jogo(meios, simbolo_X) != 0:
        
        if posicao_jogo(cantos, simbolo_O) != 0 and cantos_livres:
            return random.choice(cantos_livres)
        
        elif posicao_jogo(meios, simbolo_X) != 0 and centro:
            return 4

    if jogo[4] == simbolo_X and cantos_livres:
        return random.choice(cantos_livres)
    
    return gerar_escolha_aleatoria_CPU()

#

frase_menu = f"""\n{cor['blueUP']}
{"# JOGO DA VELHA #":=^52}

(Digite 1) - Comece o insano jogo com um robô...
(Digite 2) - Sair do jogo (Está com medo?)

{"="*52}
{cor['reset']}"""

frase_dificuldade = f"""{cor['blueUP']}
{"# DIFICULDADE #":=^52}

(Digite 1) - Jogue com um burro
(Digite 2) - Jogue com um inteligente, diff de vc

{"="*52}
{cor['reset']}"""

#

while True:

    jogo = [
        0, 1, 2, 
        3, 4, 5, 
        6, 7, 8
    ]
    
    time.sleep(0.6)
    print(frase_menu)
    
    menu_escolha = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

    if menu_escolha == "1":
        
        time.sleep(0.6)
        print(frase_dificuldade)
        
        dificuldade_escolhida = input(f"\n{cor['cyan']}ESCOLHA: {cor['reset']}")

        time.sleep(0.6)
        match dificuldade_escolhida:
            case "1": print(f"\n{cor['blueUP']}MODO: BURRO{cor['reset']}")
            case "2": print(f"\n{cor['blueUP']}MODO: INTELIGENTE{cor['reset']}")
            case _:
                print(f"\n{cor['yellow']}# Cara, você não consegue digitar 2? Nem me fala que ia digitar 1...{cor['reset']}")
                print(f"{cor['yellow']}# VOLTOU AO MENU...{cor['reset']}")
                continue

        primeiro_a_jogar = random.randint(1, 2)

        if primeiro_a_jogar == 2:
            time.sleep(0.6)
            print(f"\n{cor['blueUP']}# O robô vai começar...{cor['reset']}")
            
            match dificuldade_escolhida:
                case "1": jogo[gerar_escolha_aleatoria_CPU()] = simbolo_O
                case "2": jogo[gerar_escolha_inteligente_CPU()] = simbolo_O
            
            time.sleep(0.6)
            print(f"\n{cor['blueUP']}# O robô JOGOU!{cor['reset']}")
        
        print(desenho(jogo))

        while True:
            try:
                jogada = int(input(f"\n{cor['cyan']}Quer marcar o seu X onde? {cor['reset']}"))    

                if jogo[jogada] in [simbolo_O, simbolo_X]:
                    print(f"\n{cor['yellow']}# Já está marcado neste espaço burro{cor['reset']}")
                    continue
                else:
                    jogo[jogada] = simbolo_X
                    print(desenho(jogo))
            except (IndexError, ValueError):
                print(f"\n{cor['yellow']}# Digite um número entre 0 a 9 mano, olha aí{cor['reset']}")
                continue
            
            if verificar_vitoria(simbolo_X):
                match dificuldade_escolhida:
                    case "1": print(f"\n{cor['green']}# VOCÊ GANHOU! Mas era o modo burro...{cor['reset']}")
                    case "2": print(f"\n{cor['green']}# VOCÊ GANHOU! Mas era o modo bur-... Ah, acho que eu errei em alguma coisa no bot rs{cor['reset']}")
                time.sleep(0.6)
                break

            if verificar_empate():
                print(f"\n{cor['yellow']}# EMPATE... Pô veí...{cor['reset']}")
                break

            match dificuldade_escolhida:
                case "1": jogo[gerar_escolha_aleatoria_CPU()] = simbolo_O
                case "2": jogo[gerar_escolha_inteligente_CPU()] = simbolo_O
            
            time.sleep(0.6)
            print(f"\n{cor['blueUP']}# O robô JOGOU!{cor['reset']}")
            print(desenho(jogo))
            
            if verificar_vitoria(simbolo_O):
                print(f"\n{cor['redUP']}# VOCÊ PERDEUKKK Ok... Já era de esperar{cor['reset']}")
                time.sleep(0.6)
                break

            if verificar_empate():
                print(f"\n{cor['yellow']}# EMPATE... Pô veí...{cor['reset']}")
                time.sleep(0.6)
                break
                    
    elif menu_escolha == "2":
        print(f"\n{cor['yellow']}# Tchau ahh Covarde...{cor['reset']}")
        time.sleep(1)
        break

    else:
        print(f"\n{cor['yellow']}# Digite certo mano kkkk 1 ou 2 poxa...{cor['reset']}")