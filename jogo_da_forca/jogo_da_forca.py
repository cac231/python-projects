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

RESPOSTAS = [
   "TAYLOR", 
   "JALECO", 
   "UVA", 
   "MUSGO", 
   "ELIZABETH",
]

DICA = [
   "É famoso(a)...",
   "É uma roupa zé...",
   "Uma fruta rara kkk...",
   "Um tipo de planta eu acho, sei lá...",
   "É uma rainha...",
]

#////

inicio_menu = rf"""{"\n"}
{"=" * 70}
{"BEM-VINDO AO JOGO DA FORCA ... do Cac rs":^70}
{"=" * 70}
___________
| /       |
|/      (0-0)
|        /|\
|         |
|        / \

({1}) -- Eae! Digite '1' para começar o jogo
       Serão 5 palavras para serem descobertas por você!
   
({2}) -- Para fec- fechar... o jogo, dig-... digite '2' 
       Vamos jogar... por favor... não vá embora

{"=" * 70}"""

#

def morte_0():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dick: {DICA[nivel]}
|
|  -- Não ache que vai ser fácil
|{COR['reset']}"""

#

def morte_1():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dick: {DICA[nivel]}
|
|  -- Ok, você errou, mas eu confio (confio não lol)
|{COR['reset']}"""

#

def morte_2():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dick: {DICA[nivel]}
|
|  -- Mano, cuidado aí viu, vai ficar tenso...
|{COR['reset']}"""

#

def morte_3():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dica (corrigi): {DICA[nivel]}
|
|  -- Falta 3 tentativas ein, se você perder... vai reiniciar tudo!
|{COR['reset']}"""

#

def morte_4():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dica: {DICA[nivel]}
|
|  -- Kkkkk tá difícil? HAHAHAHA ESTÁ DIFÍCIL???
|{COR['reset']}"""

#

def morte_5():
   return rf"""{COR['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
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
|  Dica: {DICA[nivel]}
|
|  -- Mano...
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
|  Palavra: {RESPOSTAS[nivel]}
|  Imprecisão: Você errou {erradas} vezes rs
|
|  -- Matou o mlk sklkkkk. Cê perdeu feio ein, besta
|{COR['reset']}"""

#

def aparecer_resposta():
   return rf"""
|
|  RESPOSTA: {RESPOSTAS[nivel]}
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
|  RESPOSTA: {RESPOSTAS[nivel]}
|  Imprecisão: Você errou {erradas} vezes rs
|
|  -- Você conseguiu acertar as {len(RESPOSTAS)} PALAVRAS! (foi de primeira? rs)
|  -- Enfim... Muito obrigado por ter jogado o meu jogo!
|  -- Fiz com muito carinho, sério, e me diverti muito fazendo
|  -- Obrigado <3
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
|     \/{COR['reset']}
|"""
   
   #
   
   time.sleep(0.6)
   print(vitoria_0)
   
   time.sleep(0.6 * 2)
   print(vitoria_1)
   
   time.sleep(1.6)
   print("|  Diretor do jogo: Cac")
   time.sleep(1.6)
   print("|  Produtor: Cac")
   time.sleep(1.6)
   print("|  Diretor de Arte: Cac")
   time.sleep(1.6)
   print("|  Designer de Jogo: Cac")
   time.sleep(1.6)
   print("|  Level Designer: Cac")
   time.sleep(1.6)
   print("|  Game Programmer: Cac")
   time.sleep(1.6)
   print("|  Artista Técnico: Cac")
   print("|")
   
   time.sleep(0.6)
   print(vitoria_2)
   time.sleep(0.6)

#////

def verificar_input_termo(input_termo, RESPOSTAS, nivel):
   if input_termo == "" or not input_termo.isalnum():
      return "erro"
   
   elif len(input_termo) == 1:
      if input_termo.isalpha():
         return "é_letra"
      else:
         return "erro"
   
   elif len(input_termo) > 1:
      lista_numerica = [str(x) for x in range(11)]
      resposta_sem_acento = remover_acento_string(RESPOSTAS[nivel])
      
      if input_termo.lower() == resposta_sem_acento.lower():
         return "acertou_tudo"
      for numero in lista_numerica:
         if numero in input_termo:
            return "erro"
      
      return "errou_tudo"

   else:
      print("Erro inesperado")

#

def letra_correta(indice, letra):
   underlines[indice] = letra
   time.sleep(0.6)
   print(f"\n{COR['green']}# Boa! Conseguiu acertar uma letra, continue assim...{COR['reset']}") 

def palavra_correta():    
   time.sleep(0.6)
   print(f"\n{COR['green']}# Oloko! Acertou a palavra de uma vez...{COR['reset']}")

def palavra_errada():
   time.sleep(0.6)
   print(f"\n{COR['redUP']}# Palavra incorreta. Digitou errado? kkk{COR['reset']}")

def palavra_invalida():
   time.sleep(0.6)
   print(f"\n{COR['yellow']}# ERRO: Digite uma letra ou uma palavra veikkkk{COR['reset']}")

#
   
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

#////

while True: 
   time.sleep(0.6)
   print(inicio_menu)
   
   time.sleep(0.6)
   escolha = input(f"\n{COR['blueUP']}# ESCOLHA: Digite a opção aqui mano: {COR['reset']}")
    
   if escolha == "1":
      nivel = 0 # RESPOSTAS e DICA
      erradas = 0
      while nivel < len(RESPOSTAS):
            
         nivel_morte = 0 # Morte
         acerto = 0 # Letra acertada 
         acerto_total = len(RESPOSTAS[nivel]) # Total de acertos que precisa
         acertou_palavra = False
         escolhidos = []
         underlines = list("_" * len(RESPOSTAS[nivel]))

         morte = [morte_0, morte_1, morte_2, morte_3, morte_4, morte_5, morte_6]

         if nivel != 0:
            time.sleep(0.6)
            print(f"\n{COR['green']}# Vamos para a próxima yeah{COR['reset']}")
         else:
            time.sleep(0.6)
            print(f"\n{COR['green']}# Vamos começar! Aqui está o tutorial:")
            print(f"# Digite uma letra OU a palavra que cê acha que é e pronto, simples!")
            print(f"# Se a palavra digitada estiver errada, vai perder vida! Não pode silábas ou fragmentos...")
            print(f"# Apenas escreva a palavra se tiver certeza ein, se não perde vida sem dó!{COR['reset']}")
         
         while nivel_morte < 6:
            perdeu_vida = True

            # SE GANHOU OU ACERTOU UMA
            if acerto == acerto_total or acertou_palavra:
               if nivel == len(RESPOSTAS) - 1:
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
            
            verificar_entrada = verificar_input_termo(input_termo_sem_acento, RESPOSTAS, nivel)
            
            # CAÇAR LETRA CORRETA
            for indice, letra in enumerate(RESPOSTAS[nivel]):
               
               if input_termo_sem_acento not in escolhidos:
                  
                  match verificar_entrada:           
                     case "é_letra":
                        input_termo_verificado = aceitar_letra_com_acento(input_termo_sem_acento)
                        
                        if letra in input_termo_verificado:
                           perdeu_vida = False
                           acerto += 1
                           letra_correta(indice, letra)
                     
                     case "acertou_tudo":
                        perdeu_vida = False
                        acertou_palavra = True 
                        palavra_correta()
                        break
                     
                     case "errou_tudo":
                        palavra_errada()
                        break
                     
                     case "erro":
                        perdeu_vida = False
                        palavra_invalida()
                        break
              
               else:
                  perdeu_vida = False
                  time.sleep(0.6)
                  print(f"\n{COR['yellow']}# ERRO: Você já escolheu essa letra ou palavra...{COR['reset']}")
                  break
            
            if not input_termo_sem_acento in escolhidos: 
               escolhidos.append(input_termo_sem_acento)
            
            if perdeu_vida:
               erradas += 1
               nivel_morte += 1
               time.sleep(0.6)
               print(f"\n{COR['redUP']}# Errou, perdeu uma parte do corpo aí{COR['reset']}")
               
         # SE ERROU O DESAFIO ATUAL
         else:
            time.sleep(0.6)
            print(f"\n{COR['red']}# Irmão, você perdeu kkkk aahh kkkk{COR['reset']}")
            print(aparecer_resposta())
            time.sleep(0.6)
            print(morte[nivel_morte]())
            time.sleep(0.6 * 10)
            break

         nivel += 1
   
   elif escolha == "2":
      time.sleep(0.6)
      print(f"\n{COR['yellow']}# Eu... Não... Não aceito isso... não tem o que fazer...")
      print(f"# Tchau... Viva a vida por mim! ;){COR['reset']}")
      time.sleep(0.6 * 8)
      break
    
   else:
      time.sleep(0.6)
      print(f"\n{COR['yellow']}# ERRO: Digite 1 ou 2 mano{COR['reset']}")