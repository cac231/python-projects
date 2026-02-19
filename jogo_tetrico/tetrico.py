import pyxel as px
import random

SHAPES = {
    "shape_1": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (0, "p"),
    },
    "shape_2": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "cor": (1, "c"),
    },
    "shape_3": {
        "formato": [[1, 1],
                    [1, 1]],
        "cor": (2, "y"),
    },
    "shape_4": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (3, "o"),
    },
    "shape_5": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (4, "b"),
    },
    "shape_6": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "cor": (5, "g"),
    },
    "shape_7": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "cor": (6, "r"),
    },
}

COLUNAS = 10
LINHAS = 20
TILE = 16
BOARD_X = 80

#todo: Erro: peça fixa mesmo nao colidino na parte de cima de uma peça fixada, tipo, posso fixar ela nas paredes da peça, oq nao pode!

#todo: Erro, quando a peça esta bem proxima, eu posso rotacionar que vai deixar, assim sobrepondo, talvez so faça uma verificação de colisa se existe alguma letra ali para nao colidir

class Jogo:
    def __init__(self):
        
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico", fps=60, display_scale=2)
        px.load("resources/my_resource.pyxres")
        
        self.mapa = [["_"] * COLUNAS for _ in range(LINHAS)]
        
        self.shape_atual = self.novo_shape()
        self.shape_pos_atual = [3, 0]
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_plano_atual = 1
        
        self.proximos_shapes = []
        
        self.negativo = True
        
        self.tempo = 0
        self.velocidade = 1
        
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        px.run(self.atualizar, self.desenhar)

   #///
   
    def novo_shape(self):
        self.shape_pos_atual = [3, 0]
        return random.choice(list(SHAPES.keys()))
   
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    def pegar_largura(self):
        return len(self.pegar_formato()[0]) # quantas espaços tem nas listas
    
    def pegar_altura(self):
        return len(self.pegar_formato()) # quantas listas
            
    def proximos_shapes_random(self):
        while len(self.proximos_shapes) <= 4:
            proximo_shape = "shape" + random.choice([f"{x}" for x in range(1, 8)])
            self.proximos_shapes.append(proximo_shape)
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0):
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
                        self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        self.shape_atual = self.novo_shape()
                        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
                        return True
                    
                    if mapa[ny][nx] != "_":
                        self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                        self.shape_atual = self.novo_shape()
                        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
                        return True
        return False
    
    def mover(self):      
        if px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_A):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1
        
        if px.btnp(px.KEY_RIGHT) or px.btnp(px.KEY_D):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
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
        
    def fixar(self, formato, pos, mapa, cor):
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    mx = pos[0] + coluna
                    my = pos[1] + linha
                    mapa[my][mx] = cor
    
    
    def atualizar(self):
        self.mover()
        self.rotacionar()
        
        self.tempo += 1
        
        self.proximos_shapes_random()
        
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
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    spritesheet_x = SHAPES[self.shape_atual]["cor"][0]
                    self.desenhar_shape(x_pos + coluna, y_pos + linha, spritesheet_x)
    
    def desenhar_shapes_fixados(self, mapa):
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != "_":
                    cor = mapa[linha][coluna]
                    for chave in SHAPES:
                        if cor == SHAPES[chave]["cor"][1]:
                            spritesheet_x = SHAPES[chave]["cor"][0]
                            print("PEGOU A COR")
                            print(self.mapa)
                            self.desenhar_shape(coluna, linha, spritesheet_x)  

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
 
Jogo()