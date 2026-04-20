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

SHAPES_TITULO = {
    "letra_T": {
        "formato": [[1, 1, 1],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0]],
    },
    "letra_E": {
        "formato": [[1, 1, 1],
                    [1, 0, 0],
                    [1, 1, 1],
                    [1, 0, 0],
                    [1, 1, 1, 1]],
    },
    "letra_R": {
        "formato": [[0, 1, 1, 1],
                    [0, 1, 0, 1],
                    [0, 1, 1, 0],
                    [0, 1, 0, 1],
                    [1, 1, 0, 1]],
    },
    "letra_I": {
        "formato": [[0, 1, 0],
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0]],
    },
    "letra_C": {
        "formato": [[1, 1, 1],
                    [1, 0, 1],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 1, 1]],
    },
    "letra_O": {
        "formato": [[1, 1, 1],
                    [1, 0, 1],
                    [1, 0, 1],
                    [1, 0, 1],
                    [1, 1, 1]],
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

def buscar_tabela_g(nivel):
    if nivel >= 20:
        return TABELA_G[20]
    return TABELA_G[nivel]

CENTRALIZAR = lambda font, string, largura: (largura / 2) - (font.text_width(string) / 2)
TRANSFORMAR_EM_DECIMAL = lambda num: num / 10

CAMINHO = lambda caminho: os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho)
FONT_1 = px.Font(CAMINHO("assets/PublicPixel.ttf"), 8)
FONT_2 = px.Font(CAMINHO("assets/PF Pixelscript Pro Regular.ttf"), 16)
FONT_3 = px.Font(CAMINHO("assets/PublicPixel.ttf"), 16)

COLUNAS = 10
LINHAS = 20
TILE = 16

CORRECAO_ALTURA = 3
ALTURA_DO_JOGO = 20 + CORRECAO_ALTURA

BOARD_X = 80
GAME_OFFSET_X = 320
VAZIO = "_"

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico: The Smoothness", fps=60, display_scale=2, quit_key=False)
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
            
            "ACIONAR": [px.KEY_RETURN, px.GAMEPAD1_BUTTON_START],
            "VOLTAR": [px.KEY_BACKSPACE, px.GAMEPAD1_BUTTON_GUIDE, px.KEY_A, px.KEY_LEFT, px.GAMEPAD1_BUTTON_DPAD_LEFT],
            #
            "PARA_CIMA": [px.KEY_UP, px.KEY_W, px.GAMEPAD1_BUTTON_DPAD_UP],
            "PARA_BAIXO": [px.KEY_DOWN, px.KEY_S, px.GAMEPAD1_BUTTON_DPAD_DOWN],
        }   
        
        self.iniciar_jogo()
        
        px.run(self.atualizar, self.desenhar)

   #//// //// ////
    
    def iniciar_jogo(self):
        self.estado_atual_do_jogo = "em_menu"
        self.modo_do_jogo = None
        self.variaveis_menu()

    def variaveis_menu(self):
        # estados
        self.pilha_menu = [["entrada", 0]]
        self.menu_atual_indice = 0
        self.opcao_atual = 0
        self.opcao_anterior = 0
        self.navegar_menu()
        
        # cores
        self.cores_aleatorias_titulo = list(range(0, 7))
        random.shuffle(self.cores_aleatorias_titulo)
        self.cor_aleatoria_titulo = random.choice(self.cores_aleatorias_titulo)
        
        # animacao
        self.offset_menu = 0
        self.offset_menu_para_jogo = 0
    
    #////
    
    def navegar_horizontalmente_menu(self, clique):
        if clique != 0:
            self.menu_atual_indice += clique
            
            if self.menu_atual_indice < 0:
                self.menu_atual_indice = 0
            
            elif clique == -1:
                self.opcao_atual = self.pilha_menu[-1][1]
                self.pilha_menu.pop()    
        
            elif self.menu_atual_indice == 1:
                self.pilha_menu.append(["inicio", self.opcao_atual])
                self.opcao_anterior = self.opcao_atual
                self.opcao_atual = 0
            
            elif self.menu_atual_indice == 2:
                match self.opcao_atual:
                    case 0: self.pilha_menu.append(["jogar", self.opcao_atual])
                    case 1: self.pilha_menu.append(["configuracao", self.opcao_atual])
                    case 2: self.pilha_menu.append(["historico", self.opcao_atual])
                    case 3: self.pilha_menu.append(["sobre", self.opcao_atual])
                    case 4: self.pilha_menu.append(["sair", self.opcao_atual])
                self.opcao_atual = 0
            
            elif self.menu_atual_indice == 3:
                
                if self.menu_ativo == "jogar":
                    match self.opcao_atual:
                        case 0:
                            self.estado_atual_do_jogo = "antes_do_jogo"
                            self.modo_do_jogo = "marathon"
                            self.iniciar_partida()
                        case 1:
                            self.estado_atual_do_jogo = "antes_do_jogo"
                            self.modo_do_jogo = "40_lines"
                            self.iniciar_partida()
                        case 2:
                            self.estado_atual_do_jogo = "antes_do_jogo"
                            self.modo_do_jogo = "ultra"
                            self.iniciar_partida()
                        case 3:
                            self.estado_atual_do_jogo = "antes_do_jogo"
                            self.modo_do_jogo = "infinito"
                            self.iniciar_partida()
                
                elif self.menu_ativo == "sobre" and clique == 1:
                    self.menu_atual_indice -= clique
                
                elif self.menu_ativo == "configuracao" and clique == 1:
                    pass
                
                elif self.menu_ativo == "historico" and clique == 1:
                    pass
                
                elif self.menu_ativo == "sair":
                    px.quit()
                
    def navegar_verticalmente_menu(self, deslize):
        self.menu_ativo = self.pilha_menu[-1][0]
        quantidade_de_opcoes = len(self.todos_os_menus[self.menu_ativo])
        
        if deslize != 0:
            self.opcao_atual += deslize
            if self.opcao_atual % quantidade_de_opcoes == 0:
                self.opcao_atual = 0
            if self.opcao_atual < 0:
                self.opcao_atual = quantidade_de_opcoes - 1
            
            if self.menu_atual_indice == 1:
                self.opcao_anterior = self.opcao_atual
    
    def navegar_menu(self, *, clique=0, deslize=0):
        self.todos_os_menus = {
            "entrada": [False],
            "inicio": [False] * 5,
            #
            "jogar": [False] * 4,
            "configuracao": [False] * 4,
            "historico": [False] * 4,
            "sobre": [True] * 4,
            "sair": [True] * 2
            #
        }   
        
        self.navegar_horizontalmente_menu(clique)
        self.navegar_verticalmente_menu(deslize)
            
        self.todos_os_menus[self.menu_ativo][self.opcao_atual] = True
        self.todas_as_opcoes = self.todos_os_menus[self.menu_ativo]   
   
    #////
    
    def iniciar_contagem_do_tempo(self):
        self.tempo_inicial = time.perf_counter()
        self.tempo_atual_em_segundos = 0
    
    def iniciar_partida(self):
        self.tempo_inicial = 0
        self.tempo_atual_em_segundos = 0
        
        self.mapa = [[VAZIO] * COLUNAS for _ in range(ALTURA_DO_JOGO)]
        
        self.linhas_limpas = 0
        self.nivel_inicial = 1
        self.nivel_atual = self.nivel_inicial
        
        self.pontos_atual = 0
        self.combo_atual = -1
        self.atual_back_to_back = 0
        
        # mostrar_quantos_shapes = 3
        self.mostrar_quantos_shapes = 6
        self.proximos_shapes = []
        self.bag_7 = []
        self.sistema_bag_7()
        
        self.shape_atual = ""
        self.shape_segurado = None
        self.gerar_novo_shape()
       
        # estados
        #self.estado_atual_do_jogo = "em_jogo"
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
        self.quantidade_holds = 0
        self.quantidade_pausadas = 0
        self.sequencia_dos_eventos = []
        
        # cores
        self.cores_aleatorias_texto = list(range(1, 8))
        random.shuffle(self.cores_aleatorias_texto)
        
        # tamanho dos rects
        self.distancia_rect_direita = 2.5
        self.offset_rect_direita = 0.5
        
        self.comprimento_do_rect_esquerdo_1 = 0
        self.comprimento_do_rect_esquerdo_2 = 0
        self.comprimento_do_rect_direito = 0
        
        # CONFIGURAÇÃO DO USUÁRIO
        
        # movimento_padrao = 6
        self.movimento_padrao = 6
        self.variaveis_movimentos()
        self.variaveis_velocidade_movimentacao()
    
    def variaveis_movimentos(self):    
        self.mov_x_esquerda = 0
        self.mov_x_direita = 0
        self.mov_x = 0
        self.mov_y_hard_drop = 0
        
        self.mov_y_slide = 0
        self.movimento_exponencial_game_over = 0
        
        self.movimento_offset_teto = 0
        
        self.variaveis_animacao_hard_drop = []
    
    def variaveis_velocidade_movimentacao(self):
        # das = 10
        self.das = 10
        # arr = 2
        self.arr = 2
        # arr_soft_drop = 2
        self.arr_soft_drop = 2
    
    #
    
    def desovar_shape(self, formato):       
       return [4, 0] if formato == "shape_O" else [3, 0]

    def ajustar_desovação(self):
        if (self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa) or 
            self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1)):
            self.shape_pos_atual[1] -= 1
            self.shape_pos_fantasma = self.shape_pos_atual[:]
   
    def gerar_novo_shape(self):
        self.shape_atual = self.proximos_shapes.pop(0)
        self.reiniciar_shape()
        
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    #
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.desovar_shape(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_pos_fantasma = self.shape_pos_atual[:]
        self.ajustar_desovação()
        self.recalcular_pos_fantasma()
        
        # rotacao e movimentacao
        self.ultimo_movimento_lateral = None        
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
        self.quantos_soft_drops = 0
        
        # movimentar os desenhos
        self.foi_para_esquerda = False
        self.foi_para_direita = False
        self.ultima_acao_foi_rotacao_animacao_lateral = False
        
        self.localizacao_das_linhas_limpas = []
        self.tempo_animacao_limpar_linha = 0
        self.constante_animacao_limpar_linha = 0
        
        # CONFIGURAÇÃO DO JOGO
        self.variaveis_are()
    
    def variaveis_are(self):
        # are_duracao = 20
        self.are_duracao = 20
        self.tempo_do_are = 0
        self.esta_em_are = False
        self.limpou_linha = False # Se False, sem ARE
    
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
            shapes = ["I", "O", "T", "L", "J", "S", "Z"]
            self.bag_7 = [f"shape_{x}" for x in shapes]
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
                    
                    if mapa[n_lin][n_col] != VAZIO: # verificar se contem uma peça fixada
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
                        self.verificar_game_over_teto()
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
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=dx, dy=dy):
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
            
            case _: raise("Erro ao rotacionar")
            
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
    
    def condicoes_do_t_spin(self, mapa, posicao):
        rotacao_preset = T_SPIN_CANTO[self.estado_rotacao]
        pos_do_centro = posicao[0] + 1, posicao[1] + 1 
        canto_f = 0
        canto_b = 0

        for diagonal, posicoes in rotacao_preset.items():
            for tupla in posicoes:
                x, y = tupla
                
                mx = pos_do_centro[0] + x
                if mx < 0 or mx >= COLUNAS:
                    if diagonal == "F": 
                            canto_f += 1
                            continue
                    if diagonal == "B": 
                            canto_b += 1
                            continue
                        
                my = pos_do_centro[1] + y + CORRECAO_ALTURA
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

    def verificar_t_spin(self, posicao):
        if self.ultima_acao_foi_rotacao and self.shape_atual == "shape_T":
            canto_f, canto_b = self.condicoes_do_t_spin(self.mapa, posicao)
            self.tipo_do_t_spin = self.retornar_tipo_do_t_spin(canto_f, canto_b)
    
    #////
    
    def anexar_eventos(self, ordem, tipo, linhas_limpas):
        duracao = 180
        cor = (SHAPES[self.shape_atual]["imagem_pos"] + 1)
        informacoes = [tipo, linhas_limpas, duracao, cor]
        self.sequencia_dos_eventos.insert(ordem, informacoes)
    
    def incrementar_os_eventos(self, linhas_limpas=0, *, perfect_clear=False, tipo_do_t_spin=None):
        if perfect_clear:
            self.anexar_eventos(0, "perfect_clear", linhas_limpas)
        
        elif tipo_do_t_spin != None:
            if linhas_limpas != 0:
                self.anexar_eventos(1, self.tipo_do_t_spin, linhas_limpas)
            else:
                self.anexar_eventos(2, self.tipo_do_t_spin, linhas_limpas)
        
        elif linhas_limpas > 0:
            self.anexar_eventos(3, f"{linhas_limpas}", linhas_limpas)
    
    def incrementar_os_status(self, *, perfect_clear=False, tipo_do_t_spin=None, linhas_limpas=0, combo=-1, back_to_back=0):
        if perfect_clear:
            self.quantidade_perfect_clears += 1
        
        if tipo_do_t_spin != None:
            self.quantidade_t_spins += 1
        
        if linhas_limpas > 0:
            match linhas_limpas:
                case 1: self.quantidade_singles += 1
                case 2: self.quantidade_doubles += 1
                case 3: self.quantidade_triples += 1
                case 4: self.quantidade_quads += 1
        
        if combo >= 1:
            self.combo_maximo = max(self.combo_maximo, combo)
        if back_to_back > 0:
            self.streak_maximo = max(self.streak_maximo, back_to_back)
    
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
            if self.tipo_do_t_spin != None:
                self.incrementar_os_status(tipo_do_t_spin=self.tipo_do_t_spin)
                self.incrementar_os_eventos(linhas_limpas, tipo_do_t_spin=self.tipo_do_t_spin)
                if self.tipo_do_t_spin == "t_spin": return 400 * self.nivel_atual
                if self.tipo_do_t_spin == "mini_t_spin": return 100 * self.nivel_atual
            return 0

        self.combo_atual += 1  
        pontuacao += self.verificar_combo(self.combo_atual)
        
        if linhas_limpas == 4 or self.tipo_do_t_spin != None: self.atual_back_to_back += 1
        elif linhas_limpas in (1, 2, 3): self.atual_back_to_back = 0
        aumento_do_back_to_back = 1.5 if self.atual_back_to_back >= 2 else 1
        
        if self.verificar_perfect_clear(self.mapa[::-1]):
            pontuacao += TABELA_PONTUACAO("perfect_clear", linhas_limpas, self.nivel_atual)
            self.incrementar_os_status(perfect_clear=True)
            self.incrementar_os_eventos(linhas_limpas, perfect_clear=True)
        else:
            self.incrementar_os_eventos(linhas_limpas, tipo_do_t_spin=self.tipo_do_t_spin)
        
        self.incrementar_os_status(
            tipo_do_t_spin=self.tipo_do_t_spin, 
            linhas_limpas=linhas_limpas,
            combo=self.combo_atual, 
            back_to_back=self.atual_back_to_back, 
        )
      
        if self.tipo_do_t_spin == None:
            pontuacao += TABELA_PONTUACAO("normal", linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        else:
            pontuacao += TABELA_PONTUACAO(self.tipo_do_t_spin, linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        
        return int(pontuacao)
  
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
                if linha_i + 1 >= len(mapa_temp) - CORRECAO_ALTURA:
                    break
                elif linha_e.count(VAZIO) == COLUNAS and mapa_temp[linha_i + 1].count(VAZIO) != COLUNAS: 
                    mapa_temp[linha_i + 1], mapa_temp[linha_i] = mapa_temp[linha_i], mapa_temp[linha_i + 1]
                    continuar_loop = True          
        self.mapa = mapa_temp[::-1]

    def verificar_game_over_colisao(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa):
            self.estado_atual_do_jogo = "game_over"
            self.shape_pos_atual = [0, 0]
    
    def verificar_game_over_teto(self):
        for coluna in range(COLUNAS):
            for linha in range(CORRECAO_ALTURA):
                if self.mapa[linha][coluna] != VAZIO:
                    self.estado_atual_do_jogo = "game_over"
                    self.shape_pos_atual = [0, 0]
                    return True
        return False
        
    def aumentar_lock_reset(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            if self.lock_movimentos != 15:
                self.lock_movimentos += 1
                self.lock_tempo = 0
    
    def verificar_movimento_lateral(self):
        esquerda_puro = self.pegar_input("ESQUERDA", input_puro=True) and not self.pegar_input("DIREITA", input_puro=True)
        direita_puro = self.pegar_input("DIREITA", input_puro=True) and not self.pegar_input("ESQUERDA", input_puro=True)
        
        dx = 2 if self.shape_atual != "shape_I" else 3
        
        if self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, 1):
            self.foi_para_direita = True
            self.ultima_acao_foi_rotacao_animacao_lateral = False
        elif self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, -1):
            self.foi_para_esquerda = True
            self.ultima_acao_foi_rotacao_animacao_lateral = False
        
        elif self.ultima_acao_foi_rotacao_animacao_lateral and direita_puro and self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, dx):
            self.foi_para_direita = True
        elif self.ultima_acao_foi_rotacao_animacao_lateral and esquerda_puro and self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, -dx):
            self.foi_para_esquerda = True  
        
        else:
            self.foi_para_esquerda, self.foi_para_direita = False, False
            self.ultima_acao_foi_rotacao_animacao_lateral = False   
    
    #////
    
    def segurar_shape(self, *, input_puro=False):
        if self.pegar_input("SEGURAR", input_puro=input_puro) and not self.segurou_neste_frame:
            self.segurou_neste_frame = True
            self.quantidade_holds += 1
            
            if self.shape_segurado == None:
                self.shape_segurado = self.shape_atual
                self.gerar_novo_shape()
            else:
                self.shape_atual, self.shape_segurado = self.shape_segurado, self.shape_atual
                self.reiniciar_shape()    

    def mover_lados_shape(self):
        hold = self.das        
        repeticao = self.arr
        
        direita = self.pegar_input("DIREITA", repeticao, hold)
        esquerda = self.pegar_input("ESQUERDA", repeticao, hold)
        
        if self.pegar_input("DIREITA"):
            self.ultimo_movimento_lateral = "direita"
        elif self.pegar_input("ESQUERDA"):
            self.ultimo_movimento_lateral = "esquerda"
        elif self.ultimo_movimento_lateral is None:
            if self.pegar_input("DIREITA", input_puro=True):
                self.ultimo_movimento_lateral = "direita"
            elif self.pegar_input("ESQUERDA", input_puro=True):
                self.ultimo_movimento_lateral = "esquerda"
        
        if self.ultimo_movimento_lateral == "esquerda" and esquerda:
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=-1):
                self.shape_pos_atual[0] -= 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
        
        elif self.ultimo_movimento_lateral == "direita" and direita:
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=1):
                self.shape_pos_atual[0] += 1
                self.shape_pos_fantasma = self.shape_pos_atual[:]
                self.aumentar_lock_reset()
                self.ultima_acao_foi_rotacao = False
    
    def verificar_rotacao_shape(self, *, input_puro=False):
        if self.pegar_input("ROTACAO_ESQUERDA", input_puro=input_puro):
            self.rotacionar_shape("KEY_Q")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao, self.ultima_acao_foi_rotacao_animacao_lateral = True, True

        if self.pegar_input("ROTACAO_DIREITA", input_puro=input_puro):
            self.rotacionar_shape("KEY_E")
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao, self.ultima_acao_foi_rotacao_animacao_lateral = True, True
    
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
            self.verificar_t_spin(self.shape_pos_fantasma)
            self.fixar(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
            self.esta_em_are = True
            self.acionou_hard_drop = True
            
            variaveis = [self.pegar_formato(), self.shape_pos_fantasma]
            self.variaveis_animacao_hard_drop.append([variaveis, 20])
    
            self.pontos_atual += self.quantos_soft_drops
            self.pontos_atual += (self.shape_pos_fantasma[1] - self.shape_pos_atual[1]) * 2
    
    def teclas_especiais(self):
        if self.pegar_input("REINICIAR"):
            self.estado_atual_do_jogo = "em_menu"
            self.iniciar_jogo()
            
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
    
    def teclas_navegacao(self):
        if self.pegar_input("ACIONAR"):
            self.navegar_menu(clique=+1)
        
        if self.pegar_input("VOLTAR"):
            self.navegar_menu(clique=-1)

        if self.pegar_input("PARA_CIMA"):
            self.navegar_menu(deslize=-1)
        
        if self.pegar_input("PARA_BAIXO"):
            self.navegar_menu(deslize=+1)
    
    def verificar_estado_do_modo(self):
        
        if self.modo_do_jogo == "marathon":
            if self.nivel_atual >= 15:
                self.estado_atual_do_jogo = "game_over"
        
        elif self.modo_do_jogo == "40_lines":
            if self.linhas_limpas >= 40:
                self.estado_atual_do_jogo = "game_over"
                
        elif self.modo_do_jogo == "ultra":
            if self.tempo_atual_em_segundos >= (3 * 60):
                self.estado_atual_do_jogo = "game_over"
        
        elif self.modo_do_jogo == "infinito":
            pass
            # fi... apenas relaxe e jogue infinitamente!!!
    
    #////

    def atualizar(self):
        #self.tempo_fps_ms = time.perf_counter()
        
        if self.estado_atual_do_jogo == "em_menu":
            self.teclas_navegacao()
            return
        
        if self.estado_atual_do_jogo == "pausado":
            self.teclas_especiais()
            return
        
        self.sistema_bag_7()
        
        if self.estado_atual_do_jogo == "antes_do_jogo":
            if self.offset_menu_para_jogo >= GAME_OFFSET_X:
                self.estado_atual_do_jogo = "em_jogo"
                self.iniciar_contagem_do_tempo()
                self.offset_menu_para_jogo = 0
            return
        
        if self.estado_atual_do_jogo == "game_over":
            self.teclas_especiais()
            if self.mov_y_slide >= LINHAS + 1:
                self.estado_atual_do_jogo = "apos_game_over"
            return

        if self.estado_atual_do_jogo == "apos_game_over":
            self.teclas_especiais()
            return  
                
        self.fixou_neste_frame = False
        if not self.esta_em_are:
            self.input_tecla()
            self.queda_automatica()
            
            if self.lock_tempo >= 30 or self.lock_movimentos == 15:
                self.verificar_t_spin(self.shape_pos_atual)
                self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
                self.esta_em_are = True
                self.pontos_atual += self.quantos_soft_drops
        
            if self.fixou_neste_frame:
                    self.segurou_neste_frame = False                 
                    self.verificar_linha(self.mapa)
                    self.pontos_atual += self.calcular_pontos()
                    self.verificar_nivel(self.linhas_limpas)
              
        if self.esta_em_are: 
            if not self.limpou_linha:
                self.are_duracao = 0
            
            if self.tempo_do_are > self.are_duracao:
                if self.limpou_linha:
                    self.mover_linhas_do_mapa(self.mapa[::-1])
                self.verificar_estado_do_modo()
                self.gerar_novo_shape()
                self.segurar_shape(input_puro=True)
                self.verificar_rotacao_shape(input_puro=True)
                self.verificar_game_over_colisao()
            else:
                self.foi_para_esquerda, self.foi_para_direita = False, False
                self.tempo_do_are += 1
        
        self.tempo_atual_em_segundos = (time.perf_counter() - self.tempo_inicial)
        #print(self.shape_pos_atual)

    #//// //// ////
    
    def desenhar_letra(self, coluna_x, linha_y, spritesheet_x, spritesheet_y):
        px.blt(
            (coluna_x), (linha_y), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            TILE, TILE
        )
    
    def desenhar_titulo_menu(self):
        pos_x, pos_y = 2, 15
        largura = TILE * LINHAS
        spritesheet_x = self.cores_aleatorias_titulo
        offset = self.offset_menu_para_jogo
        
        ordem = ["letra_T", "letra_E", "letra_T", "letra_R", "letra_I", "letra_C", "letra_O"]
        for index, letra in enumerate(ordem):
            formato = SHAPES_TITULO[letra]["formato"]
            
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                            self.desenhar_letra(
                                pos_x + (i_coluna * TILE) - offset,
                                pos_y + (i_linha * TILE), 
                                spritesheet_x[index], 0,
                            )
            if index != (len(ordem) - 1) and ordem[index + 1] == "letra_I":
                pos_x += 34 + 16
            elif index != (len(ordem) - 1) and ordem[index + 1] == "letra_R":
                pos_x += 34
            elif letra == "letra_I":
                pos_x += 34
            else:
                pos_x += 50
                
        texto = "The Smoothness"
        px.text(CENTRALIZAR(FONT_2, texto, largura) - offset, 115, texto, self.cor_aleatoria_titulo + 9, FONT_2)
    
    #
    
    def desenhar_texto_menu(self, pos_x, pos_y, largura, ativo, frase):
        offset = self.offset_menu_para_jogo
        
        def _desenhar_texto(*, dx=0, dy=0, cor=0):
           px.text(
                pos_x + dx + CENTRALIZAR(FONT_3, frase, largura) - offset, 
                pos_y + dy, 
                frase, cor, FONT_3
            )
        
        if ativo != True:
            px.dither(0.3)
            _desenhar_texto(cor=self.cor_aleatoria_titulo + 9)
            px.dither(1)    
        else:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 or dy != 0:
                        _desenhar_texto(dx=dx, dy=dy, cor=8)
            _desenhar_texto(cor=self.cor_aleatoria_titulo + 1)
    
    def desenhar_os_botoes(self, offset):
        maximo = LINHAS * TILE # 320
        altura_da_fonte = 18
        centro_y = (maximo/2 + maximo) / 2
        
        #
        
        espacamento = 0
        todas_as_opcoes = self.todos_os_menus["entrada"] 
        
        altura_total =  (len(todas_as_opcoes) - 1) * espacamento + altura_da_fonte
        pos_y = centro_y - altura_total / 2
       
        frase = "Pressione [ENTER]"
        self.desenhar_texto_menu(
            -offset, pos_y, 
            (TILE * LINHAS), True, frase)
        
        #
        
        espacamento = 28
        todas_as_opcoes = self.todos_os_menus["inicio"]  
        
        altura_total = (len(todas_as_opcoes) - 1) * espacamento + altura_da_fonte
        pos_y = centro_y - altura_total / 2

        frase = ["Modos", "Ajustes", "Histórico", "Sobre", "Sair"] 
        for frase, ativo in zip(frase, todas_as_opcoes):
            self.desenhar_texto_menu(
                maximo - offset, pos_y, 
                (TILE * LINHAS), ativo, frase)
            pos_y += espacamento

        #
        
        if self.menu_atual_indice >= 1:
            frases = {
                "jogar": (["MARATHON", "40 LINES", "ULTRA", "INFINITO"], 30),
                "configuracao": (["XX", "FDS", "FDSF", "FSDFS"], 30),
                "historico": (["1", "2"], 30),
                "sobre": (["Feito pelo Cac", "Feito com Pyxel", "Feito com carinho", ":D"], 25),
                "sair": (["Pressione [ENTER]", "para confirmar"], 25),
            }
            
            proximo_menu = list(frases.keys())[self.opcao_anterior]
            
            frases_atuais = frases[proximo_menu][0]
            espacamento = frases[proximo_menu][1]
            todas_as_opcoes = self.todos_os_menus[proximo_menu]
            
            altura_total =  (len(todas_as_opcoes) - 1) * espacamento + altura_da_fonte
            pos_y = centro_y - altura_total / 2

            for frase, ativo in zip(frases_atuais, todas_as_opcoes):
                self.desenhar_texto_menu(
                    (maximo * 2) - offset, pos_y, 
                    (TILE * LINHAS), ativo, frase)
                pos_y += espacamento
        
    #////
    
    def rects_da_esquerda(self, margem, largura, mov_x_esquerda, mov_y, offset):
        if self.shape_segurado != None:
            imagem_do_shape_segurado = SHAPES[self.shape_segurado]["imagem_pos"] + 1
        else:
            imagem_do_shape_segurado = 0
        
        self.desenhar_rect(
            margem + offset, 0, 
            largura, 4, 
            imagem_do_shape_segurado, 
            mov_x_esquerda=mov_x_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset, margem, 
            largura, largura, 
            0, 
            mov_x_esquerda=mov_x_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset, largura + (margem * 2), 
            largura, self.comprimento_do_rect_esquerdo_1, 
            0, 
            mov_x_esquerda=mov_x_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset, largura + self.comprimento_do_rect_esquerdo_1 + (margem * 3), 
            largura, self.comprimento_do_rect_esquerdo_2, 
            0, 
            mov_x_esquerda=mov_x_esquerda,
            mov_y=mov_y
        )
    
    def rects_da_direita(self, margem, largura, mov_x_direita, mov_y, offset):
        pos_x = ((TILE * 10) + BOARD_X) + margem
        comprimento_dir = TILE * (self.mostrar_quantos_shapes * self.distancia_rect_direita + self.offset_rect_direita)
        
        self.desenhar_rect(
            pos_x + offset, 0, 
            largura, 4,
            SHAPES[self.proximos_shapes[0]]["imagem_pos"] + 1,
            mov_x_direita=mov_x_direita,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            pos_x + offset, margem, 
            largura, comprimento_dir,
            0,
            mov_x_direita=mov_x_direita,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            pos_x + offset, comprimento_dir + (margem * 2), 
            largura, self.comprimento_do_rect_direito,
            0,
            mov_x_direita=mov_x_direita,
            mov_y=mov_y
        )
        
            
    def todos_os_rects(self, mov_x_esquerda, mov_x_direita, mov_y, *, offset_soma=0):
        margem = 4
        largura_do_espaco = 80
        largura_final = largura_do_espaco - (margem * 2)
        offset = offset_soma - self.offset_menu_para_jogo
        self.rects_da_esquerda(margem, largura_final, mov_x_esquerda, mov_y, offset)
        self.rects_da_direita(margem, largura_final, mov_x_direita, mov_y, offset)
    
    def desenhar_rect(self, pos_x, pos_y, largura, comprimento, cor, *, mov_x=0, mov_x_esquerda=0, mov_x_direita=0, mov_y=0):
        px.rect(
            pos_x + ((mov_x_esquerda + mov_x_direita + mov_x) * TILE), pos_y + (mov_y * TILE), 
            largura, comprimento, 
            cor
        )
    
    #////
    
    def textos_da_esquerda_1(self, altura_da_fonte, largura, cor, mov_x_esquerda, mov_y, offset):
        espaco = 8
        espacamento = altura_da_fonte + espaco
        espacamento_entre_valores = altura_da_fonte + 3
        
        offset_fonte = 1
        pos_y = 80 - offset_fonte
        
        tempo_formatado = self.transformar_segundos()
        frases_esqueda_1 = [
            (f"{tempo_formatado}", None),
            ("LINHAS", f"{self.linhas_limpas}"),
            ("LEVEL",  f"{self.nivel_atual}"),
            ("PONTOS", f"{self.pontos_atual}"),
        ]
        
        pos_y += espaco
        for index, (frase, valor) in enumerate(frases_esqueda_1):
            px.text((mov_x_esquerda * TILE) + CENTRALIZAR(FONT_1, frase, largura) + offset, pos_y + (mov_y * TILE), frase, cor[index], FONT_1)
            
            if valor != None:
                pos_y += espacamento_entre_valores
                px.text((mov_x_esquerda * TILE) + CENTRALIZAR(FONT_1, valor, largura) + offset, pos_y + (mov_y * TILE), valor, cor[index], FONT_1)
            pos_y += espacamento
        self.comprimento_do_rect_esquerdo_1 = pos_y - 80 + offset_fonte
    
    def textos_da_esquerda_2(self, altura_da_fonte, largura, cor, mov_x_esquerda, mov_y, offset):
        espaco = 8
        espacamento = altura_da_fonte + espaco
        espacamento_entre_valores = altura_da_fonte + 3

        margem =  4
        offset_fonte = 1
        pos_y = (80 - offset_fonte) + self.comprimento_do_rect_esquerdo_1 + margem
        
        cor_combo = cor[4] if self.combo_atual >= 1 else 0
        cor_streak = cor[5] if self.atual_back_to_back >= 1 else 0
        
        frases_esqueda_2 = [
            ("COMBO", f"{self.combo_atual}x"),
            ("STREAK", f"{self.atual_back_to_back}x")
        ]
        pos_y += espaco
        for (frase, valor) in frases_esqueda_2:
            cor_final = cor_combo if frase == "COMBO" else cor_streak        
            
            px.text((mov_x_esquerda * TILE) + CENTRALIZAR(FONT_1, frase, largura) + offset, pos_y + (mov_y * TILE), frase, cor_final, FONT_1)
            pos_y += espacamento_entre_valores
            px.text((mov_x_esquerda * TILE) + CENTRALIZAR(FONT_1, valor, largura) + offset, pos_y + (mov_y * TILE), valor, cor_final, FONT_1)
            pos_y += espacamento
        
        self.comprimento_do_rect_esquerdo_2 = pos_y - ((80 - offset_fonte) + self.comprimento_do_rect_esquerdo_1 + margem)
    
    def textos_da_direita_1(self, altura_da_fonte, largura, mov_x_direita, mov_y, offset):
        espaco = 8
        espacamento = altura_da_fonte + espaco
        
        pos_x = ((TILE * 10) + BOARD_X)
        
        comprimento_dir = TILE * (self.mostrar_quantos_shapes * self.distancia_rect_direita + self.offset_rect_direita)
        comprimento_dir += 0
        pos_y = comprimento_dir
        
        frase = f"{self.modo_do_jogo.upper().replace("_", " ")}"
        cor = self.cor_aleatoria_titulo + 1
        
        pos_y += espacamento
        px.text((mov_x_direita * TILE) + pos_x + CENTRALIZAR(FONT_1, frase, largura) + offset, pos_y + (mov_y * TILE), frase, cor, FONT_1)
        
        self.comprimento_do_rect_direito = pos_y - comprimento_dir + (espacamento / 2)
    
    def todos_os_textos(self, mov_x_esquerda, mov_x_direita, mov_y, *, offset_soma=0):
        largura = 80
        altura_da_fonte = 14 / 2 # 14 é a altura literal desta fonte
        cor = self.cores_aleatorias_texto
        offset = offset_soma - self.offset_menu_para_jogo
        self.textos_da_esquerda_1(altura_da_fonte, largura, cor, mov_x_esquerda, mov_y, offset)
        self.textos_da_esquerda_2(altura_da_fonte, largura, cor, mov_x_esquerda, mov_y, offset)
        self.textos_da_direita_1(altura_da_fonte, largura, mov_x_direita, mov_y, offset)
    
    #
    
    #
    
    def textos_estatisticas(self, *, mov_y, pos_y_negativo):
        tempo_formatado = self.transformar_segundos()
        frases_status = [
            ("Tempo:",           f"{tempo_formatado}", 6),
            ("Start Level:",     f"{self.nivel_inicial}", 1),
            ("Final Level:",     f"{self.nivel_atual}", 1),
            ("Linhas:",          f"{self.linhas_limpas}", 2),
            ("Pontos:",          f"{self.pontos_atual}", 2),
            ("Singles:",         f"{self.quantidade_singles}", 3),
            ("Doubles:",         f"{self.quantidade_doubles}", 3),
            ("Triples:",         f"{self.quantidade_triples}", 3),
            ("Tetris:",          f"{self.quantidade_quads}", 3),
            ("T-Spins:",         f"{self.quantidade_t_spins}", 4),
            ("Perfect Clears:",  f"{self.quantidade_perfect_clears}", 4),
            ("Max Combo:",       f"{self.combo_maximo}", 5),
            ("Max Streak:",      f"{self.streak_maximo}", 5),
            ("Times Held:",      f"{self.quantidade_holds}", 6),
            ("Times Pause:",     f"{self.quantidade_pausadas}", 6),  
        ]

        cor = self.cores_aleatorias_texto
        
        espacamento = 20
        espacamento_entre_valores = 11

        altura_total = (len(frases_status)) * espacamento - (espacamento / 2)
        pos_y = ((TILE * LINHAS) / 2 - altura_total / 2) - pos_y_negativo
        
        for tupla in frases_status:
            frase, valor, cor_i = tupla
            px.text((BOARD_X + espacamento_entre_valores), pos_y + (mov_y * TILE), frase, cor[cor_i], FONT_1)
            px.text((BOARD_X + espacamento_entre_valores) + FONT_1.text_width(frase) + 2, pos_y + (mov_y * TILE), valor, cor[cor_i], FONT_1)
            pos_y += espacamento
    
    def textos_dos_popups(self, mov_x):
        largura = TILE * LINHAS
        altura_da_fonte = 14
        
        for evento in self.sequencia_dos_eventos[:]:
            tipo, linhas_limpas, duracao, cor = evento  
            
            match linhas_limpas:
                case 1: frase_linhas = " SINGLE"
                case 2: frase_linhas = " DOUBLE"
                case 3: frase_linhas = " TRIPLE"
                case 4: frase_linhas = " QUAD"
                case _: frase_linhas = ""
            
            match tipo: 
                case "perfect_clear": frase = "PERFECT CLEAR!"
                case "t_spin": frase =       f"T-SPIN{frase_linhas}"
                case "mini_t_spin": frase =  f"MINI T-SPIN{frase_linhas}"
                
                case "4": frase = "TETRIS!"
                case "3": frase = "TRIPLE"
                case "2": frase = "DOUBLE"
                case "1": 
                    self.sequencia_dos_eventos.remove(evento)
                    continue
            
            duracao_max = 180
            progresso = (duracao_max - duracao) / duracao_max # 1.0 a 0.0
            
            pos_inicial = 210
            extra = 30
            range_animacao = pos_inicial + altura_da_fonte + extra
            
            constante = 3
            fator = (progresso/2) + 2 * (progresso ** constante)
            
            bit = 8
            pos_y = round((pos_inicial / bit) - int(fator * range_animacao) / bit) * bit
            
            px.text((mov_x * TILE) + CENTRALIZAR(FONT_1, frase, largura), pos_y, frase, cor, FONT_1)
            
            evento[2] -= 1
            if duracao == 0:
                self.sequencia_dos_eventos.remove(evento)
    
    #////

    def verificar_pos_y_negativo(self, formato):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    match self.shape_pos_atual[1] + i_linha:
                        case -3: return -3
                        case -2: return -2
                        case -1: return -1
        return 0
    
    def calcular_offset(self):
        pos_y_alto = self.verificar_pos_y_negativo(self.pegar_formato())
        if pos_y_alto < 0:
            return abs(pos_y_alto)
        return 0
    
    def calcular_offset_pelo_mapa(self):
        for linha_i in range(CORRECAO_ALTURA):
            for espaco in self.mapa[linha_i]:
                if espaco != VAZIO:
                    return CORRECAO_ALTURA - linha_i
        return 0
    
    #////
    
    def desenhar_fundo(self, pos, spritesheet_pos, tamanho, *, mov_x=0, mov_y=0, colkey=None):
        pos_x, pos_y = pos
        px.bltm(
            pos_x + (mov_x * TILE), 
            pos_y + (mov_y * TILE), 
            0, 
            (TILE * spritesheet_pos[0]), (TILE * spritesheet_pos[1]), 
            (TILE * tamanho[0]), (TILE * tamanho[1]),
            colkey=colkey,
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_x, spritesheet_y, *, mov_x=0, mov_y=0, offset=0, diminuir=0):
        px.blt(
            (TILE - diminuir) * (coluna_x + mov_x) + BOARD_X, 
            (TILE - diminuir) * ((linha_y + mov_y) + offset), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            (TILE - diminuir), (TILE - diminuir),
            colkey=0
        )
        
    #////
    
    def desenhar_shape_fantasma(self, formato, mov_x, mov_y, *, offset):
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            self.shape_pos_fantasma[0] + i_coluna,
                            self.shape_pos_fantasma[1] + i_linha, 
                            spritesheet_x, 2,
                            mov_x=mov_x,
                            mov_y=mov_y,
                            offset=offset
                        )
    
    def desenhar_shape_atual(self, formato, pos, mov_x, mov_y, *, offset):
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        pos_x, pos_y = pos
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            pos_x + i_coluna,
                            pos_y + i_linha, 
                            spritesheet_x, 0,
                            mov_x=mov_x,
                            mov_y=mov_y, 
                            offset=offset
                        )
    
    def desenhar_shapes_fixados(self, mapa, mov_x, mov_y, *, offset):
        for linha in range(0, ALTURA_DO_JOGO):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != VAZIO:
                    cor = mapa[linha][coluna]
                    spritesheet_x = COR_IMAGEM[cor]
                    
                    self.desenhar_shape(
                        coluna,
                        linha - CORRECAO_ALTURA,
                        spritesheet_x, 0,
                        mov_x=mov_x,
                        mov_y=mov_y,
                        offset=offset
                    )
    
    #////
    
    def desenhar_shapes_proximos(self, proximos_shapes, mov_x_direita, mov_y):
        ajustar_valor_x = 10.5
        ajustar_valor_y = self.offset_rect_direita
        
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
                            mov_x=mov_x_direita,
                            mov_y=mov_y
                        )
            acrescimo_distancia += self.distancia_rect_direita
    
    def desenhar_shape_segurado(self, shape_segurado, mov_x_esquerda, mov_y):
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
                        mov_x=mov_x_esquerda,
                        mov_y=mov_y,
                        diminuir=escalonar_tamanho
                    )
    
    #///
    
    def desenhar_animacao_limpar_linha(self, mov_x, mov_y, *, offset):
        def _animacao_de_limpar_linha(start, end, constante, *, constante_na_pos_x=0):
            for localizacao in self.localizacao_das_linhas_limpas:
                for pos_x in range(start, end - constante):
                    self.desenhar_shape(
                        pos_x + constante_na_pos_x,
                        localizacao,
                        spritesheet_x, 0,
                        mov_x=mov_x,
                        mov_y=mov_y, 
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
        if self.tipo_do_t_spin == None:
            _animacao_de_limpar_linha(0,       COLUNAS // 2, constante, constante_na_pos_x=constante)
            _animacao_de_limpar_linha(COLUNAS // 2, COLUNAS, constante)
        else:
            _animacao_de_limpar_linha(0,       COLUNAS // 2, constante)
            _animacao_de_limpar_linha(COLUNAS // 2, COLUNAS, constante, constante_na_pos_x=constante)
    
    def desenhar_animacao_hard_drop(self, mov_x, mov_y):
        diminuicao = 2
        duracao_total = 0.5
        duracao_diminuicao = 0.5
        
        for variaveis in self.variaveis_animacao_hard_drop:
            (formato, pos), constante = variaveis[0], variaveis[1]
            
            if constante <= 0:
                self.variaveis_animacao_hard_drop.remove(variaveis)
                continue
            
            largura = set()
            for linha in formato:
                for i, cel in enumerate(linha):
                    if cel == 1:
                        largura.add(i)
            
            lar_max = max(largura)
            lar_min = min(largura)
            
            largura = lar_max - lar_min + 1
                        
            x = BOARD_X + ((pos[0] + lar_min) * TILE)
            
            um_por_linha = 0
            linha_com_mais_um = 0
            for index, linha in enumerate(formato):
                if linha.count(1) >= um_por_linha:
                    um_por_linha = linha.count(1)
                    linha_com_mais_um = index
            
            comprimento = (pos[1] + linha_com_mais_um)
            
            fator = duracao_diminuicao * (1 - constante / 20)
            px.dither(duracao_total - fator)
            self.desenhar_rect(
                x, 0,
                largura * TILE, comprimento * TILE,
                8,
                mov_x=mov_x,
                mov_y=mov_y,
            )
            px.dither(1)
            variaveis[1] -= diminuicao
            
    #////
    
    def calcular_animacao_menu(self):
        pos_x_destino = self.menu_atual_indice * 320
        distancia_restante = pos_x_destino - self.offset_menu
        self.offset_menu += distancia_restante * 0.1
        if abs(distancia_restante) < 1:
            self.offset_menu = pos_x_destino
    
    def calcular_animacao_menu_para_jogo(self):
        pos_x_destino = 320
        distancia_restante = pos_x_destino - self.offset_menu_para_jogo
        self.offset_menu_para_jogo += distancia_restante * 0.1
        if abs(distancia_restante) < 1:
            self.offset_menu_para_jogo = pos_x_destino
    
    #
    
    def calcular_valores_das_animacoes(self):
        inicio = 0.5
        constante = 0.2
        
        if self.foi_para_esquerda:
            self.mov_x_direita = 0
            if self.mov_x_esquerda > -self.movimento_padrao:
                self.mov_x_esquerda += -(inicio + abs(self.mov_x_esquerda) * constante)
                self.mov_x_esquerda = max(self.mov_x_esquerda, -self.movimento_padrao)
                self.mov_x = self.mov_x_esquerda
        else:
            if self.mov_x_esquerda < 0:
                self.mov_x_esquerda -= -(inicio + abs(self.mov_x_esquerda) * constante)
                self.mov_x = self.mov_x_esquerda
                if abs(self.mov_x_esquerda) < 0.5:
                    self.mov_x_esquerda = 0
                    self.mov_x = 0
        #
        if self.foi_para_direita:
            self.mov_x_esquerda = 0
            if self.mov_x_direita < self.movimento_padrao:
                self.mov_x_direita += (inicio + abs(self.mov_x_direita) * constante)
                self.mov_x_direita = min(self.mov_x_direita, self.movimento_padrao)
                self.mov_x = self.mov_x_direita
        else:
            if self.mov_x_direita > 0:
                self.mov_x_direita -= (inicio + abs(self.mov_x_direita) * constante)
                self.mov_x = self.mov_x_direita
                if abs(self.mov_x_direita) < 0.5:
                    self.mov_x_direita = 0
                    self.mov_x = 0   
        #
        if self.acionou_hard_drop:
            if self.mov_y_hard_drop < (self.movimento_padrao - 1): # diminuir 1
                self.mov_y_hard_drop += (inicio + abs(self.mov_y_hard_drop) * constante)
                self.mov_y_hard_drop = min(self.mov_y_hard_drop, (self.movimento_padrao - 1)) # diminuir 1
            else:
                self.acionou_hard_drop = False
        else:
            if self.mov_y_hard_drop > 0:
                self.mov_y_hard_drop -= (inicio + abs(self.mov_y_hard_drop) * constante)
            else:
                self.mov_y_hard_drop = 0

    def calcular_animacao_game_over_slide(self):
        velocidade = 100
        limite = LINHAS + 1
        
        if self.mov_y_hard_drop > 0:
            return 0
            
        if self.movimento_exponencial_game_over < limite:
            progresso = self.mov_y_slide / (limite)
            incremento = ((1 + self.mov_y_slide) / velocidade) ** (0.5 + progresso ** 1.5)
            self.movimento_exponencial_game_over = min(self.movimento_exponencial_game_over + incremento, limite)
       
        return self.movimento_exponencial_game_over
    
    def calcular_animacao_offset_teto(self, offset_abs):
        valor = 0.25
        
        if offset_abs > self.movimento_offset_teto:
            self.movimento_offset_teto = min(self.movimento_offset_teto + valor, offset_abs)
        elif offset_abs < self.movimento_offset_teto:
            self.movimento_offset_teto = max(self.movimento_offset_teto - (1/3), offset_abs)
        if abs(self.movimento_offset_teto) < 0.1:
            self.movimento_offset_teto = 0
        
        return self.movimento_offset_teto
    
    def retornar_valores_das_animacao_em_jogo(self):
        mov_x = TRANSFORMAR_EM_DECIMAL(self.mov_x)
        mov_x_esquerda = TRANSFORMAR_EM_DECIMAL(self.mov_x_esquerda)
        mov_x_direita = TRANSFORMAR_EM_DECIMAL(self.mov_x_direita)
        mov_y_hard_drop = TRANSFORMAR_EM_DECIMAL(self.mov_y_hard_drop)
        return mov_x, mov_x_esquerda, mov_x_direita, mov_y_hard_drop, self.mov_y_slide
    
    #////
    
    def desenhar_shape_segurado_e_proximos(self, mov_x_esquerda, mov_x_direita, *, mov_y=0, offset=0):
        self.desenhar_shapes_proximos(self.proximos_shapes, (mov_x_direita + offset), mov_y)
        if self.shape_segurado != None:
            self.desenhar_shape_segurado(self.shape_segurado, (mov_x_esquerda + offset), mov_y)
    
    def desenhar_tabuleiro_e_teto(self, mov_x, mov_y, *, offset):
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS), mov_x=mov_x, mov_y=mov_y)
        if offset > 0:
            px.dither(0.4)
            self.desenhar_fundo((BOARD_X, 0), (0, LINHAS * 2), (COLUNAS, offset), mov_x=mov_x, mov_y=mov_y)
            px.dither(1)
    
    def desenhar_tudo_em_menu(self):
        self.desenhar_titulo_menu()        
        self.desenhar_os_botoes(self.offset_menu)

    #
    
    def desenhar_tudo_em_jogo(self, *, offset_soma=0):
        offset_abs = self.calcular_offset()
        offset_teto = self.calcular_animacao_offset_teto(offset_abs)
        
        offset_menu = (offset_soma - self.offset_menu_para_jogo) / TILE
        
        mov_x, mov_x_esquerda, mov_x_direita, mov_y_hard_drop, mov_y_slide = self.retornar_valores_das_animacao_em_jogo()
               
        self.desenhar_tabuleiro_e_teto((mov_x + offset_menu), mov_y_hard_drop, offset=offset_teto)
        
        if self.acionou_hard_drop or len(self.variaveis_animacao_hard_drop) > 0:
            self.desenhar_animacao_hard_drop(mov_x, mov_y_hard_drop)
        
        if not self.esta_em_are:
            self.desenhar_shape_fantasma(self.pegar_formato(), (mov_x + offset_menu), mov_y_hard_drop, offset=offset_teto)
            if self.nivel_atual < (len(TABELA_G) - 3):
                self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual, (mov_x + offset_menu), mov_y_hard_drop, offset=offset_teto)
        
        if self.limpou_linha:
            self.desenhar_animacao_limpar_linha(mov_x, mov_y_hard_drop, offset=offset_teto)
        
        self.desenhar_shapes_fixados(self.mapa, mov_x, mov_y_hard_drop, offset=offset_teto)
        self.desenhar_shape_segurado_e_proximos(mov_x_esquerda, mov_x_direita, mov_y=0, offset=offset_menu)
        self.textos_dos_popups(mov_x)
    
    #
    
    def desenhar_tudo_no_game_over(self):
        offset = self.calcular_offset_pelo_mapa()
        
        mov_x, mov_x_esquerda, mov_x_direita, mov_y_hard_drop, mov_y_slide = self.retornar_valores_das_animacao_em_jogo()
        
        if mov_y_hard_drop > 0:
            self.desenhar_tabuleiro_e_teto(mov_x, mov_y_hard_drop, offset=offset)
            self.desenhar_shapes_fixados(self.mapa, mov_x, mov_y_hard_drop, offset=offset)
        else:
            self.desenhar_tabuleiro_e_teto(mov_x, mov_y_slide, offset=offset)
            self.desenhar_shapes_fixados(self.mapa, mov_x, mov_y_slide, offset=offset)
            
        self.desenhar_shape_segurado_e_proximos(mov_x_esquerda, mov_x_direita, mov_y=mov_y_slide)
        self.textos_dos_popups(mov_x)
         
        self.desenhar_fundo((BOARD_X, (-LINHAS - 1) * TILE), (0, LINHAS), (COLUNAS, LINHAS), mov_x=0, mov_y=mov_y_slide)
        self.textos_estatisticas(mov_y=mov_y_slide, pos_y_negativo=(-(-LINHAS - 1) * TILE))
    
    #////
    
    def desenhar(self):
        px.cls(0)
        
        if self.estado_atual_do_jogo in ("em_menu", "antes_do_jogo"):
            maximo = LINHAS * TILE
            offset = self.offset_menu_para_jogo
            
            px.dither(0.4)
            px.rect((0 - offset), 0, maximo, (maximo / 2), 8)
            px.dither(0.1)
            px.rect((0 - offset), (maximo / 2), maximo, (maximo / 2), 8)
            px.dither(1)

            self.calcular_animacao_menu() 
            self.desenhar_tudo_em_menu()
        
        #/
        
        if self.estado_atual_do_jogo not in ("em_menu", "pausado"):
            self.calcular_valores_das_animacoes()
            if self.estado_atual_do_jogo == "game_over":
                self.mov_y_slide = self.calcular_animacao_game_over_slide()

        #/

        offst_menu_para_jogo_visuis = 0
        offst_menu_para_jogo_fundo = 0
        
        if self.estado_atual_do_jogo == "antes_do_jogo":
            self.calcular_animacao_menu_para_jogo()
            
            offst_menu_para_jogo_visuis = GAME_OFFSET_X
            offst_menu_para_jogo_fundo = GAME_OFFSET_X - self.offset_menu_para_jogo
        
        #/
        
        if self.estado_atual_do_jogo in ("antes_do_jogo", "em_jogo", "game_over", "apos_game_over"):
            px.dither(0.6)
            px.rect(offst_menu_para_jogo_fundo, 0, LINHAS * TILE, LINHAS * TILE, 8)
            px.dither(1)
            
            mov_x, mov_x_esquerda, mov_x_direita, mov_y_hard_drop, mov_y_slide = self.retornar_valores_das_animacao_em_jogo()
            
            self.todos_os_rects(mov_x_esquerda, mov_x_direita, mov_y_slide, offset_soma=offst_menu_para_jogo_visuis)
            self.todos_os_textos(mov_x_esquerda, mov_x_direita, mov_y_slide, offset_soma=offst_menu_para_jogo_visuis)
        
        if self.estado_atual_do_jogo in ("antes_do_jogo", "em_jogo"):
            self.desenhar_tudo_em_jogo(offset_soma=offst_menu_para_jogo_visuis)
    
        if self.estado_atual_do_jogo == "game_over":
            self.desenhar_tudo_no_game_over()            
        
        if self.estado_atual_do_jogo == "apos_game_over":
            self.desenhar_fundo((BOARD_X, 0), (0, LINHAS), (COLUNAS, LINHAS), mov_x=0, mov_y=0)
            self.textos_estatisticas(mov_y=0, pos_y_negativo=0)
        
        # self.tempo_inical_test_fim = time.perf_counter()
        # print(f"{((self.tempo_inical_test_fim - self.tempo_fps_ms) * 1000):.2f} MS")
        
Jogo()