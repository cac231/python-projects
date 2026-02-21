import pyxel as px
import random

SHAPES = {
    "shape_1": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (0, "p"),
        "centralizado": 11,
    },
    "shape_2": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "cor": (1, "c"),
        "centralizado": 10.5,
    },
    "shape_3": {
        "formato": [[1, 1],
                    [1, 1]],
        "cor": (2, "y"),
        "centralizado": 11.5,
    },
    "shape_4": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (3, "o"),
        "centralizado": 11,
    },
    "shape_5": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (4, "b"),
        "centralizado": 11,
    },
    "shape_6": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "cor": (5, "g"),
        "centralizado": 11,
    },
    "shape_7": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "cor": (6, "r"),
        "centralizado": 11,
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
        
        self.mapa = [["_"] * COLUNAS for _ in range(LINHAS)]
        
        self.proximos_quatro_shapes = []
        self.bag_7 = []
        self.randomizar_bag_7()
        
        self.shape_atual = self.novo_shape()
        
        self.shape_pos_atual = [3, 0]
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        
        self.tempo = 0
        self.velocidade = 1
        
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        px.run(self.atualizar, self.desenhar)

   #///
   
    def novo_shape(self):
        self.shape_pos_atual = [3, 0]
        return self.proximos_quatro_shapes.pop(0)
   
    def pegar_formato(self):
        return self.shape_matriz_atual
            
    def randomizar_bag_7(self):
        if len(self.bag_7) == 0:
            self.bag_7 = [f"shape_{x}" for x in range(1, 8)]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_quatro_shapes) < 6:
            self.proximos_quatro_shapes.append(self.bag_7.pop(0))
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0, direita_esquerda=False):
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    
                    # soma a posição atual com a posição do bloco iterado e, além disso, a próxima movimentação
                    nx = pos[0] + coluna + dx 
                    ny = pos[1] + linha + dy
                    
                    if nx < 0:
                        return True
                    
                    if nx >= COLUNAS:
                        return True
                    
                    if ny >= 20:
                        self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        return True
                    
                    if mapa[ny][nx] != "_":
                        if direita_esquerda:
                            return True
                        self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        return True
        return False
    
    def mover(self):      
        if px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_A):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1, direita_esquerda=True):
                self.shape_pos_atual[0] -= 1
        
        if px.btnp(px.KEY_RIGHT) or px.btnp(px.KEY_D):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1, direita_esquerda=True):
                self.shape_pos_atual[0] += 1
        
        if px.btnp(px.KEY_DOWN) or px.btnp(px.KEY_S):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.shape_pos_atual[1] += 1
                
    def verificar_colisao_ao_rotacionar(self):
        pass
    
    def rotacionar(self):
        if px.btnp(px.KEY_Q):
            nova_matriz_menos_90 = list(zip(*self.shape_matriz_atual))[::-1]
            self.shape_matriz_atual = nova_matriz_menos_90

        if px.btnp(px.KEY_E):
            nova_matriz_mais_90 = list(zip(*self.shape_matriz_atual[::-1]))
            self.shape_matriz_atual = nova_matriz_mais_90
            
            #nova_matriz_mais_90 = self.shape_matriz_atual[::-1]     

        if px.btnp(px.KEY_R):
            nova_matriz_virar_180 = [el[::-1] for el in self.shape_matriz_atual[::-1]]
            self.shape_matriz_atual = nova_matriz_virar_180
        
    def fixar_e_novo_shape(self, formato, pos, mapa, cor):
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    mx = pos[0] + coluna
                    my = pos[1] + linha
                    mapa[my][mx] = cor
        
        self.shape_atual = self.novo_shape()
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
    
    
    def atualizar(self):
        self.randomizar_bag_7()
        
        self.mover()
        self.rotacionar()
        
        self.tempo += 1
        
        
        self.verificar_colisao(self.shape_atual, self.shape_pos_atual, self.mapa)

    #///
    
    def desenhar_fundo(self, pos, pos_spritesheet, tamanho):
        px.bltm(
            pos[0], pos[1], 
            0, 
            pos_spritesheet[0] * TILE, pos_spritesheet[1] * TILE, 
            tamanho[0] * TILE, tamanho[1] * TILE
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x):
        px.blt(
            BOARD_X + coluna_x * TILE, 
            linha_y * TILE, 
            0, 
            spritesheet_x * 16,
            0, TILE, TILE, 0
        )

    def desenha_shape_atual(self, formato, x_pos, y_pos):
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
        acrescimo_distancia = 0
        for proximo_shape in proximos_shapes:
            spritesheet_x = SHAPES[proximo_shape]["cor"][0]
            formato = SHAPES[proximo_shape]["formato"]
            for linha in range(len(formato)):
                for coluna in range(len(formato[linha])):
                    if formato[linha][coluna] == 1:
                        self.desenhar_shape(
                            SHAPES[proximo_shape]["centralizado"] + coluna, 
                            1 + acrescimo_distancia + linha, 
                            spritesheet_x
                        )
            acrescimo_distancia += 3

    def desenhar(self):
        px.cls(0)
        
        # desenhar fundo
        self.desenhar_fundo((80, 0), (0, 0), (10, 20))
        # desenhar bordas
        self.desenhar_fundo(       (0, 0), (16, 0), (5, 20))
        self.desenhar_fundo((320 - 80, 0), (16, 0), (5, 20))
        
        # desenhar shape atual
        self.desenha_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1])
        
        # desenhar shape fixados
        self.desenhar_shapes_fixados(self.mapa)
        
        # desenhar próximos shapes
        self.desenhar_proximos_shapes(self.proximos_quatro_shapes)
 
Jogo()