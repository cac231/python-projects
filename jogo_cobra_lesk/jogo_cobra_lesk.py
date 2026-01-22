import pygame
import os
import sys
import ctypes
import pywinstyles
import math
import random

os.environ['SDL_VIDEO_CENTERED'] = 'centered'
myappid = 'jogo.HoraDoLesk.version1.0' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def pegar_caminho_recurso(nome_arquivo):
      if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, nome_arquivo)
      return os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_arquivo)

#//

CAMINHOS = {
   "fonte": pegar_caminho_recurso(r"assets/ARCADE_N.TTF"),

   "imagem_icon": pegar_caminho_recurso(r"assets/images/icon/icon_png.png"),

   "tutorial_1": pegar_caminho_recurso(r"assets/images/jogo_0001.png"),
   "tutorial_2": pegar_caminho_recurso(r"assets/images/jogo_0002.png"),
   "tutorial_3": pegar_caminho_recurso(r"assets/images/jogo_0003.png"),
   "tutorial_4": pegar_caminho_recurso(r"assets/images/jogo_0004.png"),
   
   "musica_menu": pegar_caminho_recurso(r"assets/sounds/music/Crystal Clear Loop.mp3"),
   "musica_tutorial": pegar_caminho_recurso(r"assets/sounds/music/Curiosity (Black).mp3"),
   "musica_jogo": pegar_caminho_recurso(r"assets/sounds/music/Unknown Caverns.mp3"),
   "musica_creditos": pegar_caminho_recurso(r"assets/sounds/music/Think About It.mp3"),

   "clicar_botao": pegar_caminho_recurso(r"assets/sounds/_clicar_botao.wav"),
   "sair_do_jogo": pegar_caminho_recurso(r"assets/sounds/_sair_do_jogo.wav"),
   "comecando_partida_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/_comecando_partida_MINHAVOZ.wav"),
   "voltando_para_menu_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/_voltando_para_menu_MINHAVOZ.wav"),
   
   "musica_perder_jogo": pegar_caminho_recurso(r"assets/sounds/perder_jogo.wav"),
   "perder_jogo_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/perder_jogo_MINHAVOZ.wav"),
   "musica_ganhar_jogo": pegar_caminho_recurso(r"assets/sounds/ganhar_jogo.wav"),
   "ganhar_jogo_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/ganhar_jogo_MINHAVOZ.wav"),

   "pegar_moeda": pegar_caminho_recurso(r"assets/sounds/pegar_moeda.wav"),
   "pegar_moeda_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/pegar_moeda_MINHAVOZ.wav"),
   "pegar_inimigo": pegar_caminho_recurso(r"assets/sounds/pegar_inimigo.wav"),
   
   "pausar": pegar_caminho_recurso(r"assets/sounds/pausar.wav"),
   "pausar_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/pausar_MINHAVOZ.wav"),
   "despausar": pegar_caminho_recurso(r"assets/sounds/despausar.wav"),
   "despausar_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/despausar_MINHAVOZ.wav"),

   "aumentar_fase": pegar_caminho_recurso(r"assets/sounds/aumentar_fase.wav"),
   "aumentar_fase_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/aumentar_fase_MINHAVOZ.wav"),
   "diminuir_fase": pegar_caminho_recurso(r"assets/sounds/diminuir_fase.wav"),
   "diminuir_fase_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/diminuir_fase_MINHAVOZ.wav"),
   
   "alertar_ultima_sala": pegar_caminho_recurso(r"assets/sounds/alertar_ultima_sala.wav"),
   "alertar_vitoria_sala": pegar_caminho_recurso(r"assets/sounds/alertar_vitoria_sala.wav"),
   "alertar_vitoria_sala_MINHAVOZ": pegar_caminho_recurso(r"assets/sounds/my_voice/alertar_vitoria_sala_MINHAVOZ.wav"),
}

ARRAY_TUTORIAL = [
   CAMINHOS["tutorial_1"],
   CAMINHOS["tutorial_2"],
   CAMINHOS["tutorial_3"],
   CAMINHOS["tutorial_4"]
   ]

FONTE = lambda tamanho: pygame.font.Font(CAMINHOS["fonte"], tamanho)

CORES = { 
   "tela_menu": (0, 0, 10),
   "tela_jogo": (5, 15, 40),
   
   "texto1_pause": (200, 200, 200),
   "texto2_pause": (150, 150, 150),
   
   "texto1_menu": (250, 100, 100),
   "texto2_menu": (200, 100, 100),
   
   "texto_botoes": (200, 100, 100),
   "botoes_fundo": (10, 10, 10),
   "botoes_borda": (200, 200, 200),

   "texto_espaco_vitoriaMorte": (100, 100, 100),
   "texto_vitoria": (250, 250, 100),
   "texto_morte": (250, 100, 100),

   "texto_titulo_credito": (250, 250, 100),
   "texto_estatisticas_tempo_de_jogo": (210, 200, 165), #RGB
   "texto_estatisticas_moedas": (140, 180, 210),
   "texto_estatisticas_inimigos": (220, 30, 90),
   "texto_outros_creditos": (240, 240, 180),
   
   "cobra_ativo": (10, 200, 100),
   "cobra_safe": (70, 70, 80),
   
   "moeda": (140, 180, 210),
   "moedaVitoria": (250, 250, 100),
   
   "inimigo": (220, 30, 90),
   "inimigoQuicante": (215, 20, 100),

   "decoracaoEstrela": (110, 100, 130),
   "contagemAviso": (10, 0, 35),

   "moeda_obstaculoAviso": (110, 110, 140),
   "inimigo_obstaculoAviso": (140, 110, 110),
   "aumentou_obstaculoAviso": (100, 100, 250),
   "diminuiu_obstaculoAviso": (250, 100, 100),
}

#//

#TODO: PROTNO!    Colocar decoração... EM PROCESSO, resetar quando mudar de tamanho

#TODO: PRONTO   ? organizar as cores?

#TODO: VERIFICADO TUDO CERTO! Verificar se os avisos de obstaculos estao sendo centralizados quando pula de fase para outra

#TODO: CORRIGIDO... BUG: quando clica muito rápido, os efeitos sonoras que contem alguma diminuiçar/aumento de som CRASHA

#TODO: ACHO QUE TA BOM...! Diminuir o tempo de diminuir e aumentar a musica no PAUSE

#TODO: PRONTO! + SOM AO CHEGAR NA FASE DE GANHAR

#TODO: FIZ A TELA DE VITORIA - MAS, não implementei o "fade", usei o mesmo do GameOver de clicar no espaço, e além disso não coloquei AINDA os créditos...

#TODO: tirei os "bumps" no final dos efeitos sonoros. Mas não sei se eu devo trocar o efeito de pegar moeda... e de aumentar nivel, mas estou mais de muda o da moeda, mas não sei, enfim, tirei os bumps

#TODO: BUG tem como ganhar e perder... eu encostei no bloco da vitoria, acionou o som da vitoria mas apareceu a tela de GameOver, não se se eu peguei o inimigo antes ou depois de ter pego o bloco amarelo
###
#TODO: CORRIGIDO o bug de cima... eu coloquei pra a cobra aparecer no meio inves da posicao anterior, assim nao sendo possivel ele continuar na posicao que a tela nao exista quando for diminuir a tela... ela ficava fora e dava que colidiu com o exterior. E alem disso eu coloquei condiçao se o obstaculo esta na lista antes de remove-lo

#TODO: ? Colocar uma velocidade extra que vai aumentar ao decorrer o jogo TODO. Talvez não seja necessário pois ja diminuir a quantidade de salas e com isso aumentei a possibilidade de chegar na fase final de perder...

#TODO: FEITO: Adicionar a minha voz junto com os efetios sonoros, com moeda, vitória, boas-vindas... use Audacity para modicar a voz e ficar 8-bit style

#TODO: FEITO fazer som AO sair do JOGO!!!!!!!

#TODO: FEITO  FAZER O TUTORIAL: Melhor fazer isso quando a mecánica do jogo estiver 100% pronta

#TODO: EU FIZ!!! EU FIZ!!! E TERMINEI NO MESMO DIA... HOJE DIA 20 01 2026!!! FAZER OS CRÉDTIOS QUANDO GANHAR

#TODO FEITO BUG mesmo pausado o cronometro da ultima fase fica on


#/ POR FIM...

#TODO: colocar as estatisticas aparecendo aos poucos igual com os outros creditos
#
#TODO: ajeitar o cronometro que ativa as funçao de desenhar nos creditos

#TODO: ajeitar os sons e remover os sons de pausar_MINHAVOZ

#TODO: ajustar o fade da musica ao pausar e despausar, esta demorando demais e quebra o clima

#TODO: ajustar variaveis? talvez tenha uma variavel que encaixa na Classe dela e nao na Classe Jogo





#TODO corrigir bugs...
#TODO: Organizar o código e otimizar, principalmente as listas... 

#

#TODO: Deixar o jogo justo, divertido e aleatório 

#TODO VERSAO 2.0: Colocar powerUps hehe tipo de ficar invisivel? muita rapidez??? sei la, talvez eu nem faça, vamos ver a Crtiica ne 

#//

def criar_botoes(*, tamanho_tela, tamanho_botoes, quantos_botoes, pos_y, gap, frases, razao=1):
   tamanho_botoes = (int(tamanho_botoes[0]), int(tamanho_botoes[1]))
   tela_meio_botao = (tamanho_tela // 2) - (tamanho_botoes[0] // 2)

   lista_botoes = []
   gapTotal = 0
   for i in range(quantos_botoes):
      lista_botoes.append(pygame.Rect((tela_meio_botao, pos_y + gapTotal), tamanho_botoes))
      gapTotal += gap + tamanho_botoes[1]
      
   palavras_botoes = frases
   texto_botoes = []
   texto_botoes_rect_pos = []
   for i, palavra in enumerate(palavras_botoes):
      texto_botoes.append(FONTE(int(20 * razao)).render(palavra, 0, CORES["texto_botoes"]))
      texto_botoes_rect_pos.append(texto_botoes[i].get_rect(center=(lista_botoes[i].center)))
   
   return lista_botoes, texto_botoes, texto_botoes_rect_pos

def centralizar_texto_corretamente(texto_surface, pos_x, pos_y):
   rect_todo = texto_surface.get_rect()
   rect_apenas_texto = texto_surface.get_bounding_rect()
   espaço_extra = rect_todo.width - rect_apenas_texto.width
   rect_todo.center = (pos_x + (espaço_extra//2), pos_y)
   return rect_todo

#//

FPS = 60

class Variaveis:
   def __init__(self):
      self.variavel = { 
         # tela, bloco, V, distancia_minima, moedas / inimigos
         "tela-vitoria": [(600, 600), 0, 0, 0, 0, 0],

         "tela+5": [(825, 825), 55, 11, 95, 0, 21],
         "tela+4": [(780, 780), 52, 11, 94, 2, 20],
         "tela+3": [(735, 735), 49, 10, 90, 3, 18],
         "tela+2": [(690, 690), 46,  9, 80, 4, 18],
         "tela+1": [(645, 645), 43,  8, 76, 5, 15],
         "tela0": [(600, 600), 40, 7, 72, 5, 15],
         "tela-1": [(555, 555), 37,  7, 66, 5, 15],
         "tela-2": [(510, 510), 34,  8, 64, 4, 14],
         
         "tela-morte": [(600, 600), 0, 0, 0, 0, 0],
      }

      fase_boot = 1
      self.array = list(self.variavel.values())
      self.atual = self.array[fase_boot]
      self.atual_inicio = self.array[6]
      
      self.indice = self.array.index(self.atual)
      self.bloco_inicial = self.array[6][1]
   
   def preset_tudo_atualizar(self, preset_novo_soma):
      self.indice += preset_novo_soma
      self.atual = self.array[self.indice]

#! [0] -> Tela (x, y)
#! [1] -> Bloco (cobra, moedas e inimigos)
#! [2] -> Velocidade da cobra
#! [3] -> distancia_minima
#! [4] -> moedas quantidade
#! [5] -> inimigos quantidade

#//

class Cobra:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      decrescimo = -100
      inicio_x = (self.VARIAVEIS.atual[0][0] / 2) - (self.VARIAVEIS.atual[1] / 2)
      inicio_y = self.VARIAVEIS.atual[0][1] + decrescimo
      
      self.CIMA = (0, -self.VARIAVEIS.atual[2])
      self.DIREITA = (self.VARIAVEIS.atual[2], 0)
      self.BAIXO = (0, self.VARIAVEIS.atual[2])
      self.ESQUERDA = (-self.VARIAVEIS.atual[2], 0)
      self.constante_razao_velocidade = 1
      
      self.corpo = pygame.Rect(inicio_x, inicio_y, self.VARIAVEIS.atual[1], self.VARIAVEIS.atual[1])
      self.velocidade = list(self.CIMA) 

      self.cobra_rect_atualizar(inicio_x, inicio_y)
   def cobra_rect_atualizar(self, x, y):
      self.pos_x = x
      self.pos_y = y
      self.corpo = pygame.Rect(self.pos_x, self.pos_y, self.VARIAVEIS.atual[1], self.VARIAVEIS.atual[1])
   
   def mover_cobra(self):
      self.CIMA = (0, -self.VARIAVEIS.atual[2])
      self.DIREITA = (self.VARIAVEIS.atual[2], 0)
      self.BAIXO = (0, self.VARIAVEIS.atual[2])
      self.ESQUERDA = (-self.VARIAVEIS.atual[2], 0)

      self.corpo.x += int(self.velocidade[0] * self.constante_razao_velocidade)
      self.corpo.y += int(self.velocidade[1] * self.constante_razao_velocidade)
   
   def colidiu_borda_cobra(self):
      if (self.corpo.x + self.VARIAVEIS.atual[1] > self.VARIAVEIS.atual[0][0] or 
          self.corpo.y + self.VARIAVEIS.atual[1] > self.VARIAVEIS.atual[0][1] or 
          self.corpo.x < 0 or 
          self.corpo.y < 0):
         return True

   def direcionar_cobra(self, direcao_nova):
      if not (self.velocidade[0] != 0 and direcao_nova[0] != 0 or
              self.velocidade[1] != 0 and direcao_nova[1] != 0):
         self.velocidade = list(direcao_nova)

   def desenhar_cobra(self, tela, cor):
      pygame.draw.rect(tela, cor, self.corpo)
   
#//

class Moeda:
   def __init__(self, VARIAVEIS, posicao):
      self.VARIAVEIS = VARIAVEIS

      self.tamanho_padrao = self.VARIAVEIS.atual[1] / 1.6
      self.tamanho_atual = self.VARIAVEIS.atual[1] / 7
      self.fase = "crescendo"

      self.centro_xy = (posicao[0], posicao[1])
      self.rect = pygame.Rect(posicao, [self.tamanho_atual, self.tamanho_atual])

   def animacao_moeda(self):
      velocidade = 2

      if self.fase == "crescendo":
         self.tamanho_atual += velocidade
         if self.tamanho_atual >= self.tamanho_padrao * 1.3: # Aumentar o tamanho padrão
            self.fase = "encolhendo"
      
      if self.fase == "encolhendo":
         self.tamanho_atual -= velocidade
         if self.tamanho_atual <= self.tamanho_padrao:
            self.tamanho_atual = self.tamanho_padrao
            self.fase = "completo"
      
      self.rect.size = (self.tamanho_atual, self.tamanho_atual) 
      self.rect.center = (self.centro_xy)

#//

class Inimigo:
   def __init__(self, VARIAVEIS, posicao):
      self.VARIAVEIS = VARIAVEIS

      self.tamanho_padrao = self.VARIAVEIS.atual[1] / 2
      self.tamanho_atual = [self.VARIAVEIS.atual[1] / 1.2, self.VARIAVEIS.atual[1] / 1.28]
      self.fase = "encolhendo"

      self.centro_xy = (posicao[0], posicao[1])
      self.rect = pygame.Rect(posicao, self.tamanho_atual)

   def animacao_inimigo(self):
      velocidade = 0.8

      if self.fase == "encolhendo":
         self.tamanho_atual[0] -= velocidade
         self.tamanho_atual[1] -= velocidade
         if self.tamanho_atual[0] <= self.tamanho_padrao * 0.8: #Diminuir o tamanho padrão
            self.fase = "crescendo"
      
      if self.fase == "crescendo":
         self.tamanho_atual[0] += velocidade
         self.tamanho_atual[1] += velocidade
         if self.tamanho_atual[0] >= self.tamanho_padrao:
            self.tamanho_atual[1] = self.tamanho_padrao
            self.tamanho_atual[0] = self.tamanho_padrao
            self.fase = "completo"
      
      self.rect.size = (self.tamanho_atual[0], self.tamanho_atual[1])
      self.rect.center = (self.centro_xy)

#//

class QuicanteInimigo:
   def __init__(self, VARIAVEIS, pos):
      self.VARIAVEIS = VARIAVEIS
      
      self.qui_tamanho_padrao = self.VARIAVEIS.atual[1] // 1.7
      self.rect = pygame.Rect(pos, (self.qui_tamanho_padrao, self.qui_tamanho_padrao))

      velocidade = 4
      self.velocidade_x = random.choice([-velocidade, velocidade]) * (random.random() + 1)
      self.velocidade_y = random.choice([-velocidade, velocidade]) * (random.random() + 1)
   
   def quicante_desenhar_inimigo(self, tela):
      pygame.draw.rect(tela, CORES["inimigoQuicante"], self.rect)
   
   def quicante_mover_inimigo(self):
      self.rect.x += self.velocidade_x
      self.rect.y += self.velocidade_y

      if self.rect.x <= 0 or self.rect.x + self.qui_tamanho_padrao >= self.VARIAVEIS.atual[0][0]:
         self.velocidade_x *= -1
      
      if self.rect.y <= 0 or self.rect.y + self.qui_tamanho_padrao >= self.VARIAVEIS.atual[0][1]:
         self.velocidade_y *= -1

#//

class Obstaculo:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.moedas_objetos = []
      self.inimigos_objetos = []
      self.moeda_vitoria_objeto = []
      self.posicoes_feitas = []

   def criar_posicoes(self):
      self.QUANTIDADE_MOEDAS = self.VARIAVEIS.atual[4]
      self.QUANTIDADE_INIMIGOS = self.VARIAVEIS.atual[5]
      self.QUANTIDADE_POSICOES = int((self.QUANTIDADE_MOEDAS + self.QUANTIDADE_INIMIGOS) + 2)
      
      self.distancia_minima = self.VARIAVEIS.atual[3]

      numero_de_posicoes_minimas = 10
      
      while len(self.posicoes_feitas) < numero_de_posicoes_minimas:
         procurar = True
         
         tentativas = 0
         tentativas_max = 100
         while procurar:
            procurar = False

            tentativas += 1
            if tentativas > tentativas_max:
               print("ERRO NA CRIAÇÃO DE OBSTÁCULOS - LIMITE ULTRAPASSADO")
               break
            
            margem = self.VARIAVEIS.atual[1] // 2
            pos_x = random.randint(margem, self.VARIAVEIS.atual[0][0] - margem)
            pos_y = random.randint(margem, self.VARIAVEIS.atual[0][1] - margem)

            for moeda in self.moedas_objetos:
               distancia_entre_blocos = math.sqrt((moeda.centro_xy[0] - pos_x)**2 + (moeda.centro_xy[1] - pos_y)**2)   
               if not (distancia_entre_blocos > self.distancia_minima):
                  procurar = True
                  break
            
            for inimigo in self.inimigos_objetos:
               distancia_entre_blocos = math.sqrt((inimigo.centro_xy[0] - pos_x)**2 + (inimigo.centro_xy[1] - pos_y)**2)   
               if not (distancia_entre_blocos > self.distancia_minima):
                  procurar = True
                  break
            
            for (x, y) in self.posicoes_feitas:
               distancia_entre_blocos = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
               if not (distancia_entre_blocos > self.distancia_minima):
                  procurar = True
                  break
         self.posicoes_feitas.append((pos_x, pos_y))      

   def criar_objetos_obstaculos(self):
      for posicao in self.posicoes_feitas[:]:
         if len(self.moedas_objetos) < self.QUANTIDADE_MOEDAS:
            moeda = Moeda(self.VARIAVEIS, posicao)
            self.moedas_objetos.append(moeda)
            self.posicoes_feitas.remove(posicao)
         
         elif len(self.inimigos_objetos) < self.QUANTIDADE_INIMIGOS:
            inimigo = Inimigo(self.VARIAVEIS, posicao)
            self.inimigos_objetos.append(inimigo)
            self.posicoes_feitas.remove(posicao)
   
   def desenhar_obstaculos(self, tela):
      for moeda in self.moedas_objetos:
         pygame.draw.rect(tela, CORES["moeda"], moeda.rect)
      
      for inimigo in self.inimigos_objetos:
         pygame.draw.rect(tela, CORES["inimigo"], inimigo.rect)
   
   def criar_vitoria_moeda(self):
      if len(self.moeda_vitoria_objeto) < 1:
         for posicao in self.posicoes_feitas[:]:
            moeda_vitoria = Moeda(self.VARIAVEIS, posicao)
            self.moeda_vitoria_objeto.append(moeda_vitoria)
            self.posicoes_feitas.remove(posicao)
   def desenhar_vitoria_moeda(self, tela):
      pygame.draw.rect(tela, CORES["moedaVitoria"], self.moeda_vitoria_objeto[0].rect)

#//

class Decoracao:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.posicoes_feitas = []
      self.decoracoes_feitas = []
      self.distancia_minima = 25
      self.quantidade = 80
      # self.cor = (110, 100, 130)
      self.transparencia = 45

      self.resetar_decoracao()
   def resetar_decoracao(self):
      self.posicoes_feitas = []
      self.decoracoes_feitas = []
      self.criar_decoracao_posicoes()
      self.criar_decoracao_rect()
   
   def criar_decoracao_posicoes(self):
      self.posicoes_feitas = []
      while len(self.posicoes_feitas) < self.quantidade:
         procurar = True
         while procurar:
            procurar = False
            
            tamanho = 30
            margem = tamanho // 2
            pos_x = random.randint(margem, self.VARIAVEIS.atual[0][0] - margem - tamanho)
            pos_y = random.randint(margem, self.VARIAVEIS.atual[0][1] - margem - tamanho)
            
            for (x, y) in self.posicoes_feitas:
               distancia_entre_blocos = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
               if not (distancia_entre_blocos > self.distancia_minima):
                  procurar = True
                  break
         self.posicoes_feitas.append((pos_x, pos_y))
      
   def criar_decoracao_rect(self):
      for posicao in self.posicoes_feitas:
         tamanho = random.randint(5, 11)
         surface = pygame.Surface((tamanho, tamanho))
         surface.fill(CORES["decoracaoEstrela"])
         surface.set_alpha(self.transparencia)

         self.decoracoes_feitas.append((surface, posicao))
   def desenhar_decoracao(self, tela):
      for surface, posicao in self.decoracoes_feitas:
         tela.blit(surface, posicao)

#//

class Aviso:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

   def criar_desenho_avisos(self, tela, texto, cor):
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2
      self.pos_y_meio = self.VARIAVEIS.atual[0][1] // 2
      self.razao = self.VARIAVEIS.atual[1] / self.VARIAVEIS.bloco_inicial # Bloco inicial e bloco atual da tela
      
      self.tituloAviso = FONTE(int(60 * self.razao)).render((texto), 0, cor)
      self.tituloAviso.set_alpha(100) 
      self.tituloAviso_pos = centralizar_texto_corretamente(self.tituloAviso, self.pos_x_meio, self.pos_y_meio)

      tela.blit(self.tituloAviso, self.tituloAviso_pos)
   
   def criar_desenho_contagem(self, tela, texto):
      decrescimo = -200
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2
      self.pos_y = self.VARIAVEIS.atual[0][1] + decrescimo
      
      self.tituloContagem = FONTE(250).render((texto), 0, CORES["contagemAviso"])
      self.tituloContagem_pos = centralizar_texto_corretamente(self.tituloContagem, self.pos_x_meio, self.pos_y)

      tela.blit(self.tituloContagem, self.tituloContagem_pos)

#//

class Pause:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.lista_botoes, self.texto_botoes, self.texto_botoes_pos = [], [], []

      self.criar_pause()
   def criar_pause(self):
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2
      self.razao = self.VARIAVEIS.atual[1] / self.VARIAVEIS.bloco_inicial # Bloco inicial e bloco atual da tela

      espaco_ate_margem = int(self.VARIAVEIS.atual[0][1] / 6)
      pos_y = 30 + espaco_ate_margem
      
      self.tituloPause = FONTE(int(35 * self.razao)).render(("Pausado!"), 0, CORES["texto1_pause"])
      self.tituloPause_pos = centralizar_texto_corretamente(self.tituloPause, self.pos_x_meio, pos_y * self.razao)

      acrescimo_na_pos_y = pos_y + 40
      self.subTituloPause = FONTE(int(15 * self.razao)).render(("Pressione [space] para continuar"), 0, CORES["texto2_pause"])
      self.subTituloPause_pos = centralizar_texto_corretamente(self.subTituloPause, self.pos_x_meio, acrescimo_na_pos_y * self.razao)

      self.lista_botoes, self.texto_botoes, self.texto_botoes_pos = criar_botoes(tamanho_tela = self.VARIAVEIS.atual[0][0],
                                                                               tamanho_botoes = (380 * self.razao, 80 * self.razao), 
                                                                               quantos_botoes = 2, 
                                                                                        pos_y = (395 - espaco_ate_margem) * self.razao,  
                                                                                          gap = 30 * self.razao, 
                                                                                       frases = ["Sair para o menu", "Sair do jogo"], 
                                                                                        razao = self.razao)
                                                                          
      
      self.overlay = pygame.Surface((self.VARIAVEIS.atual[0]))
      self.overlay.fill((0, 0, 0))
      self.overlay.set_alpha(220)
      
   def desenhar_pause(self, tela):
      tela.blit(self.overlay, (0, 0))
      tela.blit(self.tituloPause, self.tituloPause_pos)
      tela.blit(self.subTituloPause, self.subTituloPause_pos)
      
      for botao in self.lista_botoes:
         pygame.draw.rect(tela, CORES["botoes_fundo"], botao, 0, 10)
         pygame.draw.rect(tela, CORES["botoes_borda"], botao, 3, 10)
      
      for texto, texto_pos in zip(self.texto_botoes, self.texto_botoes_pos):
         tela.blit(texto, texto_pos)

#//

class Menu:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS  
      self.pos_x_meio = self.VARIAVEIS.atual_inicio[0][0] // 2

      pos_y = 100
      self.titulo = FONTE(38).render("Hora do Lesk!", 0, CORES["texto1_menu"])
      self.titulo_pos = centralizar_texto_corretamente(self.titulo, self.pos_x_meio, pos_y)

      acrescimo_na_pos_y = pos_y + 40
      self.subTitulo = FONTE(18).render("Feito por cac <3", 0, CORES["texto2_menu"])
      self.subTitulo_pos = centralizar_texto_corretamente(self.subTitulo, self.pos_x_meio, acrescimo_na_pos_y)

      #//
      
      self.lista_botoes, self.texto_botoes, self.texto_botoes_pos = criar_botoes(tamanho_tela = self.VARIAVEIS.atual_inicio[0][0], 
                                                                               tamanho_botoes = (210, 80), 
                                                                               quantos_botoes = 3, 
                                                                                        pos_y = 240, 
                                                                                          gap = 30, 
                                                                                       frases = ["Jogar", "Tutorial", "Sair"])
                                                                                  

   def desenhar_menu(self, tela):
      tela.blit(self.titulo, self.titulo_pos)
      tela.blit(self.subTitulo, self.subTitulo_pos)
      
      for botao in self.lista_botoes: # Criar bordas coloridas nos botões
         pygame.draw.rect(tela, CORES["botoes_fundo"], botao, 0, 10) 
         pygame.draw.rect(tela, CORES["botoes_borda"], botao, 3, 10)
      
      for texto, texto_pos in zip(self.texto_botoes, self.texto_botoes_pos):
         tela.blit(texto, texto_pos)

#//

class Creditos:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS 
      self.pos_x_meio = self.VARIAVEIS.atual_inicio[0][0] // 2

      pos_y = 100
      self.titulo = FONTE(40).render("Creditos", 0, CORES["texto_titulo_credito"])
      self.titulo_pos = centralizar_texto_corretamente(self.titulo, self.pos_x_meio, pos_y)

      self.outros_creditos = {
         "Diretor de Jogo": "cac",
         "Diretor Tecnico": "cac",
         "Diretor Criativo": "cac",
         "Programador": "cac",
         "Artista": "cac",
         "Audio": "cac",
      }
      
      self.tempo_espera_estatisticas = 0
      self.tempo_espera = 0

   def desenhar_creditos_titulo(self, tela):
      tela.blit(self.titulo, self.titulo_pos)
   
   def desenhar_creditos_estatisticas(self, tela, valores, tempo_de_jogo):
      pos_y_1 = 170 + (4*2)
      pos_y_2 = pos_y_1 + 25
      pos_y_3 = pos_y_2 + 25
      
      if tempo_de_jogo[0] == "segundos":
         self.estatisticas_tempo = FONTE(17).render(f"Jogou por {tempo_de_jogo[1]} segundos", 0, CORES["texto_estatisticas_tempo_de_jogo"])
      elif tempo_de_jogo[0] == "minutos":
         self.estatisticas_tempo = FONTE(17).render(f"Jogou por {tempo_de_jogo[1]} minutos", 0, CORES["texto_estatisticas_tempo_de_jogo"])
      
      self.estatisticas_tempo_pos = centralizar_texto_corretamente(self.estatisticas_tempo, self.pos_x_meio, pos_y_1)

      self.estatisticas_moedas = FONTE(17).render(f"Pegou {valores[0]} moedas!", 0, CORES["texto_estatisticas_moedas"])
      self.estatisticas_moedas_pos = centralizar_texto_corretamente(self.estatisticas_moedas, self.pos_x_meio, pos_y_2)
      
      self.estatisticas_inimigos = FONTE(17).render(f"Pegou {valores[1]} inimigos...", 0, CORES["texto_estatisticas_inimigos"])
      self.estatisticas_inimigos_pos = centralizar_texto_corretamente(self.estatisticas_inimigos, self.pos_x_meio, pos_y_3)

      # lista = [
      #    [self.estatisticas_tempo, self.estatisticas_tempo_pos],
      #    [self.estatisticas_moedas, self.estatisticas_moedas_pos],
      #    [self.estatisticas_inimigos, self.estatisticas_inimigos_pos],
      # ]

      # intervalo = 0

      # for elemento in lista:
      #    if self.tempo_espera_estatisticas > intervalo:
      #       intervalo += 350
      #       tela.blit(elemento[0], elemento[1])
      #    self.tempo_espera_estatisticas += 1
      
      tela.blit(self.estatisticas_tempo, self.estatisticas_tempo_pos)
      tela.blit(self.estatisticas_moedas, self.estatisticas_moedas_pos)
      tela.blit(self.estatisticas_inimigos, self.estatisticas_inimigos_pos)

   def desenhar_outros_creditos(self, tela):
      pos_y = 290 - (4*3)
      gap = 0
      intervalo = 350

      for tipo, nome in self.outros_creditos.items():
         if self.tempo_espera > intervalo:
            self.creditos = FONTE(17).render(f"{tipo}: {nome}", 0, CORES["texto_outros_creditos"])
            self.creditos_pos = centralizar_texto_corretamente(self.creditos, self.pos_x_meio, pos_y + gap)
            gap += 30
            intervalo += 350
            tela.blit(self.creditos, self.creditos_pos)
         self.tempo_espera += 1
   
   def desenhar_agradecimento(self, tela):
      pos_y = 500
      self.agradecimento = FONTE(21).render("Obrigado por jogar ;)", 0, CORES["texto_titulo_credito"])
      self.agradecimento_pos = centralizar_texto_corretamente(self.agradecimento, self.pos_x_meio, pos_y)
      tela.blit(self.agradecimento, self.agradecimento_pos)

#//

class TelaVitoriaMorte:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS
   
   def desenhar_vitoriaMorte(self, tela, frase, cor):
      self.pos_x_meio = self.VARIAVEIS.atual_inicio[0][0] // 2

      decrescimo = -10
      self.tituloVitoriaMorte = FONTE(50).render(frase, 0, cor)
      self.tituloVitoriaMorte_pos = centralizar_texto_corretamente(self.tituloVitoriaMorte, self.pos_x_meio, self.VARIAVEIS.atual_inicio[0][1] // 2 + decrescimo)
      
      tela.blit(self.tituloVitoriaMorte, self.tituloVitoriaMorte_pos)
   
   def desenhar_comentario_vitoriaMorte(self, tela, frase1, frase2, cor):
      acrescimo_1 = 30
      self.comentarioVitoriaMorte_1 = FONTE(15).render(frase1, 0, cor)
      self.comentarioVitoriaMorte_1_pos = centralizar_texto_corretamente(self.comentarioVitoriaMorte_1, self.pos_x_meio, self.VARIAVEIS.atual_inicio[0][1] // 2 + acrescimo_1)
      
      acrescimo_2 = acrescimo_1 + 22
      self.comentarioVitoriaMorte_2 = FONTE(15).render(frase2, 0, cor)
      self.comentarioVitoriaMorte_2_pos = centralizar_texto_corretamente(self.comentarioVitoriaMorte_2, self.pos_x_meio, self.VARIAVEIS.atual_inicio[0][1] // 2 + acrescimo_2)
      
      tela.blit(self.comentarioVitoriaMorte_1, self.comentarioVitoriaMorte_1_pos)
      tela.blit(self.comentarioVitoriaMorte_2, self.comentarioVitoriaMorte_2_pos)
   
   def desenhar_space_vitoriaMorte(self, tela):
      decrescimo = -20
      self.espacoMorte = FONTE(15).render("Pressione [space] para voltar", 0, CORES["texto_espaco_vitoriaMorte"])
      self.espacoMorte_pos = centralizar_texto_corretamente(self.espacoMorte, self.pos_x_meio - 2, self.VARIAVEIS.atual_inicio[0][1] + decrescimo)
      tela.blit(self.espacoMorte, self.espacoMorte_pos)

#// // // // // // //

class Jogo:
   def __init__(self):
      pygame.mixer.pre_init(44100, -16, 2, 512)
      pygame.init()
      self.executar_todas_classes()

      self.RELACAO_ATUAL = "no_menu"
      self.titulo = pygame.display.set_caption("HORA DO LESK!")
      self.tempo = pygame.time.Clock()
      
      imagem_icon = pygame.image.load(CAMINHOS["imagem_icon"])
      pygame.display.set_icon(imagem_icon)
      
      pywinstyles.apply_style(pygame.display.get_wm_info()['window'], "dark")

      self.TIMER_EVENT = pygame.USEREVENT + 1
      pygame.time.set_timer(self.TIMER_EVENT, 1000)

      self.EFEITOS = {
         "clicar_botao": pygame.mixer.Sound(CAMINHOS["clicar_botao"]),
         "sair_do_jogo": pygame.mixer.Sound(CAMINHOS["sair_do_jogo"]),
         "comecando_partida_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["comecando_partida_MINHAVOZ"]),
         "voltando_para_menu_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["voltando_para_menu_MINHAVOZ"]),
         
         "musica_perder_jogo": pygame.mixer.Sound(CAMINHOS["musica_perder_jogo"]),
         "perder_jogo_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["perder_jogo_MINHAVOZ"]),
         "musica_ganhar_jogo": pygame.mixer.Sound(CAMINHOS["musica_ganhar_jogo"]),
         "ganhar_jogo_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["ganhar_jogo_MINHAVOZ"]),

         "pegar_moeda": pygame.mixer.Sound(CAMINHOS["pegar_moeda"]),
         "pegar_moeda_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["pegar_moeda_MINHAVOZ"]),
         "pegar_inimigo": pygame.mixer.Sound(CAMINHOS["pegar_inimigo"]),

         "pausar": pygame.mixer.Sound(CAMINHOS["pausar"]),
         "pausar_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["pausar_MINHAVOZ"]),
         "despausar": pygame.mixer.Sound(CAMINHOS["despausar"]),
         "despausar_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["despausar_MINHAVOZ"]),

         "aumentar_fase": pygame.mixer.Sound(CAMINHOS["aumentar_fase"]),
         "aumentar_fase_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["aumentar_fase_MINHAVOZ"]),
         "diminuir_fase": pygame.mixer.Sound(CAMINHOS["diminuir_fase"]),
         "diminuir_fase_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["diminuir_fase_MINHAVOZ"]),
         
         "alertar_ultima_sala": pygame.mixer.Sound(CAMINHOS["alertar_ultima_sala"]),
         "alertar_vitoria_sala": pygame.mixer.Sound(CAMINHOS["alertar_vitoria_sala"]),
         "alertar_vitoria_sala_MINHAVOZ": pygame.mixer.Sound(CAMINHOS["alertar_vitoria_sala_MINHAVOZ"]),
      }

      self.ajustar_efeitos()

      self.volume_atual = 0
      self.acionar_musica_volume(CAMINHOS["musica_menu"], 0)

      self.rodando = True

   def _recriar_classes(self):
      self.VARIAVEIS = Variaveis()
      self.cobra = Cobra(self.VARIAVEIS)
      self.obstaculo = Obstaculo(self.VARIAVEIS)
      self.menu = Menu(self.VARIAVEIS)
      self.pause = Pause(self.VARIAVEIS)
      self.textoAviso = Aviso(self.VARIAVEIS)
      self.telaVitoriaMorte = TelaVitoriaMorte(self.VARIAVEIS)
      self.decoracao = Decoracao(self.VARIAVEIS)
      self.creditos = Creditos(self.VARIAVEIS)
      self.tela_atualizar_jogo(self.VARIAVEIS.atual_inicio[0])

   def _resetar_variaveis_jogo(self):
      self.moedas_pegas = 0
      self.inimigos_pegos = 0
      self.lista_dois_quicantes = []
      
      self.tutorial_ativo = False
      self.ordem_do_tutorial = 0

      self.moedas_inimigos_pegos_total = [0, 0]
      self.jogo_pausado = False
   
   def _resetar_timers(self):
      self.nao_pode_colidir_por = 200 # Começa a partida com 200 frames sem colidir
      self.congelar_jogo_por = 200 # Começa a partida com 200 frames tudo congelado
   
      self.colidiu_aviso_booleano()
      self.duracao_obstaculo_aviso = 0
   
      self.fase_final_contagem = -self.nao_pode_colidir_por
      self.fase_final_variavel = 0
      
      self.intervalo_dos_textos_vitoriaMorte = 0
      self.motivo_da_morte = None
      
      self.duracao_acrescentar_velocidade_porFase = 0
      self.tempo_musica_fade = 0

      self.intervalo_dos_textos_creditos = 0
      
      self.tempo_de_jogo = 0
  
   def executar_todas_classes(self):
      self._recriar_classes()
      self._resetar_variaveis_jogo()
      self._resetar_timers()

   def ajustar_efeitos(self):
      self.VOLUMES = {
         "musica_menu": 0.20,
         "musica_tutorial": 0.30,
         "musica_creditos": 0.30,
         
         "musica_jogo_max": 0.12, 
         "musica_jogo_min": 0.03, 

         "pausar": 0.30,
         "despausar": 0.30,
         "alertar_ultima_sala": 0.7,
         "sair_do_jogo": 0.30,

         "MINHAVOZ": 0.45,
      }
      
      self.EFEITOS["pausar"].set_volume(self.VOLUMES["pausar"])
      self.EFEITOS["despausar"].set_volume(self.VOLUMES["despausar"])
      self.EFEITOS["alertar_ultima_sala"].set_volume(self.VOLUMES["alertar_ultima_sala"]) 
      self.EFEITOS["sair_do_jogo"].set_volume(self.VOLUMES["sair_do_jogo"])
      
      for chave, som in self.EFEITOS.items():
         if "MINHAVOZ" in chave:
            som.set_volume(self.VOLUMES["MINHAVOZ"])

   #//

   def tela_atualizar_jogo(self, tamanho):
      self.tela = pygame.display.set_mode(tamanho)

   def acionar_musica_volume(self, musica, volume):
      pygame.mixer.music.load(musica)
      self.volume_atual = volume
      self.volume = pygame.mixer.music.set_volume(self.volume_atual)
      pygame.mixer.music.play(-1, fade_ms=2000)

   def diminuir_aumentar_som_smooth(self, soma, *, duracao=0, vol_min=0, vol_max=0, aumentar_quanto=1):
      if duracao % aumentar_quanto != 0:
         raise Exception("Número inválido")
      
      if soma == -0.01:
         if self.volume_atual > vol_min:
            if self.tempo_musica_fade > duracao: # Sempre True para efeitos
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += aumentar_quanto
      if soma == 0.01: 
         if self.volume_atual < vol_max: # Volume maximo da música de jogo
            if self.tempo_musica_fade > duracao: # Sempre True para efeitos
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += aumentar_quanto
   
   def mostrar_tutorial(self):
      if self.ordem_do_tutorial < len(ARRAY_TUTORIAL):
         if self.ordem_do_tutorial < 0:
            self.ordem_do_tutorial = 0
         imagem_tutorial = pygame.image.load(ARRAY_TUTORIAL[self.ordem_do_tutorial])
         self.tela.blit(imagem_tutorial, (0, 0))
      else:
         self.tutorial_ativo = False
         self.acionar_musica_volume(CAMINHOS["musica_menu"], self.VOLUMES["musica_menu"])
      
   #//

   def processar_eventos_jogo(self):
      for evento in pygame.event.get():
         
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas_jogo(evento.key)
         
         elif self.RELACAO_ATUAL == "no_jogo" and not self.jogo_pausado == True:
            if evento.type == self.TIMER_EVENT:
               self.tempo_de_jogo += 1
               print("DEBUG TEMPO:", self.tempo_de_jogo)
               
         elif self.RELACAO_ATUAL == "no_menu" and not self.tutorial_ativo:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
               posicao_mouse = evento.pos
               
               for botao_menu in self.menu.lista_botoes:
                  if botao_menu.collidepoint(posicao_mouse):
                     pygame.mixer.stop()
                     self.EFEITOS["clicar_botao"].play()
                     
                     if botao_menu == self.menu.lista_botoes[0]:
                        self.EFEITOS["comecando_partida_MINHAVOZ"].play()
                        self.RELACAO_ATUAL = "no_jogo"
                        self.tela_atualizar_jogo(self.VARIAVEIS.atual[0])
                        self.acionar_musica_volume(CAMINHOS["musica_jogo"], self.VOLUMES["musica_jogo_max"])
                     
                     if botao_menu == self.menu.lista_botoes[1]:
                        self.tutorial_ativo = True
                        self.acionar_musica_volume(CAMINHOS["musica_tutorial"], self.VOLUMES["musica_tutorial"])

                     if botao_menu == self.menu.lista_botoes[2]:
                        pygame.mixer.stop()
                        self.EFEITOS["sair_do_jogo"].play()
                        while pygame.mixer.get_busy():
                           self.rodando = False
 
         elif self.jogo_pausado == True:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
               posicao_mouse = evento.pos
               
               for botao_pause in self.pause.lista_botoes:
                  if botao_pause.collidepoint(posicao_mouse):
                     pygame.mixer.stop()
                     self.EFEITOS["clicar_botao"].play()

                     if botao_pause == self.pause.lista_botoes[0]:
                        self.EFEITOS["voltando_para_menu_MINHAVOZ"].play()
                        self.RELACAO_ATUAL = "no_menu"
                        self.acionar_musica_volume(CAMINHOS["musica_menu"], self.VOLUMES["musica_menu"])
                        self.executar_todas_classes()
                     
                     if botao_pause == self.pause.lista_botoes[1]:
                        pygame.mixer.stop()
                        self.EFEITOS["sair_do_jogo"].play()
                        while pygame.mixer.get_busy():
                           self.rodando = False

   def processar_teclas_jogo(self, tecla):
      if self.tutorial_ativo:
         if tecla == pygame.K_SPACE:
            self.EFEITOS["clicar_botao"].play()
            self.ordem_do_tutorial += 1
         if tecla == pygame.K_ESCAPE:
            self.EFEITOS["clicar_botao"].play()
            self.ordem_do_tutorial -= 1

      if self.RELACAO_ATUAL in ("no_gameover", "nos_creditos"):
         if tecla == pygame.K_SPACE:
            pygame.mixer.stop()
            self.EFEITOS["clicar_botao"].play()
            self.EFEITOS["voltando_para_menu_MINHAVOZ"].play()
            self.RELACAO_ATUAL = "no_menu"
            self.acionar_musica_volume(CAMINHOS["musica_menu"], self.VOLUMES["musica_menu"])
            self.executar_todas_classes()
      
      if self.RELACAO_ATUAL == "na_vitoria":
         if tecla == pygame.K_SPACE:
            pygame.mixer.stop()
            self.EFEITOS["clicar_botao"].play()
            self.RELACAO_ATUAL = "nos_creditos"
            self.acionar_musica_volume(CAMINHOS["musica_creditos"], self.VOLUMES["musica_creditos"])
            self.tela_atualizar_jogo(self.VARIAVEIS.atual_inicio[0])

      if self.RELACAO_ATUAL == "no_jogo":
         if tecla == pygame.K_RIGHT:
            self.cobra.direcionar_cobra(self.cobra.DIREITA)
         if tecla == pygame.K_UP:
            self.cobra.direcionar_cobra(self.cobra.CIMA)
         if tecla == pygame.K_LEFT:
            self.cobra.direcionar_cobra(self.cobra.ESQUERDA)
         if tecla == pygame.K_DOWN:
            self.cobra.direcionar_cobra(self.cobra.BAIXO)
         
         if tecla == pygame.K_SPACE:
            if self.jogo_pausado:
               self.congelar_jogo_por = 30
               self.EFEITOS["despausar"].play()
               #self.EFEITOS["despausar_MINHAVOZ"].play()
               self.jogo_pausado = False
            else:
               self.EFEITOS["pausar"].play()
               #self.EFEITOS["pausar_MINHAVOZ"].play()
               self.jogo_pausado = True

   #//

   def colidiu_aviso_booleano(self, *, moeda=False, inimigo=False, up=False, down=False):
      self.aviso_acertou_moeda = moeda
      self.aviso_acertou_inimigo = inimigo
      self.aviso_aumentou_nivel = up
      self.aviso_diminuiu_nivel = down

   def remover_obstaculos_aleatorios(self, remover_moedas, remover_inimigos):
      if self.obstaculo.moedas_objetos:
         for x in range(min(remover_moedas, len(self.obstaculo.moedas_objetos))):
            aleatorio = random.randint(0, len(self.obstaculo.moedas_objetos) - 1)
            self.obstaculo.moedas_objetos.pop(aleatorio)
      
      if self.obstaculo.inimigos_objetos:
         for x in range(min(remover_inimigos, len(self.obstaculo.inimigos_objetos))):
            aleatorio = random.randint(0, len(self.obstaculo.inimigos_objetos) - 1)
            self.obstaculo.inimigos_objetos.pop(aleatorio)

   def animacao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos:
            if moeda.fase != "completo":
               moeda.animacao_moeda()
      for inimigo in self.obstaculo.inimigos_objetos:
            if inimigo.fase != "completo":
               inimigo.animacao_inimigo()          
      
      if self.fase_final_variavel == 9:
         if self.obstaculo.moeda_vitoria_objeto[0].fase != "completo":
             self.obstaculo.moeda_vitoria_objeto[0].animacao_moeda()

   def criar_quicante(self):
      margem = self.VARIAVEIS.atual[1] // 2
      pos_x = random.randint(margem, self.VARIAVEIS.atual[0][0] - margem)
      pos_y = random.randint(margem, self.VARIAVEIS.atual[0][1] - margem)  
      self.lista_dois_quicantes.append(QuicanteInimigo(self.VARIAVEIS, (pos_x, pos_y))) 

   #/

   def escalonar_acionar_variaveis(self, preset_novo):
      self.VARIAVEIS.preset_tudo_atualizar(preset_novo)

      if self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 2): # Se chegou na fase antes do GameOver
         self.EFEITOS["alertar_ultima_sala"].play()
      
      if self.VARIAVEIS.indice == 1:
         self.EFEITOS["alertar_vitoria_sala"].play()
         self.EFEITOS["alertar_vitoria_sala_MINHAVOZ"].play()

      self.obstaculo.moedas_objetos = []
      self.obstaculo.inimigos_objetos = []
      self.lista_dois_quicantes = []
      self.obstaculo.posicoes_feitas = []

      self.tela_atualizar_jogo(self.VARIAVEIS.atual[0])
      self.cobra.cobra_rect_atualizar(self.VARIAVEIS.atual[0][0] // 2, self.VARIAVEIS.atual[0][1] // 2)

      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      self.pause.criar_pause()
      self.decoracao.resetar_decoracao()
   
   def pegou_obstaculo_MAX(self, escala_variaveis):
      self.escalonar_acionar_variaveis(escala_variaveis)
      
      tempo_sem_colidir_base = 160
      acrescimo = 200
      
      if self.VARIAVEIS.indice == 1:
         self.nao_pode_colidir_por = tempo_sem_colidir_base + acrescimo
         self.fase_final_contagem = -self.nao_pode_colidir_por # Contando o tempo que a cobra está sem colidir
         self.fase_final_variavel = 0     
      else:
         self.nao_pode_colidir_por = tempo_sem_colidir_base
      
      (self.moedas_pegas, self.inimigos_pegos) = (0, 0)
      self.duracao_obstaculo_aviso = 70
      self.cobra.constante_razao_velocidade = 1

   def pegou_obstaculo_APENAS(self, obstaculo, tipo):
      if tipo == "moeda":
         self.moedas_pegas += 1
         self.moedas_inimigos_pegos_total[0] += 1
         if obstaculo in self.obstaculo.moedas_objetos[:]:
            self.obstaculo.moedas_objetos.remove(obstaculo)
      
      if tipo == "inimigo_ou_quicante":
         self.inimigos_pegos += 1
         self.moedas_inimigos_pegos_total[1] += 1
         if obstaculo in self.lista_dois_quicantes[:]:
            self.lista_dois_quicantes.remove(obstaculo)
         elif obstaculo in self.obstaculo.inimigos_objetos[:]:
            self.obstaculo.inimigos_objetos.remove(obstaculo)
      
      self.nao_pode_colidir_por = 37
      self.duracao_obstaculo_aviso = 37
   
   def colidiu_obstaculo_moeda(self, moeda_objeto, moedas_maximas, remover_moedas, remover_inimigos):
            self.pegou_obstaculo_APENAS(obstaculo=moeda_objeto, tipo="moeda")
            
            if self.moedas_pegas == moedas_maximas:
               self.colidiu_aviso_booleano(up=True)
               self.pegou_obstaculo_MAX(escala_variaveis=(-1))
               
               self.EFEITOS["aumentar_fase"].play()
               self.EFEITOS["aumentar_fase_MINHAVOZ"].play()
            else:
               self.colidiu_aviso_booleano(moeda=True)
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)         
               self.EFEITOS["pegar_moeda"].play()
               self.EFEITOS["pegar_moeda_MINHAVOZ"].play()
   
   def colidiu_obstaculo_inimigo(self, inimigo_quicante_objeto, inimigos_maximos, remover_moedas, remover_inimigos):
            self.pegou_obstaculo_APENAS(obstaculo=inimigo_quicante_objeto, tipo="inimigo_ou_quicante")
            
            if self.inimigos_pegos == inimigos_maximos:
               self.colidiu_aviso_booleano(down=True)
               if self.VARIAVEIS.indice in ((len(self.VARIAVEIS.array) - 3), (len(self.VARIAVEIS.array) - 2)):
                  self.pegou_obstaculo_MAX(escala_variaveis=(1))
               else:
                  self.pegou_obstaculo_MAX(escala_variaveis=(2))
               
               if not self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1):
                  self.EFEITOS["diminuir_fase"].play()
                  self.EFEITOS["diminuir_fase_MINHAVOZ"].play()
            else:
               self.colidiu_aviso_booleano(inimigo=True)
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)               
               self.EFEITOS["pegar_inimigo"].play()
               # Sem efeito de voz ao pegar inimigo

   def colidiu_obstaculos(self):
      moedas_maximas = 5
      inimigos_maximos = 40
      remover_moedas = (self.obstaculo.QUANTIDADE_MOEDAS - 1) // 2
      remover_inimigos = (self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2
      
      if self.VARIAVEIS.indice == 1 and self.fase_final_variavel == 9:
            if self.cobra.corpo.colliderect(self.obstaculo.moeda_vitoria_objeto[0].rect):
               self.pegou_obstaculo_MAX(escala_variaveis=(-1))
      
      if self.nao_pode_colidir_por == 0:
         for moeda in self.obstaculo.moedas_objetos:
            if self.cobra.corpo.colliderect(moeda.rect):
               self.colidiu_obstaculo_moeda(moeda, moedas_maximas, remover_moedas, remover_inimigos)
      
      if self.nao_pode_colidir_por == 0:
         juncao_inimigo_quicante = self.obstaculo.inimigos_objetos + self.lista_dois_quicantes
         for inimigo_quicante in juncao_inimigo_quicante:
            if self.cobra.corpo.colliderect(inimigo_quicante.rect):
               self.colidiu_obstaculo_inimigo(inimigo_quicante, inimigos_maximos, remover_moedas, remover_inimigos)
      
      if self.nao_pode_colidir_por != 0:
         self.nao_pode_colidir_por -= 1
   
   #//
   
   def ganhou_jogo(self):
      if self.VARIAVEIS.indice == 0:
         self.EFEITOS["musica_ganhar_jogo"].play()
         self.EFEITOS["ganhar_jogo_MINHAVOZ"].play()
         self.RELACAO_ATUAL = "na_vitoria"
         self.tela_atualizar_jogo(self.VARIAVEIS.atual_inicio[0])   

   def perdeu_jogo(self):
      if self.cobra.colidiu_borda_cobra() or self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1): # Se chegou na fase "tela-morte"
         self.EFEITOS["musica_perder_jogo"].play()
         self.EFEITOS["perder_jogo_MINHAVOZ"].play()
         self.RELACAO_ATUAL = "no_gameover"
         self.tela_atualizar_jogo(self.VARIAVEIS.atual_inicio[0])
         if self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1):
            self.motivo_da_morte = "ultima_fase"
         else:
            self.motivo_da_morte = "colidiu"

   def aumentar_velocidade_por_fase(self):
      tempo = 140
      acrescimo = 1.04
      if self.duracao_acrescentar_velocidade_porFase == tempo:
         self.cobra.constante_razao_velocidade *= acrescimo
         self.duracao_acrescentar_velocidade_porFase = 0
      else:
         self.duracao_acrescentar_velocidade_porFase += 1

   def atualizar_jogo(self):
      if self.RELACAO_ATUAL == "no_menu":
         self.diminuir_aumentar_som_smooth(0.01, duracao=15, vol_max=self.VOLUMES["musica_menu"], aumentar_quanto=5)

      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      
      # if self.fase_final_variavel == 9:
      #    self.obstaculo.criar_vitoria_moeda()

      if self.RELACAO_ATUAL == "no_jogo":        
         self.animacao_obstaculos()
         
         if self.jogo_pausado:
            self.diminuir_aumentar_som_smooth(-0.01, vol_min=self.VOLUMES["musica_jogo_min"])
         else:
            self.diminuir_aumentar_som_smooth(0.01, vol_max=self.VOLUMES["musica_jogo_max"])
         
         if self.congelar_jogo_por <= 0 and not self.jogo_pausado: # Ao iniciar o jogo ou pausar -> vai congelar tudo
            
            self.cobra.mover_cobra()
            self.colidiu_obstaculos()

            self.ganhou_jogo()
            self.perdeu_jogo()

            self.aumentar_velocidade_por_fase()
            
            if self.VARIAVEIS.indice == 1:
               quantidade_quicantes = 4
               if len(self.lista_dois_quicantes) < quantidade_quicantes:
                  self.criar_quicante()
               for quicante in self.lista_dois_quicantes:
                  quicante.quicante_mover_inimigo()
            
         elif self.congelar_jogo_por > 0:
            self.congelar_jogo_por -= 1
   
   #//

   def desenhar_frase_gameover(self, tela, relacao, cor):
      if relacao == "na_vitoria":
         acrescimo = 110
         tempo_para_aparecer = 168 + acrescimo
         tempo_para_aparecer_espaco = 310 + acrescimo
         
         if self.intervalo_dos_textos_vitoriaMorte > tempo_para_aparecer:
               self.telaVitoriaMorte.desenhar_comentario_vitoriaMorte(tela, "BOA!!!", "Foi muito hard? Parabens...", cor)
         
         if self.intervalo_dos_textos_vitoriaMorte > tempo_para_aparecer_espaco:
            self.telaVitoriaMorte.desenhar_space_vitoriaMorte(tela)
         else:
            self.intervalo_dos_textos_vitoriaMorte += 1      
      
      if relacao == "no_gameover":
         tempo_para_aparecer = 168
         tempo_para_aparecer_espaco = 310
         
         if self.intervalo_dos_textos_vitoriaMorte > tempo_para_aparecer:
            if self.motivo_da_morte == "colidiu":
               self.telaVitoriaMorte.desenhar_comentario_vitoriaMorte(tela, "Colidiu com a tela?", "Cuidado hehe...", cor)
            if self.motivo_da_morte == "ultima_fase":
               self.telaVitoriaMorte.desenhar_comentario_vitoriaMorte(tela, "Chegou na fase final?", "Seja mais veloz!", cor)
         
         if self.intervalo_dos_textos_vitoriaMorte > tempo_para_aparecer_espaco:
            self.telaVitoriaMorte.desenhar_space_vitoriaMorte(tela)
         else:
            self.intervalo_dos_textos_vitoriaMorte += 1 
   
   def desenhar_creditos_logica(self, tela, valores, tempo_de_jogo):
      def verificar_tempo_de_jogo(tempo_de_jogo):
         if self.tempo_de_jogo / 60 >= 1:
            tempo = f"{(self.tempo_de_jogo / 60):,.1f}"
            return "minutos", tempo
         return "segundos", tempo_de_jogo

      self.creditos.desenhar_creditos_titulo(self.tela)

      #tempo_das_estatisticas = 100
      tempo_dos_outros_creditos = 350
      acrescimo = 15
      
      tempo_para_esperar_1 = 100 + acrescimo
      tempo_para_esperar_2 = tempo_para_esperar_1 + 100 + acrescimo
      tempo_para_esperar_3 = tempo_para_esperar_2 + tempo_dos_outros_creditos + 100 + acrescimo
      tempo_para_esperar_4 = tempo_para_esperar_3 + 150 + acrescimo

      if self.intervalo_dos_textos_creditos > tempo_para_esperar_1:
         self.creditos.desenhar_creditos_estatisticas(tela, valores, verificar_tempo_de_jogo(tempo_de_jogo))
      if self.intervalo_dos_textos_creditos > tempo_para_esperar_2:
         self.creditos.desenhar_outros_creditos(tela)
      if self.intervalo_dos_textos_creditos > tempo_para_esperar_3:
         self.creditos.desenhar_agradecimento(tela)
      if self.intervalo_dos_textos_creditos > tempo_para_esperar_4:
         self.telaVitoriaMorte.desenhar_space_vitoriaMorte(tela)
      else:
         self.intervalo_dos_textos_creditos += 1
   
   def desenhar_avisos_logica(self, tela):
      if self.duracao_obstaculo_aviso > 0:
         if self.aviso_acertou_moeda == True:
            self.textoAviso.criar_desenho_avisos(tela, "moeda!", CORES["moeda_obstaculoAviso"])
         if self.aviso_acertou_inimigo == True:
            self.textoAviso.criar_desenho_avisos(tela, "inimigo!", CORES["inimigo_obstaculoAviso"])
         if self.aviso_aumentou_nivel == True:
            self.textoAviso.criar_desenho_avisos(tela, "BOA!", CORES["aumentou_obstaculoAviso"])
         if self.aviso_diminuiu_nivel == True:
            self.textoAviso.criar_desenho_avisos(tela, "CUIDADO!", CORES["diminuiu_obstaculoAviso"])
         self.duracao_obstaculo_aviso -= 1
      else:
         self.colidiu_aviso_booleano()
         self.duracao_obstaculo_aviso = 0      
   
   def desenhar_contagem_fase_final(self, tela):
      numeros = [str(i) for i in range(1, 11)]
      tempo = 65
      if self.fase_final_contagem < (tempo * (self.fase_final_variavel+1)):
         self.textoAviso.criar_desenho_contagem(tela, numeros[self.fase_final_variavel])
         if self.congelar_jogo_por <= 0 and not self.jogo_pausado:
          self.fase_final_contagem += 1
      elif self.fase_final_variavel < 9:
         self.fase_final_variavel += 1

   def desenhar_jogo(self):
      if self.RELACAO_ATUAL == "no_menu":
         if not self.tutorial_ativo:
            self.ordem_do_tutorial = 0
            self.tela.fill(CORES["tela_menu"])
            self.decoracao.desenhar_decoracao(self.tela)
            self.menu.desenhar_menu(self.tela)
         else:
            self.mostrar_tutorial()
      
      if self.RELACAO_ATUAL == "na_vitoria":
         pygame.mixer.music.stop()
         self.tela.fill(CORES["tela_menu"])
         self.telaVitoriaMorte.desenhar_vitoriaMorte(self.tela, "VENCEU!", CORES["texto_vitoria"])
         self.desenhar_frase_gameover(self.tela, self.RELACAO_ATUAL, CORES["texto_vitoria"])

      if self.RELACAO_ATUAL == "nos_creditos":
         self.tela.fill(CORES["tela_menu"])
         self.desenhar_creditos_logica(self.tela, self.moedas_inimigos_pegos_total, self.tempo_de_jogo)
      
      if self.RELACAO_ATUAL == "no_gameover":
         pygame.mixer.music.stop()
         self.tela.fill(CORES["tela_menu"])
         self.telaVitoriaMorte.desenhar_vitoriaMorte(self.tela, "GAME OVER", CORES["texto_morte"])
         self.desenhar_frase_gameover(self.tela, self.RELACAO_ATUAL, CORES["texto_morte"])

      if self.RELACAO_ATUAL == "no_jogo":
         self.tela.fill(CORES["tela_jogo"])

         self.decoracao.desenhar_decoracao(self.tela)

         self.desenhar_avisos_logica(self.tela)
         
         if self.VARIAVEIS.indice == 1:
            self.desenhar_contagem_fase_final(self.tela)
            if self.fase_final_variavel == 9:
               self.textoAviso.criar_desenho_contagem(self.tela, "10") # Deixar o 10 sempre
               self.obstaculo.criar_vitoria_moeda() # Função da função atualizar_jogo, mas né kk
               self.obstaculo.desenhar_vitoria_moeda(self.tela)
      
         self.obstaculo.desenhar_obstaculos(self.tela)
         
         if self.VARIAVEIS.indice == 1:
            for quicante in self.lista_dois_quicantes:
               quicante.quicante_desenhar_inimigo(self.tela)
         
         if self.nao_pode_colidir_por == 0:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_ativo"])
         else:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_safe"])
         
         if self.jogo_pausado == True:
            self.pause.desenhar_pause(self.tela)

      pygame.display.flip()
   
   #//

   def loop(self):
      frames = 0
      tempo_inicio = pygame.time.get_ticks()
      while self.rodando:
         self.atualizar_jogo()
         self.desenhar_jogo()
         self.processar_eventos_jogo()
         self.tempo.tick(FPS)
         
         frames += 1
         if frames % 60 == 0:  # a cada 60 frames
            tempo_atual = pygame.time.get_ticks()
            fps_real = 60000 / (tempo_atual - tempo_inicio)
            print(f"FPS: {fps_real:.1f}")
            tempo_inicio = tempo_atual
      pygame.quit()

if __name__ == "__main__":
   Jogo().loop()