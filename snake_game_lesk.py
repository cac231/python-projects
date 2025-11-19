import time
import math
import random
import pygame

BLOCO = 32 # 32
TELA_LARGURA = BLOCO * 15 # 15
TELA_COMPRIMENTO = BLOCO * 15 # 15

FPS = 60

VELOCIDADE = 5 # 5
CIMA = (0, -VELOCIDADE)
DIREITA = (VELOCIDADE, 0)
BAIXO = (0, VELOCIDADE)
ESQUERDA = (-VELOCIDADE, 0)

CORES = {
   "tela_cor": (11, 20, 59),
   "cobra_cor": (10, 200, 100),
   "moeda_cor": (143, 181, 211),
   "inimigo_cor": (174, 0, 128),
}

#//

class Cobra:
   def __init__(self):
      self.inicio_x = TELA_LARGURA / 2 - (BLOCO / 2)
      self.inicio_y = TELA_COMPRIMENTO - 100
      
      self.corpo = pygame.Rect(self.inicio_x, self.inicio_y, BLOCO, BLOCO)
      self.velocidade = list(CIMA)

      self.tela_largura = TELA_LARGURA
      self.tela_comprimento = TELA_COMPRIMENTO

      self.obstaculo = Obstaculo()

   def mover(self):
      self.corpo.x += self.velocidade[0]
      self.corpo.y += self.velocidade[1]

   def colidiu(self):
      if (self.corpo.x + BLOCO > TELA_LARGURA or 
          self.corpo.y + BLOCO > TELA_COMPRIMENTO or 
          self.corpo.x < 0 or 
          self.corpo.y < 0):
         return True

   def direcao(self, direcao_nova):
      if not (self.velocidade[0] != 0 and direcao_nova[0] != 0 or
              self.velocidade[1] != 0 and direcao_nova[1] != 0):
         self.velocidade = list(direcao_nova)

   def desenhar_cobra(self, tela):
      pygame.draw.rect(tela, CORES["cobra_cor"], self.corpo)
   
#//

DISTANCIA_MINIMA = 45 # 40

QUANTIDADE_MOEDAS = 6 # 6

QUANTIDADE_POSICOES = QUANTIDADE_MOEDAS * 4

class Obstaculo:
   def __init__(self):
      self.posicoes_feitas = [] # LIMITE DE {QUANTIDADE_POSICOES} POSIÇÕES
      
      self.moedas_feitas = []
      self.QUANTIDADE_INIMIGOS = 6 # 4
      self.inimigos_feitos = []

   def criar_posicoes(self):

      while len(self.posicoes_feitas) < QUANTIDADE_POSICOES:
         procurar = True
         
         while procurar:
            procurar = False
            
            pos_x = random.randint(30, TELA_LARGURA - 40)
            pos_y = random.randint(30, TELA_COMPRIMENTO - 40)

            for (x, y) in self.posicoes_feitas:
               distancia_entre_blocos = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
               
               if not (distancia_entre_blocos > DISTANCIA_MINIMA):
                  procurar = True
                  break
         self.posicoes_feitas.append((pos_x, pos_y))      

   def criar_obstaculos(self):
      for posicao in self.posicoes_feitas[:]:
         if len(self.moedas_feitas) < QUANTIDADE_MOEDAS:
            moeda = pygame.Rect(posicao, (BLOCO - 15, BLOCO - 15))
            self.moedas_feitas.append(moeda)
            self.posicoes_feitas.remove(posicao)
            continue
         
         if len(self.inimigos_feitos) < self.QUANTIDADE_INIMIGOS:
            inimigo = pygame.Rect(posicao, (BLOCO - 20 , BLOCO - 20))
            self.inimigos_feitos.append(inimigo)
            self.posicoes_feitas.remove(posicao)

   def desenhar_obstaculos(self, tela):
      for moeda in self.moedas_feitas:
         pygame.draw.rect(tela, CORES["moeda_cor"], moeda)
      
      for inimigo in self.inimigos_feitos:
         pygame.draw.rect(tela, CORES["inimigo_cor"], inimigo)
   
#//

class Jogo:
   def __init__(self):
      pygame.init()

      self.cobra = Cobra()
      self.obstaculo = Obstaculo()
      
      self.titulo = pygame.display.set_caption("Lesk TIME!")
      self.time = pygame.time.Clock()
      self.rodando = True

      self.variar_tamanho_tela()
   
   def variar_tamanho_tela(self):
      self.tela = pygame.display.set_mode((self.cobra.tela_largura, self.cobra.tela_comprimento))

   def processar_eventos(self):
      for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas(evento.key)
   
   def processar_teclas(self, tecla):
      if tecla == pygame.K_RIGHT:
         self.cobra.direcao(DIREITA)
      if tecla == pygame.K_UP:
         self.cobra.direcao(CIMA)
      if tecla == pygame.K_LEFT:
         self.cobra.direcao(ESQUERDA)
      if tecla == pygame.K_DOWN:
         self.cobra.direcao(BAIXO)
   
   def atualizar(self):
      if len(self.obstaculo.posicoes_feitas) < QUANTIDADE_POSICOES:
         self.obstaculo.criar_posicoes()
      
      #TODO: transformar em uma função TUDO isso -> ... Usar a função de variar tela... Aprimorar aleatoriedade do surgimento dos obstaculos... Aprimorar a remoção?

      for moeda in self.obstaculo.moedas_feitas:
         if self.cobra.corpo.colliderect(moeda):
               print("moedadadada")
               self.obstaculo.moedas_feitas.remove(moeda)

               if random.random() < 0.6:
                  self.obstaculo.inimigos_feitos.pop(random.randint(0, self.obstaculo.QUANTIDADE_INIMIGOS - 1))
               # self.variar_tamanho_tela()
      
      for inimigo in self.obstaculo.inimigos_feitos:
         if self.cobra.corpo.colliderect(inimigo):
            self.obstaculo.inimigos_feitos.remove(inimigo)
            
            if random.random() < 0.6:
               self.obstaculo.inimigos_feitos.pop(random.randint(0, self.obstaculo.QUANTIDADE_INIMIGOS - 1))
      
      self.obstaculo.criar_obstaculos()

   
      self.cobra.mover()
      if self.cobra.colidiu():
         self.rodando = False
   
   def desenhar_tudo(self):
      self.tela.fill(CORES["tela_cor"])
      self.cobra.desenhar_cobra(self.tela)
      self.obstaculo.desenhar_obstaculos(self.tela)
      
      pygame.display.flip()  
   
   def loop(self):
      while self.rodando:

         self.atualizar()
         self.desenhar_tudo()
         self.processar_eventos()
         self.time.tick(FPS)
      
      pygame.quit()

if __name__ == "__main__":
   Jogo().loop()