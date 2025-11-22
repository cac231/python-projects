import time
import math
import random
import pygame

BLOCO = 36
TELA_LARGURA = BLOCO * 15 
TELA_COMPRIMENTO = BLOCO * 15

FPS = 60

VELOCIDADE = int(5 * (BLOCO / 30))
CIMA = (0, -VELOCIDADE)
DIREITA = (VELOCIDADE, 0)
BAIXO = (0, VELOCIDADE)
ESQUERDA = (-VELOCIDADE, 0)

CORES = {
   "tela_cor": (11, 20, 59),
   "cobra_cor": (10, 200, 100),
   "moeda_cor": (143, 181, 211),
   "inimigo_cor": (219, 29, 89),
}

#//

class Cobra:
   def __init__(self):
      self.inicio_x = TELA_LARGURA / 2 - (BLOCO / 2)
      self.inicio_y = TELA_COMPRIMENTO - 100
      
      self.corpo = pygame.Rect(self.inicio_x, self.inicio_y, BLOCO, BLOCO)
      self.velocidade = list(CIMA)

   def mover_cobra(self):
      self.corpo.x += self.velocidade[0]
      self.corpo.y += self.velocidade[1]

   def colidiu_borda_tela(self):
      if (self.corpo.x + BLOCO > TELA_LARGURA or 
          self.corpo.y + BLOCO > TELA_COMPRIMENTO or 
          self.corpo.x < 0 or 
          self.corpo.y < 0):
         return True

   def direcao_cobra(self, direcao_nova):
      if not (self.velocidade[0] != 0 and direcao_nova[0] != 0 or
              self.velocidade[1] != 0 and direcao_nova[1] != 0):
         self.velocidade = list(direcao_nova)

   def desenhar_cobra(self, tela):
      pygame.draw.rect(tela, CORES["cobra_cor"], self.corpo)
   
#//

class Moeda:
   def __init__(self, posicao):
      self.tamanho_padrao = BLOCO / 1.4
      self.tamanho_atual = 5
      self.fase = "crescendo"

      self.centro_xy = (posicao[0], posicao[1])
      self.rect = pygame.Rect(posicao, [self.tamanho_atual, self.tamanho_atual])

   def atualizar_animacao(self):
      velocidade = 2

      if self.fase == "crescendo":
         self.tamanho_atual += velocidade
         if self.tamanho_atual >= self.tamanho_padrao * 1.2:
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
   def __init__(self, posicao):
      self.tamanho_padrao = BLOCO / 1.8
      self.tamanho_atual = [30, 28]
      self.fase = "encolhendo"

      self.centro_xy = (posicao[0], posicao[1])
      self.rect = pygame.Rect(posicao, self.tamanho_atual)

   def atualizar_animacao(self):
      velocidade = 1

      if self.fase == "encolhendo":
         self.tamanho_atual[0] -= velocidade
         self.tamanho_atual[1] -= velocidade
         if self.tamanho_atual[0] <= self.tamanho_padrao / 1.8:
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
   def __init__(self):
      self.distancia_minima = 45

      self.QUANTIDADE_INIMIGOS = 10
      self.inimigos_objeto = []
      
      self.QUANTIDADE_MOEDAS = 16
      self.moedas_objeto = []
      
      self.quantidade_posicoes = (self.QUANTIDADE_MOEDAS + self.QUANTIDADE_INIMIGOS) * 1.1
      self.posicoes_feitas = []

   def criar_posicoes(self):
         while len(self.posicoes_feitas) < self.quantidade_posicoes:
            procurar = True
            while procurar:
               procurar = False
               
               pos_x = random.randint(17, TELA_LARGURA - 17)
               pos_y = random.randint(17, TELA_COMPRIMENTO - 17)

               for moeda in self.moedas_objeto:
                  distancia_entre_blocos = math.sqrt((moeda.centro_xy[0] - pos_x)**2 + (moeda.centro_xy[1] - pos_y)**2)   
                  if not (distancia_entre_blocos > self.distancia_minima):
                     procurar = True
                     break
               
               for inimigo in self.inimigos_objeto:
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

   def criar_objeto_obstaculo(self):
      for posicao in self.posicoes_feitas[:]:
         
         if len(self.moedas_objeto) < self.QUANTIDADE_MOEDAS:
            moeda = Moeda(posicao)
            self.moedas_objeto.append(moeda)
            self.posicoes_feitas.remove(posicao)
         
         elif len(self.inimigos_objeto) < self.QUANTIDADE_INIMIGOS:
            inimigo = Inimigo(posicao)
            self.inimigos_objeto.append(inimigo)
            self.posicoes_feitas.remove(posicao)

   def desenhar_rect_obstaculo(self, tela):
      for moeda in self.moedas_objeto:
         pygame.draw.rect(tela, CORES["moeda_cor"], moeda.rect)
      
      for inimigo in self.inimigos_objeto:
         pygame.draw.rect(tela, CORES["inimigo_cor"], inimigo.rect)
   
#//

class Jogo:
   def __init__(self):
      pygame.init()

      self.cobra = Cobra()
      self.obstaculo = Obstaculo()
      
      self.titulo = pygame.display.set_caption("A hora do Lesk!")
      self.time = pygame.time.Clock()
      self.rodando = True

      self.tela = pygame.display.set_mode((TELA_LARGURA, TELA_COMPRIMENTO))

   def processar_eventos(self):
      for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
            self.rodando = False
         
         elif evento.type == pygame.KEYDOWN:
            self.processar_teclas(evento.key)
   
   def processar_teclas(self, tecla):
      if tecla == pygame.K_RIGHT:
         self.cobra.direcao_cobra(DIREITA)
      if tecla == pygame.K_UP:
         self.cobra.direcao_cobra(CIMA)
      if tecla == pygame.K_LEFT:
         self.cobra.direcao_cobra(ESQUERDA)
      if tecla == pygame.K_DOWN:
         self.cobra.direcao_cobra(BAIXO)

   def acao_obstaculos(self):
      for moeda in self.obstaculo.moedas_objeto[:]:
         
         if moeda.fase != "completo":
            moeda.atualizar_animacao()

         if self.cobra.corpo.colliderect(moeda.rect):
            self.obstaculo.moedas_objeto.remove(moeda)
            print("MOEDA")
            
            if random.random() < 0.8 and self.obstaculo.inimigos_objeto:
               self.obstaculo.inimigos_objeto.pop(random.randint(0, len(self.obstaculo.inimigos_objeto) - 1))

      for inimigo in self.obstaculo.inimigos_objeto[:]:

         if inimigo.fase != "completo":
            inimigo.atualizar_animacao()

         if self.cobra.corpo.colliderect(inimigo.rect):
            self.obstaculo.inimigos_objeto.remove(inimigo)
            print("MORTE...")
   
   #TODO: Usar a função de variar tela... nao consegui. Aprimorar aleatoriedade do surgimento dos obstaculos... Aprimorar a remoção? Coloca Menu, powerups, o que vai acontecer se eu pegar 15 moedas? e se eu pegar as inimigas? aleatoriedade e divertido
   
   def atualizar(self):

      self.obstaculo.criar_posicoes()
      self.obstaculo.criar_objeto_obstaculo()

      self.acao_obstaculos()
   
      self.cobra.mover_cobra()
      if self.cobra.colidiu_borda_tela():
         self.rodando = False
   
   def desenhar_tudo(self):
      
      self.tela.fill(CORES["tela_cor"])
      self.cobra.desenhar_cobra(self.tela)
      self.obstaculo.desenhar_rect_obstaculo(self.tela)
      
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