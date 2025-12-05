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

   "efeito_clicar_botao": pegar_caminho_recurso(r"assets/sounds/Click.wav"),
   "abrir_pause": pegar_caminho_recurso(r"assets/sounds/Menu_In.wav"),
   "fechar_pause": pegar_caminho_recurso(r"assets/sounds/Menu_Out.wav"),

   "aumentar_level": pegar_caminho_recurso(r"assets/sounds/aumentar_level.wav"),
   # "diminuir_level": pegar_caminho_recurso(r"assets/sounds/diminuir_level.wav"),
   "perigo_ultima_sala": pegar_caminho_recurso(r"assets/sounds/Alert Tone E-B 1.wav"),
}

FONTE = lambda tamanho: pygame.font.Font(CAMINHOS["fonte"], tamanho)

FPS = 60
CORES = { 
   "tela_cor_menu": (0, 0, 10),
   "tela_cor_jogo": (10, 20, 50),
   "cobra_cor_ativo": (10, 200, 100),
   "cobra_cor_safe": (110, 100, 100),
   "moeda_cor": (143, 181, 211),
   "inimigo_cor": (219, 29, 89),
   "qui_inimigo_cor": (239, 19, 99),
}

#//

def criar_botoes(variaveis_classe, tamanho_tupla, quantos_botoes, pos_y, gap, string, razao=1):
   VARIAVEIS = variaveis_classe

   tamanho_botoes = (int(tamanho_tupla[0]), int(tamanho_tupla[1]))
   tela_meio_botao = (VARIAVEIS.atual[0][0] // 2) - (tamanho_botoes[0] // 2)

   lista_botoes = []
   gapTotal = 0
   for i in range(quantos_botoes):
      lista_botoes.append(pygame.Rect((tela_meio_botao, pos_y + gapTotal), tamanho_botoes))
      gapTotal += gap + tamanho_tupla[1]
      
   palavras_botoes = string
   textos_botoes = []
   textos_botoes_rect_pos = []
   for i, palavra in enumerate(palavras_botoes):
      textos_botoes.append(FONTE(int(20 * razao)).render(palavra, 0, (220, 100, 100)))
      textos_botoes_rect_pos.append(textos_botoes[i].get_rect(center=(lista_botoes[i].center)))
   
   return lista_botoes, textos_botoes, textos_botoes_rect_pos

#//

class Variaveis:
   def __init__(self):
      self.variavel = { 
         # tela, bloco, V, distancia_minima, moedas / inimigos
         "tela+5": [(825, 825), 55,  9, 92, 0, 16],
         "tela+4": [(780, 780), 52, 10, 92, 2, 16],
         "tela+3": [(735, 735), 49,  8, 86, 3, 16],
         "tela+2": [(690, 690), 46,  7, 78, 5, 16],
         "tela+1": [(645, 645), 43,  7, 75, 5, 15],
         "tela0": [(600, 600), 40,  7, 72, 5, 15],
         "tela-1": [(555, 555), 37,  7, 69, 5, 15],
         "tela-2": [(510, 510), 34,  7, 63, 5, 14],
         "tela-3": [(465, 465), 31,  6, 54, 5, 14],
         "tela-4": [(420, 420), 28,  5, 48, 6, 12],
         "tela-5": [(375, 375), 25,  4, 46, 6, 12],
         #
         "tela-morte": [(600, 600), 0, 0, 0, 0, 0],
      }
      self.array = list(self.variavel.values())
      self.atual = self.array[5]
      self.indice = self.array.index(self.atual)
      self.bloco_incial = self.array[5][1]
   
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
      self.constante_razao = 1
      
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

      self.corpo.x += int(self.velocidade[0] * self.constante_razao)
      self.corpo.y += int(self.velocidade[1] * self.constante_razao)
   
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
   def __init__(self, posicao, VARIAVEIS):
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
         if self.tamanho_atual >= self.tamanho_padrao * 1.3: #Aumentar o tamanho padrão
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
   def __init__(self, posicao, VARIAVEIS):
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
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.qui_tamanho_padrao = self.VARIAVEIS.atual[1] / 1.7
      self.qui_rect = pygame.Rect((400, 400), (self.qui_tamanho_padrao, self.qui_tamanho_padrao))

      self.velocidade = [6, -6]
   
   def quicante_desenhar_inimigo(self, tela):
      pygame.draw.rect(tela, CORES["qui_inimigo_cor"], self.qui_rect)
   
   def quicante_mover_inimigo(self):
      self.qui_rect.x += self.velocidade[0]
      self.qui_rect.y += self.velocidade[1]

      if self.qui_rect.x <= 0:
         self.velocidade[0] = -self.velocidade[0]
      if self.qui_rect.x + self.qui_tamanho_padrao >= self.VARIAVEIS.atual[0][0]:
         self.velocidade[0] = -self.velocidade[0]
      
      if self.qui_rect.y <= 0:
         self.velocidade[1] = -self.velocidade[1]
      if self.qui_rect.y + self.qui_tamanho_padrao >= self.VARIAVEIS.atual[0][0]:
         self.velocidade[1] = -self.velocidade[1]

#//

class Obstaculo:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.moedas_objetos = []
      self.inimigos_objetos = []
      self.posicoes_feitas = []

   def criar_posicoes(self):
      self.QUANTIDADE_MOEDAS = self.VARIAVEIS.atual[4]
      self.QUANTIDADE_INIMIGOS = self.VARIAVEIS.atual[5]
      self.quantidade_posicoes = (self.QUANTIDADE_MOEDAS + self.QUANTIDADE_INIMIGOS) * 1.1
      
      self.distancia_minima = self.VARIAVEIS.atual[3]
      
      while len(self.posicoes_feitas) < self.quantidade_posicoes:
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
            moeda = Moeda(posicao, self.VARIAVEIS)
            self.moedas_objetos.append(moeda)
            self.posicoes_feitas.remove(posicao)
         
         elif len(self.inimigos_objetos) < self.QUANTIDADE_INIMIGOS:
            inimigo = Inimigo(posicao, self.VARIAVEIS)
            self.inimigos_objetos.append(inimigo)
            self.posicoes_feitas.remove(posicao)

   def desenhar_obstaculos(self, tela):
      for moeda in self.moedas_objetos:
         pygame.draw.rect(tela, CORES["moeda_cor"], moeda.rect)
      
      for inimigo in self.inimigos_objetos:
         pygame.draw.rect(tela, CORES["inimigo_cor"], inimigo.rect)
   
#//

class Pause:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.lista_botoes, self.textos_botoes, self.textos_botoes_rect_pos = [], [], []

      self.criar_pause()
   def criar_pause(self):
      self.tela_meio_texto = self.VARIAVEIS.atual[0][0] // 2 + 11 #Para centrallizar a fonte que tem espaço na direita
      self.razao = self.VARIAVEIS.atual[1] / self.VARIAVEIS.bloco_incial #Tela inicial e seu bloco

      espaco_ate_margem = int(self.VARIAVEIS.atual[0][1] / 6)

      self.titulo_pause = FONTE(int(35 * self.razao)).render(("Pausado!"), 0, (200, 200, 200))
      self.titulo_pause_pos = self.titulo_pause.get_rect(center=(self.tela_meio_texto, (30 + espaco_ate_margem) * self.razao))

      self.subtitulo_pause = FONTE(int(15 * self.razao)).render(("Pressione [space] para continuar"), 0, (200, 200, 200))
      self.subtitulo_pause_pos = self.subtitulo_pause.get_rect(center=(self.tela_meio_texto, (30 + 40 + espaco_ate_margem) * self.razao))

      self.lista_botoes, self.textos_botoes, self.textos_botoes_rect_pos = criar_botoes(self.VARIAVEIS, (380 * self.razao, 80 * self.razao), 2, (395 - espaco_ate_margem) * self.razao,  30 * self.razao, ["Sair para o menu", "Sair do jogo"], self.razao)
      
      #//

      self.overlay = pygame.Surface((self.VARIAVEIS.atual[0]))
      self.overlay.fill((0, 0, 0))
      self.overlay.set_alpha(220)
      
   def desenhar_pause(self, tela):
      tela.blit(self.overlay, (0, 0))
      tela.blit(self.titulo_pause, self.titulo_pause_pos)
      tela.blit(self.subtitulo_pause, self.subtitulo_pause_pos)
      
      for botao in self.lista_botoes:
         pygame.draw.rect(tela, (10, 10, 10), botao, 0, 10)
         pygame.draw.rect(tela, (200, 200, 200), botao, 3, 10)
      
      for texto, rect_pos in zip(self.textos_botoes, self.textos_botoes_rect_pos):
         tela.blit(texto, rect_pos)

#//

class Menu:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS  
      self.tela_meio_texto = self.VARIAVEIS.atual[0][0] // 2 + 11 #Para centrallizar a fonte que tem espaço na direita

      self.titulo = FONTE(38).render("Hora do Lesk!", 0, (250, 100, 100))
      self.titulo_pos = self.titulo.get_rect(center=(self.tela_meio_texto, 100))

      self.subTitulo = FONTE(18).render("Feito por cac <3", 0, (200, 100, 100))
      self.subTitulo_pos = self.subTitulo.get_rect(center=(self.tela_meio_texto, 140))

      #//
      
      self.lista_botoes, self.textos_botoes, self.textos_botoes_rect_pos = criar_botoes(self.VARIAVEIS, (210, 80), 3, 240, 30, ["Jogar", "Tutorial", "Sair"])
   
   def desenhar_menu(self, tela):
      tela.blit(self.titulo, self.titulo_pos)
      tela.blit(self.subTitulo, self.subTitulo_pos)
      
      for botao in self.lista_botoes:
         pygame.draw.rect(tela, (10, 10, 10), botao, 0, 10)
         pygame.draw.rect(tela, (200, 200, 200), botao, 3, 10)
      
      for texto, rect_pos in zip(self.textos_botoes, self.textos_botoes_rect_pos):
         tela.blit(texto, rect_pos)

#// // // // // // //

class Jogo:
   def __init__(self):
      pygame.init()
      self.executar_todas_classes()

      self.RELACAO_ATUAL = "no_menu"
      self.titulo = pygame.display.set_caption("HORA DO LESK!")
      self.tempo = pygame.time.Clock()
      self.rodando = True
      
      pygame.mixer.music.load(CAMINHOS["musica_menu"])
      self.volume_atual = 0.12
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
         # "diminuir_level": pygame.mixer.Sound(CAMINHOS["diminuir_level"]),
         "perigo_ultima_sala": pygame.mixer.Sound(CAMINHOS["perigo_ultima_sala"]),
      }   

   def executar_todas_classes(self):
      self.VARIAVEIS = Variaveis()
      self.cobra = Cobra(self.VARIAVEIS)
      self.obstaculo = Obstaculo(self.VARIAVEIS)
      self.menu = Menu(self.VARIAVEIS)
      self.pause = Pause(self.VARIAVEIS)
      self.quicante_inimigo = QuicanteInimigo(self.VARIAVEIS)

      self.tela_atualizar_jogo(self.VARIAVEIS.atual[0])
      
      self.moedas_pegas = 0
      self.inimigos_pegos = 0
      self.nao_pode_colidir = 200 # 200 frames sem colidir
      self.congelar_jogo = 200 # 200 frames tudo congelado
      self.tempo_aumentar_velocidade = 0
      self.tempo_musica_fade = 0
      self.jogo_pausado = False
   
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
                        self.executar_todas_classes()
                        
                        pygame.mixer.music.load(CAMINHOS["musica_jogo"])
                        self.volume = 0.10
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
                        self.executar_todas_classes()
                        
                        pygame.mixer.music.load(CAMINHOS["musica_menu"])
                        self.volume = pygame.mixer.music.set_volume(self.volume_atual)
                        pygame.mixer.music.play(-1)
                     
                     if botao_pause == self.pause.lista_botoes[1]:
                        self.rodando = False
         
#TODO: quando eu clico no jogo ele reincia o jogo kkkkkkkkkkkkkkkkkkkkkkkkk doideira. CORRIGIDO kkkk

   def processar_teclas_jogo(self, tecla):
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
   
   def diminuir_aumentar_som_smooth(self, soma):
      if soma == -0.01:
         if self.volume_atual > 0.02:
            if self.tempo_musica_fade < 100:
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += 1
      if soma == 0.01:
         if self.volume_atual < 0.12:
            if self.tempo_musica_fade < 100:
               self.volume_atual += soma
               self.volume = pygame.mixer.music.set_volume(self.volume_atual)
               self.tempo_musica_fade = 0
            else:
               self.tempo_musica_fade += 1

   def animacao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
            if moeda.fase != "completo":
               moeda.animacao_moeda()
      for inimigo in self.obstaculo.inimigos_objetos[:]:
            if inimigo.fase != "completo":
               inimigo.animacao_inimigo()           

   def escalonar_variaveis(self, preset_novo):
      self.VARIAVEIS.preset_tudo_atualizar(preset_novo)

      if self.VARIAVEIS.indice == 10:
         self.EFEITOS["perigo_ultima_sala"].play()
         self.EFEITOS["perigo_ultima_sala"].set_volume(0.1)

      x, y = self.cobra.corpo.topleft #Pega a posição (x, y) atual do rect da cobra
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
   
   def colidiu_obstaculos(self):
      moedas_maximas = 5
      inimigos_maximos = 2
      remover_moedas = (self.obstaculo.QUANTIDADE_MOEDAS - 1) // 2
      remover_inimigos = (self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2
      
      for moeda in self.obstaculo.moedas_objetos[:]:
         if self.cobra.corpo.colliderect(moeda.rect):
            self.EFEITOS["efeito_moeda"].play()
            self.obstaculo.moedas_objetos.remove(moeda)
            self.moedas_pegas += 1
            self.nao_pode_colidir = 25
            
            if self.moedas_pegas == moedas_maximas:
               self.EFEITOS["aumentar_level"].play()
               (self.moedas_pegas, self.inimigos_pegos) = (0, 0)
               self.escalonar_variaveis(-1)
               self.nao_pode_colidir = 120
               self.cobra.constante_razao = 1
            else:
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)

      for inimigo in self.obstaculo.inimigos_objetos[:]:
         if self.cobra.corpo.colliderect(inimigo.rect):
            self.EFEITOS["efeito_inimigo"].play()
            self.obstaculo.inimigos_objetos.remove(inimigo)
            self.inimigos_pegos += 1
            self.nao_pode_colidir = 25
            
            if self.inimigos_pegos == inimigos_maximos:
               # self.EFEITOS["diminuir_level"].play()
               self.moedas_pegas, self.inimigos_pegos = 0, 0
               self.escalonar_variaveis(1)
               self.nao_pode_colidir = 120
               self.cobra.constante_razao = 1
            else:
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)
   
   #TODO: Aprimorar aleatoriedade do surgimento dos obstaculos... Aprimorar a remoção? Coloca Menu, powerups. Aleatoriedade e divertido
   
   #todo: colocar essas if else, variaveis, nos respectivas funcoes, por exemplo esses negocios que pode gera um rodando = False la em cima junto com os outros enfim é isso boa sorte re rs
   
   def atualizar_jogo(self):

      if self.RELACAO_ATUAL == "no_menu":
         pass

      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      
      if self.RELACAO_ATUAL == "no_jogo":
         self.animacao_obstaculos()
         
         if self.jogo_pausado:
            self.diminuir_aumentar_som_smooth(-0.01)
         else:
            self.diminuir_aumentar_som_smooth(0.01)
         
         if self.congelar_jogo <= 0 and not self.jogo_pausado: # Ao iniciar o jogo ou pausar, vai congelar tudo
            # self.quicante_inimigo.quicante_mover_inimigo()
            
            if self.nao_pode_colidir == 0:
               self.colidiu_obstaculos()
            else:
               self.nao_pode_colidir -= 1

            if self.tempo_aumentar_velocidade == 140:
               self.cobra.constante_razao *= 1.05
               self.tempo_aumentar_velocidade = 0
            else:
               self.tempo_aumentar_velocidade += 1
            
            self.cobra.mover_cobra()
            if self.cobra.colidiu_borda_cobra() or self.VARIAVEIS.indice == (len(self.VARIAVEIS.array) - 1): #Deveria abrir a tela de GAME OVER
               self.EFEITOS["musica_perder_jogo"].play()
               self.RELACAO_ATUAL = "no_menu"
               self.executar_todas_classes()
            
         elif self.congelar_jogo > 0:
            self.congelar_jogo -= 1
         
   
   def desenhar_jogo(self):
      if self.RELACAO_ATUAL == "no_menu":
         self.tela.fill(CORES["tela_cor_menu"])
         self.menu.desenhar_menu(self.tela)

      if self.RELACAO_ATUAL == "no_jogo":
         self.tela.fill(CORES["tela_cor_jogo"])
         self.obstaculo.desenhar_obstaculos(self.tela)
         
         if self.nao_pode_colidir == 0:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_ativo"])
         else:
            self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_safe"])
         
         if self.jogo_pausado == True:
            self.pause.desenhar_pause(self.tela)
         # self.quicante_inimigo.quicante_desenhar_inimigo(self.tela)

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