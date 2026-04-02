import pyxel as px
import time
import random
import os

SHAPES = {
    "shape_T": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 0,
        "cor_letra": "p",
        "centralizado": (0.5, -0.5),
    },
    "shape_I": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "imagem_pos": 1,
        "cor_letra": "c",        
        "centralizado": (0, -1),
    },
    "shape_O": {
        "formato": [[1, 1],
                    [1, 1]],
        "imagem_pos": 2,
        "cor_letra": "y",      
        "centralizado": (1, 0),
    },
    "shape_L": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 3,
        "cor_letra": "o",
        "centralizado": (0.5, -0.5),
    },
    "shape_J": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 4,
        "cor_letra": "b",
        "centralizado": (0.5, -0.5),
    },
    "shape_S": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "imagem_pos": 5,
        "cor_letra": "g",
        "centralizado": (0.5, -0.5),
    },
    "shape_Z": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 6,
        "cor_letra": "r",
        "centralizado": (0.5, -0.5),
    },
}

COR_IMAGEM = {
    "p": 0,
    "c": 1,
    "y": 2,
    "o": 3,
    "b": 4,
    "g": 5,
    "r": 6,
}

def TABELA_PONTUACAO(tipo, linhas_limpas_por_shape, nivel_atual):
    tabela = { 
        "normal": {
            1: 100 * nivel_atual,
            2: 300 * nivel_atual,
            3: 500 * nivel_atual,
            4: 800 * nivel_atual,
        },
        "t_spin": {
            1: 800 * nivel_atual,
            2: 1200 * nivel_atual,
            3: 1600 * nivel_atual,
        },
        "mini_t_spin": {            
            1: 200 * nivel_atual,
            2: 400 * nivel_atual,
        },
        "perfect_clear": {
            1: 800 * nivel_atual,
            2: 1200 * nivel_atual,
            3: 1800 * nivel_atual,
            4: 2000 * nivel_atual,
        },
    }
    return tabela[tipo][linhas_limpas_por_shape]

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

#todo: adicionar menu com um botao de começar, historico, configuracao e sair. Tela de pause, tela de game_over com as pontuações

#todo: ao pressinar segurar e espaço repetidamente, vai bugar la no teto

def buscar_tabela_g(nivel):
    if nivel >= 20:
        return TABELA_G[20]
    return TABELA_G[nivel]

CAMINHO = lambda caminho: os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho)

TRANSFORMA_EM_DECIMAL = lambda num: num / 10

FONT_1 = px.Font(CAMINHO("assets/PublicPixel.ttf"), 8)

COLUNAS = 10
LINHAS = 20
TILE = 16

ALTURA_DO_JOGO = 22
CORRECAO_ALTURA = 2

BOARD_X = 80
VAZIO = "_"

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico", fps=60, display_scale=2, quit_key=False)
        px.load("my_resource.pyxres")
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        self.MAPEAMENTO = {
            "ESQUERDA": [px.KEY_A, px.KEY_LEFT, px.GAMEPAD1_BUTTON_DPAD_LEFT],
            "DIREITA": [px.KEY_RIGHT, px.KEY_D, px.GAMEPAD1_BUTTON_DPAD_RIGHT],
            
            "ROTACAO_ESQUERDA": [px.KEY_Q, px.GAMEPAD1_BUTTON_A],
            "ROTACAO_DIREITA": [px.KEY_E, px.GAMEPAD1_BUTTON_B],
            
            "SEGURAR": [px.KEY_TAB, px.GAMEPAD1_BUTTON_Y],
            "SOFT_DROP": [px.KEY_DOWN, px.KEY_S, px.GAMEPAD1_BUTTON_DPAD_DOWN],
            "HARD_DROP": [px.KEY_SPACE, px.GAMEPAD1_BUTTON_DPAD_UP],
            
            "REINICIAR": [px.KEY_F1, px.GAMEPAD1_BUTTON_BACK],
            "PAUSAR": [px.KEY_ESCAPE, px.GAMEPAD1_BUTTON_START],
        }   
        
        self.inicializar_jogo()
        px.run(self.atualizar, self.desenhar)

   #//// //// ////
   
    def variaveis_movimentos(self):
        # movimento_padrao = 5
        self.movimento_padrao = 5
        
        self.movimento_x_esquerda = 0
        self.movimento_x_direita = 0
        self.movimento_y = 0
        self.movimento_x = 0
        
        self.tempo_animacao_game_over_cascata = 0
        self.constante_animacao_game_over_cascata = 0
        
        self.movimento_game_over_slide = 0
        self.movimento_exponencial_game_over = 0
    
    def variaveis_velocidade_movimentacao(self):
        # das = 10
        self.das = 10
        # arr = 2
        self.arr = 2
        # arr_soft_drop = 3
        self.arr_soft_drop = 3
   
    def inicializar_jogo(self):
        self.tempo_inicial = time.perf_counter()
        
        self.mapa = [[VAZIO] * COLUNAS for _ in range(ALTURA_DO_JOGO)]
        
        self.linhas_limpas = 0
        self.nivel_atual = 1
        
        self.pontos_atual = 0
        self.combo_atual = -1
        
        # mostrar_quantos_shapes = 3
        self.mostrar_quantos_shapes = 3
        self.proximos_shapes = []
        self.bag_7 = []
        self.sistema_bag_7()
        
        self.shape_atual = ""
        self.shape_segurado = None
        self.gerar_novo_shape()
       
        # estados
        self.estado_do_jogo = "em_jogo"
        self.fixou_neste_frame = False
        self.segurou_neste_frame = False
        self.acionou_hard_drop = False
        
        # status
        self.quantidade_singles = 0
        self.quantidade_doubles = 0
        self.quantidade_triples = 0
        self.quantidade_quads = 0
        self.quantidade_t_spins = 0
        self.quantidade_perfect_clears = 0
        self.combo_maximo = 0
        self.streak_maximo = 0
        
        # custumizacao
        self.cores_aleatorias = random.sample(range(1, 8), 5)
        self.comprimento_do_rect_esquerdo = 0
        self.comprimento_do_rect_direita = 0
        
        # CONFIGURAÇÃO DO USUÁRIO
        self.variaveis_movimentos()
        self.variaveis_velocidade_movimentacao()
    
    def desovar_shape(self, formato):       
       return [4, 0] if formato == "shape_O" else [3, 0]
   
    def gerar_novo_shape(self):
        self.shape_atual = self.proximos_shapes.pop(0)
        self.reiniciar_shape()
        
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    #
    
    def variaveis_are(self):
        # are_duracao = 18
        self.are_duracao = 18
        self.temp_do_are = 0
        self.esta_em_are = False
        self.limpou_linha = False # Se False, sem ARE
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.desovar_shape(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_pos_fantasma = self.shape_pos_atual[:]
        self.recalcular_pos_fantasma()
        
        # rotacao
        self.estado_rotacao = "0"
        # t-spin
        self.ultima_acao_foi_rotacao = False
        self.ultimo_srs_foi_1x2 = False
        self.tipo_do_t_spin = None
        
        # gravidade
        self.gravidade_tempo_existe = 0
        g = buscar_tabela_g(self.nivel_atual)
        self.gravidade_tempo_simulado = 1 / g
        
        # lock delay
        self.lock_tempo = 0 # 0,5 segundos / 30 frames
        self.lock_movimentos = 0 # 15 movimentos
        self.y_anterior = self.shape_pos_atual[1]
        
        # pontuacao
        self.linhas_limpas_por_shape = 0
        self.atual_back_to_back = 0
        self.quantos_soft_drops = 0
        
        # movimentar os desenhos
        self.foi_para_esquerda = False
        self.foi_para_direita = False
        
        self.localizacao_das_linhas_limpas = []
        self.tempo_animacao_limpar_linha = 0
        self.constante_animacao_limpar_linha = 0
        
        # CONFIGURAÇÃO DO JOGO
        self.variaveis_are()
    
    #//// //// ////

    def pegar_input(self, input, repeticao=0, hold=0, *, input_puro=False):
        for tecla in self.MAPEAMENTO[input]:
            if input_puro and px.btn(tecla): 
                return True
            elif px.btnp(tecla, repeat=repeticao, hold=hold):
                return True
        return False
    
    def sistema_bag_7(self):
        if len(self.bag_7) == 0:
            piece = ["I", "O", "T", "L", "J", "S", "Z"]
            self.bag_7 = [f"shape_{x}" for x in piece]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_shapes) < self.mostrar_quantos_shapes:
            self.proximos_shapes.append(self.bag_7.pop(0))
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    n_col = pos[0] + i_coluna + dx 
                    n_lin = pos[1] + i_linha + dy + CORRECAO_ALTURA
                    
                    if n_col < 0:  # parede da esquerda
                        return True
                    
                    if n_col >= COLUNAS: # parede da direita
                        return True
                    
                    if n_lin < 0: # teto
                        return True
                    
                    if n_lin >= ALTURA_DO_JOGO: # chao
                        return True
                    
                    if mapa[n_lin][n_col] != VAZIO: # verifica se contem uma peça fixada
                        return True
        return False
    
    def verificar_colisao_parede(self, formato, pos, dx=0):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    n_col = pos[0] + i_coluna + dx
                    
                    if n_col < 0:  # parede da esquerda
                        return True
                    
                    if n_col >= COLUNAS: # parede da direita
                        return True
        return False
    
    def fixar(self, formato, pos, mapa, cor):
        if not self.fixou_neste_frame:
            self.fixou_neste_frame = True
            
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):    
                    if formato[i_linha][i_coluna] == 1:
                        mx = pos[0] + i_coluna 
                        my = pos[1] + i_linha + CORRECAO_ALTURA
                        mapa[my][mx] = cor
            return True
        return False

    def transformar_segundos(self):
        minutos = int(self.tempo_atual_em_segundos // 60)
        segundos = int(self.tempo_atual_em_segundos % 60)
        centesimos = int((self.tempo_atual_em_segundos - int(self.tempo_atual_em_segundos)) * 100)
        return f"{minutos:02d}:{segundos:02d}.{centesimos:02d}"
    
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
    
    def queda_automatica(self):
        self.gravidade_tempo_existe += 1
        g = buscar_tabela_g(self.nivel_atual)
        
        while self.gravidade_tempo_existe > self.gravidade_tempo_simulado: 
                if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                    self.shape_pos_atual[1] += 1
                    
                    if self.shape_pos_atual[1] > self.y_anterior:
                        self.y_anterior = self.shape_pos_atual[1]
                        self.lock_movimentos = 0
                    
                    self.gravidade_tempo_simulado += 1 / g # linhas por frame, que vai aumentando
                    self.lock_tempo = 0
                else:
                    self.gravidade_tempo_existe = self.gravidade_tempo_simulado
                    break
        
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            self.lock_tempo += 1
    
    def condicoes_do_t_spin(self, mapa):
        rotacao_preset = T_SPIN_CANTO[self.estado_rotacao]
        pos_do_centro = self.shape_pos_atual[0] + 1, self.shape_pos_atual[1] + 1 
        canto_f = 0
        canto_b = 0

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
                        
                my = pos_do_centro[1] + tupla[1] + CORRECAO_ALTURA
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
        return (canto_f, canto_b)
    
    def retornar_tipo_do_t_spin(self, canto_f, canto_b):
        if canto_f == 2 and canto_b >= 1:
            return "t_spin"
        elif canto_f == 1 and canto_b == 2:
            if self.ultimo_srs_foi_1x2:
                return "t_spin"
            else:
                return "mini_t_spin"
        return None
    
    #////
    
    def verificar_linha(self, mapa):
        mapa_temp = mapa[::-1]
        for linha_e in mapa_temp:             
            if not VAZIO in linha_e:
                self.limpar_linhas(mapa_temp)        
                self.limpou_linha = True
                self.mapa = mapa_temp[::-1]
                break
    
    def limpar_linhas(self, mapa_temp):        
        for linha_i, linha_e in enumerate(mapa_temp):
            if not VAZIO in linha_e:
                mapa_temp[linha_i] = [VAZIO] * COLUNAS
                self.localizacao_das_linhas_limpas += [(LINHAS - 1) - linha_i]
                self.linhas_limpas += 1
                self.linhas_limpas_por_shape += 1
    
    def calcular_pontos(self):
        linhas_limpas = self.linhas_limpas_por_shape
        pontuacao = 0
        
        if linhas_limpas == 0:
            self.combo_atual = -1
            match self.tipo_do_t_spin:
                case "t_spin": return 400 * self.nivel_atual
                case "mini_t_spin": return 100 * self.nivel_atual
            return 0
        else:
            self.combo_atual += 1  
            pontuacao += self.verificar_combo(self.combo_atual)
        
        if self.verificar_perfect_clear(self.mapa[::-1]):
            pontuacao += TABELA_PONTUACAO("perfect_clear", linhas_limpas, self.nivel_atual)
                        
        if linhas_limpas == 4:
            self.atual_back_to_back += 1
        elif self.tipo_do_t_spin != None:
            self.atual_back_to_back += 1
        elif linhas_limpas in (1, 2, 3):
            self.atual_back_to_back = 0
        
        aumento_do_back_to_back = 1.5 if self.atual_back_to_back >= 2 else 1 
    
        if self.tipo_do_t_spin == None:
            pontuacao += TABELA_PONTUACAO("normal", linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        else:
            pontuacao += TABELA_PONTUACAO(self.tipo_do_t_spin, linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        
        return pontuacao
  
    def verificar_combo(self, combo_atual):
        if combo_atual >= 1:
            return 50 * combo_atual * self.nivel_atual
        return 0
    
    def verificar_perfect_clear(self, mapa):
        for linha in mapa:
            if any(espaco != VAZIO for espaco in linha):
                return False
        return True
    
    def verificar_nivel(self, linhas_limpas):
        if linhas_limpas >= self.nivel_atual * 10:
            self.nivel_atual += 1

    #////
    
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

    def ajustar_desovação(self):
        if (self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa) or 
            self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1)):
            self.shape_pos_atual[1] -= 1
            self.shape_pos_fantasma = self.shape_pos_atual[:]

    def verificar_game_over(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa):
            self.estado_do_jogo = "game_over"
            self.shape_pos_atual = [0, 0]
        
    def aumentar_lock_reset(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            if self.lock_movimentos != 15:
                self.lock_movimentos += 1
                self.lock_tempo = 0
    
    def verificar_movimento_lateral(self):
        if self.shape_pos_atual[0] >= 6:
            movimento = "direita"
        elif self.shape_pos_atual[0] <= 1:
            movimento = "esquerda"
        else:
            return
    
        dx = -1 if movimento == "esquerda" else 1
        
        if self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, dx):
            if movimento == "esquerda":
                self.foi_para_esquerda = True
            if movimento == "direita":
                self.foi_para_direita = True
        else:
            self.foi_para_esquerda, self.foi_para_direita = False, False
    
    #////
    
    def segurar_shape(self, *, input_puro=False):
        if self.pegar_input("SEGURAR", input_puro=input_puro) and not self.segurou_neste_frame:
            self.segurou_neste_frame = True
            
            if self.shape_segurado == None:
                self.shape_segurado = self.shape_atual
                self.gerar_novo_shape()
            else:
                self.shape_atual, self.shape_segurado = self.shape_segurado, self.shape_atual
                self.reiniciar_shape()    

    def mover_lados_shape(self):
        hold = self.das        
        repeticao = self.arr
        
        esquerda = self.pegar_input("ESQUERDA", repeticao, hold)
        direita = self.pegar_input("DIREITA", repeticao, hold)

        esquerda_puro = self.pegar_input("ESQUERDA", input_puro=True) and not self.pegar_input("DIREITA", input_puro=True)
        direita_puro = self.pegar_input("DIREITA", input_puro=True) and not self.pegar_input("ESQUERDA", input_puro=True)
        
        if esquerda_puro and esquerda:
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
        
        elif direita_puro and direita:
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                self.shape_pos_atual[0] += 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
    
    def verificar_rotacao_shape(self, *, input_puro=False):
        if self.pegar_input("ROTACAO_ESQUERDA", input_puro=input_puro):
            self.rotacionar_shape("KEY_Q")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao = True

        if self.pegar_input("ROTACAO_DIREITA", input_puro=input_puro):
            self.rotacionar_shape("KEY_E")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao = True
    
    def recalcular_pos_fantasma(self):
         while not self.verificar_colisao(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, dy=1):
            self.shape_pos_fantasma[1] += 1    
    
    def soft_drop(self):
        repeticao = self.arr_soft_drop
        
        if self.pegar_input("SOFT_DROP", repeticao):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.gravidade_tempo_existe = self.gravidade_tempo_simulado + (1 / 60)
                self.quantos_soft_drops += 1        
                self.ultima_acao_foi_rotacao = False
    
    def hard_drop(self):
        if self.pegar_input("HARD_DROP"):
            self.fixar(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
            self.pontos_atual += (self.shape_pos_fantasma[1] - self.shape_pos_atual[1]) * 2
            self.pontos_atual += self.quantos_soft_drops
            self.esta_em_are = True
            self.acionou_hard_drop = True
    
    def teclas_especiais(self):
        if self.pegar_input("REINICIAR"):
            self.inicializar_jogo()
        elif self.pegar_input("PAUSAR"):
            pass
    
    def input_tecla(self):
        self.segurar_shape()
        self.mover_lados_shape()
        self.verificar_rotacao_shape()
        self.verificar_movimento_lateral()
        self.recalcular_pos_fantasma()
        self.soft_drop()
        self.hard_drop()
        self.teclas_especiais()
    
    #////

    def atualizar(self):
        self.tempo_fps_ms = time.perf_counter()
        print(self.estado_do_jogo)
        
        if self.estado_do_jogo == "pausado":
            self.teclas_especiais()
            return
        
        self.sistema_bag_7()
        
        if self.estado_do_jogo == "game_over":
            self.teclas_especiais()
            if self.movimento_game_over_slide >= LINHAS + 1:
                self.estado_do_jogo = "apos_game_over"
            return

        if self.estado_do_jogo == "apos_game_over":
            self.teclas_especiais()
            return  
        
        self.fixou_neste_frame = False
        if not self.esta_em_are:
            self.input_tecla()
            self.queda_automatica()
            
            if self.lock_tempo >= 30 or self.lock_movimentos == 15:
                if self.ultima_acao_foi_rotacao and self.shape_atual == "shape_T":
                    canto_f, canto_b = self.condicoes_do_t_spin(self.mapa)
                    self.tipo_do_t_spin = self.retornar_tipo_do_t_spin(canto_f, canto_b)
                
                self.pontos_atual += self.quantos_soft_drops
                self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
                self.esta_em_are = True
        
            if self.fixou_neste_frame:
                    self.segurou_neste_frame = False                 
                    self.verificar_linha(self.mapa)
                    self.pontos_atual += self.calcular_pontos()
                    self.verificar_nivel(self.linhas_limpas)
              
        if self.esta_em_are: 
            if not self.limpou_linha:
                self.are_duracao = 0
            
            if self.temp_do_are > self.are_duracao:
                if self.limpou_linha:
                    self.mover_linhas_do_mapa(self.mapa[::-1])
                self.gerar_novo_shape()
                self.segurar_shape(input_puro=True)
                self.ajustar_desovação()
                self.verificar_rotacao_shape(input_puro=True)
                self.verificar_game_over()
            else:
                self.foi_para_esquerda = False
                self.foi_para_direita = False
                self.temp_do_are += 1
        
        self.tempo_atual_em_segundos = (time.perf_counter() - self.tempo_inicial)
        #print(self.shape_pos_atual)

    #//// //// ////
    
    def desenhar_rect(self, pos_x, pos_y, largura, comprimento, cor, *, movimento_x_esquerda=0, movimento_x_direita=0, movimento_y=0):
        px.rect(pos_x + ((movimento_x_esquerda + movimento_x_direita) * TILE), pos_y + (movimento_y * TILE), largura, comprimento, cor)
    
    def rects_da_esquerda(self, margem, largura, movimento_x_esquerda, movimento_y):
        if self.shape_segurado != None:
            imagem_do_shape_segurado = SHAPES[self.shape_segurado]["imagem_pos"] + 1
        else:
            imagem_do_shape_segurado = 0       
        
        self.desenhar_rect(
            margem, 0, 
            largura, 4, 
            imagem_do_shape_segurado, 
            movimento_x_esquerda=movimento_x_esquerda,
            movimento_y=movimento_y
        )
        
        self.desenhar_rect(
            margem, margem, 
            largura, largura, 
            0, 
            movimento_x_esquerda=movimento_x_esquerda,
            movimento_y=movimento_y
        )
        
        self.desenhar_rect(
            margem, largura + (margem * 2), 
            largura, self.comprimento_do_rect_esquerdo , 
            0, 
            movimento_x_esquerda=movimento_x_esquerda,
            movimento_y=movimento_y
        )
    
    def rects_da_direita(self, margem, largura, movimento_x_direita, movimento_y):
        pos_y = ((TILE * 10) + BOARD_X) + margem
        comprimento_dir = TILE * (self.mostrar_quantos_shapes * 3 + 1)
        
        self.desenhar_rect(
            pos_y, 0, 
            largura, 4,
            SHAPES[self.proximos_shapes[0]]["imagem_pos"] + 1,
            movimento_x_direita=movimento_x_direita,
            movimento_y=movimento_y
        )
        
        self.desenhar_rect(
            pos_y, margem, 
            largura, comprimento_dir,
            0,
            movimento_x_direita=movimento_x_direita,
            movimento_y=movimento_y
        )
        
        self.desenhar_rect(
            pos_y, comprimento_dir + (margem * 2), 
            largura, self.comprimento_do_rect_direita,
            0,
            movimento_x_direita=movimento_x_direita,
            movimento_y=movimento_y
        )
            
    def todos_os_rects(self, movimento_x_esquerda=0, movimento_x_direita=0, movimento_y=0):
        margem = 4
        largura_do_espaco = 80
        largura_final = largura_do_espaco - (margem * 2)
        self.rects_da_esquerda(margem, largura_final, movimento_x_esquerda, movimento_y)
        self.rects_da_direita(margem, largura_final, movimento_x_direita, movimento_y)
    
    #////
    
    def textos_da_esquerda(self, altura_da_fonte, largura, cor, movimento_x_esquerda, movimento_y):
        espacamento = 12
        espacamento_entre_valores = 3
        
        espacamento = altura_da_fonte + espacamento
        espacamento_entre_valores = altura_da_fonte + espacamento_entre_valores
        
        centralizado = lambda string, largura: (largura / 2) - (FONT_1.text_width(string) / 2)
        pos_y = (80 - 1) - altura_da_fonte
        
        tempo_formatado = self.transformar_segundos()
        frases = [
            (f"{tempo_formatado}",),
            ("LINHAS", f"{self.linhas_limpas}"),
            ("LEVEL",  f"{self.nivel_atual}"),
            ("PONTOS", f"{self.pontos_atual}"),
        ]
        
        for index, tupla in enumerate(frases):
            pos_y += espacamento
            px.text((movimento_x_esquerda * TILE) + centralizado(tupla[0], largura), pos_y + (movimento_y * TILE), tupla[0], cor[index], FONT_1)
            if len(tupla) == 2:
                pos_y += espacamento_entre_valores
                px.text((movimento_x_esquerda * TILE) + centralizado(tupla[1], largura), pos_y + (movimento_y * TILE), tupla[1], cor[index], FONT_1)
        
        self.comprimento_do_rect_esquerdo = pos_y - (80 - 1) + espacamento
    
    def textos_da_direita(self, altura_da_fonte, largura, cor, movimento_x_direita, movimento_y):
        espacamento = 5
        espacamento_entre_valores = 4
        
        espacamento = altura_da_fonte + espacamento
        espacamento_entre_valores = altura_da_fonte + espacamento_entre_valores
        
        centralizado = lambda string, largura: (largura / 2) - (FONT_1.text_width(string) / 2)
        
        comprimento_dir, margem = TILE * (self.mostrar_quantos_shapes * 3 + 1), 4
        pos_x = (TILE * 10) + BOARD_X
        pos_y = comprimento_dir + (margem * 2)
        
        combo = ["COMBO", f"{self.combo_atual}"]
        
        if self.combo_atual >= 1:
            cor_final = cor[4]
        else:
            cor_final = 0
        
        pos_y += espacamento
        px.text((movimento_x_direita * TILE) + pos_x + centralizado(combo[0], largura), pos_y + (movimento_y * TILE), combo[0], cor_final, FONT_1)
        pos_y += espacamento_entre_valores
        px.text((movimento_x_direita * TILE) + pos_x + centralizado(combo[1], largura), pos_y + (movimento_y * TILE), combo[1], cor_final, FONT_1)
        
        self.comprimento_do_rect_direita = pos_y - comprimento_dir + espacamento
    
    def todos_os_textos(self, movimento_x_esquerda=0, movimento_x_direita=0, movimento_y=0):
        largura = 80
        # 14 é a altura literal desta fonte
        altura_da_fonte = 14 / 2
        cor = self.cores_aleatorias
        
        self.textos_da_esquerda(altura_da_fonte, largura, cor, movimento_x_esquerda, movimento_y)
        self.textos_da_direita(altura_da_fonte, largura, cor, movimento_x_direita, movimento_y)
 
    #////
    
    def textos_apos_game_over(self, *, pos_y_negativo=0, movimento_y):
        tempo_formatado = self.transformar_segundos()
        frases = [
            (f"Tempo",           f"{tempo_formatado}"),
            (f"Level Final",     f"{self.nivel_atual}"),
            (f"Linhas | Pontos", f"{self.linhas_limpas:^-7}|{self.pontos_atual:^7}"),
            (f"Singles|Doubles", f"{self.quantidade_singles:^-7}|{self.quantidade_doubles:^7}"),
            (f"Triples| Quads ", f"{self.quantidade_triples:^-7}|{self.quantidade_quads:^7}"),
            (f"T-spins",         f"{self.quantidade_t_spins}"),
            (f"Perfect Clears",  f"{self.quantidade_perfect_clears}"),
            (f"Combo Max",       f"{self.combo_maximo}"),
            (f"Streak Max",      f"{self.streak_maximo}"),
        ]

        largura = TILE * LINHAS
        espacamento = 32
        espacamento_entre_valores = 10
        
        centralizado = lambda string, largura: (largura / 2) - (FONT_1.text_width(string) / 2)
        
        altura_total = (len(frases)) * espacamento - (espacamento / 2) + espacamento_entre_valores / 2
        pos_y = ((TILE * LINHAS) / 2 - altura_total / 2) - pos_y_negativo
        
        cores = [1, 2, 3, 4, 5, 6, 7]
        cores_atual = 0
        
        for tupla in frases:
            frase, valor = tupla
            if cores_atual == 7:
                cores_atual = 0
            
            px.text(centralizado(frase, largura), pos_y + (movimento_y * TILE), frase, cores[cores_atual], FONT_1)
            px.text(centralizado(valor, largura), pos_y + (movimento_y * TILE) + espacamento_entre_valores, valor, cores[cores_atual], FONT_1)
            
            pos_y += espacamento
            cores_atual += 1
    
    #////
    
    def desenhar_fundo(self, pos, spritesheet_pos, tamanho, *, movimento_x=0, movimento_y=0):
        px.bltm(
            pos[0] + (movimento_x * TILE), 
            pos[1] + (movimento_y * TILE), 
            0, 
            (TILE * spritesheet_pos[0]), (TILE * spritesheet_pos[1]), 
            (TILE * tamanho[0]), (TILE * tamanho[1])
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x, spritesheet_y, *, movimento_x=0, movimento_y=0, offset=0, diminuir=0):
        px.blt(
            (TILE - diminuir) * (coluna_x + movimento_x) + BOARD_X, 
            (TILE - diminuir) * ((linha_y + movimento_y) + offset), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            (TILE - diminuir), (TILE - diminuir)
        )
        
    #////

    def verificar_pos_y_negativo(self, formato):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    match self.shape_pos_atual[1] + i_linha:
                        case -2: return -2
                        case -1: return -1
        return 0
    
    def calcular_offset(self):
        pos_y_alto = self.verificar_pos_y_negativo(self.pegar_formato())
        if pos_y_alto < 0:
            return abs(pos_y_alto)
        return 0
    
    def calcular_offset_pelo_mapa(self):
        for linha_i in range(2):
            for espaco in self.mapa[linha_i]:
                if espaco != VAZIO:
                    return 2 - linha_i
        return 0
    
    #////
    
    def desenhar_shape_fantasma(self, formato, offset, movimento_x, movimento_y):
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            self.shape_pos_fantasma[0] + i_coluna,
                            self.shape_pos_fantasma[1] + i_linha, 
                            spritesheet_x, 2,
                            movimento_x=movimento_x,
                            movimento_y=movimento_y,
                            offset=offset
                        )
    
    def desenhar_shape_atual(self, formato, pos_x, pos_y, offset, movimento_x, movimento_y):
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            pos_x + i_coluna,
                            pos_y + i_linha, 
                            spritesheet_x, 0,
                            movimento_x=movimento_x,
                            movimento_y=movimento_y, 
                            offset=offset
                        )
    
    def desenhar_shapes_fixados(self, mapa, offset, movimento_x, movimento_y):
        for linha in range(0, ALTURA_DO_JOGO):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != VAZIO:
                    cor = mapa[linha][coluna]
                    spritesheet_x = COR_IMAGEM[cor]
                    
                    self.desenhar_shape(
                        coluna,
                        linha - CORRECAO_ALTURA,
                        spritesheet_x, 0,
                        movimento_x=movimento_x,
                        movimento_y=movimento_y,
                        offset=offset
                    )
    
    #////
    
    def desenhar_shape_proximos(self, proximos_shapes, movimento_x, movimento_y):
        escalonar_tamanho = 0
        ajustar_valor_x = 10.5
        ajustar_valor_y = 1
        
        acrescimo_distancia = (0.05 * 5)
        for proximo_shape in proximos_shapes:
    
            aumentar = -0.5 if proximo_shape == "shape_I" else 0
            
            spritesheet_x = SHAPES[proximo_shape]["imagem_pos"]
            formato = SHAPES[proximo_shape]["formato"]
 
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            ajustar_valor_x + i_coluna + SHAPES[proximo_shape]["centralizado"][0],
                            ajustar_valor_y + i_linha + acrescimo_distancia + aumentar, 
                            spritesheet_x, 0,
                            movimento_x=movimento_x,
                            movimento_y=movimento_y,
                            diminuir=escalonar_tamanho
                        )
            acrescimo_distancia += 3
    
    def desenhar_shape_segurado(self, shape_segurado, movimento_x, movimento_y):
        escalonar_tamanho = 0
        ajustar_valor_x = -3.5
        
        inicio, fim = (0.05 * 5), 4.5
        ajustar_valor_y = inicio + (fim / 2) - 1
        
        aumentar = -0.5 if self.shape_segurado == "shape_I" else 0
        
        spritesheet_x = SHAPES[shape_segurado]["imagem_pos"]
        formato = SHAPES[shape_segurado]["formato"]

        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    self.desenhar_shape(
                        ajustar_valor_x + i_coluna + SHAPES[shape_segurado]["centralizado"][1], 
                        ajustar_valor_y + i_linha + aumentar, 
                        spritesheet_x, 0,
                        movimento_x=movimento_x,
                        movimento_y=movimento_y,
                        diminuir=escalonar_tamanho
                    )
    
    #////
    
    def calcular_valores_das_animacoes(self):
        if self.foi_para_esquerda:
            if self.movimento_x_esquerda > -self.movimento_padrao:
                self.movimento_x_esquerda += -1
                self.movimento_x = self.movimento_x_esquerda
        else:
            if self.movimento_x_esquerda < 0:
                self.movimento_x_esquerda -= -1
                self.movimento_x = self.movimento_x_esquerda    
        #
        if self.foi_para_direita:
            if self.movimento_x_direita < self.movimento_padrao:
                self.movimento_x_direita += 1
                self.movimento_x = self.movimento_x_direita
        else:
            if self.movimento_x_direita > 0:
                self.movimento_x_direita -= 1
                self.movimento_x = self.movimento_x_direita
        #
        if self.acionou_hard_drop:
            if self.movimento_y < self.movimento_padrao:
                self.movimento_y += 1
            else:
                self.acionou_hard_drop = False
        else:
            if self.movimento_y > 0:
                self.movimento_y -= 1
    
    def desenhar_animacao_de_limpar_linha(self, offset, *, movimento_x=0, movimento_y=0):
        def _animacao_de_limpar_linha(start, end, constante, *, constante_na_pos_x=0):
            for localizacao in self.localizacao_das_linhas_limpas:
                for pos_x in range(start, end - constante):
                    self.desenhar_shape(
                        pos_x + constante_na_pos_x,
                        localizacao,
                        spritesheet_x, 0,
                        movimento_x=movimento_x,
                        movimento_y=movimento_y, 
                        offset=offset
                    )
        
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        partes = 7
        tempo_divido = self.are_duracao // partes

        if self.tempo_animacao_limpar_linha > tempo_divido * (self.constante_animacao_limpar_linha + 1):
            self.constante_animacao_limpar_linha += 1
        else:
            self.tempo_animacao_limpar_linha += 1
            
        constante = self.constante_animacao_limpar_linha
        _animacao_de_limpar_linha(0, COLUNAS // 2, constante, constante_na_pos_x=constante)
        _animacao_de_limpar_linha(COLUNAS // 2, COLUNAS, constante)
    
    #
    
    def desenhar_animacao_game_over_cascata(self, offset, movimento_y):
        velocidade = 12
        duracao = 100
        tempo_divido = duracao // velocidade
        
        if (self.tempo_animacao_game_over_cascata > tempo_divido * (self.constante_animacao_game_over_cascata + 1) 
            and self.constante_animacao_game_over_cascata < 20):
            self.constante_animacao_game_over_cascata += 1
        else:
            self.tempo_animacao_game_over_cascata += 1
        
        imagem_do_shape_atual = SHAPES[self.shape_atual]["imagem_pos"]
        constante = ((LINHAS + 1) - offset) - self.constante_animacao_game_over_cascata
        
        for linha in range(LINHAS + 1, constante, -1):
            for coluna in range(COLUNAS):
                spritesheet_x = imagem_do_shape_atual
                self.desenhar_shape(
                    coluna,
                    linha - CORRECAO_ALTURA,
                    spritesheet_x, 2,
                    movimento_y=movimento_y,
                    offset=offset
                )
    
    def calcular_animacao_game_over_slide(self):
        velocidade = 120
        
        if self.acionou_hard_drop:
            self.movimento_exponencial_game_over = TRANSFORMA_EM_DECIMAL(self.movimento_y)            
            self.acionou_hard_drop = False
            
        if self.movimento_exponencial_game_over < LINHAS + 1:
            self.movimento_exponencial_game_over += ((1 + self.movimento_game_over_slide) / velocidade) * 2
            
            while self.movimento_exponencial_game_over > LINHAS + 1:
                self.movimento_exponencial_game_over -= 0.1
                self.movimento_exponencial_game_over = round(self.movimento_exponencial_game_over, 1)
        self.movimento_game_over_slide = self.movimento_exponencial_game_over 
    
    #////
    
    def desenhar_tabuleiro_com_teto(self, offset, movimento_x, movimento_y):
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS), movimento_x=movimento_x, movimento_y=movimento_y)
        if offset > 0:
            self.desenhar_fundo((BOARD_X, 0), (0, LINHAS * 2), (COLUNAS, offset), movimento_x=movimento_x, movimento_y=movimento_y)
    
    def desenhar_shape_segurado_e_proximos(self, movimento_x_esquerda, movimento_x_direita, movimento_y=0):
        self.desenhar_shape_proximos(self.proximos_shapes, movimento_x_direita, movimento_y)
        if self.shape_segurado != None:
            self.desenhar_shape_segurado(self.shape_segurado, movimento_x_esquerda, movimento_y)
    
    #////
    
    def desenhar_tudo_em_jogo(self, movimento_x, movimento_x_esquerda, movimento_x_direita, movimento_y):
        offset = self.calcular_offset()        
            
        self.desenhar_tabuleiro_com_teto(offset, movimento_x, movimento_y)
        
        if not self.esta_em_are:
            self.desenhar_shape_fantasma(self.pegar_formato(), offset, movimento_x, movimento_y)
            self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual[0], self.shape_pos_atual[1], offset, movimento_x, movimento_y)
        
        if self.limpou_linha:
            self.desenhar_animacao_de_limpar_linha(offset, movimento_x=movimento_x, movimento_y=movimento_y)
        
        self.desenhar_shapes_fixados(self.mapa, offset, movimento_x, movimento_y)
        self.desenhar_shape_segurado_e_proximos(movimento_x_esquerda, movimento_x_direita)
        
    #
    
    def desenhar_tudo_no_game_over(self, movimento_x, movimento_x_esquerda, movimento_x_direita):
        offset = self.calcular_offset_pelo_mapa()
        
        self.desenhar_fundo((BOARD_X, (-LINHAS - 1) * TILE), (0, LINHAS), (COLUNAS, LINHAS), movimento_x=0, movimento_y=self.movimento_game_over_slide)
        self.textos_apos_game_over(pos_y_negativo=-(-LINHAS - 1) * TILE, movimento_y=self.movimento_game_over_slide)
        
        self.desenhar_tabuleiro_com_teto(offset, 0, self.movimento_game_over_slide)
        
        #self.desenhar_animacao_game_over_cascata(offset, self.movimento_game_over_slide)
        self.desenhar_shapes_fixados(self.mapa, offset, movimento_x, self.movimento_game_over_slide)
        
        self.desenhar_shape_segurado_e_proximos(movimento_x_esquerda, movimento_x_direita, movimento_y=self.movimento_game_over_slide)
        
    
    #////
    
    def desenhar(self):
        px.cls(0)
    
        if self.estado_do_jogo != "pausado":
            self.calcular_valores_das_animacoes()
        
        movimento_x_esquerda = TRANSFORMA_EM_DECIMAL(self.movimento_x_esquerda)
        movimento_x_direita = TRANSFORMA_EM_DECIMAL(self.movimento_x_direita)
        movimento_x = TRANSFORMA_EM_DECIMAL(self.movimento_x)
        movimento_y = TRANSFORMA_EM_DECIMAL(self.movimento_y)
                
        if self.estado_do_jogo in ("em_jogo", "game_over", "apos_game_over"):
            px.dither(0.9)
            px.rect(0, 0, LINHAS * TILE, LINHAS * TILE, 8)
            px.dither(1)
            self.todos_os_rects(movimento_x_esquerda, movimento_x_direita, self.movimento_game_over_slide)
            self.todos_os_textos(movimento_x_esquerda, movimento_x_direita, self.movimento_game_over_slide)
        
        if self.estado_do_jogo == "em_jogo":
            self.desenhar_tudo_em_jogo(movimento_x, movimento_x_esquerda, movimento_x_direita, movimento_y) 
    
        if self.estado_do_jogo == "game_over":
            self.calcular_animacao_game_over_slide()
            self.desenhar_tudo_no_game_over(movimento_x, movimento_x_esquerda, movimento_x_direita)            
        
        if self.estado_do_jogo == "apos_game_over":
            self.desenhar_fundo((BOARD_X, (-LINHAS - 1) * TILE), (0, LINHAS), (COLUNAS, LINHAS), movimento_x=0, movimento_y=self.movimento_game_over_slide)
            self.textos_apos_game_over(pos_y_negativo=0, movimento_y=0)
        
        self.tempo_inical_test_fim = time.perf_counter()
        #(f"{((self.tempo_inical_test_fim - self.tempo_fps_ms) * 1000):.2f} MS")
        
Jogo()