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

resposta = [
   "TAYLOR", 
   "JALECO", 
   "UVA", 
   "MUSGO", 
   "ELIZABETH",
   "SOPA",
   "TESTE" 
]

dica = ["Sem nenhuma dica..."] * len(resposta)
dicaBRUTO = [
   "É famoso(a)...",
   "É uma roupa zé...",
   "Uma fruta rara kkk...",
   "Um tipo de planta eu acho, sei lá...",
   "É uma rainha...",
   "É uma comida..."
]
for i in range(len(dicaBRUTO)):
   dica[i] = dicaBRUTO[i]

def isLetra(letraPalavra, resposta, nivel):
   if len(letraPalavra) == 1 and letraPalavra.isalpha():
      return True
   elif letraPalavra.lower() == resposta[nivel].lower():
      return "acertou"
   elif len(letraPalavra) > 1:
      return "errou"
   else:
      return False

while True:
   inicio_menu = rf"""{"\n"}
=====================================================================
            BEM-VINDO AO JOGO DA FORCA ... do Cac rs
=====================================================================
___________
| /       |
|/      (0-0)
|        /|\
|         |
|        / \

({1}) -- Eae! Digite "1" para começar o jogo
       Serão 5 palavras para serem descobertas por você!
   
({2}) -- Para fec- fechar... o jogo, dig-... digite "2" 
       Vamos jogar... por favor... não vá embora

====================================================================="""
   
   time.sleep(0.8)
   print(inicio_menu)
   
   time.sleep(0.8)
   escolha = input(f"\n\n{cor['blueUP']}# ESCOLHA: Digite a opção aqui mano: {cor['reset']}")
    
   if escolha == "1":
      nivel = 0 # Resposta e dica
      erradas = 0
      while nivel < len(resposta):
            
         nivel_morte = 0 # Morte
         acerto = 0 # Letra acertada 
         acertoTotal = len(resposta[nivel]) # Total de acertos que precisa
         acertoPalavra = False
         escolhidos = []
         underlines = list("_" * len(resposta[nivel]))
         resetLetraOk = False

         def morte0():
            return rf"""{cor['cyan']}
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
|  Dick: {dica[nivel]}
|  
|  Usados: {", ".join(escolhidos)}
|
|  -- Não ache que vai ser fácil
|{cor['reset']}"""

         def morte1():
            return rf"""{cor['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
|  ___________
|  | /       |          
|  |/      (nivel-nivel)       
|  |                /|\
|  |                 |
|  |                / \           
|
|  Palavra: {"".join(underlines)}
|  Dick: {dica[nivel]}
|  
|  Usados: {", ".join(escolhidos)}
|
|  -- Ok, você errou, mas eu confio (confio não lol)
|{cor['reset']}"""

         def morte2():
            return rf"""{cor['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (nivel-nivel)       
|  |         |      / \
|  |         |        
|  |                / \                   
|
|  Palavra: {"".join(underlines)}
|  Dick: {dica[nivel]}
|
|  Usados: {", ".join(escolhidos)}
|
|  -- Mano, cuidado aí viu, vai ficar tenso...
|{cor['reset']}"""

         def morte3():
            return rf"""{cor['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (nivel-nivel)       
|  |        /|        \
|  |         |        
|  |                / \          
|
|  Palavra: {"".join(underlines)}
|  Dica (corrigi): {dica[nivel]}
|
|  Usados: {", ".join(escolhidos)}
|
|  -- Falta 3 tentativas ein, se você perder... vai reiniciar tudo!
|{cor['reset']}"""

         def morte4():
            return rf"""{cor['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (nivel-nivel)       
|  |        /|\
|  |         |        
|  |                / \
|
|  Palavra: {"".join(underlines)}
|  Dica: {dica[nivel]}
|
|  Usados: {", ".join(escolhidos)}
|
|  -- Kkkkk tá difícil? HAHAHAHA ESTÁ DIFÍCIL???
|{cor['reset']}"""

         def morte5():
            return rf"""{cor['cyan']}
|
|  -- {nivel + 1}º DESAFIO --
|  ___________
|  | /       |
|  |/      (nivel-nivel)       
|  |        /|\
|  |         |        
|  |        /         \
|
|  Palavra: {"".join(underlines)}
|  Dica: {dica[nivel]}
|
|  Usados: {", ".join(escolhidos)}
|
|  -- Hm...
|{cor['reset']}"""

         def morte6():
            return rf"""{cor['red']}
|
|  -- GAME OVER --
|  ___________
|  | /       |
|  |/      (nivel-nivel)       
|  |        /|\     
|  |         |       
|  |        / \                   
|
|  Palavra: {resposta[nivel]}
|  imprecisão: Você errou {erradas} vezes rs
|
|  -- Matou o mlk sklkkkk. Cê perdeu feio ein, besta
|{cor['reset']}"""

         def getResposta():
            return rf"""
|
|  Resposta: {resposta[nivel]}
|"""

         morte = [morte0, morte1, morte2, morte3, morte4, morte5, morte6]

         if nivel != 0:
            time.sleep(0.8)
            print(f"\n\n{cor['green']}# # Vamos para próxima yeahh{cor['reset']}")

         else:
            time.sleep(0.8)
            print(f"\n\n{cor['green']}# # Vamos começar!")
            print(f"# # TUTORIAL: Digite uma letra OU uma palavra que cê acha que é e pronto, simples!")
            print(f"# # Se a palavra estiver errada, vai perder vida! Não pode silábas ou fragmentos...")
            print(f"# # Escreva a palavra correta ein, se não perde vida também!{cor['reset']}")
         
         while nivel_morte < 6:
            resetLetraOk = False

            # SE GANHOU OU ACERTOU UMA
            if acerto == acertoTotal or acertoPalavra:
               if nivel == len(resposta) - 1:

                  def vitoria0():
                     return rf"""{cor['yellow']}
|
|  -- YOU WIN --
|  ___________
|  | /       |
|  |/              (0-0)
|  |                /|\
|  |                 |
|  |                / \
|
|  Resposta: {resposta[nivel]}
|  imprecisão: Você errou {erradas} vezes rs
|
|  -- Você conseguiu acertar as {len(resposta)} PALAVRAS! (foi de primeira? rs)
|  -- Enfim... Muito obrigado por ter jogado o meu jogo!
|  -- Fiz com muito carinho, sério, e me diverti muito fazendo
|  -- Obrigado <3
|"""

                  def vitoria1():
                     print("""
|
|  -- CRÉDITOS --
|""" ) 
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
               
                  def vitoria2():
                     print(rf"""
|   __  __
|  /  \/  \
|  \      /
|   \    /
|    \  /
|     \/{cor['reset']}""")

                  time.sleep(0.8)
                  print(vitoria0())
                  time.sleep(7+3)
                  vitoria1()
                  time.sleep(0.8)
                  vitoria2()
                  
                  time.sleep(0.8)
                  break
               
               else:
                  time.sleep(0.8)
                  print(f"\n\n{cor['green']}# # CONSEGUIU UMA!{cor['reset']}")
                  print(getResposta())
                  break
            
            print(morte[nivel_morte]())
            escolhaLetra = input(f"\n\n{cor['blueUP']}# ESCOLHA: Digite a letra ou a palavra: {cor['reset']}").strip().upper()
            verificarEntrada = isLetra(escolhaLetra, resposta, nivel)
            
            # CAÇAR LETRA CORRETA
            for i, letra in enumerate(resposta[nivel]):

               if escolhaLetra.lower() not in escolhidos:
                  
                  if verificarEntrada == True and escolhaLetra == letra:
                     resetLetraOk = True
                     underlines[i] = escolhaLetra
                     acerto += 1
                     time.sleep(0.8)
                     print(f"\n\n{cor['green']}# # Boa... conseguiu acertar uma letra, continue assim...{cor['reset']}")
                  
                  elif verificarEntrada == "acertou":
                     resetLetraOk = True
                     acertoPalavra = True
                     time.sleep(0.8)
                     print(f"\n\n{cor['green']}# # BOAKK acertou a palavra de uma vez...{cor['reset']}")
                     break
                  
                  elif verificarEntrada == "errou":
                     time.sleep(0.8)
                     print(f"\n\n{cor['redUP']}# # Palavra incorreta kkk, digitou errado?{cor['reset']}")
                     break

                  elif verificarEntrada == False:
                     resetLetraOk = True
                     time.sleep(0.8)
                     print(f"\n\n{cor['yellow']}# # ERRO: Digite uma letra ou uma palavra véikkkk{cor['reset']}")
                     break
               
               else:
                  resetLetraOk = True
                  time.sleep(0.8)
                  print(f"\n\n{cor['yellow']}# # ERRO: Você já escolheu essa letra ou palavra dumb{cor['reset']}")
                  break
                  
            escolhidos.append(escolhaLetra.lower())
            if not resetLetraOk:
               erradas += 1
               nivel_morte += 1
               time.sleep(0.8)
               print(f"\n\n{cor['redUP']}# # Errou kkkk perdeu uma parte do corpo aí{cor['reset']}")
               
         # SE ERROU O DESAFIO ATUAL
         else:
            time.sleep(0.8)
            print(f"\n\n{cor['red']}# # Burro tu perdeu kkkkkk aaahhh kkkk{cor['reset']}")
            print(getResposta())
            time.sleep(0.8)
            print(morte[nivel_morte]())
            time.sleep(7)
            break

         nivel += 1
   
   elif escolha == "2":
      time.sleep(0.8)
      print(f"\n\n{cor['yellow']}# # Eu... Não... Não aceito isso... não tem o que fazer...")
      print(f"# # Tchau! ;) Viva a vida por mim!{cor['reset']}")
      time.sleep(7)
      break
    
   else:
      time.sleep(0.8)
      print(f"\n\n{cor['yellow']}# # ERRO: Digite 1 ou 2 porrakkkkkk{cor['reset']}")