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

#todo: fazer animacao ao limpar linha... fazer isso antes de mover as linhas tlg... tipo, quando acabar o ARE, acionaria mover linha

TABELA_G = {
    1: 0.01667,
    2: 0.021017,
    3: 0.026977,
    4: 0.035256,
    5: 0.04693,
    6: 0.06361,
    7: 0.0879,
    8: 0.1236,
    9: 0.1775,
    10: 0.2598,
    11: 0.388,
    12: 0.59,
    13: 0.92,
    14: 1.46,
    15: 2.36,
    16:	3.91,
    17:	6.61,
    18:	11.43,
    19:	20.23,
    20:	36.6,
}

def buscar_tabela_g(nivel):
    if nivel >= 20:
        return TABELA_G[20]
    return TABELA_G[nivel]

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
        
        self.linhas_limpas = 0 # a cada 10 * nivel_atual, suba de nivel
        self.nivel_atual = 1
        
        self.pontos_atual = 0
        self.combo_atual = -1
        
        self.proximos_shapes = []
        self.bag_7 = []
        self.sistema_bag_7()
        
        self.shape_atual = ""
        self.novo_shape()
        
        self.shape_guardado = None
        self.fixou_neste_frame = False
        self.guardado_neste_frame = False
        
        self.das = 10
        self.arr = 2
        
        # animacao
        self.movimento_padrao = 4
        self.movimento_y_esquerda = 0
        self.movimento_y_direita = 0
        self.movimento_y = 0
        self.movimento_x = 0 
        self.temporizador_animacao_hard_drop = self.movimento_padrao
   
    def desovar_shape(self, formato):       
       return [4, 0] if formato == "shape_O" else [3, 0]
   
    def novo_shape(self):
        self.shape_atual = self.proximos_shapes.pop(0)
        self.reiniciar_shape()
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.desovar_shape(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_pos_fantasma = self.shape_pos_atual[:]
        self.recalcular_pos_fantasma()
        
        # rotacao e outras funções que a utilizam
        self.estado_rotacao = "0"
        # t-spin
        self.ultima_acao_foi_rotacao = False
        self.ultimo_srs_foi_1x2 = False
        self.situacao_t_spin = None
        
        # gravidade
        self.tempo_existe = 0
        g = buscar_tabela_g(self.nivel_atual)
        self.tempo_simulado = 1 / g
        
        # lock delay
        self.lock_tempo = 0
        self.lock_movimentos = 0
        self.y_anterior = self.shape_pos_atual[1]
        
        # pontuacao
        self.quantos_soft_drops = 0
        self.atual_back_to_back = 0
        
        # ARE
        self.temp_do_are = 0
        self.esta_em_are = False
        self.limpou_linha = False
        
        # movimentar desenho
        self.foi_para_esquerda = False
        self.foi_para_direita = False 
        
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    #////

    def sistema_bag_7(self):
        quantidades_de_shapes = 3
        if len(self.bag_7) == 0:
            piece = ["I", "O", "T", "L", "J", "S", "Z"]
            self.bag_7 = [f"shape_{x}" for x in piece]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_shapes) < quantidades_de_shapes:
            self.proximos_shapes.append(self.bag_7.pop(0))
    
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
                    
                    if n_lin < 0: # teto
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
        
        for index, (dx, dy) in enumerate(lista_das_sequencias):
            resultado = self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=dx, dy=dy)
            if not resultado:
                if index == 4:
                    self.ultimo_srs_foi_1x2 = True
                else:
                    self.ultimo_srs_foi_1x2 = False
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
    
    def fixar(self, formato, pos, mapa, cor):
        correcao_altura = 2
        if not self.fixou_neste_frame:
            self.fixou_neste_frame = True
            
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                        
                        mx = pos[0] + i_coluna
                        my = pos[1] + i_linha + correcao_altura
                        mapa[my][mx] = cor
            return True
        return False
    
    def queda_automatica(self):
        self.tempo_existe += 1
        g = buscar_tabela_g(self.nivel_atual)
        
        while self.tempo_existe > self.tempo_simulado: 
                if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                    self.shape_pos_atual[1] += 1
                    
                    if self.shape_pos_atual[1] > self.y_anterior:
                        self.y_anterior = self.shape_pos_atual[1]
                        self.lock_movimentos = 0
                    
                    self.tempo_simulado += 1 / g # linhs por frame, que vai aumentando
                    self.lock_tempo = 0
                else:
                    self.tempo_existe = self.tempo_simulado
                    break
        
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            self.lock_tempo += 1
    
    def condicoes_do_t_spin(self, mapa):
        T_SPIN_CANTO = {
            "0": {
                "F": [(-1,-1), (1,-1)], 
                "B": [(-1, 1), (1, 1)],
                },
            "R": {
                "F": [( 1,-1), (1, 1)], 
                "B": [(-1,-1), (-1,1)],
                },
            "2": {
                "F": [(-1, 1), (1, 1)], 
                "B": [(-1,-1), (1,-1)],
                },
            "L": {
                "F": [(-1,-1), (-1,1)], 
                "B": [( 1,-1), (1, 1)],
                },
        }
        
        rotacao_preset = T_SPIN_CANTO[self.estado_rotacao]
        pos_do_centro = self.shape_pos_atual[0] + 1, self.shape_pos_atual[1] + 1 
        
        canto_f = 0
        canto_b = 0
        
        correcao_altura = 2
        for diagonal, posicoes in rotacao_preset.items():
            for tupla in posicoes:
                mx = pos_do_centro[0] + tupla[0]
                if mx < 0 or mx >= COLUNAS:
                    if diagonal == "F": 
                            canto_f += 1
                            continue
                    if diagonal == "B": 
                            canto_b += 1
                            continue
                        
                my = pos_do_centro[1] + tupla[1] + correcao_altura
                if my < 0 or my >= ALTURA_DO_JOGO:
                    if diagonal == "F": 
                            canto_f += 1
                            continue
                    if diagonal == "B": 
                            canto_b += 1
                            continue
                
                if mapa[my][mx] != VAZIO:
                    match diagonal:
                        case "F": canto_f += 1
                        case "B": canto_b += 1
        
        print("canto_f", canto_f)
        print("canto_b", canto_b, "\n")
        return (canto_f, canto_b)
    
    def t_spin(self, canto_f, canto_b):
        if canto_f == 2 and canto_b >= 1:
            return "t_spin"
        elif canto_f == 1 and canto_b == 2:
            if self.ultimo_srs_foi_1x2:
                return "t_spin"
            else:
                return "mini_t_spin"
        return None
    
    #////
    
    def verificar_combo(self, combo_atual):
        if combo_atual >= 1:
            return 50 * combo_atual * self.nivel_atual
        return 0
    
    def verificar_linha(self, mapa):
        mapa_temp = mapa[::-1]
        for linha_e in mapa_temp:             
            if not VAZIO in linha_e:
                self.limpou_linha = True
                pontuacao = self.limpar_linhas_e_pontuar(mapa_temp)              
                self.mapa = mapa_temp[::-1]         
                self.combo_atual += 1
                pontuacao += self.verificar_combo(self.combo_atual)         
                return pontuacao
        
        self.combo_atual = -1
        
        match self.situacao_t_spin:
            case "t_spin": return 400 * self.nivel_atual
            case "mini_t_spin": return 100 * self.nivel_atual
        
        return 0
                
    def limpar_linhas_e_pontuar(self, mapa_temp):
        def calcular_pontos(linhas_limpas_consecutivas):
            PONTUACAO_POR_LINHAS = {
                1: 100 * self.nivel_atual,
                2: 300 * self.nivel_atual,
                3: 500 * self.nivel_atual,
                4: 800 * self.nivel_atual,
            }
            PONTUACAO_POR_T_SPIN = {
                1: 800 * self.nivel_atual,
                2: 1200 * self.nivel_atual,
                3: 1600 * self.nivel_atual,
            }
            PONTUACAO_POR_MINI_T_SPIN = {            
                1: 200 * self.nivel_atual,
                2: 400 * self.nivel_atual,
            }
            
            pontuacao_pelas_linhas_consecutivas = 0
            
            if self.situacao_t_spin == None:
                pontuacao_pelas_linhas_consecutivas += PONTUACAO_POR_LINHAS[linhas_limpas_consecutivas]
            else:
                match self.situacao_t_spin:
                    case "t_spin": pontuacao_pelas_linhas_consecutivas += PONTUACAO_POR_T_SPIN[linhas_limpas_consecutivas]
                    case "mini_t_spin": pontuacao_pelas_linhas_consecutivas += PONTUACAO_POR_MINI_T_SPIN[linhas_limpas_consecutivas]           
            
            return pontuacao_pelas_linhas_consecutivas
        
        def calcular_back_to_back(linhas_limpas_consecutivas):
            if linhas_limpas_consecutivas == 4:
                self.atual_back_to_back += 1
                return
            if self.situacao_t_spin != None:
                self.atual_back_to_back += 1
                return
            self.atual_back_to_back = 0    
        
        pontuacao_total = 0
        linhas_limpas_consecutivas = 0
        
        for linha_i, linha_e in enumerate(mapa_temp):
            if not VAZIO in linha_e:
                mapa_temp[linha_i] = [VAZIO] * COLUNAS
                self.linhas_limpas += 1
                linhas_limpas_consecutivas += 1
            else:
                if linhas_limpas_consecutivas > 0:
                    pontuacao_soma = calcular_pontos(linhas_limpas_consecutivas)
                    
                    calcular_back_to_back(linhas_limpas_consecutivas)
                    (aumento_do_back_to_back := 1.5) if self.atual_back_to_back >= 2 else (aumento_do_back_to_back := 1)
                    print(aumento_do_back_to_back)         
                    
                    pontuacao_total += pontuacao_soma * aumento_do_back_to_back  
                    linhas_limpas_consecutivas = 0
        
        if linhas_limpas_consecutivas > 0:
            pontuacao_soma = calcular_pontos(linhas_limpas_consecutivas)
            
            calcular_back_to_back(linhas_limpas_consecutivas)
            (aumento_do_back_to_back := 1.5) if self.atual_back_to_back >= 2 else (aumento_do_back_to_back := 1)         
            
            pontuacao_total += pontuacao_soma * aumento_do_back_to_back  
            linhas_limpas_consecutivas = 0
        
        return pontuacao_total

    def mover_linhas_do_mapa(self, mapa_temp):
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

    def verificar_nivel(self, linhas_limpas):
        if linhas_limpas >= self.nivel_atual * 10:
            self.nivel_atual += 1

    def ajustar_desovação(self):
        if (self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa) or 
            self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1)):
            self.shape_pos_atual[1] -= 1
            self.shape_pos_fantasma = self.shape_pos_atual[:]

    def verificar_game_over(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa):
            self.iniciamente_jogo()
        
    #////
    
    def aumentar_lock_reset(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            if self.lock_movimentos != 15:
                self.lock_movimentos += 1
                self.lock_tempo = 0
        else:
            pass
            #print("Sem encostar|Wall Wick subiu")
    
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
        hold = self.das        
        repeticao = self.arr
        if px.btnp(px.KEY_LEFT, hold=hold, repeat=repeticao) or px.btnp(px.KEY_A, hold=hold, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
                
                if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                    self.foi_para_esquerda = True
                else:
                    self.foi_para_esquerda, self.foi_para_direita = False, False
        
        elif px.btnp(px.KEY_RIGHT, hold=hold, repeat=repeticao) or px.btnp(px.KEY_D, hold=hold, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                self.shape_pos_atual[0] += 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
                
                if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                    self.foi_para_direita = True
                else:
                    self.foi_para_esquerda, self.foi_para_direita = False, False
    
    def verificar_rotacao_shape(self):
        if px.btnp(px.KEY_Q):
            self.rotacionar_shape("KEY_Q")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao = True

        if px.btnp(px.KEY_E):
            self.rotacionar_shape("KEY_E")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao = True
    
    def recalcular_pos_fantasma(self):
         while not self.verificar_colisao(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, dy=1):
            self.shape_pos_fantasma[1] += 1    
    
    def soft_drop(self):
        repeticao = 3
        if px.btnp(px.KEY_DOWN, repeat=repeticao) or px.btnp(px.KEY_S, repeat=repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.tempo_existe = self.tempo_simulado + (1 / 60)
                self.ultima_acao_foi_rotacao = False
                print(self.quantos_soft_drops)
                self.quantos_soft_drops += 1        
    
    def hard_drop(self):
        if px.btnp(px.KEY_SPACE):
            self.fixar(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, SHAPES[self.shape_atual]["cor"][1])
            self.pontos_atual += (self.shape_pos_fantasma[1] - self.shape_pos_atual[1]) * 2
            self.temporizador_animacao_hard_drop = 0
            self.esta_em_are = True
    
    def teclas_especiais(self):
        if px.btnp(px.KEY_F1):
            self.iniciamente_jogo()
    
    def input_tecla(self):
        self.segurar_shape()
        self.mover_lados_shape()
        self.verificar_rotacao_shape()
        self.recalcular_pos_fantasma()
        self.soft_drop()
        self.hard_drop()
        self.teclas_especiais()
    
    #////

    def atualizar(self):
        self.fixou_neste_frame = False
        if not self.esta_em_are:
        
            self.sistema_bag_7()
            self.input_tecla()        
            self.queda_automatica()
            
            if self.lock_tempo >= 30 or self.lock_movimentos == 15:
                if self.ultima_acao_foi_rotacao and self.shape_atual == "shape_T":
                    canto_f, canto_b = self.condicoes_do_t_spin(self.mapa)
                    self.situacao_t_spin = self.t_spin(canto_f, canto_b)
                
                self.pontos_atual += self.quantos_soft_drops
                self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor"][1])
                self.esta_em_are = True
        
            if self.fixou_neste_frame:
                    self.guardado_neste_frame = False
                    
                    self.pontos_atual += self.verificar_linha(self.mapa)
                    self.verificar_nivel(self.linhas_limpas)
         
        (are_duracao := 6) if self.limpou_linha else (are_duracao := 0)
            
        if self.esta_em_are: 
            if self.temp_do_are > are_duracao:
                if self.limpou_linha:
                    self.mover_linhas_do_mapa(self.mapa[::-1])
                self.novo_shape()
                self.ajustar_desovação()
                self.verificar_game_over()
            else:
                self.foi_para_esquerda = False
                self.foi_para_direita = False
                self.temp_do_are += 1
        
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
        
        px.text(2, 10 * 0.5, f"Tempo: {self.tempo_ocorrendo/60:.2f}min", 1)
        px.text(2, 10 * 1.5, f"Linhas limpas: {self.linhas_limpas}", 2)
        px.text(2, 10 * 2.5, f"Nivel: {self.nivel_atual}", 3)
        px.text(2, 10 * 3.5, f"Pontos {self.pontos_atual}", 4)
        px.text(2, 10 * 4.5, f"Combo {self.combo_atual}", 5)
        px.text(2, 10 * 5.5, f"Back-to-back {self.atual_back_to_back}", 6)
    
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
    
    def desenhar_fundo(self, pos, spritesheet_pos, tamanho, *, movimento_x=0, movimento_y=0):
        px.bltm(
            pos[0] + movimento_y * 16, 
            pos[1] + movimento_x * 16, 
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
    
    def desenhar_shape_fantasma(self, formato, movimento_y, movimento_x):
        offset = self.calcular_offset_camera()
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]   
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            self.shape_pos_fantasma[0] + i_coluna + movimento_y,
                            self.shape_pos_fantasma[1] + i_linha + movimento_x, 
                            spritesheet_x, 3, 
                            offset=offset
                        )
    
    def desenhar_shape_atual(self, formato, pos_x, pos_y, movimento_y, movimento_x):
        offset = self.calcular_offset_camera()
        spritesheet_x = SHAPES[self.shape_atual]["cor"][0]
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            pos_x + i_coluna + movimento_y, 
                            pos_y + i_linha + movimento_x, 
                            spritesheet_x, 0, 
                            offset=offset
                        )
    
    def desenhar_shapes_fixados(self, mapa, movimento_y, movimento_x):
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
                                coluna + movimento_y,
                                linha - correcao_altura + movimento_x, 
                                spritesheet_x, 0, 
                                offset=offset
                            )
    
    #////
    
    def desenhar_proximos_shapes(self, proximos_shapes, movimento_y):
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
                            valor_ajustar_x + i_coluna + SHAPES[proximo_shape]["centralizado"][0] + movimento_y, 
                            valor_ajustar_y + i_linha + acrescimo_distancia + aumentar, 
                            spritesheet_x, 0,
                            diminuir=escalonar_tamanho
                        )
            acrescimo_distancia += 3
    
    def desenhar_shape_guardado(self, shape_guardado, movimento_y):
        # escalonar_tamanho = 3
        # valor_ajustar_x = -4.1
        escalonar_tamanho = 0
        valor_ajustar_x = -3.5
        valor_ajustar_y = 5
        
        spritesheet_x = SHAPES[shape_guardado]["cor"][0]
        formato = SHAPES[shape_guardado]["formato"]

        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    self.desenhar_shape(
                        valor_ajustar_x + i_coluna + SHAPES[shape_guardado]["centralizado"][1] + movimento_y, 
                        valor_ajustar_y + i_linha, 
                        spritesheet_x, 0,
                        diminuir=escalonar_tamanho
                    )
    
    #////
    
    def calcular_variaveis_animacao(self):
        if self.foi_para_esquerda:
            if self.movimento_y_esquerda > -self.movimento_padrao:
                self.movimento_y_esquerda += -1
                self.movimento_y = self.movimento_y_esquerda
        else:
            if self.movimento_y_esquerda < 0:
                self.movimento_y_esquerda -= -1
                self.movimento_y = self.movimento_y_esquerda    
        
        if self.foi_para_direita:
            if self.movimento_y_direita < self.movimento_padrao:
                self.movimento_y_direita += 1
                self.movimento_y = self.movimento_y_direita
        else:
            if self.movimento_y_direita > 0:
                self.movimento_y_direita -= 1
                self.movimento_y = self.movimento_y_direita
        
        if self.temporizador_animacao_hard_drop < self.movimento_padrao:
            if self.movimento_x < self.movimento_padrao:
                self.movimento_x += 1
                self.temporizador_animacao_hard_drop += 1
        else:
            if self.movimento_x > 0:
                self.movimento_x -= 1
                self.temporizador_animacao_hard_drop = 6
    
    def desenhar(self):
        px.cls(0)
    
        self.calcular_variaveis_animacao()
        
        movimento_y_esquerda = self.movimento_y_esquerda / 10
        movimento_y_direita = self.movimento_y_direita / 10
        movimento_y = self.movimento_y / 10
        movimento_x = self.movimento_x  / 10
        
        print(movimento_y_direita)  
        
        # desenhar bordas
        self.desenhar_fundo((0, 0), (12, 0), (LINHAS, LINHAS))
        
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS), movimento_x=movimento_x, movimento_y=movimento_y,)

        if not self.esta_em_are:
            self.desenhar_shape_fantasma(self.pegar_formato(), movimento_y, movimento_x)
            self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1], movimento_y, movimento_x)
        
        self.desenhar_shapes_fixados(self.mapa, movimento_y, movimento_x)
        
        self.todos_os_textos()
        
        self.desenhar_proximos_shapes(self.proximos_shapes, movimento_y_direita)
        
        if self.shape_guardado != None:
            self.desenhar_shape_guardado(self.shape_guardado, movimento_y_esquerda)
 
Jogo()