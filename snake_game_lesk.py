import math
import random
import os
os.environ['SDL_VIDEO_CENTERED'] = 'centered'
import pygame

FPS = 60
CORES = {
   "tela_cor": (11, 20, 59),
   "cobra_cor_ativo": (10, 200, 100),
   "cobra_cor_safe": (110, 100, 100),
   "moeda_cor": (143, 181, 211),
   "inimigo_cor": (219, 29, 89),
}

#//

class Variaveis:
   def __init__(self):
      self.variavel = { 
         #         tela, bloco, V, distancia_minima, moedas / inimigos
         "tela+5": [(825, 825), 55,  9, 90, 0, 15],
         "tela+4": [(780, 780), 52, 10, 90, 3, 14],
         "tela+3": [(735, 735), 49,  8, 82, 3, 14],
         "tela+2": [(690, 690), 46,  7, 68, 5, 14],
         "tela+1": [(645, 645), 43,  7, 68, 5, 14],
         "tela0": [(600, 600), 40,  7, 68, 5, 14],
         "tela-1": [(555, 555), 37,  7, 68, 5, 14],
         "tela-2": [(510, 510), 34,  6, 64, 5, 14],
         "tela-3": [(465, 465), 31,  6, 54, 5, 14],
         "tela-4": [(420, 420), 28,  5, 48, 6, 12],
         "tela-5": [(375, 375), 25,  4, 46, 6, 12],
         #
         "tela-morte": [(600, 600), 0, 0, 0, 0, 0],
      }
      self.array = list(self.variavel.values())
      self.atual = self.array[5]
      self.indice = self.array.index(self.atual)
   
   def preset_tudo_atualizar(self, preset_novo_soma):
      self.indice += preset_novo_soma
      print(self.indice)
      print(self.indice)
      print(self.indice, "\n")
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

      inicio_x = self.VARIAVEIS.atual[0][0] / 2 - (self.VARIAVEIS.atual[1] / 2)
      inicio_y = self.VARIAVEIS.atual[0][1] - 100
      
      self.CIMA = (0, -self.VARIAVEIS.atual[2])
      self.DIREITA = (self.VARIAVEIS.atual[2], 0)
      self.BAIXO = (0, self.VARIAVEIS.atual[2])
      self.ESQUERDA = (-self.VARIAVEIS.atual[2], 0)
      
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

      self.corpo.x += self.velocidade[0]
      self.corpo.y += self.velocidade[1]
   
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
         if self.tamanho_atual >= self.tamanho_padrao * 1.3: # aumentar o tamanho padrão
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
         if self.tamanho_atual[0] <= self.tamanho_padrao * 0.8: # diminuir o tamanho padrão
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

class Obstaculo:
   def __init__(self, VARIAVEIS):
      self.VARIAVEIS = VARIAVEIS

      self.QUANTIDADE_MOEDAS = self.VARIAVEIS.atual[4]
      self.moedas_objetos = []
      
      self.QUANTIDADE_INIMIGOS = self.VARIAVEIS.atual[5]
      self.inimigos_objetos = []
      
      self.quantidade_posicoes = (self.QUANTIDADE_MOEDAS + self.QUANTIDADE_INIMIGOS) * 1.1
      self.posicoes_feitas = []

   def criar_posicoes(self):
      self.QUANTIDADE_MOEDAS = self.VARIAVEIS.atual[4]
      self.QUANTIDADE_INIMIGOS = self.VARIAVEIS.atual[5]
      self.distancia_minima = self.VARIAVEIS.atual[3]
      
      while len(self.posicoes_feitas) < self.quantidade_posicoes:
         procurar = True
         while procurar:
            procurar = False
            
            pos_x = random.randint(17, self.VARIAVEIS.atual[0][0] - 17)
            pos_y = random.randint(17, self.VARIAVEIS.atual[0][1] - 17)

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

class Jogo:
   def __init__(self):
      pygame.init()

      self.VARIAVEIS = Variaveis()
      self.cobra = Cobra(self.VARIAVEIS)
      self.obstaculo = Obstaculo(self.VARIAVEIS)
      
      self.moedas_pegas = 0
      self.inimigos_pegos = 0
      self.pode_colidir = 60 # começa com 60 frames sem colidir
      self.aumentar_velocidade_tempo = 0
      
      self.titulo = pygame.display.set_caption("A hora do Lesk!")
      self.tempo = pygame.time.Clock()
      self.rodando = True

      self.tela = pygame.display.set_mode(self.VARIAVEIS.atual[0])
   def tela_atualizar_jogo(self):
      self.tela = pygame.display.set_mode(self.VARIAVEIS.atual[0])

   def processar_eventos_jogo(self):
      for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas_jogo(evento.key)
   
   def processar_teclas_jogo(self, tecla):
      if tecla == pygame.K_RIGHT:
         self.cobra.direcionar_cobra(self.cobra.DIREITA)
      if tecla == pygame.K_UP:
         self.cobra.direcionar_cobra(self.cobra.CIMA)
      if tecla == pygame.K_LEFT:
         self.cobra.direcionar_cobra(self.cobra.ESQUERDA)
      if tecla == pygame.K_DOWN:
         self.cobra.direcionar_cobra(self.cobra.BAIXO)

   def animacao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
            if moeda.fase != "completo":
               moeda.animacao_moeda()
      for inimigo in self.obstaculo.inimigos_objetos[:]:
            if inimigo.fase != "completo":
               inimigo.animacao_inimigo()           

   def escalonar_variaveis(self, preset_novo):
      self.VARIAVEIS.preset_tudo_atualizar(preset_novo)

      x, y = self.cobra.corpo.topleft # pegar a posição x e y atual do rect da cobra
      self.obstaculo.moedas_objetos = []
      self.obstaculo.inimigos_objetos = []
      self.obstaculo.posicoes_feitas = []

      self.cobra.cobra_rect_atualizar(x, y)
      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      self.tela_atualizar_jogo()

   def remover_obstaculos_aleatorios(self, remover_moedas, remover_inimigos):
      if self.obstaculo.moedas_objetos:
         for x in range(remover_moedas):
            self.obstaculo.moedas_objetos.pop(random.randint(0, len(self.obstaculo.moedas_objetos) - 1))
      
      if self.obstaculo.inimigos_objetos:
         for x in range(remover_inimigos):
            self.obstaculo.inimigos_objetos.pop(random.randint(0, len(self.obstaculo.inimigos_objetos) - 1))
   
   def colidiu_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
         if self.cobra.corpo.colliderect(moeda.rect):
            self.obstaculo.moedas_objetos.remove(moeda)
            self.moedas_pegas += 1
            self.pode_colidir = 25
            
            if self.moedas_pegas == 5:
               self.moedas_pegas, self.inimigos_pegos = 0, 0
               self.escalonar_variaveis(-1)
               self.pode_colidir = 140
            else:
               remover_moedas = (self.obstaculo.QUANTIDADE_MOEDAS - 1) // 2
               remover_inimigos = (self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)

      for inimigo in self.obstaculo.inimigos_objetos[:]:
         if self.cobra.corpo.colliderect(inimigo.rect):
            self.obstaculo.inimigos_objetos.remove(inimigo)
            self.inimigos_pegos += 1
            self.pode_colidir = 25
            
            if self.inimigos_pegos == 2:
               self.moedas_pegas, self.inimigos_pegos = 0, 0
               self.escalonar_variaveis(1)
               self.pode_colidir = 140
            else:
               remover_moedas = (self.obstaculo.QUANTIDADE_MOEDAS - 1) // 2
               remover_inimigos = (self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2
               self.remover_obstaculos_aleatorios(remover_moedas, remover_inimigos)
   
   #TODO: Aprimorar aleatoriedade do surgimento dos obstaculos... Aprimorar a remoção? Coloca Menu, powerups. Aleatoriedade e divertido
   #todo: colocar essas if else, variaveis, nos respectivas funcoes, por exemplo esses negocios que pode gera um rodando = False la em cima junto com os outros enfim é isso boa sorte re rs
   
   def atualizar_jogo(self):
      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      
      if self.pode_colidir == 0:
         self.colidiu_obstaculos()
      else:
         self.pode_colidir -= 1
      self.animacao_obstaculos()

      # if self.aumentar_velocidade_tempo == 10:
      #    self.cobra.constante_razao *= 20
      #    self.aumentar_velocidade_tempo = 0
      # else:
      #    self.aumentar_velocidade_tempo += 1
      
      self.cobra.mover_cobra()
      if self.cobra.colidiu_borda_cobra() or self.VARIAVEIS.indice == 11: # deveria abrir a teal de GAME OVER
         self.rodando = False
   
   def desenhar_jogo(self):
      self.tela.fill(CORES["tela_cor"])
      self.obstaculo.desenhar_obstaculos(self.tela)
      
      if self.pode_colidir == 0:
         self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_ativo"])
      else:
         self.cobra.desenhar_cobra(self.tela, CORES["cobra_cor_safe"])

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