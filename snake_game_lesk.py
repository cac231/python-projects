import math
import random
import os
os.environ['SDL_VIDEO_CENTERED'] = 'centered'
import pygame

BLOCO = 36
TELA_LARGURA = BLOCO * 15
TELA_COMPRIMENTO = BLOCO * 15

FPS = 60

VELOCIDADE = 5
CIMA = (0, -VELOCIDADE)
DIREITA = (VELOCIDADE, 0)
BAIXO = (0, VELOCIDADE)
ESQUERDA = (-VELOCIDADE, 0)

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
      self.BLOCO = BLOCO
      self.TELA_LARGURA = TELA_LARGURA
      self.TELA_COMPRIMENTO = TELA_COMPRIMENTO
      self.DISTANCIA_MINIMA = 40
   def variaveis_tudo_atualizar(self, constante):
      self.BLOCO *= constante
      self.TELA_LARGURA *= constante
      self.TELA_COMPRIMENTO *= constante
      self.DISTANCIA_MINIMA *= constante

#TODO: essa constante na distancia_minima não esta estavel. Quando aumenta muito a tela, os blocos enconstam um no outro

#//

class Cobra:
   def __init__(self, variaveis_classe):
      self.variaveis_classe = variaveis_classe

      inicio_x = self.variaveis_classe.TELA_LARGURA / 2 - (self.variaveis_classe.BLOCO / 2)
      inicio_y = self.variaveis_classe.TELA_COMPRIMENTO - 100
      
      self.corpo = pygame.Rect(inicio_x, inicio_y, self.variaveis_classe.BLOCO, self.variaveis_classe.BLOCO)
      self.velocidade = list(CIMA)

      self.cobra_rect_atualizar(inicio_x, inicio_y)
   def cobra_rect_atualizar(self, x, y):
      self.pos_x = x
      self.pos_y = y
      self.corpo = pygame.Rect(self.pos_x, self.pos_y, self.variaveis_classe.BLOCO, self.variaveis_classe.BLOCO)
   
   def mover_cobra(self):
      self.corpo.x += self.velocidade[0]
      self.corpo.y += self.velocidade[1]

   def colidiu_borda_cobra(self):
      if (self.corpo.x + self.variaveis_classe.BLOCO > self.variaveis_classe.TELA_LARGURA or 
          self.corpo.y + self.variaveis_classe.BLOCO > self.variaveis_classe.TELA_COMPRIMENTO or 
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
   def __init__(self, posicao, variaveis_classe):
      self.variaveis_classe = variaveis_classe

      self.tamanho_padrao = self.variaveis_classe.BLOCO / 1.4
      self.tamanho_atual = self.variaveis_classe.BLOCO / 7
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
   def __init__(self, posicao, variaveis_classe):
      self.variaveis_classe = variaveis_classe

      self.tamanho_padrao = self.variaveis_classe.BLOCO / 1.8
      self.tamanho_atual = [self.variaveis_classe.BLOCO / 1.2, self.variaveis_classe.BLOCO / 1.28]
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
   def __init__(self, variaveis_classe):
      self.variaveis_classe = variaveis_classe

      self.distancia_minima = self.variaveis_classe.DISTANCIA_MINIMA

      self.QUANTIDADE_INIMIGOS = 10
      self.inimigos_objetos = []
      
      self.QUANTIDADE_MOEDAS = (self.QUANTIDADE_INIMIGOS // 2)
      self.moedas_objetos = []
      
      self.quantidade_posicoes = (self.QUANTIDADE_MOEDAS + self.QUANTIDADE_INIMIGOS) * 1.1
      self.posicoes_feitas = []

   def criar_posicoes(self):
         while len(self.posicoes_feitas) < self.quantidade_posicoes:
            procurar = True
            while procurar:
               procurar = False
               
               pos_x = random.uniform(17, self.variaveis_classe.TELA_LARGURA - 17)
               pos_y = random.uniform(17, self.variaveis_classe.TELA_COMPRIMENTO - 17)

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
            moeda = Moeda(posicao, self.variaveis_classe)
            self.moedas_objetos.append(moeda)
            self.posicoes_feitas.remove(posicao)
         
         elif len(self.inimigos_objetos) < self.QUANTIDADE_INIMIGOS:
            inimigo = Inimigo(posicao, self.variaveis_classe)
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

      self.variaveis_classe = Variaveis()
      self.cobra = Cobra(self.variaveis_classe)
      self.obstaculo = Obstaculo(self.variaveis_classe)
      
      self.moedas_pegas = 0
      self.inimigos_pegos = 0
      self.pode_colidir = 60 # começa com 60 frames sem colidir
      
      self.titulo = pygame.display.set_caption("A hora do Lesk!")
      self.tempo = pygame.time.Clock()
      self.rodando = True

      self.tela = pygame.display.set_mode((self.variaveis_classe.TELA_LARGURA, self.variaveis_classe.TELA_COMPRIMENTO))
   def tela_atualizar_jogo(self):
      self.tela = pygame.display.set_mode((self.variaveis_classe.TELA_LARGURA, self.variaveis_classe.TELA_COMPRIMENTO))

   def processar_eventos_jogo(self):
      for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas_jogo(evento.key)
   
   def processar_teclas_jogo(self, tecla):
      if tecla == pygame.K_RIGHT:
         self.cobra.direcionar_cobra(DIREITA)
      if tecla == pygame.K_UP:
         self.cobra.direcionar_cobra(CIMA)
      if tecla == pygame.K_LEFT:
         self.cobra.direcionar_cobra(ESQUERDA)
      if tecla == pygame.K_DOWN:
         self.cobra.direcionar_cobra(BAIXO)

   def animacao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
            if moeda.fase != "completo":
               moeda.animacao_moeda()
      for inimigo in self.obstaculo.inimigos_objetos[:]:
            if inimigo.fase != "completo":
               inimigo.animacao_inimigo()           

   def escalonar_variaveis(self, constante):
      self.variaveis_classe.variaveis_tudo_atualizar(constante)

      x, y = self.cobra.corpo.topleft # pegar a posição x e y atual do rect da cobra
      self.obstaculo.moedas_objetos = []
      self.obstaculo.inimigos_objetos = []
      self.obstaculo.posicoes_feitas = []

      self.cobra.cobra_rect_atualizar(x, y)
      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      self.tela_atualizar_jogo()

   def remover_obstaculos_aleatorios(self, remover_quantos):
      if self.obstaculo.inimigos_objetos and self.obstaculo.moedas_objetos:
         for x in range(remover_quantos):
            self.obstaculo.inimigos_objetos.pop(random.randint(0, len(self.obstaculo.inimigos_objetos) - 1))
            self.obstaculo.moedas_objetos.pop(random.randint(0, len(self.obstaculo.moedas_objetos) - 1))

   def colidiu_obstaculos(self):
      for moeda in self.obstaculo.moedas_objetos[:]:
         if self.cobra.corpo.colliderect(moeda.rect):
            self.obstaculo.moedas_objetos.remove(moeda)
            self.moedas_pegas += 1
            self.pode_colidir = 25
            
            if self.moedas_pegas == 5:
               self.moedas_pegas, self.inimigos_pegos = 0, 0
               self.escalonar_variaveis(1.1)
               self.pode_colidir = 120
            else:
               self.remover_obstaculos_aleatorios((self.obstaculo.QUANTIDADE_INIMIGOS - 1) // 2)

      for inimigo in self.obstaculo.inimigos_objetos[:]:
         if self.cobra.corpo.colliderect(inimigo.rect):
            self.obstaculo.inimigos_objetos.remove(inimigo)
            self.inimigos_pegos += 1
            self.pode_colidir = 25
            
            if self.inimigos_pegos == 2:
               self.moedas_pegas, self.inimigos_pegos = 0, 0
               self.escalonar_variaveis(0.9)
               self.pode_colidir = 120
            else:   
               self.remover_obstaculos_aleatorios(2)
   
   #TODO: Aprimorar aleatoriedade do surgimento dos obstaculos... Aprimorar a remoção? Coloca Menu, powerups. Aleatoriedade e divertido
   
   def atualizar_jogo(self):
      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objetos_obstaculos()
      
      if self.pode_colidir == 0:
         self.colidiu_obstaculos()
      else:
         self.pode_colidir -= 1
      self.animacao_obstaculos()
      
      self.cobra.mover_cobra()
      if self.cobra.colidiu_borda_cobra() or (self.variaveis_classe.TELA_LARGURA < 310):
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