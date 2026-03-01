import time
from unidecode import unidecode
from colorama import init, Fore

init()

COR = {
   "blueUP": Fore.LIGHTBLUE_EX,
   "cyan": Fore.CYAN,
   "red": Fore.RED,
   "redUP": Fore.LIGHTRED_EX,
   "yellow": Fore.YELLOW,
   "green": Fore.GREEN,
   "reset": Fore.RESET,
}

PRESET = {
   "1": {
      "palavras": [
            "SOPA",
            "ABACATE",
            "CAMISOLA",
            "CUBA",
            "JABUTI",
            ],
      "dicas": [
         "É líquido...",
         "É uma fruta kkk tá...",
         "É um vestimento, com certeza...",
         "País...",
         "Animal lento kk dica ridícula"
      ],
   },
   "2": {
      "palavras": [
            "CALENDÁRIO",
            "TRIÂNGULO",
            "RETROVISOR",
            "OCEANO",
            "GOLFINHO",
            ],
      "dicas": [
         "Se localiza no tempo...",
         "Matemática...",
         "Evita acidentes!",
         "É grandioso...",
         "____ cor de rosa kkk"
      ],
   },
   "3": {
      "palavras": [
            "JALECO",
            "ELIZABETH",
            "MUSGO",
            "HAITI",
            "FOTOSSÍNTESE",
            ],
      "dicas": [
         "É um vestimento, não esqueça que está na dificuldade difícil...",
         "Uma rainha... Como que escreve?",
         "Uma planta briófita... é kkk",
         "País... Apenas.",
         "É um processo biológico daora"
      ],
   },
   "4": {
      "palavras": [
            "PITAYA",
            "SERIGUELA",
            "CAJA",
            "JACA",
            "LIXIA",
            ],
      "dicas": [
         "É uma fruta né... (OBS: Essa fruta tem duas formas de escrever, fique atento a isso)",
         "É uma fruta né...",
         "É uma fruta né...",
         "É uma fruta né...",
         "É uma fruta né...",
      ],
   },
   "5": {
      "palavras": [
            "LÍBANO",
            "BANGLADESH",
            "GEÓRGIA",
            "ROMÊNIA",
            "PERU",
            ],
      "dicas": [
         "É um país né...",
         "É um país né...",
         "É um país né...",
         "É um país né...",
         "É um país né...",
      ],
   },
   "6": {
      "palavras": [
            "VETERINÁRIO",
            "ENCANADOR",
            "SOCIÓLOGO",
            "ELETRICISTA",
            "FOTÓGRAFO",
            ],
      "dicas": [
         "É uma profissão né... (OBS: Está no masculino, se for necessário)",
         "É uma profissão né... (OBS: Está no masculino, se for necessário)",
         "É uma profissão né... (OBS: Está no masculino, se for necessário)",
         "É uma profissão né... (OBS: Está no masculino, se for necessário)",
         "É uma profissão né... (OBS: Está no masculino, se for necessário)",
      ],
   },
}

RESPOSTAS = []
DICAS = []

#////

menu_inicio = rf"""{"\n"}
{"=" * 70}
{"BEM-VINDO AO JOGO DA FORCA ... do Cac rs":^70}
{"=" * 70}
___________
| /       |
|/      (0u0)
|        /|\
|         |
|        / \

({1}) -- Eae! Digite '1' para começar o jogo
       Serão 5 palavras para serem descobertas por você!
   
({2}) -- Para fec- fechar... o jogo, dig-... digite '2' 
       Vamos jogar... Por favor... Não vá embora

{"=" * 70}"""

#

menu_preset = rf"""{"\n"}
{"=" * 70}
{"QUAL TEMA DE PALAVRAS VOCÊ QUER USAR?":^70}
{"=" * 70}
___________   
| /       |  (balão bem legal)
|/      (7-7) /
|        /|--/
|         |
|        / \

({1}) -- Dificuldade fácil ahh
   
({2}) -- Dificuldade média, ok

({3}) -- Dificuldade DIFÍCIL, boa sorte
   
({4}) -- Frutas kkkk maça

({5}) -- Países hehe Buona fortuna (Boa sorte em italiano)
   
({6}) -- Profissões... CLT?

{"=" * 70}"""

#

def morte_0():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/              (0-0)
|  |                /|\
|  |                 |
|  |                / \
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|  
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Não ache que vai ser fácil (Só se você escolheu o fácil né)
|{COR['reset']}"""

#

def morte_1():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |          
|  |/      (X-X)       
|  |                /|\
|  |                 |
|  |                / \           
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|  
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Ok, tudo bem... Eu confio (Confio não he)
|{COR['reset']}"""

#

def morte_2():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (X-X)       
|  |         |      / \
|  |         |        
|  |                / \                   
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Mano, cuidado aí viu, vai ficar tenso o bagui...
|{COR['reset']}"""

#

def morte_3():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (X-X)       
|  |        /|        \
|  |         |        
|  |                / \          
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Falta 3 tentativas ein, se você perder... vai reiniciar tudo!
|{COR['reset']}"""

#

def morte_4():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (X-X)       
|  |        /|\
|  |         |        
|  |                / \
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Está difícil? HAHAHAHA ESTÁ DIFÍCIL???
|{COR['reset']}"""

#

def morte_5():
   return rf"""{COR['cyan']}
|
|  -- {nivel_resposta + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (X-X)       
|  |        /|\
|  |         |        
|  |        /         \
|
|  Palavra: {"".join(underlines)}
|  Usadas: {", ".join(escolhidos)}
|
|  Dica: {DICAS[nivel_resposta]}
|
|  -- Eh...
|{COR['reset']}"""

#

def morte_6():
   return rf"""{COR['red']}
|
|  -- GAME OVER --
|  ___________
|  | /       |
|  |/      (X-X)       
|  |        /|\     
|  |         |       
|  |        / \                   
|
|  Imprecisão: Você errou {erradas} vezes... tome
|
|  -- Matou o menino kkkk Cê perdeu feio ein, besta
|{COR['reset']}"""

#

def aparecer_resposta():
   return rf"""
|
|  RESPOSTA: {RESPOSTAS[nivel_resposta]}
|"""

#

def ganhou_jogo():
   vitoria_0 = rf"""{COR['yellow']}
|
|  -- YOU WIN --
|  ___________
|  | /       |
|  |/              (0-0)
|  |                /|\
|  |                 |
|  |                / \
|
|  Imprecisão: Você errou {erradas} vezes rs
|
|  -- Você conseguiu acertar as {len(RESPOSTAS)} PALAVRAS! (Foi de primeira???)
|  -- Enfim... Muito obrigado por ter jogado o meu jogo!
|  -- Fiz com muito carinho, sério, e me diverti muito fazendo
|  -- Obrigado!
|"""

   vitoria_1 = """
|
|  -- CRÉDITOS --
|""" 

   vitoria_2 = rf"""
|   __  __
|  /  \/  \
|  \      /
|   \    /
|    \  /
|     \/
|{COR['reset']}"""
   
   #
   
   time.sleep(0.6)
   print(aparecer_resposta())
   
   time.sleep(0.6)
   print(vitoria_0)
   
   time.sleep(0.6 * 8)
   print(vitoria_1)
   
   time.sleep(1.2)
   print("|  Diretor do jogo: Cac")
   time.sleep(1.2)
   print("|  Produtor: Cac")
   time.sleep(1.2)
   print("|  Diretor de Arte: Cac")
   time.sleep(1.2)
   print("|  Designer de Jogo: Cac")
   time.sleep(1.2)
   print("|  Level Designer: Cac")
   time.sleep(1.2)
   print("|  Programador: Cac")
   time.sleep(1.2)
   print("|  Artista Técnico: Cac\n|")
   
   time.sleep(0.6)
   print(vitoria_2)
   time.sleep(0.6 * 3)

def perdeu_jogo():
   time.sleep(0.6)
   print(f"\n{COR['red']}# Irmão, você perdeu kkkk aahh kkkk{COR['reset']}")
   time.sleep(0.6)
   print(aparecer_resposta())
   time.sleep(0.6)
   print(morte[nivel_morte]())
   time.sleep(0.6 * 10)

#////

def verificar_input_termo(input_termo, RESPOSTAS, nivel_resposta):
   if input_termo in escolhidos:
      return "repetido"
   
   if input_termo == "" or not input_termo.isalnum():
      return "erro"
   
   elif len(input_termo) == 1:
      if input_termo.isalpha():
         return "é_letra"
      else:
         return "erro"
   
   elif len(input_termo) > 1:
      lista_numerica = [str(x) for x in range(11)]
      resposta_sem_acento = remover_acento_string(RESPOSTAS[nivel_resposta])
      
      if input_termo.lower() == resposta_sem_acento.lower():
         return "acertou_tudo"
      for numero in lista_numerica:
         if numero in input_termo:
            return "erro"
      
      return "errou_tudo"

   else:
      print("Erro inesperado")

def remover_acento_string(input):
   return unidecode(input)

def aceitar_letra_com_acento(letra):
   grupos = {
      "A": ["A", "Á", "Â", "Ã", "À"],
      "E": ["E", "É", "Ê"],
      "I": ["I", "Í"],
      "O": ["O", "Ó", "Ô", "Õ"],
      "U": ["U", "Ú"],
      "C": ["C", "Ç"]
   }
   for grupo in grupos.values():
      if letra in grupo:
         return grupo
   return [letra]

#

def escolher_preset_palavras():
   while True:
      time.sleep(0.6)
      print(menu_preset)
      
      time.sleep(0.6)
      escolha = input(f"\n{COR['blueUP']}# ESCOLHA: Digite o número do tema: {COR['reset']}")
      
      descricao = {"1": "Fácil", "2": "Médio", "3": "Difícil", "4": "Frutas", "5": "Países", "6": "Profissões"}
      
      time.sleep(0.6)
      match escolha:
         case "1" | "2" | "3" | "4" |  "5" | "6":
            for numero in descricao:
               if escolha == numero:
                  print(f"\n{COR['green']}# TEMA ESCOLHIDO: {descricao[escolha]}{COR['reset']}")
                  break
            return PRESET[escolha]["palavras"], PRESET[escolha]["dicas"]
         case _:
            print(f"\n{COR['yellow']}# ERRO: Digite 1 a 6 mano{COR['reset']}")
            continue

#

frase_tutorial = f"""
{COR['green']}# Vamos começar! Aqui está o tutorial:
# Digite uma letra OU a palavra que cê acha que é e pronto, simples!
# Se a palavra digitada estiver errada, vai perder vida! Não pode silábas ou fragmentos...
# Apenas escreva a palavra se tiver certeza ein, se não perde vida sem dó!
# Não precisa se preocupar com acentos nem com letras maiúsculas ou minúsculas...{COR['reset']}"""

frase_sair_do_jogo = f"""
{COR['yellow']}# Eu... Não... Não aceito isso. Não tem o que fazer...
Tchau... Viva a vida por mim! ;){COR['reset']}"""

#

def letra_correta(mais_de_uma):
   time.sleep(0.6)
   if not mais_de_uma:
      print(f"\n{COR['green']}# Boa! Conseguiu acertar uma letra, continue assim...{COR['reset']}")
   else:
      print(f"\n{COR['green']}# Hmm! A palavra tem outro letra igual a essa...{COR['reset']}") 

def palavra_correta():    
   time.sleep(0.6)
   print(f"\n{COR['green']}# Oloko! Acertou a palavra de uma vez...{COR['reset']}")

def palavra_errada():
   time.sleep(0.6)
   print(f"\n{COR['redUP']}# Palavra incorreta. Digitou errado? kkk{COR['reset']}")

def palavra_invalida():
   time.sleep(0.6)
   print(f"\n{COR['yellow']}# ERRO: Digite uma letra ou uma palavra veikkkk{COR['reset']}")

#////

while True: 
   time.sleep(0.6)
   print(menu_inicio)
   
   time.sleep(0.6)
   escolha = input(f"\n{COR['blueUP']}# ESCOLHA: Digite a opção aqui mano: {COR['reset']}")
    
   if escolha == "1":
      morte = [morte_0, morte_1, morte_2, morte_3, morte_4, morte_5, morte_6]
      RESPOSTAS, DICAS = escolher_preset_palavras()
      nivel_resposta = 0
      erradas = 0
      time.sleep(0.6)
      print(frase_tutorial)
      
      while nivel_resposta < len(RESPOSTAS):
         nivel_morte = 0
         acertos_atual = 0
         acerto_total = len(RESPOSTAS[nivel_resposta])
         acertou_palavra = False
         escolhidos = []
         underlines = list("_" * len(RESPOSTAS[nivel_resposta]))

         if nivel_resposta != 0:
            time.sleep(0.6)
            print(f"\n{COR['green']}# Vamos para a próxima yeah{COR['reset']}")
         
         while nivel_morte < 6:
            perdeu_vida = True

            if acertos_atual == acerto_total or acertou_palavra:
               if nivel_resposta == len(RESPOSTAS) - 1:
                  ganhou_jogo()
                  break
               else:
                  time.sleep(0.6)
                  print(f"\n{COR['green']}# CONSEGUIU ADIVINHAR!{COR['reset']}")
                  print(aparecer_resposta())
                  break
            
            print(morte[nivel_morte]())
            
            input_termo = input(f"\n{COR['blueUP']}# ESCOLHA: Digite a letra ou a palavra: {COR['reset']}").strip().upper()       
            input_termo_sem_acento = remover_acento_string(input_termo)    
            verificar_entrada = verificar_input_termo(input_termo_sem_acento, RESPOSTAS, nivel_resposta)
                  
            match verificar_entrada:           
               case "é_letra":
                  input_termo_grupo_acentos = aceitar_letra_com_acento(input_termo_sem_acento)
                  mais_de_uma = False                      
                  for indice, letra in enumerate(RESPOSTAS[nivel_resposta]):
                     if letra in input_termo_grupo_acentos:
                        perdeu_vida = False
                        acertos_atual += 1
                        underlines[indice] = letra
                        letra_correta(mais_de_uma)
                        mais_de_uma = True
               
               case "acertou_tudo":
                  perdeu_vida = False
                  acertou_palavra = True 
                  palavra_correta()
               
               case "errou_tudo":
                  palavra_errada()
               
               case "erro":
                  perdeu_vida = False
                  palavra_invalida()
               
               case "repetido":
                  perdeu_vida = False
                  time.sleep(0.6)
                  print(f"\n{COR['yellow']}# ERRO: Você já escolheu essa letra ou palavra...{COR['reset']}")
               
               case _:
                  print("Match inesperado")                  
            
            if not input_termo_sem_acento in escolhidos: 
               escolhidos.append(input_termo_sem_acento)
            
            if perdeu_vida:
               erradas += 1
               nivel_morte += 1
               time.sleep(0.6)
               print(f"\n{COR['redUP']}# Errou, perdeu uma parte do corpo aí{COR['reset']}")
               
         if nivel_morte == 6:
            perdeu_jogo()
            break
         
         nivel_resposta += 1
   
   elif escolha == "2":
      time.sleep(0.6)
      print(frase_sair_do_jogo)      
      time.sleep(0.6 * 8)
      break
    
   else:
      time.sleep(0.6)
      print(f"\n{COR['yellow']}# ERRO: Digite 1 ou 2 mano{COR['reset']}")