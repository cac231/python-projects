import pyxel as px
import time
import random

SHAPES = {
    "shape_1": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (0, "p"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 1, 0],
                                 [1, 1, 1]],
    },
    "shape_2": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "cor": (1, "c"),
        
        "centralizado": (0, -1),
        "formato_visualizacao": [[1, 1, 1, 1]]
    },
    "shape_3": {
        "formato": [[1, 1],
                    [1, 1]],
        "cor": (2, "y"),
        
        "centralizado": (1, 0),
        "formato_visualizacao": [[1, 1],
                                 [1, 1]],
    },
    "shape_4": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (3, "o"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 0, 1],
                                 [1, 1, 1]],
    },
    "shape_5": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (4, "b"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[1, 0, 0],
                                 [1, 1, 1]],
    },
    "shape_6": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "cor": (5, "g"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 1, 1],
                                 [1, 1, 0]],
    },
    "shape_7": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "cor": (6, "r"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[1, 1, 0],
                                 [0, 1, 1]],
    },
}

COLUNAS = 10
LINHAS = 20
TILE = 16
BOARD_X = 80

#todo: Erro, quando a peça esta bem proxima, eu posso rotacionar que vai deixar, assim sobrepondo, talvez so faça uma verificação de colisa se existe alguma letra ali para nao colidir

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico", fps=60, display_scale=2)
        px.load("my_resource.pyxres")
        
        self.tempo_inicial = time.perf_counter()
        
        self.mapa = [["_"] * COLUNAS for _ in range(LINHAS)]
        
        self.proximos_quatro_shapes = []
        self.bag_7 = []
        self.randomizar_bag_7()
        
        self.shape_atual = ""
        self.novo_shape()
        
        self.guardado_neste_momento = False
        self.shape_guardado = None
        
        self.tempo = 0
        self.velocidade = 1
        
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        px.run(self.atualizar, self.desenhar)

   #///
   
    def reiniciar_shape(self):
        self.shape_pos_atual = [3, 0]
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
   
    def novo_shape(self):
        self.shape_atual = self.proximos_quatro_shapes.pop(0)
        self.reiniciar_shape()
   
    def pegar_formato(self):
        return self.shape_matriz_atual
            
    def randomizar_bag_7(self):
        if len(self.bag_7) == 0:
            self.bag_7 = [f"shape_{x}" for x in range(1, 8)]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_quatro_shapes) < 5:
            self.proximos_quatro_shapes.append(self.bag_7.pop(0))
    
    def guardar_e_pegar_shape(self):
        if self.shape_guardado == None:
            self.shape_guardado = self.shape_atual
            self.novo_shape()
        else:
            self.shape_atual, self.shape_guardado = self.shape_guardado, self.shape_atual
            self.reiniciar_shape()
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0, direita_esquerda=False):
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    
                    # soma a posição atual com a posição do bloco iterado e, além disso, a próxima movimentação
                    nx = pos[0] + coluna + dx 
                    ny = pos[1] + linha + dy
                    
                    # colidir com a parede da esquerda
                    if nx < 0:
                        return True
                    
                    # colidir com a parede da direita
                    if nx >= COLUNAS:
                        return True
                    
                    # colidir com o chão
                    if ny >= 20:
                        self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        return True
                    
                    # fixar se colidir com bloco, mas não coldir se for lateral do bloco
                    if mapa[ny][nx] != "_":
                        if direita_esquerda:
                            return True
                        self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        return True
        return False
    
    def mover(self):      
        if px.btnp(px.KEY_LEFT, repeat=5) or px.btnp(px.KEY_A, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1, direita_esquerda=True):
                self.shape_pos_atual[0] -= 1
                self.tempo, self.constante_do_tempo = 0, 0
                
        
        if px.btnp(px.KEY_RIGHT, repeat=5) or px.btnp(px.KEY_D, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1, direita_esquerda=True):
                self.shape_pos_atual[0] += 1
                self.tempo, self.constante_do_tempo = 0, 0
        
        if px.btnp(px.KEY_DOWN, repeat=5) or px.btnp(px.KEY_S, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.shape_pos_atual[1] += 1
                self.tempo, self.constante_do_tempo = 0, 0
                
    def corrigir_rotacao_fora_do_mapa(self):
        formato = self.pegar_formato()
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    while self.shape_pos_atual[0] + coluna < 0:
                        self.shape_pos_atual[0] += 1
                    while self.shape_pos_atual[0] + coluna >= COLUNAS:
                        self.shape_pos_atual[0] -= 1
        
    def rotacionar_e_hold(self):
        if px.btnp(px.KEY_Q):
            nova_matriz_menos_90 = list(zip(*self.pegar_formato()))[::-1]
            self.shape_matriz_atual = nova_matriz_menos_90     
            self.corrigir_rotacao_fora_do_mapa()

        if px.btnp(px.KEY_E):
            nova_matriz_mais_90 = list(zip(*self.pegar_formato()[::-1]))
            self.shape_matriz_atual = nova_matriz_mais_90  
            self.corrigir_rotacao_fora_do_mapa()

        if px.btnp(px.KEY_R):
            nova_matriz_virar_180 = [el[::-1] for el in self.pegar_formato()[::-1]]
            self.shape_matriz_atual = nova_matriz_virar_180
            self.corrigir_rotacao_fora_do_mapa()
        
        if px.btnp(px.KEY_TAB) and not self.guardado_neste_momento:
            self.guardado_neste_momento = True
            self.guardar_e_pegar_shape()
        
    def fixar_e_novo_shape(self, formato, pos, mapa, cor):
        self.guardado_neste_momento = False
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    mx = pos[0] + coluna
                    my = pos[1] + linha
                    mapa[my][mx] = cor
        self.novo_shape()
    
    # def movimentacao_automatica(self, tempo, constante):
    #     if tempo > 120 * constante:
    #         self.constante_do_tempo += 1
    #         # o y do shape atual
    #         self.shape_pos_atual[1] += 1
    
    def atualizar(self):
        self.tempo_ocorrendo = (time.perf_counter() - self.tempo_inicial)
        print(self.shape_pos_atual)
        
        self.randomizar_bag_7()
        
        self.mover()
        self.rotacionar_e_hold()
        
        self.tempo += 1
        self.constante_do_tempo = 1
        
        # self.movimentacao_automatica(self.tempo, self.constante_do_tempo)
        
        self.verificar_colisao(self.shape_atual, self.shape_pos_atual, self.mapa)

    #///
    
    def todos_os_textos(self):
        for x in range(4):
            self.desenhar_texto(
                (x + (0.2 * (x + 1))), 
                0.7, 
                x
            )
            
        px.text(0, 30, f"Tempo: {self.tempo_ocorrendo:.3f}s", 7)
    
    def desenhar_texto(self, coluna_x, linha_y, spritesheet_x, *, diminuir=0):
        px.blt(
            coluna_x * (TILE - diminuir), 
            linha_y * (TILE - diminuir), 
            0, 
            spritesheet_x * 16, 32, 
            (TILE - diminuir), (TILE - diminuir), scale=1.2
        )
    
    def desenhar_fundo(self, pos, pos_spritesheet, tamanho):
        px.bltm(
            pos[0], pos[1], 
            0, 
            pos_spritesheet[0] * TILE, pos_spritesheet[1] * TILE, 
            tamanho[0] * TILE, tamanho[1] * TILE
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x, *, diminuir=0):
        px.blt(
            BOARD_X + coluna_x * (TILE - diminuir), 
            linha_y * (TILE - diminuir), 
            0, 
            spritesheet_x * 16, 0, 
            (TILE - diminuir), (TILE - diminuir)
        )

    def desenhar_shape_atual(self, formato, x_pos, y_pos):
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    self.desenhar_shape(x_pos + coluna, y_pos + linha, spritesheet_x)
    
    def desenhar_shapes_fixados(self, mapa):
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != "_":
                    cor = mapa[linha][coluna]
                    for chave in SHAPES:
                        if cor == SHAPES[chave]["cor"][1]:
                            spritesheet_x = SHAPES[chave]["cor"][0]
                            #print("PEGOU A COR")
                            #print(self.mapa)
                            self.desenhar_shape(coluna, linha, spritesheet_x)
    
    def desenhar_proximos_shapes(self, proximos_shapes):
        menos_tamanho = 3
        valor_ajustar_x = 13.3
        valor_ajustar_y = 1
        
        acrescimo_distancia = 0
        for proximo_shape in proximos_shapes:
            spritesheet_x = SHAPES[proximo_shape]["cor"][0]
            formato = SHAPES[proximo_shape]["formato_visualizacao"]
 
            for linha in range(len(formato)):
                for coluna in range(len(formato[linha])):               
                    if formato[linha][coluna] == 1:
                        self.desenhar_shape(
                            valor_ajustar_x + coluna + SHAPES[proximo_shape]["centralizado"][0], 
                            valor_ajustar_y + linha + acrescimo_distancia, 
                            spritesheet_x,
                            diminuir=menos_tamanho
                        )
            acrescimo_distancia += 3
    
    def desenhar_shape_guardado(self, shape_guardado):
        menos_tamanho = 3
        valor_ajustar_x = -4.1
        valor_ajustar_y = 3
        
        spritesheet_x = SHAPES[shape_guardado]["cor"][0]
        formato = SHAPES[shape_guardado]["formato"]

        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    self.desenhar_shape(
                        valor_ajustar_x + coluna + SHAPES[shape_guardado]["centralizado"][1], 
                        valor_ajustar_y + linha, 
                        spritesheet_x,
                        diminuir=menos_tamanho
                    )
        
    def desenhar(self):
        px.cls(0)
        
        # desenhar fundo
        self.desenhar_fundo((80, 0), (0, 0), (10, 20))
        # desenhar bordas
        self.desenhar_fundo(       (0, 0), (16, 0), (5, 20))
        self.desenhar_fundo((320 - 80, 0), (16, 0), (5, 20))
        
        # desenhar textos
        self.todos_os_textos()
        
        # desenhar shape atual
        self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1])
        
        # desenhar shape fixados
        self.desenhar_shapes_fixados(self.mapa)
        
        # desenhar próximos shapes
        self.desenhar_proximos_shapes(self.proximos_quatro_shapes)
        
        # desenhar o shape hold
        if self.shape_guardado != None:
            self.desenhar_shape_guardado(self.shape_guardado)
 
Jogo()