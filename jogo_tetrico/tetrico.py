import pyxel as px
import time
import random

SHAPES = {
    "shape_T": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (0, "p"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 1, 0],
                                 [1, 1, 1]],
    },
    "shape_I": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "cor": (1, "c"),
        
        "centralizado": (0, -1),
        "formato_visualizacao": [[1, 1, 1, 1]]
    },
    "shape_O": {
        "formato": [[1, 1],
                    [1, 1]],
        "cor": (2, "y"),
        
        "centralizado": (1, 0),
        "formato_visualizacao": [[1, 1],
                                 [1, 1]],
    },
    "shape_L": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (3, "o"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 0, 1],
                                 [1, 1, 1]],
    },
    "shape_J": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (4, "b"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[1, 0, 0],
                                 [1, 1, 1]],
    },
    "shape_S": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "cor": (5, "g"),
        
        "centralizado": (0.5, -0.5),
        "formato_visualizacao": [[0, 1, 1],
                                 [1, 1, 0]],
    },
    "shape_Z": {
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

ALTURA_DO_JOGO = 22
BOARD_X = 80

#todo: Erro, quando a peça esta bem proxima, eu posso rotacionar que vai deixar, assim sobrepondo, talvez so faça uma verificação de colisa se existe alguma letra ali para nao colidir

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico", fps=60, display_scale=2)
        px.load("my_resource.pyxres")
        
        self.tempo_inicial = time.perf_counter()
        
        self.mapa = [["_"] * COLUNAS for _ in range(ALTURA_DO_JOGO)]
        
        self.proximos_quatro_shapes = []
        self.bag_7 = []
        self.randomizar_bag_7()
        
        self.shape_atual = ""
        self.novo_shape()
        
        self.fixou_neste_frame = False
        self.guardado_neste_momento = False
        self.shape_guardado = None
        
        self.tempo_cair = 0
        
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        px.run(self.atualizar, self.desenhar)

   #///
   
    def pegar_shape_spawn(self, formato):
       if formato == "shape_O":
           return [4, 0]
       elif formato == "shape_I":
           return [3, 0]
       else:
           return [3, 0]
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.pegar_shape_spawn(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.estado_rotacao = "0"
   
    def novo_shape(self):
        self.shape_atual = self.proximos_quatro_shapes.pop(0)
        self.reiniciar_shape()
   
    def pegar_formato(self):
        return self.shape_matriz_atual
            
    def randomizar_bag_7(self):
        if len(self.bag_7) == 0:
            piece = ["I", "O", "T", "L", "J", "S", "Z"]
            self.bag_7 = [f"shape_{x}" for x in piece]
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
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0):
        correcao_altura = 2
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:  
                    # soma a posição atual com a posição do bloco iterado e, além disso, a próxima movimentação
                    n_col = pos[0] + coluna + dx 
                    n_lin = pos[1] + linha + dy + correcao_altura
                    
                    # colidir com a parede da esquerda
                    if n_col < 0:
                        return True
                    
                    if n_lin <= 0:
                        return True
                    
                    # colidir com a parede da direita
                    if n_col >= COLUNAS:
                        return True
                    
                    # colidir com o chão
                    if n_lin >= ALTURA_DO_JOGO:
                        return True
                    
                    # fixar se colidir com bloco, mas não coldir se for lateral do bloco
                    if mapa[n_lin][n_col] != "_":
                        return True
        return False
    
    def mover(self):
        if px.btnp(px.KEY_UP):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[1] -= 1          
              
        if px.btnp(px.KEY_LEFT, repeat=5) or px.btnp(px.KEY_A, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1   
        
        if px.btnp(px.KEY_RIGHT, repeat=5) or px.btnp(px.KEY_D, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                self.shape_pos_atual[0] += 1
        
        if px.btnp(px.KEY_DOWN, repeat=5) or px.btnp(px.KEY_S, repeat=5):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.shape_pos_atual[1] += 1
                self.tempo_cair = 0
            else:
                self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                    
                
    def sistema_de_super_rotacao(self, novo_estado):        
        SEQUENCIA = {
            "todos_shapes": {       
                "0->R": [(0,0), (-1,0), (-1,-1), (0,2),  (-1,2)],
                "R->0": [(0,0), (1,0),  (1,1),   (0,-2), (1,-2)],
                "R->2": [(0,0), (1,0),  (1,1),   (0,-2), (1,-2)],
                "2->R": [(0,0), (-1,0), (-1,-1), (0,2),  (-1,2)],
                "2->L": [(0,0), (1,0),  (1,-1),  (0,2),  (1,2)],
                "L->2": [(0,0), (-1,0), (-1,1),  (0,-2), (-1,-2)],
                "L->0": [(0,0), (-1,0), (-1,1),  (0,-2), (-1,-2)],
                "0->L": [(0,0), (1,0),  (1,-1),  (0,2),  (1,2)],
                "R->L": [(0,0), (2,0),  (2,0),   (0,0), (1,0)],
            },
            "shape_I": {
                "0->R": [(0,0), (-2,0), (1,0),  (-2,1),  (1,-2)],
                "R->0": [(0,0), (2,0),  (-1,0), (2,-1),  (-1,2)],
                "R->2": [(0,0), (-1,0), (2,0),  (-1,-2), (2,1)],
                "2->R": [(0,0), (1,0),  (-2,0), (1,2),   (-2,-1)],
                "2->L": [(0,0), (2,0),  (-1,0), (2,-1),  (-1,2)],
                "L->2": [(0,0), (-2,0), (1,0),  (-2,1),  (1,-2)],
                "L->0": [(0,0), (1,0),  (-2,0), (1,2),   (-2,-1)],
                "0->L": [(0,0), (-1,0), (2,0),  (-1,-2), (2,1)],
            }
        }
        
        if self.shape_atual == "shape_O":
            return (False, (0, 0))
        
        transcricao = f"{self.estado_rotacao}->{novo_estado}"
        lista_das_sequencias = SEQUENCIA["shape_I" if self.shape_atual == "shape_I" else "todos_shapes"][transcricao]
        
        for (dx, dy) in lista_das_sequencias:
            resultado = self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=dx, dy=dy)
            if not resultado:
                return (True, (dx, dy))
        return (False, (0, 0)) 
                    
    def retornar_novo_estado_da_rotacao(self, direcao):
        estados = ["0", "R", "2", "L"]
        
        if direcao == "direita":
            soma = +1
        elif direcao == "esquerda":
            soma = -1
        elif direcao == "180":
            soma = +2
        else:
            raise("Erro nas direções")
        
        indice_atual = estados.index(self.estado_rotacao)
        return estados[(indice_atual + soma) % 4] # a string de estados            
        
    def rotacionar(self):
        if px.btnp(px.KEY_Q):
            backup = self.shape_matriz_atual     
            
            nova_matriz_esquerda = [list(linha) for linha in list(zip(*self.pegar_formato()))[::-1]]
            self.shape_matriz_atual = nova_matriz_esquerda
            
            novo_estado_da_rotacao = self.retornar_novo_estado_da_rotacao("esquerda")
            correcao = self.sistema_de_super_rotacao(novo_estado_da_rotacao)
            
            if correcao[0] == True:
                self.shape_pos_atual[0] += correcao[1][0]
                self.shape_pos_atual[1] += correcao[1][1]
                self.estado_rotacao = self.retornar_novo_estado_da_rotacao("esquerda")
            else:
                self.shape_matriz_atual = backup

        if px.btnp(px.KEY_E):
            backup = self.shape_matriz_atual
            
            nova_matriz_direita = [list(linha) for linha in list(zip(*self.pegar_formato()[::-1]))]
            self.shape_matriz_atual = nova_matriz_direita  
            
            novo_estado_da_rotacao = self.retornar_novo_estado_da_rotacao("direita")
            correcao = self.sistema_de_super_rotacao(novo_estado_da_rotacao)
            
            if correcao[0] == True:
                self.shape_pos_atual[0] += correcao[1][0]
                self.shape_pos_atual[1] += correcao[1][1]
                self.estado_rotacao = self.retornar_novo_estado_da_rotacao("direita")
            else:
                self.shape_matriz_atual = backup
        
    def fixar_e_novo_shape(self, formato, pos, mapa, cor):
        if self.fixou_neste_frame:
            return
        self.fixou_neste_frame = True
        correcao_altura = 2
        self.guardado_neste_momento = False
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    mx = pos[0] + coluna
                    my = pos[1] + linha + correcao_altura
                    mapa[my][mx] = cor
        self.novo_shape()
    
    def atualizar(self):
        self.fixou_neste_frame = False
        
        self.tempo_ocorrendo = (time.perf_counter() - self.tempo_inicial)
        print(self.shape_pos_atual)
        
        self.randomizar_bag_7()
        
        self.rotacionar()
        if px.btnp(px.KEY_TAB) and not self.guardado_neste_momento:
            self.guardado_neste_momento = True
            self.guardar_e_pegar_shape()
        self.mover()
        
        self.tempo_cair += 1
        self.velocidade = 64
        if self.tempo_cair >= self.velocidade:
            self.tempo_cair = 0
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.shape_pos_atual[1] += 1
            else:
                self.fixar_e_novo_shape(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])

    #/// //// ////
    
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
        
    #////
    
    def desenhar_fundo(self, pos, pos_spritesheet, tamanho):
        px.bltm(
            pos[0], pos[1], 
            0, 
            pos_spritesheet[0] * TILE, pos_spritesheet[1] * TILE, 
            tamanho[0] * TILE, tamanho[1] * TILE
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x, *, diminuir=0, offset=0):
        px.blt(
            BOARD_X + coluna_x * (TILE - diminuir), 
            (linha_y + offset) * (TILE - diminuir), 
            0, 
            spritesheet_x * 16, 0, 
            (TILE - diminuir), (TILE - diminuir)
        )

    def verificar_pos_y_no_mapa(self):
        formato = self.pegar_formato()
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                    
                    match self.shape_pos_atual[1] + linha:
                        case -2: return -2
                        case -1: return -1
                        case 19: return 19
        return 0
    
    def calcular_offset_camera(self):
        y_mais_alto = self.verificar_pos_y_no_mapa()  # y atual da peça
        if y_mais_alto < 0:
            return abs(y_mais_alto)  # ex: y=-2 → offset=2
        return 0

    def desenhar_shape_atual(self, formato, x_pos, y_pos):
        offset = self.calcular_offset_camera()
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]
        for linha in range(len(formato)):
            for coluna in range(len(formato[linha])):
                if formato[linha][coluna] == 1:
                        self.desenhar_shape(x_pos + coluna, y_pos + linha, spritesheet_x, offset=offset)
    
    def desenhar_shapes_fixados(self, mapa):
        correcao_altura = 2
        offset = self.calcular_offset_camera()
        for linha in range(2, ALTURA_DO_JOGO):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != "_":
                    cor = mapa[linha][coluna]
                    for chave in SHAPES:
                        if cor == SHAPES[chave]["cor"][1]:
                            spritesheet_x = SHAPES[chave]["cor"][0]
                            self.desenhar_shape(coluna, linha - correcao_altura, spritesheet_x, offset=offset)
    
    #////
    
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
        
        # # desenhar fundo
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS))
        # # desenhar shape atual
        self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1])
        # desenhar shape fixados
        self.desenhar_shapes_fixados(self.mapa)
    
        #////
        
        # desenhar bordas
        self.desenhar_fundo(       (0, 0), (TILE, 0), (5, 20))
        self.desenhar_fundo(((TILE * LINHAS) - BOARD_X, 0), (TILE, 0), (5, LINHAS))
        
        # desenhar textos
        self.todos_os_textos()
        
        # desenhar próximos shapes
        self.desenhar_proximos_shapes(self.proximos_quatro_shapes)
        
        # desenhar o shape hold
        if self.shape_guardado != None:
            self.desenhar_shape_guardado(self.shape_guardado)
 
Jogo()