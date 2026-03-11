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
    },
    "shape_I": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "cor": (1, "c"),        
        "centralizado": (0, -1),
    },
    "shape_O": {
        "formato": [[1, 1],
                    [1, 1]],
        "cor": (2, "y"),      
        "centralizado": (1, 0),
    },
    "shape_L": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (3, "o"),   
        "centralizado": (0.5, -0.5),
    },
    "shape_J": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "cor": (4, "b"),
        "centralizado": (0.5, -0.5),
    },
    "shape_S": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "cor": (5, "g"),
        "centralizado": (0.5, -0.5),
    },
    "shape_Z": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "cor": (6, "r"),
        "centralizado": (0.5, -0.5),
    },
}

#todo: detalhes: na visualização dos proximos shapes, queria que a peça I tivesse uma distância igual aos outros
#todo: !: com a ghost piece, quando fico movimentando rapido, da umas travadinhas de leve

#TODO pelo fato que tem um while no pos_fantasma rodando junto com o jogo, se apertar Hard Drop rapido, vai parar onde o while estiver, entao precisa calcular a pos antes de clicar, entede?


COLUNAS = 10
LINHAS = 20
TILE = 16

ALTURA_DO_JOGO = 22
BOARD_X = 80

VAZIO = "_"

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico", fps=60, display_scale=2)
        px.load("my_resource.pyxres")
        
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        self.iniciamente_jogo()
        
        px.run(self.atualizar, self.desenhar)

   #//// //// ////
   
    def iniciamente_jogo(self):
        self.tempo_inicial = time.perf_counter()
        
        self.mapa = [[VAZIO] * COLUNAS for _ in range(ALTURA_DO_JOGO)]
        
        self.proximos_shapes = []
        self.bag_7 = []
        self.sistema_bag_7()
        
        self.shape_atual = ""
        self.novo_shape()
        
        self.fixou_neste_frame = False
        self.guardado_neste_frame = False
        self.shape_guardado = None
   
    def desovar_shape(self, formato):       
       return [4, 0] if formato == "shape_O" else [3, 0]
   
    def novo_shape(self):
        self.shape_atual = self.proximos_shapes.pop(0)
        self.reiniciar_shape()
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.desovar_shape(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_pos_fantasma = self.shape_pos_atual[:]
        self.estado_rotacao = "0"
        self.tempo_cair = 0
   
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    #////

    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0):
        correcao_altura = 2
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:  
                    # soma a posição atual com a posição do bloco iterado e, além disso, a próxima movimentação
                    n_col = pos[0] + i_coluna + dx 
                    n_lin = pos[1] + i_linha + dy + correcao_altura
                    
                    if n_col < 0:  # parede da esquerda
                        return True
                    
                    if n_lin <= 0: # teto
                        return True
                    
                    if n_col >= COLUNAS: # parede da direita
                        return True
                    
                    if n_lin >= ALTURA_DO_JOGO: # chao
                        return True
                    
                    if mapa[n_lin][n_col] != VAZIO: # verifica se contem uma peça fixada
                        return True
        return False
    
    #////
                
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
        return estados[(indice_atual + soma) % 4]            
    
    def rotacionar_shape(self, direcao):
        backup = self.shape_matriz_atual
        
        match direcao:
            case "KEY_Q":
                nova_matriz = [list(linha) for linha in list(zip(*self.pegar_formato()))[::-1]]
                self.shape_matriz_atual = nova_matriz
                
                novo_estado_da_rotacao = self.retornar_novo_estado_da_rotacao("esquerda")
                correcao = self.sistema_de_super_rotacao(novo_estado_da_rotacao)
            
            case "KEY_E": 
                nova_matriz = [list(linha) for linha in list(zip(*self.pegar_formato()[::-1]))]
                self.shape_matriz_atual = nova_matriz  
                
                novo_estado_da_rotacao = self.retornar_novo_estado_da_rotacao("direita")
                correcao = self.sistema_de_super_rotacao(novo_estado_da_rotacao)               

            case _: raise("Erro na rotação")
            
        if correcao[0] == True:
            self.shape_pos_atual[0] += correcao[1][0]
            self.shape_pos_atual[1] += correcao[1][1]
            self.shape_pos_fantasma = self.shape_pos_atual[:]
            match direcao:
                case "KEY_Q": self.estado_rotacao = self.retornar_novo_estado_da_rotacao("esquerda")
                case "KEY_E": self.estado_rotacao = self.retornar_novo_estado_da_rotacao("direita")
        else:
            self.shape_matriz_atual = backup
    
    #////

    def sistema_bag_7(self):
        quantidades_de_shapes = 3
        if len(self.bag_7) == 0:
            piece = ["I", "O", "T", "L", "J", "S", "Z"]
            self.bag_7 = [f"shape_{x}" for x in piece]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_shapes) < quantidades_de_shapes:
            self.proximos_shapes.append(self.bag_7.pop(0))
    
    def fixar(self, formato, pos, mapa, cor):
        correcao_altura = 2
        if not self.fixou_neste_frame:
            self.fixou_neste_frame = True
            for linha in range(len(formato)):
                for coluna in range(len(formato[linha])):
                    if formato[linha][coluna] == 1:
                        mx = pos[0] + coluna
                        my = pos[1] + linha + correcao_altura
                        mapa[my][mx] = cor
            return True
        return False

    def lock_delay(self):
        pass
    
    def queda_automatica(self):
        self.tempo_cair += 1
        self.velocidade = 64
        if self.tempo_cair >= self.velocidade:
            self.tempo_cair = 0
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.lock_delay()
                self.shape_pos_atual[1] += 1
            else:
                self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
    
    def verificar_linha(self, mapa):
        mapa_temp = mapa[::-1]
        
        for linha_e in mapa_temp:             
            if not VAZIO in linha_e:
                self.atualizar_mapa(mapa_temp)
                
    def atualizar_mapa(self, mapa_temp):
        pontuacao = 0
        
        for linha_i, linha_e in enumerate(mapa_temp):
            if not VAZIO in linha_e:
                mapa_temp[linha_i] = [VAZIO] * COLUNAS
        
        continuar_loop = True
        while continuar_loop:
            continuar_loop = False
                    
            for linha_i, linha_e in enumerate(mapa_temp):
                if linha_i + 1 >= len(mapa_temp) - 3:
                    break
                elif linha_e.count(VAZIO) == COLUNAS and mapa_temp[linha_i + 1].count(VAZIO) != COLUNAS: 
                    mapa_temp[linha_i + 1], mapa_temp[linha_i] = mapa_temp[linha_i], mapa_temp[linha_i + 1]
                    continuar_loop = True
                
        self.mapa = mapa_temp[::-1]
        return pontuacao

    def verificar_game_over(self):
        pass 
    
    #////
    
    def segurar_shape(self):
        if px.btnp(px.KEY_TAB) and not self.guardado_neste_frame:
            self.guardado_neste_frame = True
            
            if self.shape_guardado == None:
                self.shape_guardado = self.shape_atual
                self.novo_shape()
            else:
                self.shape_atual, self.shape_guardado = self.shape_guardado, self.shape_atual
                self.reiniciar_shape()    

    def mover_lados_shape(self):
        repeticao = 5        
        if px.btnp(px.KEY_LEFT, repeat=repeticao) or px.btnp(px.KEY_A, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
        
        elif px.btnp(px.KEY_RIGHT, repeat=repeticao) or px.btnp(px.KEY_D, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                self.shape_pos_atual[0] += 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
    
    def verificar_rotacao_shape(self):
        if px.btnp(px.KEY_Q):
            self.rotacionar_shape("KEY_Q")
        if px.btnp(px.KEY_E):
            self.rotacionar_shape("KEY_E")
    
    def soft_drop(self):
        repeticao = 5
        if px.btnp(px.KEY_DOWN, repeat=repeticao) or px.btnp(px.KEY_S, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.tempo_cair = self.velocidade
    
    def hard_drop(self):
        if px.btnp(px.KEY_SPACE):
            self.fixar(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, SHAPES[self.shape_atual]["cor"][1])
    
    def teclas_especiais(self):
        if px.btnp(px.KEY_F1):
            self.iniciamente_jogo()
    
    def input_tecla(self):
        self.segurar_shape()
        self.mover_lados_shape()
        self.verificar_rotacao_shape()
        self.soft_drop()
        self.hard_drop()
        self.teclas_especiais()
    
    #////
    
    def atualizar(self):
        self.fixou_neste_frame = False
        
        self.sistema_bag_7()
        self.input_tecla()
        self.queda_automatica()
        
        if self.fixou_neste_frame:
            self.guardado_neste_frame = False
            self.verificar_linha(self.mapa)
            self.novo_shape()
            self.verificar_game_over()
        
        self.tempo_ocorrendo = (time.perf_counter() - self.tempo_inicial)
        #print(self.shape_pos_atual)

    #//// //// ////
    
    def todos_os_textos(self):
        # for x in range(4):
        #     self.desenhar_texto(
        #         (x + (0.2 * (x + 1))), 
        #         0.7, 
        #         x
        #     )
        px.text(0, 30, f"Tempo: {self.tempo_ocorrendo:.3f}s", 7)
    
    def desenhar_texto(self, coluna_x, linha_y, spritesheet_x, *, diminuir=0):
        px.blt(
            (TILE - diminuir) * coluna_x, 
            (TILE - diminuir) * linha_y, 
            0, 
            (TILE * spritesheet_x), (TILE * 2), 
            (TILE - diminuir), (TILE - diminuir), 
            scale=1.2
        )
        
    #////
    
    def desenhar_fundo(self, pos, spritesheet_pos, tamanho):
        px.bltm(
            pos[0], 
            pos[1], 
            0, 
            (TILE * spritesheet_pos[0]), (TILE * spritesheet_pos[1]), 
            (TILE * tamanho[0]), (TILE * tamanho[1])
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x, spritesheet_y, *, diminuir=0, offset=0):
        px.blt(
            ((TILE - diminuir) * coluna_x) + BOARD_X, 
            (TILE - diminuir) * (linha_y + offset), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            (TILE - diminuir), (TILE - diminuir)
        )
        
    #////

    def verificar_pos_y_negativo(self):
        formato = self.pegar_formato()
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    match self.shape_pos_atual[1] + i_linha:
                        case -2: return -2
                        case -1: return -1
        return 0
    
    def calcular_offset_camera(self):
        pos_y_alto = self.verificar_pos_y_negativo()
        if pos_y_alto < 0:
            return abs(pos_y_alto)  # ex: y=-2 → offset=2
        return 0
    
    #////
    
    def desenhar_shape_fantasma(self, formato):
        while not self.verificar_colisao(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, dy=1):
            self.shape_pos_fantasma[1] += 1
        
        offset = self.calcular_offset_camera()
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]   
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            self.shape_pos_fantasma[0] + i_coluna,
                            self.shape_pos_fantasma[1] + i_linha, 
                            spritesheet_x, 3, 
                            offset=offset
                        )

    def desenhar_shape_atual(self, formato, pos_x, pos_y):
        offset = self.calcular_offset_camera()
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            pos_x + i_coluna, 
                            pos_y + i_linha, 
                            spritesheet_x, 0, 
                            offset=offset
                        )
    
    def desenhar_shapes_fixados(self, mapa):
        correcao_altura = 2
        offset = self.calcular_offset_camera()
        
        for linha in range(2, ALTURA_DO_JOGO):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != VAZIO:
                    cor = mapa[linha][coluna]
                    
                    for chave in SHAPES:
                        if cor == SHAPES[chave]["cor"][1]:
                            spritesheet_x = SHAPES[chave]["cor"][0]
                            self.desenhar_shape(
                                coluna,
                                linha - correcao_altura, 
                                spritesheet_x, 0, 
                                offset=offset
                            )
    
    #////
    
    def desenhar_proximos_shapes(self, proximos_shapes):
        # escalonar_tamanho = 3
        # valor_ajustar_x = 13.3
        escalonar_tamanho = 0
        valor_ajustar_x = 10.5
        valor_ajustar_y = 1
        
        acrescimo_distancia = 0
        for proximo_shape in proximos_shapes:
            
            (aumentar := -0.5) if proximo_shape == "shape_I" else (aumentar := 0)
            spritesheet_x = SHAPES[proximo_shape]["cor"][0]
            formato = SHAPES[proximo_shape]["formato"]
 
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            valor_ajustar_x + i_coluna + SHAPES[proximo_shape]["centralizado"][0], 
                            valor_ajustar_y + i_linha + acrescimo_distancia + aumentar, 
                            spritesheet_x, 0,
                            diminuir=escalonar_tamanho
                        )
            acrescimo_distancia += 3
    
    def desenhar_shape_guardado(self, shape_guardado):
        # escalonar_tamanho = 3
        # valor_ajustar_x = -4.1
        escalonar_tamanho = 0
        valor_ajustar_x = -3.5
        valor_ajustar_y = 3
        
        spritesheet_x = SHAPES[shape_guardado]["cor"][0]
        formato = SHAPES[shape_guardado]["formato"]

        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    self.desenhar_shape(
                        valor_ajustar_x + i_coluna + SHAPES[shape_guardado]["centralizado"][1], 
                        valor_ajustar_y + i_linha, 
                        spritesheet_x, 0,
                        diminuir=escalonar_tamanho
                    )
    
    #////
    
    def desenhar(self):
        px.cls(0)
        
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS))

        self.desenhar_shape_fantasma(self.pegar_formato())
        self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1])
        self.desenhar_shapes_fixados(self.mapa)
            
        # desenhar bordas
        self.desenhar_fundo(                        (0, 0), (TILE, 0), (5, 20))
        self.desenhar_fundo(((TILE * LINHAS) - BOARD_X, 0), (TILE, 0), (5, LINHAS))
        
        self.todos_os_textos()
        
        self.desenhar_proximos_shapes(self.proximos_shapes)
        
        if self.shape_guardado != None:
            self.desenhar_shape_guardado(self.shape_guardado)
 
Jogo()