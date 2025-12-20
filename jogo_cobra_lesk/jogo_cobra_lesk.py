import pygame
import math
import random
import os
os.environ['SDL_VIDEO_CENTERED'] = 'centered'
import sys
def pegar_caminho_recurso(nome_arquivo):
      if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, nome_arquivo)
      return os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_arquivo)

#//

CAMINHOS = {
   "fonte": pegar_caminho_recurso(r"assets/ARCADE_N.TTF"),

   "musica_menu": pegar_caminho_recurso(r"assets/sounds/Crystal Clear Loop.mp3"),
   "musica_jogo": pegar_caminho_recurso(r"assets/sounds/Unknown Caverns.mp3"),
   
   "musica_perder_jogo": pegar_caminho_recurso(r"assets/sounds/perder_jogo.wav"),
   "musica_ganhar_jogo": pegar_caminho_recurso(r"assets/sounds/ganhar_jogo.wav"),

   "efeito_moeda": pegar_caminho_recurso(r"assets/sounds/efeito_moeda.wav"),
   "efeito_inimigo": pegar_caminho_recurso(r"assets/sounds/efeito_inimigo.wav"),

   "efeito_clicar_botao": pegar_caminho_recurso(r"assets/sounds/click_botao.wav"),
   "abrir_pause": pegar_caminho_recurso(r"assets/sounds/Menu_In.wav"),
   "fechar_pause": pegar_caminho_recurso(r"assets/sounds/Menu_Out.wav"),

   "aumentar_level": pegar_caminho_recurso(r"assets/sounds/aumentar_level.wav"),
   "diminuir_level": pegar_caminho_recurso(r"assets/sounds/diminuir_level.wav"),
   "perigo_ultima_sala": pegar_caminho_recurso(r"assets/sounds/Alert Tone E-B 1.wav"),
}

FONTE = lambda tamanho: pygame.font.Font(CAMINHOS["fonte"], tamanho)

FPS = 60
CORES = { 
   "tela_cor_menu": (0, 0, 10),
   "tela_cor_jogo": (10, 20, 50),
   "cobra_cor_ativo": (10, 200, 100),
   "cobra_cor_safe": (70, 70, 80),
   "moeda_cor": (143, 181, 211),
   "moeda_vitoria_objeto_cor": (245, 255, 95),
   "inimigo_cor": (219, 29, 89),
   "qui_inimigo_cor": (239, 19, 99),
}

#TODO: Colocar e organizar todas as musicas e sfx. 
#TODO: FEITO::: COLOCAR TEXTO NO FUNDO DO JOGO, tipo: quando pegar moeda, colocar la tipo (1/5), seria melhor colocar um .png de bloquinhos sabe, enfim, quando estiver pausado tambem, ja que eu coloquei um "congelar" quando despausar. 

#TODO: Usar a bola quicante na sala final, esperar 10 segundos, aparecer a moeda dourada e vencer o jogo. 
#TODO: 1/2 FEITO::: Por fim, colocar as telas de gameOVER e de vitoria. Ela vai aparecer por sei la 5 segudos e vai desaparecendo fade lentamente com o menu prinicpal de fundo, fazendo uma transição legal

#TODO: COLOCAR uma velocidade extra que vai aumentar ao decorrer do jogo todo, porque so tem de quanto tempo a pessoa fica na sala, mas quero uma do jogo todo, pra ter mais chance da pessoa chegar na ultima sala. E quando chegar na ultima sala, essa velocidae extra é resetada

#TODO: Deixar o jogo justo e divertido, e aleatorio? precisa ver isso. 
#TODO: FAZER O TUTORIAL, mas é melhor fazer isso quando a mecanica do jogo estiver 100% pronta. 
#TODO: Organizar o code em si e otimizar de certa forma. 

#TODO VERSAO 2.0: Colocar powerUps hehe tipo de ficar invisivel? muita rapidez??? sei la, talvez eu nem faça, vamos ver a Crtiica ne 

#//

def criar_botoes(variaveis_classe, *, tamanho_botoes, quantos_botoes, pos_y, gap, frases, razao=1):
   VARIAVEIS = variaveis_classe

   tamanho_botoes = (int(tamanho_botoes[0]), int(tamanho_botoes[1]))
   tela_meio_botao = (VARIAVEIS.atual[0][0] // 2) - (tamanho_botoes[0] // 2)

   lista_botoes = []
   gapTotal = 0
   for i in range(quantos_botoes):
      lista_botoes.append(pygame.Rect((tela_meio_botao, pos_y + gapTotal), tamanho_botoes))
      gapTotal += gap + tamanho_botoes[1]
      
   palavras_botoes = frases
   texto_botoes = []
   texto_botoes_rect_pos = []
   for i, palavra in enumerate(palavras_botoes):
      texto_botoes.append(FONTE(int(20 * razao)).render(palavra, 0, (220, 100, 100)))
      texto_botoes_rect_pos.append(texto_botoes[i].get_rect(center=(lista_botoes[i].center)))
   
   return lista_botoes, texto_botoes, texto_botoes_rect_pos

def centralizar_texto_corretamente(texto_surface, pos_x, pos_y):
   rect_todo = texto_surface.get_rect()
   rect_apenas_texto = texto_surface.get_bounding_rect()
   espaço_extra = rect_todo.width - rect_apenas_texto.width
   rect_todo.center = (pos_x + (espaço_extra//2), pos_y)
   return rect_todo

#//

class Variaveis:
   def __init__(self):
      self.variavel = { 
         # tela, bloco, V, distancia_minima, moedas / inimigos
         "tela-vitoria": [(600, 600), 0, 0, 0, 0, 0],

         "tela+5": [(825, 825), 55, 11, 95, 0, 21],
         "tela+4": [(780, 780), 52, 10, 92, 2, 17],
         "tela+3": [(735, 735), 49,  9, 86, 3, 17],
         "tela+2": [(690, 690), 46,  8, 81, 4, 17],
         "tela+1": [(645, 645), 43,  8, 74, 6, 15],
         "tela0": [(600, 600), 40,  7, 72, 6, 15],
         "tela-1": [(555, 555), 37,  7, 68, 6, 15],
         "tela-2": [(510, 510), 34,  7, 63, 5, 14],
         "tela-3": [(465, 465), 31,  6, 54, 5, 14],
         "tela-4": [(420, 420), 28,  5, 48, 6, 12],
         "tela-5": [(375, 375), 25,  5, 46, 6, 12],
         
         "tela-morte": [(600, 600), 0, 0, 0, 0, 0],
      }
      self.array = list(self.variavel.values())
      self.atual = self.array[6]
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

      inicio_x = (self.VARIAVEIS.atual[0][0] / 2) - (self.VARIAVEIS.atual[1] / 2)
      inicio_y = self.VARIAVEIS.atual[0][1] - 100
      
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
      pygame.draw.rect(tela, CORES["qui_inimigo_cor"], self.rect)
   
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
      
      while len(self.posicoes_feitas) < self.QUANTIDADE_POSICOES:
         procurar = True
         while procurar:
            procurar = False
            
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
         pygame.draw.rect(tela, CORES["moeda_cor"], moeda.rect)
      
      for inimigo in self.inimigos_objetos:
         pygame.draw.rect(tela, CORES["inimigo_cor"], inimigo.rect)
   
   def criar_vitoria_moeda(self):
      if len(self.moeda_vitoria_objeto) < 1:
         for posicao in self.posicoes_feitas[:]:
            moeda_vitoria = Moeda(self.VARIAVEIS, posicao)
            self.moeda_vitoria_objeto.append(moeda_vitoria)
            self.posicoes_feitas.remove(posicao)
   def desenhar_vitoria_moeda(self, tela):
      pygame.draw.rect(tela, CORES["moeda_vitoria_objeto_cor"], self.moeda_vitoria_objeto[0].rect)

   
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
   
   def criar_desenho_contagem(self, tela, texto, cor):
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2
      self.pos_y_meio = self.VARIAVEIS.atual[0][1] - 200
      
      self.tituloContagem = FONTE(250).render((texto), 0, cor)
      self.tituloContagem_pos = centralizar_texto_corretamente(self.tituloContagem, self.pos_x_meio, self.pos_y_meio)

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

      self.tituloPause = FONTE(int(35 * self.razao)).render(("Pausado!"), 0, (200, 200, 200))
      self.tituloPause_pos = centralizar_texto_corretamente(self.tituloPause, self.pos_x_meio, (30 + espaco_ate_margem) * self.razao)

      self.subTituloPause = FONTE(int(15 * self.razao)).render(("Pressione [space] para continuar"), 0, (200, 200, 200))
      self.subTituloPause_pos = centralizar_texto_corretamente(self.subTituloPause, self.pos_x_meio, (30 + 40 + espaco_ate_margem) * self.razao)

      self.lista_botoes, self.texto_botoes, self.texto_botoes_pos = criar_botoes(self.VARIAVEIS, 
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
         pygame.draw.rect(tela, (10, 10, 10), botao, 0, 10)
         pygame.draw.rect(tela, (200, 200, 200), botao, 3, 10)
      
      for texto, texto_pos in zip(self.texto_botoes, self.texto_botoes_pos):
         tela.blit(texto, texto_pos)

#//

class Menu:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS  
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2

      self.titulo = FONTE(38).render("Hora do Lesk!", 0, (250, 100, 100))
      self.titulo_pos = centralizar_texto_corretamente(self.titulo, self.pos_x_meio, 100)

      self.subTitulo = FONTE(18).render("Feito por cac <3", 0, (200, 100, 100))
      self.subTitulo_pos = centralizar_texto_corretamente(self.subTitulo, self.pos_x_meio, 100 + 40)

      #//
      
      self.lista_botoes, self.texto_botoes, self.texto_botoes_pos = criar_botoes(self.VARIAVEIS, 
                                                                        tamanho_botoes = (210, 80), 
                                                                        quantos_botoes = 3, 
                                                                                 pos_y = 240, 
                                                                                   gap = 30, 
                                                                                frases = ["Jogar", "Tutorial", "Sair"])

   def desenhar_menu(self, tela):
      tela.blit(self.titulo, self.titulo_pos)
      tela.blit(self.subTitulo, self.subTitulo_pos)
      
      for botao in self.lista_botoes: # Criar borda colorida nos botões
         pygame.draw.rect(tela, (10, 10, 10), botao, 0, 10) 
         pygame.draw.rect(tela, (200, 200, 200), botao, 3, 10)
      
      for texto, texto_pos in zip(self.texto_botoes, self.texto_botoes_pos):
         tela.blit(texto, texto_pos)

#//

class GameOver:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS
   
   def desenhar_gameover(self, tela):
      self.pos_x_meio = self.VARIAVEIS.atual[0][0] // 2

      self.tituloGameover = FONTE(50).render("GAME OVER", 0, (250, 100, 100))
      self.tituloGameover_pos = centralizar_texto_corretamente(self.tituloGameover, self.pos_x_meio, self.VARIAVEIS.atual[0][1] // 2 - 10)
      
      tela.blit(self.tituloGameover, self.tituloGameover_pos)
   
   def desenhar_comentario_gameover(self, tela, frase1, frase2):
      self.comentarioMorte_1 = FONTE(15).render(frase1, 0, (250, 100, 100))
      self.comentarioMorte_1_pos = centralizar_texto_corretamente(self.comentarioMorte_1, self.pos_x_meio, self.VARIAVEIS.atual[0][1] // 2 + 30)
      
      self.comentarioMorte_2 = FONTE(15).render(frase2, 0, (250, 100, 100))
      self.comentarioMorte_2_pos = centralizar_texto_corretamente(self.comentarioMorte_2, self.pos_x_meio, self.VARIAVEIS.atual[0][1] // 2 + 52)
      
      tela.blit(self.comentarioMorte_1, self.comentarioMorte_1_pos)
      tela.blit(self.comentarioMorte_2, self.comentarioMorte_2_pos)
   
   def desenhar_space_gameover(self, tela):
      self.espacoMorte = FONTE(15).render("Pressione [space] para voltar ao menu", 0, (250, 100, 100))
      self.espacoMorte_pos = centralizar_texto_corretamente(self.espacoMorte, self.pos_x_meio - 2, self.VARIAVEIS.atual[0][1] - 20)
      tela.blit(self.espacoMorte, self.espacoMorte_pos)

#// // // // // // //

class Jogo:
   def __init__(self):
      pygame.mixer.init(44100, -16, 2, 2048)
      pygame.init()
      self.executar_todas_classes()

      self.RELACAO_ATUAL = "no_menu"
      self.titulo = pygame.display.set_caption("HORA DO LESK!")
      self.tempo = pygame.time.Clock()
      self.rodando = True
      
      pygame.mixer.music.load(CAMINHOS["musica_menu"])
      self.volume_atual = 0
      self.volume = pygame.mixer.music.set_volume(self.volume_atual)
      pygame.mixer.music.play(-1)

      self.EFEITOS = {
         "musica_perder_jogo": pygame.mixer.Sound(CAMINHOS["musica_perder_jogo"]),
         "musica_ganhar_jogo": pygame.mixer.Sound(CAMINHOS["musica_ganhar_jogo"]),

         "efeito_moeda": pygame.mixer.Sound(CAMINHOS["efeito_moeda"]),
         "efeito_inimigo": pygame.mixer.Sound(CAMINHOS["efeito_inimigo"]),

         "efeito_clicar_botao": pygame.mixer.Sound(CAMINHOS["efeito_clicar_botao"]),
         "abrir_pause": pygame.mixer.Sound(CAMINHOS["abrir_pause"]),
         "fechar_pause": pygame.mixer.Sound(CAMINHOS["fechar_pause"]),

         "aumentar_level": pygame.mixer.Sound(CAMINHOS["aumentar_level"]),
         "diminuir_level": pygame.mixer.Sound(CAMINHOS["diminuir_level"]),
         "perigo_ultima_sala": pygame.mixer.Sound(CAMINHOS["perigo_ultima_sala"]),
      }   

   def executar_todas_classes(self):
      self.VARIAVEIS = Variaveis()
      self.cobra = Cobra(self.VARIAVEIS)
      self.obstaculo = Obstaculo(self.VARIAVEIS)
      self.menu = Menu(self.VARIAVEIS)
      self.pause = Pause(self.VARIAVEIS)
      self.textoAviso = Aviso(self.VARIAVEIS)
      self.gameOver = GameOver(self.VARIAVEIS)

      self.tela_atualizar_jogo(self.VARIAVEIS.atual[0])
      
      self.moedas_pegas = 0
      self.inimigos_pegos = 0
      self.nao_pode_colidir = 200 # Começa a partida com 200 frames sem colidir
      self.congelar_jogo = 200 # Começa a partida com 200 frames tudo congelado
      self.tempo_aumentar_velocidade_porFase = 0
      self.tempo_musica_fade = 0
      self.colidiu_aviso_booleano()
      self.duracao_pegou_aviso = 0
      
      self.fase_final_contagem = -self.nao_pode_colidir
      self.fase_final_variavel = 0
      
      self.intervalo_gameover_texto = 0
      self.motivo_da_morte = None
      self.jogo_pausado = False
      self.lista_dois_quicantes = []
   
   def tela_atualizar_jogo(self, tamanho):
      self.tela = pygame.display.set_mode(tamanho)

   def processar_eventos_jogo(self):
      for evento in pygame.event.get():
         
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas_jogo(evento.key)
               
         elif self.RELACAO_ATUAL == "no_menu":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
               posicao_mouse = evento.pos
               
               for botao_menu in self.menu.lista_botoes:
                  if botao_menu.collidepoint(posicao_mouse):
                     self.EFEITOS["efeito_clicar_botao"].play()
                     
                     if botao_menu == self.menu.lista_botoes[0]:
                        self.RELACAO_ATUAL = "no_jogo"
                        
                        pygame.mixer.music.load(CAMINHOS["musica_jogo"])
                        self.volume_atual = 0.10
                        self.volume = pygame.mixer.music.set_volume(self.volume_atual)
                        pygame.mixer.music.play(-1)
                     
                     if botao_menu == self.menu.lista_botoes[1]:
                        pass

                     if botao_menu == self.menu.lista_botoes[2]:
                        self.rodando = False

         elif self.jogo_pausado == True:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
               posicao_mouse = evento.pos
               
               for botao_pause in self.pause.lista_botoes:
                  if botao_pause.collidepoint(posicao_mouse):
                     self.EFEITOS["efeito_clicar_botao"].play()

                     if botao_pause == self.pause.lista_botoes[0]:
                        self.RELACAO_ATUAL = "no_menu"
                        
                        pygame.mixer.music.load(CAMINHOS["musica_menu"])
                        self.volume_atual = 0.12
                        self.volume = pygame.mixer.music.set_volume(self.volume_atual)
                        pygame.mixer.music.play(-1)
                        self.executar_todas_classes()
                     
                     if botao_pause == self.pause.lista_botoes[1]:
                        self.rodando = False

   def processar_teclas_jogo(self, tecla):
      if self.RELACAO_ATUAL == "no_gameover":
         if tecla == pygame.K_SPACE:
            self.RELACAO_ATUAL = "no_menu"
            self.executar_todas_classes()
            
            pygame.mixer.music.load(CAMINHOS["musica_menu"])
            self.volume_atual = 0.12
            self.volume = pygame.mixer.music.set_volume(self.volume_atual)
            pygame.mixer.music.play(-1)

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
               self.congelar_jogo = 30
               self.EFEITOS["fechar_pause"].play().set_volume(0.08)
               self.jogo_pausado = False
            else:
               self.EFEITOS["abrir_pause"].play().set_volume(0.08)
               self.jogo_pausado = True
   
   def diminuir_aumentar_som_smooth(self, soma, *, duracao=0, vol_min=0.035, vol_max=0.10):
      if soma == -0.01:
         if self.volume_atual > vol_min:
            if self.tempo_musica_fade > duracao:
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += 1
      if soma == 0.01:
         if self.volume_atual < vol_max: #Volume maximo da música em jogo
            if self.tempo_musica_fade > duracao:
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += 1

   #//

   def animacao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
            if moeda.fase != "completo":
               moeda.animacao_moeda()
      for inimigo in self.obstaculo.inimigos_objetos[:]:
            if inimigo.fase != "completo":
               inimigo.animacao_inimigo()          
      
      if self.fase_final_variavel == 9:
         if self.obstaculo.moeda_vitoria_objeto[0].fase != "completo":
             self.obstaculo.moeda_vitoria_objeto[0].animacao_moeda()

   def escalonar_acionar_variaveis(self, preset_novo):
      self.VARIAVEIS.preset_tudo_atualizar(preset_novo)

      if self.VARIAVEIS.indice == 11:
         self.EFEITOS["perigo_ultima_sala"].play()
         self.EFEITOS["perigo_ultima_sala"].set_volume(0.5)
      
      self.lista_dois_quicantes = [] # Sempre reseta a lista dos quicantes

      x, y = self.cobra.corpo.topleft # Pega a posição (x, y) atual da cobra.rect
      self.obstaculo.moedas_objetos = []
      self.obstaculo.inimigos_objetos = []
      self.obstaculo.posicoes_feitas = []

      self.cobra.cobra_rect_atualizar(x, y)
      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      self.pause.criar_pause()
      self.tela_atualizar_jogo(self.VARIAVEIS.atual[0])

   def remover_obstaculos_aleatorios(self, remover_moedas, remover_inimigos):
      if self.obstaculo.moedas_objetos:
         for x in range(remover_moedas):
            self.obstaculo.moedas_objetos.pop(random.randint(0, len(self.obstaculo.moedas_objetos) - 1))
      
      if self.obstaculo.inimigos_objetos:
         for x in range(remover_inimigos):
            self.obstaculo.inimigos_objetos.pop(random.randint(0, len(self.obstaculo.inimigos_objetos) - 1))
   
   def colidiu_aviso_booleano(self, *, moeda=False, inimigo=False, up=False, down=False):
      self.aviso_acertou_moeda = moeda
      self.aviso_acertou_inimigo = inimigo
      self.aviso_aumentou_nivel = up
      self.aviso_diminuiu_nivel = down
   
   def pegou_moeda_inimigo_maximo(self, escala_variaveis):
      self.duracao_pegou_aviso = 0
      self.escalonar_acionar_variaveis(escala_variaveis)
      (self.moedas_pegas, self.inimigos_pegos) = (0, 0)
      self.cobra.constante_razao_velocidade = 1
      if self.VARIAVEIS.indice == 1:
         self.nao_pode_colidir = 160 + 40
         self.fase_final_contagem, self.fase_final_variavel = -self.nao_pode_colidir, 0 # resetando a contagem da fase final
      else:
         self.nao_pode_colidir = 160

   def pegou_moeda_inimigo_apenas(self, obstaculo):
      self.duracao_pegou_aviso = 0
      self.nao_pode_colidir = 30
      
      if obstaculo in self.obstaculo.moedas_objetos[:]:
         self.moedas_pegas += 1
         self.obstaculo.moedas_objetos.remove(obstaculo)
      
      if obstaculo in self.obstaculo.inimigos_objetos[:]:
         self.inimigos_pegos += 1
         self.obstaculo.inimigos_objetos.remove(obstaculo)
      
      if obstaculo in self.lista_dois_quicantes[:]:
         self.inimigos_pegos += 1
         self.lista_dois_quicantes.remove(obstaculo)

   def colidiu_obstaculos(self):
      moedas_maximas = 5
      inimigos_maximos = 4
      remover_moedas = (self.obstaculo.QUANTIDADE_MOEDAS - 1) // 2
      remover_inimigos = (self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2
      
      for moeda in self.obstaculo.moedas_objetos[:]:
         if self.cobra.corpo.colliderect(moeda.rect):
            self.EFEITOS["efeito_moeda"].play()
            self.colidiu_aviso_booleano(moeda=True)
            self.pegou_moeda_inimigo_apenas(obstaculo=moeda)
            
            if self.moedas_pegas == moedas_maximas:
               self.EFEITOS["aumentar_level"].play()
               self.colidiu_aviso_booleano(up=True)
               self.pegou_moeda_inimigo_maximo(escala_variaveis=(-1))
            else:
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)

      for inimigo in self.obstaculo.inimigos_objetos[:]:
         if self.cobra.corpo.colliderect(inimigo.rect):
            self.EFEITOS["efeito_inimigo"].play()
            self.colidiu_aviso_booleano(inimigo=True)
            self.pegou_moeda_inimigo_apenas(obstaculo=inimigo)
            
            if self.inimigos_pegos == inimigos_maximos:
               self.EFEITOS["diminuir_level"].play()
               self.colidiu_aviso_booleano(down=True)
               self.pegou_moeda_inimigo_maximo(escala_variaveis=(1))
            else:
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)
      
      if self.VARIAVEIS.indice == 1:
         if self.fase_final_variavel == 9:
            if self.cobra.corpo.colliderect(self.obstaculo.moeda_vitoria_objeto[0].rect):
               print("pegou o bloco amarelo!!!!")

         for quicante in self.lista_dois_quicantes[:]:
            if self.cobra.corpo.colliderect(quicante.rect):
               self.EFEITOS["efeito_inimigo"].play()
               self.colidiu_aviso_booleano(inimigo=True)
               self.pegou_moeda_inimigo_apenas(obstaculo=quicante)
            
            if self.inimigos_pegos == inimigos_maximos:
               self.EFEITOS["diminuir_level"].play()
               self.colidiu_aviso_booleano(down=True)
               self.pegou_moeda_inimigo_maximo(escala_variaveis=(1))
   
   def criar_quicante(self):
      margem = self.VARIAVEIS.atual[1] // 2
      pos_x = random.randint(margem, self.VARIAVEIS.atual[0][0] - margem)
      pos_y = random.randint(margem, self.VARIAVEIS.atual[0][1] - margem)  
      self.lista_dois_quicantes.append(QuicanteInimigo(self.VARIAVEIS, (pos_x, pos_y))) 
   
   #//

   def perdeu_jogo(self):
      if self.cobra.colidiu_borda_cobra() or (self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1)):
         self.EFEITOS["musica_perder_jogo"].play()
         self.RELACAO_ATUAL = "no_gameover"
         self.VARIAVEIS.atual = self.VARIAVEIS.array[6] # Atualizar o tamanho da tela
         self.tela_atualizar_jogo(self.VARIAVEIS.atual[0]) # Atualizar o tamanho da tela
         if self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1):
            self.motivo_da_morte = "ultima_fase"
         else:
            self.motivo_da_morte = "colidiu"

   def atualizar_jogo(self):
      if self.RELACAO_ATUAL == "no_menu":
         self.diminuir_aumentar_som_smooth(0.01, duracao=10, vol_max=0.12)

      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      
      if self.RELACAO_ATUAL == "no_jogo":
         
         if self.fase_final_variavel == 9:
            self.obstaculo.criar_vitoria_moeda()
         
         self.animacao_obstaculos()
         
         if self.jogo_pausado:
            self.diminuir_aumentar_som_smooth(-0.01, vol_min=0.035)
         else:
            self.diminuir_aumentar_som_smooth(0.01, vol_max=0.10)
         
         if self.congelar_jogo <= 0 and not self.jogo_pausado: # Ao iniciar o jogo ou pausar -> vai congelar tudo
            self.cobra.mover_cobra()

            self.perdeu_jogo()
            
            if self.nao_pode_colidir <= 0:
               self.colidiu_obstaculos()
            else:
               self.nao_pode_colidir -= 1

            if self.tempo_aumentar_velocidade_porFase == 140:
               self.cobra.constante_razao_velocidade *= 1.04
               self.tempo_aumentar_velocidade_porFase = 0
            else:
               self.tempo_aumentar_velocidade_porFase += 1
            
            if self.VARIAVEIS.indice == 1:
               if len(self.lista_dois_quicantes) < 3:
                  self.criar_quicante()
               
               for quicante in self.lista_dois_quicantes[:]:
                  quicante.quicante_mover_inimigo()
               
               # if self.fase_final_variavel == 9:
               #    self.obstaculo.criar_moeda_vitoria_objeto = True
            
         elif self.congelar_jogo > 0:
            self.congelar_jogo -= 1
   
   #//

   def desenhar_frase_gameover(self, tela):
      if self.intervalo_gameover_texto > 168:
         if self.motivo_da_morte == "colidiu":
            self.gameOver.desenhar_comentario_gameover(tela, "Colidiu com a tela?", "Cuidado hehe...")
         if self.motivo_da_morte == "ultima_fase":
            self.gameOver.desenhar_comentario_gameover(tela, "Chegou na fase final?", "Seja mais veloz!")
      
      if self.intervalo_gameover_texto > 310:
         self.gameOver.desenhar_space_gameover(tela)
      else:
         self.intervalo_gameover_texto += 1      
   
   def desenhar_avisos_logica(self, tela):
      if self.duracao_pegou_aviso < 35:
         if self.aviso_acertou_moeda == True:
            self.textoAviso.criar_desenho_avisos(tela, "moeda!", (110, 110, 140))
         if self.aviso_acertou_inimigo == True:
            self.textoAviso.criar_desenho_avisos(tela, "inimigo!", (140, 110, 110))
         if self.aviso_aumentou_nivel == True:
            self.textoAviso.criar_desenho_avisos(tela, "BOA!", (110, 110, 250))
         if self.aviso_diminuiu_nivel == True:
            self.textoAviso.criar_desenho_avisos(tela, "CUIDADO!", (250, 110, 110))
         self.duracao_pegou_aviso += 1
      else:
         self.colidiu_aviso_booleano()
         self.duracao_pegou_aviso = 0      
      
      if self.VARIAVEIS.indice == 1:
         numeros = [str(i) for i in range(1, 11)]
         tempo = 60
         if self.fase_final_contagem < (tempo * (self.fase_final_variavel+1)):
            self.textoAviso.criar_desenho_contagem(tela, numeros[self.fase_final_variavel], (0, 10, 40))
            self.fase_final_contagem += 1
         elif self.fase_final_variavel < 9:
            self.fase_final_variavel += 1
         elif self.fase_final_variavel == 9:
            self.textoAviso.criar_desenho_contagem(tela, "10", (0, 10, 40))

   def desenhar_jogo(self):
      if self.RELACAO_ATUAL == "no_menu":
         self.tela.fill(CORES["tela_cor_menu"])
         self.menu.desenhar_menu(self.tela)
      
      if self.RELACAO_ATUAL == "no_gameover":
         pygame.mixer.music.stop()
         self.tela.fill(CORES["tela_cor_menu"])
         self.gameOver.desenhar_gameover(self.tela)
         self.desenhar_frase_gameover(self.tela)

      if self.RELACAO_ATUAL == "no_jogo":
         self.tela.fill(CORES["tela_cor_jogo"])

         self.desenhar_avisos_logica(self.tela)
         
         self.obstaculo.desenhar_obstaculos(self.tela)
         
         if self.nao_pode_colidir == 0:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_ativo"])
         else:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_safe"])
         
         if self.VARIAVEIS.indice == 1:
            for quicante in self.lista_dois_quicantes[:]:
               quicante.quicante_desenhar_inimigo(self.tela)
            if self.fase_final_variavel == 9:
               self.obstaculo.criar_vitoria_moeda()
               self.obstaculo.desenhar_vitoria_moeda(self.tela)
         
         if self.jogo_pausado == True:
            self.pause.desenhar_pause(self.tela)

      pygame.display.flip()
   
   def loop(self):
      while self.rodando:
         self.atualizar_jogo()
         self.desenhar_jogo()
         self.processar_eventos_jogo()
         self.tempo.tick(FPS)
      pygame.quit()

if __name__ == "__main__":
   Jogo().loop()