import pyxel as px
import time
import random
import os
import json

SHAPES = {
    "shape_T": {
        "formato": [[0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 0,
        "cor_letra": "p",
    },
    "shape_I": {
        "formato": [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "imagem_pos": 1,
        "cor_letra": "c",
    },
    "shape_O": {
        "formato": [[1, 1],
                    [1, 1]],
        "imagem_pos": 2,
        "cor_letra": "y",
    },
    "shape_L": {
        "formato": [[0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 3,
        "cor_letra": "o",
    },
    "shape_J": {
        "formato": [[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 4,
        "cor_letra": "b",
    },
    "shape_S": {
        "formato": [[0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]],
        "imagem_pos": 5,
        "cor_letra": "g",
    },
    "shape_Z": {
        "formato": [[1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]],
        "imagem_pos": 6,
        "cor_letra": "r",
    },
    #
    "shape_IL": {
        "formato": [[0, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "imagem_pos": 3,
        "cor_letra": "o",
    },
    "shape_IJ": {
        "formato": [[1, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
        "imagem_pos": 4,
        "cor_letra": "b",
    },
    "shape_D": {
        "formato": [[1, 1, 1],
                    [1, 1, 1]],
        "imagem_pos": 2,
        "cor_letra": "y",
    },
    "shape_C": {
        "formato": [[0, 1],
                    [1, 1]],
        "imagem_pos": 0,
        "cor_letra": "p",
    },
    "shape_P": {
        "formato": [[1, 1, 0],
                    [1, 1, 1]],
        "imagem_pos": 6,
        "cor_letra": "r",
    },
}

SHAPES_PROXIMOS_SEGURADO = {
    "shape_T": {
        "formato": [[0, 1, 0],
                    [1, 1, 1]],
        "centralizado": (0.5, -0.5),
    },
    "shape_I": {
        "formato": [[1, 1, 1, 1]],
        "centralizado": (0, -1),
    },
    "shape_O": {
        "formato": [[1, 1],
                    [1, 1]],  
        "centralizado": (1, 0),
    },
    "shape_L": {
        "formato": [[0, 0, 1],
                    [1, 1, 1]],
        "centralizado": (0.5, -0.5),
    },
    "shape_J": {
        "formato": [[1, 0, 0],
                    [1, 1, 1]],
        "centralizado": (0.5, -0.5),
    },
    "shape_S": {
        "formato": [[0, 1, 1],
                    [1, 1, 0]],
        "centralizado": (0.5, -0.5),
    },
    "shape_Z": {
        "formato": [[1, 1, 0],
                    [0, 1, 1]],
        "centralizado": (0.5, -0.5),
    },
    #
    "shape_IL": {
        "formato": [[0, 0, 0, 1],
                    [1, 1, 1, 1]],
        "centralizado": (0, -1),
    },
    "shape_IJ": {
        "formato": [[1, 0, 0, 0],
                    [1, 1, 1, 1]],
        "centralizado": (0, -1),
    },
    "shape_D": {
        "formato": [[1, 1, 1],
                    [1, 1, 1]],
        "centralizado": (0.5, -0.5),
    },
    "shape_C": {
        "formato": [[0, 1],
                    [1, 1]], 
        "centralizado": (1, 0),
    },
    "shape_P": {
        "formato": [[1, 1, 0],
                    [1, 1, 1]],
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
                    [1, 0, 1],
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

def TABELA_PONTUACAO(tipo, linhas_limpas_pelo_shape, nivel_atual):
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
    return tabela[tipo][linhas_limpas_pelo_shape]

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

TECLA_PARA_NOME = {
    # Letras A-Z
    px.KEY_A: "A", px.KEY_B: "B", px.KEY_C: "C", px.KEY_D: "D",
    px.KEY_E: "E", px.KEY_F: "F", px.KEY_G: "G", px.KEY_H: "H",
    px.KEY_I: "I", px.KEY_J: "J", px.KEY_K: "K", px.KEY_L: "L",
    px.KEY_M: "M", px.KEY_N: "N", px.KEY_O: "O", px.KEY_P: "P",
    px.KEY_Q: "Q", px.KEY_R: "R", px.KEY_S: "S", px.KEY_T: "T",
    px.KEY_U: "U", px.KEY_V: "V", px.KEY_W: "W", px.KEY_X: "X",
    px.KEY_Y: "Y", px.KEY_Z: "Z",
    
    # Números 0-9
    px.KEY_0: "0", px.KEY_1: "1", px.KEY_2: "2", px.KEY_3: "3",
    px.KEY_4: "4", px.KEY_5: "5", px.KEY_6: "6", px.KEY_7: "7",
    px.KEY_8: "8", px.KEY_9: "9",
    
    # Setas
    px.KEY_UP: "↑",
    px.KEY_DOWN: "↓",
    px.KEY_LEFT: "←",
    px.KEY_RIGHT: "→",
    
    # Especiais
    px.KEY_SPACE: "SPACE",
    px.KEY_RETURN: "ENTER",
    px.KEY_TAB: "TAB",
    px.KEY_ESCAPE: "ESC",
    px.KEY_BACKSPACE: "BACK",
    px.KEY_SHIFT: "SHIFT",
    px.KEY_CTRL: "CTRL",
    px.KEY_ALT: "ALT",
    
    # F-keys
    px.KEY_F1: "F1", px.KEY_F2: "F2", px.KEY_F3: "F3",
    px.KEY_F4: "F4", px.KEY_F5: "F5", px.KEY_F6: "F6",
    px.KEY_F7: "F7", px.KEY_F8: "F8", px.KEY_F9: "F9",
    px.KEY_F10: "F10", px.KEY_F11: "F11", px.KEY_F12: "F12",
    
    px.GAMEPAD1_BUTTON_A: "(A)",
    px.GAMEPAD1_BUTTON_B: "(B)",
    px.GAMEPAD1_BUTTON_X: "(X)",
    px.GAMEPAD1_BUTTON_Y: "(Y)",
    px.GAMEPAD1_BUTTON_START: "(START)",
    px.GAMEPAD1_BUTTON_BACK: "(MENU)",
    px.GAMEPAD1_BUTTON_DPAD_UP: "(↑)",
    px.GAMEPAD1_BUTTON_DPAD_DOWN: "(↓)",
    px.GAMEPAD1_BUTTON_DPAD_LEFT: "(←)",
    px.GAMEPAD1_BUTTON_DPAD_RIGHT: "(→)",
    px.GAMEPAD1_BUTTON_LEFTSHOULDER: "(LB)",
    px.GAMEPAD1_BUTTON_RIGHTSHOULDER: "(LR)",
}

#/

#todo: json nao é salvo no web pyxel launcher
#todo: adicionar config nos controles - NAO
#todo ver como vai ficar os popus, com borda ou nao - SEM

#todo: adicionar 180 rotacao

#todo: adicionar talvez particular? nao sei

#todo: adiconar o fixed time step.... dificl mas ok

#todo: adicionar sons

#/

def carregar_jogos_recentes():
    try:
        with open("recent_games.json", 'r', encoding='utf-8') as f:
            historico = json.load(f)
    except:
        historico = []
    return [p for p in historico if isinstance(p, dict)]

def salvar_jogos_recentes(historico):
    with open("recent_games.json", 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

LOCK_DELAY_FRAMES = 30
LOCK_MAX_MOVIMENTOS = 15

SHAPES_1_DE_LARGURA = ("shape_I",)
SHAPES_COM_SRS_I = ("shape_I", "shape_IL", "shape_IJ")

CORES_ALEATORIAS_TETRIS = list(range(1, 8))
random.shuffle(CORES_ALEATORIAS_TETRIS)
COR_PRINCIPAL_ALEATORIA = random.choice(CORES_ALEATORIAS_TETRIS)

def alterar_valor(valor, soma, *, min, max):
    novo = valor + soma
    if min <= novo <= max:
        return round(novo, 2)
    return min if novo > max else max

def buscar_tabela_g(nivel):
    if nivel >= 20:
        return TABELA_G[20]
    return TABELA_G[nivel]

CENTRALIZAR = lambda font, string, largura: (largura / 2) - (font.text_width(string) / 2)
TRANSFORMAR_EM_DECIMAL = lambda num: num / 10

CAMINHO = lambda caminho: os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho)

FONT_10 = px.Font(CAMINHO("assets/PublicPixel.ttf"), 8)
ALTURA_DA_FONTE_10 = 14

FONT_11 = px.Font(CAMINHO("assets/PublicPixel.ttf"), 16)
ALTURA_DA_FONTE_11 = 18

FONT_20 = px.Font(CAMINHO("assets/PF Pixelscript Pro Regular.ttf"), 16)

COLUNAS = 10
LINHAS = 20

TILE = 16

CORRECAO_ALTURA = 4
ALTURA_DO_JOGO = 20 + CORRECAO_ALTURA

FPS = 60

BOARD_X = TILE * 5
LARGURA_TELA = 320
VAZIO = "_"

class Jogo:
    def __init__(self):  
        px.init(LINHAS * TILE, LINHAS * TILE, title="Tetrico: The Smoothness", fps=FPS, display_scale=2, quit_key=False)
        px.load("my_resource.pyxres")
        px.tilemaps[0].set(0, 32, ["0"])
        px.tilemaps[0].set(32, 32, ["1"])
        
        self.tempo_fps_ms = 0
        
        self.MAPEAMENTO = {
            "ESQUERDA": [px.KEY_LEFT, px.KEY_A, px.GAMEPAD1_BUTTON_DPAD_LEFT],
            "DIREITA": [px.KEY_RIGHT, px.KEY_D, px.GAMEPAD1_BUTTON_DPAD_RIGHT],
            
            "ROTACAO_ESQUERDA": [px.KEY_Q, px.KEY_Z, px.KEY_CTRL, px.GAMEPAD1_BUTTON_A],
            "ROTACAO_DIREITA": [px.KEY_E, px.KEY_X, px.KEY_UP, px.GAMEPAD1_BUTTON_B],
            "ROTACAO_180": [px.KEY_W, px.KEY_SHIFT, px.GAMEPAD1_BUTTON_X],
            
            "SEGURAR": [px.KEY_TAB, px.KEY_C, px.GAMEPAD1_BUTTON_LEFTSHOULDER, px.GAMEPAD1_BUTTON_RIGHTSHOULDER, px.GAMEPAD1_BUTTON_Y],
            "SOFT_DROP": [px.KEY_DOWN, px.KEY_S, px.GAMEPAD1_BUTTON_DPAD_DOWN],
            "HARD_DROP": [px.KEY_SPACE, px.GAMEPAD1_BUTTON_DPAD_UP],
            
            "PAUSAR": [px.KEY_ESCAPE, px.KEY_P, px.GAMEPAD1_BUTTON_START],
            "REINICIAR": [px.KEY_F1],
            
            "ACIONAR": [px.KEY_RETURN, px.GAMEPAD1_BUTTON_A],
            "VOLTAR": [px.KEY_BACKSPACE, px.GAMEPAD1_BUTTON_B],
            #
            "PARA_CIMA": [px.KEY_UP, px.GAMEPAD1_BUTTON_DPAD_UP],
            "PARA_BAIXO": [px.KEY_DOWN, px.GAMEPAD1_BUTTON_DPAD_DOWN],
            #
            "OPCAO_AUMENTAR": [px.KEY_RIGHT, px.GAMEPAD1_BUTTON_DPAD_RIGHT],
            "OPCAO_DIMINUIR": [px.KEY_LEFT, px.GAMEPAD1_BUTTON_DPAD_LEFT],
            #
            "DELETAR": [px.KEY_X, px.GAMEPAD1_BUTTON_X],
        }
          
        self.historico_partidas = carregar_jogos_recentes()
        self.iniciar_jogo()
        
        self.tempo_acumulado = 0.0
        self.ultimo_frame_tempo = time.perf_counter()
        
        px.run(self.atualizar_jogo, self.desenhar)

   #//// //// FUNÇÕES INICIAIS //// ////
    
    def variaveis_iniciais(self):
        self.estado_atual_do_jogo = "em_menu"
        self.modo_do_jogo = None
        self.resetou_jogo = False
        
        self.esta_pausado = False
        self.esta_despausando = False 
        self.clicou_em_resetar_partida = False

    def variaveis_configuracao(self):
        self.nivel_inicial_config = 1 # 1
        self.shapes_visiveis_config = 3 # 3
        self.mostrar_fantasma_config = True
        
        self.movimento_duracao_config = 7 # 7
        self.movimento_inicio_config = 0.5 # 0.50
        self.movimento_constante_config = 0.15 # 0.15
        
        self.are_duracao_config = 20 # 20
        self.das_config = 10 # 10
        self.arr_config = 2 # 2
        self.arr_soft_drop_config = 2 # 2
        
        self.visual_vel_x_config = 0.80 # 0.80
        self.visual_vel_y_config = 0.90  # 0.90

    def variaveis_rects_e_constantes(self):
        # distancia entre os shapes proximos desenhados
        self.distancia_entre_shapes_proximos = 2.5
        self.distancia_inicial_shapes_proximos = 0.5
        self.distancia_extra_modo_crazy = 0.5
        
        # comprimento dos rects
        self.comprimento_rect_esquerdo_1 = 0
        self.comprimento_rect_esquerdo_2 = 0
        self.comprimento_rect_direito = 0
    
    def iniciar_jogo(self):
        self.variaveis_iniciais()
        self.variaveis_configuracao()
        self.variaveis_rects_e_constantes()
        self.variaveis_menu()
    
    #//// INICIAR PARTIDA ////
    
    def formar_fundo(self, largura, comprimento, quantidade):
        lista = [[0] * largura for _ in range(comprimento)]
        for linha in lista:
                k = random.randint(0, quantidade)
                indices = random.sample(range(0, largura), k)
                for indice in indices:
                        linha[indice] = 1
        quantos_1 = sum([linha.count(1) for linha in lista])
        lista_y = [random.choice([0, 1]) for _ in range(quantos_1)]
        return lista, lista_y
    
    def iniciar_contagem_do_tempo(self):
        self.tempo_inicial = time.perf_counter()
        self.tempo_atual_em_segundos = 0
        self.tempo_pausado = 0
    
    def iniciar_partida(self):
        self.tempo_inicial = 0
        self.tempo_atual_em_segundos = 0
        self.tempo_pausado = 0
        
        self.mapa = [[VAZIO] * COLUNAS for _ in range(ALTURA_DO_JOGO)]
        self.pos_shapes_fundo_em_jogo, self.tipo_shapes_fundo_em_jogo = self.formar_fundo(20, 20, 12)
        
        self.nivel_inicial = self.nivel_inicial_config # CONFIG
        self.nivel_atual = self.nivel_inicial
        
        self.linhas_limpas = 0
        self.pontos_atual = 0
        self.combo_atual = -1
        self.back_to_back_atual = 0
        
        self.shapes_visiveis = self.shapes_visiveis_config # CONFIG
        self.proximos_shapes = []
        self.bag_7 = []
        self.sistema_bag_7()
        
        self.shape_atual = ""
        self.shape_segurado = None
        self.gerar_novo_shape()
       
        self.fixou_neste_frame = False
        self.segurou_neste_frame = False
        self.acionou_hard_drop = False
        self.desenhar_shape_apos_colisao = True
        
        self.status = {
            "quantidade_singles": 0,
            "quantidade_doubles": 0,
            "quantidade_triples": 0,
            "quantidade_quads": 0,
            
            "quantidade_t_spins": 0,
            "quantidade_perfect_clears": 0,
            
            "combo_maximo": 0,
            "streak_maximo": 0,
            
            "quantidade_holds": 0,
            "quantidade_pausadas": 0,
        }
        self.sequencia_dos_eventos = []
        
        self.modo_completado = False
        self.informacoes_status_da_partida = self.retornar_status_da_partida()
        
        self.variaveis_velocidade_movimentacao()
        self.estados_animacao_hard_drop = []
    
    def variaveis_movimentos(self):
        self.movimento_duracao = self.movimento_duracao_config # CONFIG
        
        self.mov_em_jogo = {
            "mov_x": 0,
            "mov_esquerda": 0,
            "mov_direita": 0,
            "mov_hard_drop": 0,
        }
        self.offset_em_jogo = {    
            "teto": 0,
            "pause": 0,
            "status": 0,
        }
        
        self.mov_slide_gameover = 0
        self.velocidade_slide_gameover = 0
    
    def variaveis_velocidade_movimentacao(self):
        self.das = self.das_config # CONFIG
        self.arr = self.arr_config # CONFIG
        self.arr_soft_drop = self.arr_soft_drop_config # CONFIG
        self.visual_vel_x = self.visual_vel_x_config
        self.visual_vel_y = self.visual_vel_y_config
    
    #//// REINICIAR SHAPE ////
   
    def reiniciar_shape(self):
        self.shape_pos_atual = self.desovar_shape(self.shape_atual)
        self.shape_matriz_atual = SHAPES[self.shape_atual]["formato"]
        self.shape_pos_fantasma = self.shape_pos_atual[:]
        self.ajustar_desovacao()
        self.recalcular_pos_fantasma()
        
        self.visual_pos_x = self.shape_pos_atual[0]
        self.visual_pos_y = self.shape_pos_atual[1]
        
        # rotacao e movimentacao
        self.ultimo_movimento_lateral = None        
        self.estado_rotacao = "0"

        # t-spin
        self.ultima_acao_foi_rotacao = False
        self.ultimo_srs_foi_1x2 = False
        self.tipo_t_spin = None
        
        # gravidade
        self.gravidade_acumulador = 0
        g = buscar_tabela_g(self.nivel_atual)
        self.gravidade_threshold = 1 / g
        
        # lock delay
        self.lock_tempo = 0 # 0,5 segundos / 30 frames
        self.lock_movimentos = 0 # 15 movimentos
        self.y_anterior = self.shape_pos_atual[1]
        
        # pontuacao
        self.linhas_limpas_pelo_shape = 0
        self.quantos_soft_drops = 0
        
        # movimentar os desenhos
        self.foi_esquerda = False
        self.foi_direita = False
        self.ultima_acao_foi_rotacao_animacao_lateral = False
        
        self.localizacao_linhas_limpas = []
        self.tempo_animacao_limpar_linha = 0
        self.constante_animacao_limpar_linha = 0
        
        self.variaveis_are()
    
    def variaveis_are(self):
        self.are_duracao = self.are_duracao_config  # CONFIG
        self.tempo_do_are = 0
        self.esta_em_are = False
        self.limpou_linha = False # Se False, sem ARE
    
    #//// FUNÇÕES AO GERAR O SHAPE ////
    
    def gerar_novo_shape(self):
        self.shape_atual = self.proximos_shapes.pop(0)
        self.reiniciar_shape()
        self.sistema_bag_7()
    
    def desovar_shape(self, formato):
       return [4, 0] if formato == "shape_O" else [3, 0]

    def ajustar_desovacao(self):
        if (self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa) or 
            self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1)):
            self.shape_pos_atual[1] -= 1
            self.shape_pos_fantasma = self.shape_pos_atual[:]
   
    def pegar_formato(self):
        return self.shape_matriz_atual
    
    def resetar_voltar_ao_menu(self):
        self.variaveis_iniciais()
        self.frases_menu()
        # Não reseta configuração, tamanho predefinidos dos rects e variáveis do menu
    
    #//// //// MENU //// ////

    def frases_quantidades(self):
        lista_frases_submenus = list(self.frases_submenus.values())
        self.quantidades_opcoes_menus = {
            "entrada": [False],
            "principal": [False] * len(self.frases_menu_principal),
            
            "jogar": [False] * len(lista_frases_submenus[0][0]),
            "configuracao": [False] * len(lista_frases_submenus[1][0]),
            "controles": [False] * len(lista_frases_submenus[2][0]),
            "recentes": [False] * len(lista_frases_submenus[3][0]),
            "sobre": [True] * len(lista_frases_submenus[4][0]),
            "sair": [True] * len(lista_frases_submenus[5][0]),
        }
    
    def frases_configuracao(self):
        frase_mostrar_fantasma = "Yeah" if self.mostrar_fantasma_config else "Nop"
        frases = ([
            f"Starting Level:{self.nivel_inicial_config:02d}", 
            f"Previews:{self.shapes_visiveis_config}",
            f"Ghost Piece:{frase_mostrar_fantasma}",
            f"FLUIDITY:",
            f" Duration:{self.movimento_duracao_config:02d}s",
            f" Outset:{self.movimento_inicio_config:0.2f}",
            f" Constant:{self.movimento_constante_config:0.2f}",
            f"ARE:{self.are_duracao_config:02d}ms",
            f"DAS:{self.das_config:02d}ms", 
            f"ARR:{self.arr_config:02d}ms",
            f"ARR SoftDrop:{self.arr_soft_drop_config:02d}ms", 
            f"SHAPE SPEED:", 
            f" X Speed:{self.visual_vel_x_config:0.2f}s", 
            f" Y Speed:{self.visual_vel_y_config:0.2f}s", 
            f"",
            "RESET COLORS",
            f"RESET VALUES"], 
            30)
        return frases
      
    def frases_controles(self):        
        def mostrar_controles(tecla):      
            teclas = self.MAPEAMENTO[tecla]
            nomes = [TECLA_PARA_NOME.get(tecla, f"#{tecla}") for tecla in teclas]
            return f"{', '.join(nomes)}"
        
        frases = ([
            f"MOVEMENTS:", 
            f"  Left: {mostrar_controles("ESQUERDA")}", 
            f" Right: {mostrar_controles("DIREITA")}", 
            f" Rotate-L: {mostrar_controles("ROTACAO_ESQUERDA")}", 
            f" Rotate-R: {mostrar_controles("ROTACAO_DIREITA")}", 
            f" Rotate-180: {mostrar_controles("ROTACAO_180")}", 
            f"ACTIONS:", 
            f" Hold: {mostrar_controles("SEGURAR")}", 
            f" Soft Drop: {mostrar_controles("SOFT_DROP")}", 
            f" Hard Drop: {mostrar_controles("HARD_DROP")}", 
            f" Pause: {mostrar_controles("PAUSAR")}", 
            f"MENU ACTIONS:", 
            f" Next Menu: {mostrar_controles("ACIONAR")}", 
            f" Back Menu: {mostrar_controles("VOLTAR")}",
            f" Up Menu: {mostrar_controles("PARA_CIMA")}", 
            f" Down Menu: {mostrar_controles("PARA_BAIXO")}", 
            f" Increment Value: {mostrar_controles("OPCAO_AUMENTAR")}",
            f" Decrement Value: {mostrar_controles("OPCAO_DIMINUIR")}",
            f" Delete: {mostrar_controles("DELETAR")}"],
            30)
        return frases
    
    def frases_menu(self):
        if len(self.historico_partidas) > 0:
            frase_recentes = []
            for index, partida in enumerate(self.historico_partidas):
                frase_recentes.append(f"{index + 1:02}: {partida["DT"]}")
        else:
            frase_recentes = ["..."]
       
        self.frase_entrada = "Press [ENTER]"
        self.frases_menu_principal = ["Play", "Settings", "Controls", "Recent Games", "About", "Quit"]
        self.frases_submenus = {
            "jogar": (["MARATHON 150", "40 LINES", "ULTRA", "CRAZY", "ZEN"], 30),
            "configuracao": self.frases_configuracao(),
            "controles": self.frases_controles(),
            "recentes": (["Press [X] for delete", *frase_recentes], 30),
            "sobre": (["Made by Cac", "Made with Pyxel", "Made with love", ":D"], 25),
            "sair": (["Press [ENTER]", "to confirm"], 25)
        }
        
    def variaveis_menu(self):
        self.pilha_menu = ["entrada"]
        self.profundidade_menu = 0
        self.opcao_atual_menu = [0, 0, 0]
        self.mostrar_status_menu = False
        
        self.offset_menu = {
            "scroll": [0, 0, 0],
            "entre_menus": 0,
            "entre_menu_e_jogo": 0,
            "status": 0,
        }
        
        self.animacoes_texto_menu = {}
        
        self.frases_menu()
        self.navegar_menu()
    
    def navegar_menu(self, *, clique=0, deslize=0, soma=0, deletar=False):
        self.frases_quantidades()
        
        if clique != 0:
            self.navegar_horizontalmente_menu(clique)
        self.menu_ativo = self.pilha_menu[-1] 
        if deslize != 0:
            self.navegar_verticalmente_menu(deslize)
        self.ajustar_configuracao_menu(soma)
        if deletar:
            if self.apagar_status():
                self.frases_menu()
                self.frases_quantidades()
        self.quantidades_opcoes_menus[self.menu_ativo][self.opcao_atual_menu[self.profundidade_menu]] = True
    
    def navegar_horizontalmente_menu(self, clique):
        if clique == 1:
            self.profundidade_menu += clique
        else:
            if self.offset_menu["status"] <= 0:
                if self.profundidade_menu > 0:
                    self.profundidade_menu += clique
                    self.pilha_menu.pop()
                    self.frases_submenus["configuracao"][0][-2] = "RESET COLORS"
                    self.frases_submenus["configuracao"][0][-1] = "RESET VALUES"
    
        if self.profundidade_menu == 1:
            self.pilha_menu.append("principal")
        
        elif self.profundidade_menu == 2:
            match self.opcao_atual_menu[1]:
                case 0: self.pilha_menu.append("jogar")
                case 1: self.pilha_menu.append("configuracao")
                case 2: self.pilha_menu.append("controles")
                case 3: self.pilha_menu.append("recentes")
                case 4: self.pilha_menu.append("sobre")
                case 5: self.pilha_menu.append("sair")
        
        elif self.profundidade_menu == 3:
            self.profundidade_menu -= clique
            
            if self.menu_ativo == "jogar":
                match self.opcao_atual_menu[2]:
                    case 0: self.modo_do_jogo = "marathon_150"
                    case 1: self.modo_do_jogo = "40_lines"
                    case 2: self.modo_do_jogo = "ultra"
                    case 3: self.modo_do_jogo = "crazy"
                    case 4: self.modo_do_jogo = "zen"
                self.iniciar_partida()
                self.variaveis_movimentos()
                self.variaveis_pause()
                self.estado_atual_do_jogo = "entre_menu_e_jogo"
            
            elif self.menu_ativo == "configuracao":
                if self.opcao_atual_menu[2] == (len(self.frases_configuracao()[0]) - 1): # clicou em resetar configuracao
                    self.variaveis_configuracao()
                    self.frases_submenus["configuracao"] = self.frases_configuracao()
                    self.frases_submenus["configuracao"][0][-1] = "RESET"
                elif self.opcao_atual_menu[2] == (len(self.frases_configuracao()[0]) - 2): # clicou em resetar cores
                    global COR_PRINCIPAL_ALEATORIA
                    random.shuffle(CORES_ALEATORIAS_TETRIS)
                    COR_PRINCIPAL_ALEATORIA = random.choice(CORES_ALEATORIAS_TETRIS)
                    self.frases_submenus["configuracao"][0][-2] = "RESET COLORS!"
            
            elif self.menu_ativo == "controles":
                pass
            
            elif self.menu_ativo == "recentes":
                if len(self.historico_partidas) > 0 and self.opcao_atual_menu[2] > 0:
                    self.mostrar_status_menu = False if self.mostrar_status_menu else True
            
            elif self.menu_ativo == "sair":
                self.profundidade_menu += clique
                self.estado_atual_do_jogo = "sair_do_jogo"
                px.quit()
                
    def navegar_verticalmente_menu(self, deslize):
        indice_maximo = len(self.quantidades_opcoes_menus[self.menu_ativo]) - 1
        
        if not self.mostrar_status_menu:
            self.opcao_atual_menu[self.profundidade_menu] = alterar_valor(self.opcao_atual_menu[self.profundidade_menu], deslize, min=0, max=indice_maximo)
        else:
            self.opcao_atual_menu[self.profundidade_menu] = alterar_valor(self.opcao_atual_menu[self.profundidade_menu], deslize, min=1, max=indice_maximo)
        
        if self.profundidade_menu == 1:
            self.offset_menu["scroll"][2] = 0
            self.opcao_atual_menu[2] = 0
   
    def ajustar_configuracao_menu(self, soma):
        if self.menu_ativo == "configuracao" and soma != 0:
            match self.opcao_atual_menu[2]:
                case 0:
                    self.nivel_inicial_config = alterar_valor(self.nivel_inicial_config, soma, min=1, max=20)
                case 1:
                    self.shapes_visiveis_config = alterar_valor(self.shapes_visiveis_config, soma, min=1, max=5)
                case 2:
                    self.mostrar_fantasma_config = False if self.mostrar_fantasma_config else True
                case 3:
                    pass
                case 4:
                    self.movimento_duracao_config = alterar_valor(self.movimento_duracao_config, soma, min=0, max=10)
                case 5:
                    self.movimento_inicio_config = alterar_valor(self.movimento_inicio_config, (soma/10), min=0, max=1)
                case 6:
                    self.movimento_constante_config = alterar_valor(self.movimento_constante_config, (soma/20), min=0, max=0.5)
                case 7:
                    self.are_duracao_config = alterar_valor(self.are_duracao_config, soma, min=0, max=200)
                case 8:
                    self.das_config = alterar_valor(self.das_config, soma, min=0, max=50)
                case 9:
                    self.arr_config = alterar_valor(self.arr_config, soma, min=0, max=10)
                case 10:
                    self.arr_soft_drop_config = alterar_valor(self.arr_soft_drop_config, soma, min=0, max=10)
                case 11:                          
                    pass
                case 12:
                    self.visual_vel_x_config = alterar_valor(self.visual_vel_x_config, (soma/20), min=0.05, max=1.0)
                case 13:                          
                    self.visual_vel_y_config = alterar_valor(self.visual_vel_y_config, (soma/20), min=0.05, max=1)
            
            self.frases_submenus["configuracao"] = self.frases_configuracao()
    
    def apagar_status(self):
        if len(self.historico_partidas) > 0 and self.opcao_atual_menu[2] > 0:
            self.historico_partidas.pop(self.opcao_atual_menu[2] - 1)
            salvar_jogos_recentes(self.historico_partidas)
            self.opcao_atual_menu[self.profundidade_menu] -= 1
            if self.opcao_atual_menu[self.profundidade_menu] == 0:
                self.opcao_atual_menu[self.profundidade_menu] = 1
            if len(self.historico_partidas) == 0:
                self.mostrar_status_menu = False
            return True
        return False
    
    #//// //// PAUSE //// ////
    
    def variaveis_despausar(self):
        self.pos_shapes_fundo_pause, self.tipo_shapes_fundo_pause = self.formar_fundo(10, 10, 10)            
        self.frases_pause = ["Continue", "Stats", "Restart", "Back", "Quit"]
        self.confirmacao_valor = {chave: 0 for chave in self.confirmacao_valor}
    
    def confirmacao_opcao(self, indice, tipo, frase):
        if self.confirmacao_valor[tipo] == 1:
            self.frases_pause[indice] = frase + "!"
            return True
        else:
            self.confirmacao_valor[tipo] += 1
            self.frases_pause[indice] = frase + "?"
            return False
    
    def variaveis_pause(self):
        self.pos_shapes_fundo_pause, self.tipo_shapes_fundo_pause = self.formar_fundo(10, 10, 10)
        self.distancia_do_pause = 160
        self.frases_pause = ["Continue", "Stats", "Restart", "Back", "Quit"]
        self.frase_titulo_pause = "PAUSED"
        
        self.confirmacao_valor = {
            "resetar": 0,
            "sair": 0,
            "voltar": 0,
        }
        self.mostrar_status_pause = False
        
        self.opcao_atual_pause = 0
        self.quantidades_opcoes_pause = [False] * len(self.frases_pause)
        self.quantidades_opcoes_pause[self.opcao_atual_pause] = True
    
    def navegar_pause(self, *, clique=0, deslize=0):
        self.quantidades_opcoes_pause = [False] * len(self.frases_pause)
        
        if clique != 0:
            if self.opcao_atual_pause == 0:
                self.esta_despausando = True
            
            elif self.opcao_atual_pause == 1:
                if self.estado_atual_do_jogo == "em_jogo":
                    self.informacoes_status_da_partida = self.retornar_status_da_partida()
                    self.mostrar_status_pause = False if self.mostrar_status_pause else True
                elif self.estado_atual_do_jogo == "game_over":
                    self.esta_despausando = True
            
            elif self.opcao_atual_pause == 2:
                if self.confirmacao_opcao(2, "resetar", "Restart"):
                    self.iniciar_partida()
                    self.clicou_em_resetar_partida = True
                    self.velocidade_slide_gameover = 0
                    self.mostrar_status_pause = False
            
            elif self.opcao_atual_pause == 3:
                if self.confirmacao_opcao(3, "voltar", "Back"):
                    if self.estado_atual_do_jogo == "em_jogo":
                        self.informacoes_status_da_partida = self.retornar_status_da_partida("abortado")
                        self.salvar_partida(self.informacoes_status_da_partida)
                    self.estado_atual_do_jogo = "entre_menu_e_jogo"
            
            elif self.opcao_atual_pause == 4:
                if self.confirmacao_opcao(4, "sair", "Quit"):
                    self.estado_atual_do_jogo = "sair_do_jogo"
                    px.quit()
        
        if deslize != 0:
            indice_maximo = len(self.quantidades_opcoes_pause) - 1
            self.opcao_atual_pause = alterar_valor(self.opcao_atual_pause, deslize, min=0, max=indice_maximo)
        
        self.quantidades_opcoes_pause[self.opcao_atual_pause] = True

    #//// //// JOGO //// ////
    
    #//// FUNÇÕES - DIVERSAS (INPUT, BAG 7, FIXAR, MODO, TEMPO FORMATADO) ////
    
    def retornar_status_da_partida(self, resultado=None):
        agora_fuso = time.localtime()
        tempo_string = time.strftime("%d.%m.%y %H:%M", agora_fuso)
        match self.modo_do_jogo:
            case "marathon_150": frase_modo = "MARATHON"
            case "40_lines": frase_modo = "40 LINES"
            case "ultra": frase_modo = "ULTRA"
            case "crazy": frase_modo = "CRAZY"
            case "zen": frase_modo = "ZEN"
        match resultado:
            case "game_over": frase_resultado = "GAME OVER"
            case "completo": frase_resultado = "COMPLETED"
            case "abortado": frase_resultado = "ABORTED"
            case _: frase_resultado = "..."
            
        status_dict = {
            "DT":            f"{tempo_string}",  
            "Mode":            f"{frase_modo}",  
            "Result":          f"{frase_resultado}",
            "Duration":        f"{self.tempo_formatado()}",
            "Start Level":     f"{self.nivel_inicial}",
            "Final Level":     f"{self.nivel_atual}",
            "Lines":           f"{self.linhas_limpas}",
            "Score":           f"{self.pontos_atual}",
            "Singles":         f"{self.status['quantidade_singles']}",
            "Doubles":         f"{self.status['quantidade_doubles']}",
            "Triples":         f"{self.status['quantidade_triples']}",
            "Tetris":          f"{self.status['quantidade_quads']}",
            "T-Spins":         f"{self.status['quantidade_t_spins']}",
            "Perfect Clears":  f"{self.status['quantidade_perfect_clears']}",
            "Max Combo":       f"{self.status['combo_maximo']}",
            "Max Streak":      f"{self.status['streak_maximo']}",
            "Times Held":      f"{self.status['quantidade_holds']}",
            "Times Pause":     f"{self.status['quantidade_pausadas']}"
        }
        
        return status_dict
    
    def salvar_partida(self, status_da_partida):
        self.historico_partidas.append(status_da_partida)
        salvar_jogos_recentes(self.historico_partidas)
    
    def pegar_input(self, input, repeticao=0, hold=0, *, input_puro=False):
        for tecla in self.MAPEAMENTO[input]:
            if input_puro and px.btn(tecla): 
                return True
            elif px.btnp(tecla, repeat=repeticao, hold=hold):
                return True
        return False
    
    def sistema_bag_7(self):
        shapes = ["I", "O", "T", "L", "J", "S", "Z"]
        shapes_adicionais = ["IL", "IJ", "D", "C", "P"]
        if len(self.bag_7) == 0:
            if self.modo_do_jogo == "crazy":
                shapes.extend(shapes_adicionais) 
            self.bag_7 = [f"shape_{x}" for x in shapes]
            random.shuffle(self.bag_7)
        
        while len(self.proximos_shapes) < self.shapes_visiveis:
            self.proximos_shapes.append(self.bag_7.pop(0))
    
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
    
    def verificar_estado_do_modo(self):
        if self.modo_do_jogo == "marathon_150" and self.linhas_limpas >= 150:
            self.modo_completado = True
        
        elif self.modo_do_jogo == "40_lines" and self.linhas_limpas >= 40:
            self.modo_completado = True

        elif self.modo_do_jogo == "ultra" and self.tempo_atual_em_segundos >= (tempo := (3 * 60)):
            self.modo_completado = True
            self.tempo_atual_em_segundos = tempo
    
    def tempo_formatado(self):
        minutos = int(self.tempo_atual_em_segundos // 60)
        segundos = int(self.tempo_atual_em_segundos % 60)
        centesimos = int((self.tempo_atual_em_segundos - int(self.tempo_atual_em_segundos)) * 100)
        return f"{minutos:02d}:{segundos:02d}.{centesimos:02d}"
    
    #//// COLISÃO ////
    
    def verificar_colisao(self, formato, pos, mapa, dx=0, dy=0):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    n_col = pos[0] + i_coluna + dx 
                    n_lin = pos[1] + i_linha + dy + CORRECAO_ALTURA
                    
                    if n_col < 0: # parede da esquerda
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
    
    #//// SISTEMA DE ROTAÇÃO ////
    
    def sistema_super_rotacao(self, novo_estado):
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
                #
                # "0->2": [],
                # "R->L": [],
                # "2->0": [],
                # "L->R": [],
            },
            "shapes_largos": {
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
        lista_das_sequencias = SEQUENCIA["shapes_largos" if self.shape_atual in SHAPES_COM_SRS_I else "todos_shapes"][transcricao]
        
        for index, (dx, dy) in enumerate(lista_das_sequencias):
            if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dx=dx, dy=dy):
                if index == 4:
                    self.ultimo_srs_foi_1x2 = True
                else:
                    self.ultimo_srs_foi_1x2 = False
                return (True, (dx, dy))
        return (False, (0, 0)) 
                    
    def proximo_estado_rotacao(self, direcao):
        estados = ["0", "R", "2", "L"]
        if direcao == "direita":
            soma = +1
        elif direcao == "esquerda":
            soma = -1
        elif direcao == "180":
            soma = +2
        indice_atual = estados.index(self.estado_rotacao)
        return estados[(indice_atual + soma) % 4]            
    
    def rotacionar_shape(self, direcao):
        backup = self.shape_matriz_atual
        match direcao:
            case "KEY_ESQUERDA":
                nova_matriz = [list(linha) for linha in list(zip(*self.pegar_formato()))[::-1]]
                self.shape_matriz_atual = nova_matriz
                novo_estado_da_rotacao = self.proximo_estado_rotacao("esquerda")
                correcao = self.sistema_super_rotacao(novo_estado_da_rotacao)
            case "KEY_DIREITA": 
                nova_matriz = [list(linha) for linha in list(zip(*self.pegar_formato()[::-1]))]
                self.shape_matriz_atual = nova_matriz  
                novo_estado_da_rotacao = self.proximo_estado_rotacao("direita")
                correcao = self.sistema_super_rotacao(novo_estado_da_rotacao)
            case "KEY_180": 
                nova_matriz = [list(linha) for linha in list(zip(*self.pegar_formato()[::-1]))]
                nova_matriz = [list(linha) for linha in list(zip(*nova_matriz[::-1]))]
                self.shape_matriz_atual = nova_matriz  
                novo_estado_da_rotacao = self.proximo_estado_rotacao("180")
                correcao = self.sistema_super_rotacao(novo_estado_da_rotacao)
            
        if correcao[0] == True:
            self.shape_pos_atual[0] += correcao[1][0]
            self.shape_pos_atual[1] += correcao[1][1]
            self.shape_pos_fantasma = self.shape_pos_atual[:]
            match direcao:
                case "KEY_ESQUERDA": self.estado_rotacao = self.proximo_estado_rotacao("esquerda")
                case "KEY_DIREITA": self.estado_rotacao = self.proximo_estado_rotacao("direita")
                case "KEY_180": self.estado_rotacao = self.proximo_estado_rotacao("180")
        else:
            self.shape_matriz_atual = backup

    #//// GRAVIDADE E T-SPIN ////
    
    def queda_automatica(self):
        self.gravidade_acumulador += 1
        g = buscar_tabela_g(self.nivel_atual)
        
        while self.gravidade_acumulador > self.gravidade_threshold: 
                if not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                    self.shape_pos_atual[1] += 1
                    
                    if self.shape_pos_atual[1] > self.y_anterior:
                        self.y_anterior = self.shape_pos_atual[1]
                        self.lock_movimentos = 0
                    
                    self.gravidade_threshold += 1 / g # linhas por frame, que vai aumentando
                    self.lock_tempo = 0
                else:
                    self.gravidade_acumulador = self.gravidade_threshold
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
            self.tipo_t_spin = self.retornar_tipo_do_t_spin(canto_f, canto_b)
    
    #//// INCREMENTAR OS STATUS E EVENTOS ////
    
    def anexar_eventos(self, ordem, tipo, linhas_limpas):
        duracao = 130
        cor = (SHAPES[self.shape_atual]["imagem_pos"] + 1)
        informacoes = [tipo, linhas_limpas, duracao, cor]
        self.sequencia_dos_eventos.insert(ordem, informacoes)
    
    def incrementar_os_eventos(self, linhas_limpas=0, *, perfect_clear=False, tipo_t_spin=None):
        if perfect_clear:
            self.anexar_eventos(0, "perfect_clear", linhas_limpas)
        elif tipo_t_spin != None:
            if linhas_limpas != 0:
                self.anexar_eventos(1, self.tipo_t_spin, linhas_limpas)
            else:
                self.anexar_eventos(2, self.tipo_t_spin, linhas_limpas)
        elif linhas_limpas > 0:
            self.anexar_eventos(3, f"{linhas_limpas}", linhas_limpas)
    
    def incrementar_os_status(self, *, perfect_clear=False, tipo_t_spin=None, linhas_limpas=0, combo=-1, back_to_back=0):
        if perfect_clear:
            self.status["quantidade_perfect_clears"] += 1
        if tipo_t_spin != None:
            self.status["quantidade_t_spins"] += 1
        if linhas_limpas > 0:
            match linhas_limpas:
                case 1: self.status["quantidade_singles"] += 1
                case 2: self.status["quantidade_doubles"] += 1
                case 3: self.status["quantidade_triples"] += 1
                case 4: self.status["quantidade_quads"] += 1
        if combo >= 1:
            self.status["combo_maximo"] = max(self.status["combo_maximo"], combo)
        if back_to_back > 0:
            self.status["streak_maximo"] = max(self.status["streak_maximo"], back_to_back)
    
    #//// LINHAS EM GERAL ////
    
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
                self.localizacao_linhas_limpas += [(LINHAS - 1) - linha_i]
                self.linhas_limpas += 1
                self.linhas_limpas_pelo_shape += 1
    
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
    
    #//// CALCULAR PONTOS ////
    
    def calcular_pontos(self):
        linhas_limpas = self.linhas_limpas_pelo_shape
        pontuacao = 0
        
        if linhas_limpas == 0:
            self.combo_atual = -1
            if self.tipo_t_spin != None:
                self.incrementar_os_status(tipo_t_spin=self.tipo_t_spin)
                self.incrementar_os_eventos(linhas_limpas, tipo_t_spin=self.tipo_t_spin)
                if self.tipo_t_spin == "t_spin": return 400 * self.nivel_atual
                if self.tipo_t_spin == "mini_t_spin": return 100 * self.nivel_atual
            return 0

        self.combo_atual += 1  
        pontuacao += self.verificar_combo(self.combo_atual)
        
        if linhas_limpas == 4 or self.tipo_t_spin != None: self.back_to_back_atual += 1
        elif linhas_limpas in (1, 2, 3): self.back_to_back_atual = 0
        aumento_do_back_to_back = 1.5 if self.back_to_back_atual >= 2 else 1
        
        if self.verificar_perfect_clear(self.mapa[::-1]):
            pontuacao += TABELA_PONTUACAO("perfect_clear", linhas_limpas, self.nivel_atual)
            self.incrementar_os_status(perfect_clear=True)
            self.incrementar_os_eventos(linhas_limpas, perfect_clear=True)
        else:
            self.incrementar_os_eventos(linhas_limpas, tipo_t_spin=self.tipo_t_spin)
        
        self.incrementar_os_status(
            tipo_t_spin=self.tipo_t_spin, 
            linhas_limpas=linhas_limpas,
            combo=self.combo_atual, 
            back_to_back=self.back_to_back_atual, 
        )
      
        if self.tipo_t_spin == None:
            pontuacao += TABELA_PONTUACAO("normal", linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        else:
            pontuacao += TABELA_PONTUACAO(self.tipo_t_spin, linhas_limpas, self.nivel_atual) * aumento_do_back_to_back
        
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

    #//// VERIFICAR GAME OVER ////
    
    def acionar_game_over(self, resultado):
        self.estado_atual_do_jogo = "game_over"
        self.informacoes_status_da_partida = self.retornar_status_da_partida(resultado)
        self.salvar_partida(self.informacoes_status_da_partida)
    
    def verificar_game_over_colisao(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa):
            self.acionar_game_over("game_over")
            self.desenhar_shape_apos_colisao = False
            return True
        return False
    
    def verificar_game_over_teto(self):
        for coluna in range(COLUNAS):
            for linha in range(CORRECAO_ALTURA):
                if self.mapa[linha][coluna] != VAZIO:
                    self.acionar_game_over("game_over")
                    self.desenhar_shape_apos_colisao = False
                    return True
        return False
    
    #//// VERIFICAÇÕES - DIVERSAS (LOCK, MOVIMENTO LATERAL)////
        
    def aumentar_lock_reset(self):
        if self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
            if self.lock_movimentos != LOCK_MAX_MOVIMENTOS:
                self.lock_movimentos += 1
                self.lock_tempo = 0
    
    def verificar_movimento_lateral(self):
        esquerda_puro = self.pegar_input("ESQUERDA", input_puro=True) and not self.pegar_input("DIREITA", input_puro=True)
        direita_puro = self.pegar_input("DIREITA", input_puro=True) and not self.pegar_input("ESQUERDA", input_puro=True)
        
        dx = 3 if self.shape_atual in SHAPES_COM_SRS_I else 2
        
        if self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, 1):
            self.foi_direita = True
            self.ultima_acao_foi_rotacao_animacao_lateral = False
        elif self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, -1):
            self.foi_esquerda = True
            self.ultima_acao_foi_rotacao_animacao_lateral = False
        
        elif self.ultima_acao_foi_rotacao_animacao_lateral and direita_puro and self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, dx):
            self.foi_direita = True
        elif self.ultima_acao_foi_rotacao_animacao_lateral and esquerda_puro and self.verificar_colisao_parede(self.pegar_formato(), self.shape_pos_atual, -dx):
            self.foi_esquerda = True  
        else:
            self.foi_esquerda, self.foi_direita = False, False
            self.ultima_acao_foi_rotacao_animacao_lateral = False   
    
    #//// FUNÇÕES AO INPUT ////
    
    def segurar_shape(self, *, input_puro=False):
        if self.pegar_input("SEGURAR", input_puro=input_puro) and not self.segurou_neste_frame:
            self.segurou_neste_frame = True
            self.status["quantidade_holds"] += 1
            
            if self.shape_segurado == None:
                self.shape_segurado = self.shape_atual
                self.gerar_novo_shape()
            else:
                self.shape_atual, self.shape_segurado = self.shape_segurado, self.shape_atual
                self.reiniciar_shape()    

    def mover_shape(self):
        hold = self.das        
        repeticao = self.arr
        
        direita = self.pegar_input("DIREITA", repeticao, hold)
        esquerda = self.pegar_input("ESQUERDA", repeticao, hold)
        
        if self.pegar_input("DIREITA"):
            self.ultimo_movimento_lateral = "direita"
        elif self.pegar_input("ESQUERDA"):
            self.ultimo_movimento_lateral = "esquerda"
       
        if self.ultimo_movimento_lateral is None:
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
        rotacoes = {
            "ROTACAO_ESQUERDA": "KEY_ESQUERDA",
            "ROTACAO_DIREITA": "KEY_DIREITA",
            #"ROTACAO_180": "KEY_180",
        }
        rotacionou = False

        for input_nome, direcao in rotacoes.items():
            if self.pegar_input(input_nome, input_puro=input_puro):
                self.rotacionar_shape(direcao)
                rotacionou = True
        if rotacionou:
            self.aumentar_lock_reset()
            self.ultima_acao_foi_rotacao = True
            self.ultima_acao_foi_rotacao_animacao_lateral = True
        
    def recalcular_pos_fantasma(self):
        while not self.verificar_colisao(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, dy=1):
            self.shape_pos_fantasma[1] += 1
    
    def soft_drop(self):
        repeticao = self.arr_soft_drop
        
        if self.pegar_input("SOFT_DROP", repeticao):
            if repeticao == 0:
                self.shape_pos_atual = self.shape_pos_fantasma[:]
            elif not self.verificar_colisao(self.pegar_formato(), self.shape_pos_atual, self.mapa, dy=1):
                self.gravidade_acumulador = self.gravidade_threshold + (1 / 60)
                self.quantos_soft_drops += 1        
                self.ultima_acao_foi_rotacao = False
    
    def hard_drop(self):
        if self.pegar_input("HARD_DROP"):
            self.verificar_t_spin(self.shape_pos_fantasma)
            self.fixar(self.pegar_formato(), self.shape_pos_fantasma, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
            self.esta_em_are = True
            self.acionou_hard_drop = True
            
            estado = [self.pegar_formato(), self.shape_pos_fantasma]
            duracao = 20
            self.estados_animacao_hard_drop.append([estado, duracao])
    
            self.pontos_atual += self.quantos_soft_drops
            self.pontos_atual += (self.shape_pos_fantasma[1] - self.shape_pos_atual[1]) * 2
    
    def teclas_especiais(self):
        if self.pegar_input("REINICIAR"):
            self.resetar_voltar_ao_menu()
            self.resetou_jogo = True
            
        if self.pegar_input("PAUSAR"):
            if self.esta_pausado == False:
                self.esta_pausado = True
                self.tempo_pausado = time.perf_counter()
                if self.estado_atual_do_jogo == "em_jogo":
                    self.status["quantidade_pausadas"] += 1
            else:
                self.esta_despausando = True
    
    def input_tecla(self):
        self.segurar_shape()
        self.mover_shape()
        self.verificar_rotacao_shape()
        self.verificar_movimento_lateral()
        self.recalcular_pos_fantasma()
        self.soft_drop()
        self.hard_drop()
    
    #//// NAVEGAÇÃO DO MENU E DO PAUSE ////
    
    def teclas_navegacao_menu(self):
        if self.pegar_input("ACIONAR"):
            self.navegar_menu(clique=1)
        elif self.pegar_input("VOLTAR"):
            self.navegar_menu(clique=-1)
        
        elif self.pegar_input("PARA_CIMA"):
            self.navegar_menu(deslize=-1)
        elif self.pegar_input("PARA_BAIXO"):
            self.navegar_menu(deslize=1)
        
        elif self.pegar_input("OPCAO_AUMENTAR", repeticao=7):
            self.navegar_menu(soma=1)
        elif self.pegar_input("OPCAO_DIMINUIR", repeticao=7):
            self.navegar_menu(soma=-1)
        
        elif self.pegar_input("DELETAR"):
            self.navegar_menu(deletar=True)
    
    def teclas_navegacao_pause(self):
        if self.pegar_input("ACIONAR"):
            self.navegar_pause(clique=1)

        elif self.pegar_input("PARA_CIMA"):
            self.navegar_pause(deslize=-1)
        elif self.pegar_input("PARA_BAIXO"):
            self.navegar_pause(deslize=1)
    
    #//// FIXED TIME STEP ////

    def atualizar(self):
        agora = time.perf_counter()
        delta = agora - self.ultimo_frame_tempo
        self.ultimo_frame_tempo = agora
       
        delta = min(delta, 0.1) 
        self.tempo_acumulado += delta
        
        while self.tempo_acumulado >= (1 / 60):
            self.atualizar_jogo()
            self.tempo_acumulado -= (1 / 60) 
    
    #//// ENCAPSULAMENTO - GERAL ////
    
    def atualizar_estado_resetar_partida(self):
        if self.mov_slide_gameover == 0:
                self.estado_atual_do_jogo = "em_jogo"
                self.clicou_em_resetar_partida = False
                self.velocidade_slide_gameover = 0
    
    def atualizar_estado_entre_menu_e_jogo(self):
        if self.offset_menu["entre_menu_e_jogo"] >= LARGURA_TELA:
            if self.esta_pausado and self.confirmacao_valor["voltar"] == 1:
                self.offset_menu["entre_menu_e_jogo"] = 0
                self.resetar_voltar_ao_menu()
            else:
                self.offset_menu["entre_menu_e_jogo"] = 0
                self.estado_atual_do_jogo = "em_jogo"
                self.iniciar_contagem_do_tempo()
    
    def atualizar_estado_pausado(self):
        if self.esta_despausando:
            self.mostrar_status_pause = False
            if self.offset_em_jogo["pause"] <= 0:
                self.variaveis_despausar()
                self.esta_pausado = False
                self.esta_despausando = False
                self.tempo_inicial += time.perf_counter() - self.tempo_pausado
                self.tempo_pausado = 0
        else:
            self.teclas_navegacao_pause()
    
    def atualizar_estado_em_jogo(self):
        self.fixou_neste_frame = False
        
        if not self.esta_em_are:
            self.input_tecla()
            self.queda_automatica()
            
            if self.lock_tempo >= LOCK_DELAY_FRAMES or self.lock_movimentos == LOCK_MAX_MOVIMENTOS:
                self.verificar_t_spin(self.shape_pos_atual)
                self.fixar(self.pegar_formato(), self.shape_pos_atual, self.mapa, SHAPES[self.shape_atual]["cor_letra"])
                self.esta_em_are = True
                self.pontos_atual += self.quantos_soft_drops
            
            if self.fixou_neste_frame:
                    self.segurou_neste_frame = False                 
                    self.verificar_linha(self.mapa)
                    self.pontos_atual += self.calcular_pontos()
                    self.verificar_nivel(self.linhas_limpas)
        else: 
            if not self.limpou_linha:
                self.are_duracao = 0            
            if self.tempo_do_are > self.are_duracao:
                
                if self.limpou_linha:
                    self.mover_linhas_do_mapa(self.mapa[::-1])              
                if self.modo_completado: 
                    self.acionar_game_over("completo")
                    self.modo_completado = False
                    return    
                
                self.gerar_novo_shape()
                self.segurar_shape(input_puro=True)
                self.verificar_rotacao_shape(input_puro=True)
                self.verificar_game_over_colisao()
            else:
                self.foi_esquerda, self.foi_direita = False, False
                self.tempo_do_are += 1
        
        self.verificar_estado_do_modo()
        if not self.modo_completado:
            self.tempo_atual_em_segundos = (time.perf_counter() - self.tempo_inicial)
    
    #//// //// ATUALIZAR TUDO //// ////
    
    def atualizar_jogo(self):
        self.tempo_fps_ms = time.perf_counter()
        
        if self.estado_atual_do_jogo == "em_menu":
            self.teclas_navegacao_menu()
            return
        
        if self.estado_atual_do_jogo == "entre_menu_e_jogo":
            self.atualizar_estado_entre_menu_e_jogo()
            return
        
        self.teclas_especiais()

        if self.clicou_em_resetar_partida:
            self.atualizar_estado_resetar_partida()
         
        if self.resetou_jogo:
            self.resetou_jogo = False
            return
        
        if self.esta_pausado:
            self.atualizar_estado_pausado()
            return
        else:
            self.frase_titulo_pause = "GAME\nOVER" if self.estado_atual_do_jogo == "game_over" else "PAUSED"
        
        if self.estado_atual_do_jogo == "game_over":
            return
        
        self.atualizar_estado_em_jogo()

    #//// //// DESENHOS //// ////
    
    #//// FUNÇÕES - DIVERSAS ////
    
    def calcular_interpolacao_linear(self, valor, destino, velocidade):
        distancia = destino - valor
        if abs(distancia) <= velocidade:
            return destino
        if distancia > 0:
            return valor + velocidade
        else:
            return valor - velocidade
    
    def calcular_interpolacao(self, valor, destino, velocidade, limite):
        distancia = destino - valor
        if abs(distancia) < limite:
                return destino
        return valor + distancia * velocidade
    
    def desenhar_shapes_fundo_em_jogo(self, offset_x):
        formato = self.pos_shapes_fundo_em_jogo
        y_soma = 0
        cinza = 8
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        y = self.tipo_shapes_fundo_em_jogo[y_soma]
                        y_soma += 1
                        self.desenhar_shape_como_letra(
                            offset_x + (i_coluna * TILE),
                            (i_linha * TILE), 
                            (cinza - 1, y)
                        ) 
    
    def desenhar_shape_como_letra(self, coluna_x, linha_y, spritesheet_pos):
        spritesheet_x, spritesheet_y = spritesheet_pos
        px.blt(
            (coluna_x), (linha_y), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            TILE, TILE,
            colkey=0
        )
    
    def desenhar_texto_dos_botoes(self, pos, largura, frase, ativo, fonte, *, somar_y=0, espacamento=0, profundidade_menu=0, offset_x, offset_y, min=-1, max=2):
        def _calcular_animacao_texto():
            comprimento_maximo = 304
            velocidade_ativo = 0.004
            velocidade_nao_ativo = 0.03
            largura_frase = fonte.text_width(frase)
            
            if (largura_frase <= comprimento_maximo):
                return somar_y
            if frase not in self.animacoes_texto_menu:
                self.animacoes_texto_menu[frase] = {
                    "offset": 0,
                    "indo_direita": True
                }
            
            diferenca = largura_frase - (comprimento_maximo - 16)
            anim = self.animacoes_texto_menu[frase]
        
            if not ativo and abs(anim["offset"]) < 0.1:
                del self.animacoes_texto_menu[frase]
            if not ativo:
                #anim["offset"] = self.calcular_interpolacao_linear(anim["offset"], 0, velocidade_nao_ativo)
                anim["offset"] = self.calcular_interpolacao(anim["offset"], 0, velocidade_nao_ativo, 0.01)
                anim["indo_direita"] = False
                return somar_y + anim["offset"]

            variacao = 0.5
            if self.offset_menu["entre_menus"] >= (LARGURA_TELA * profundidade_menu):
                if anim["offset"] <= (-diferenca + variacao) and anim["indo_direita"]:
                    anim["indo_direita"] = False
                elif anim["offset"] >= -variacao and not anim["indo_direita"]:
                    anim["indo_direita"] = True

                destino_x = -diferenca if anim["indo_direita"] else 0
                #anim["offset"] = self.calcular_interpolacao_linear(anim["offset"], destino_x, velocidade_ativo)
                anim["offset"] = self.calcular_interpolacao(anim["offset"], destino_x, velocidade_ativo, 0.01)
            return somar_y + anim["offset"]
        
        def _desenhar_texto(*, dx=0, dy=0, cor=0):
            somar_y_final = _calcular_animacao_texto()
            pos_x, pos_y = pos 
            px.text(
                pos_x + dx + somar_y_final - offset_x, 
                pos_y + dy - round(espacamento * offset_y), 
                frase, cor, fonte
            )
        
        somar_y = somar_y if somar_y != 0 else CENTRALIZAR(fonte, frase, largura) 
        cor_escura = 8
    
        if not ativo:
            _desenhar_texto(cor=0)
            px.dither(0.2)
            _desenhar_texto(cor=(COR_PRINCIPAL_ALEATORIA + cor_escura))
            px.dither(1)
        else:
            for dx in range(min, max):
                for dy in range(min, max):
                    if dx != 0 or dy != 0:
                        _desenhar_texto(dx=dx, dy=dy, cor=cor_escura)
            _desenhar_texto(cor=COR_PRINCIPAL_ALEATORIA)
    
    #//// MENU ////
    
    def desenhar_titulo_menu(self, offset_x):
        spritesheet_x = CORES_ALEATORIAS_TETRIS
        acertar_imagem = 1
        
        pos_x, pos_y = 2, 15
        ordem = ["letra_T", "letra_E", "letra_T", "letra_R", "letra_I", "letra_C", "letra_O"]
        
        for index, letra in enumerate(ordem):
            formato = SHAPES_TITULO[letra]["formato"]    
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                            self.desenhar_shape_como_letra(
                                pos_x + (i_coluna * TILE) - offset_x,
                                pos_y + (i_linha * TILE), 
                                (spritesheet_x[index] - acertar_imagem, 0)
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
        pos_x = CENTRALIZAR(FONT_20, texto, LARGURA_TELA) - offset_x
        pos_y = 115
        px.text(pos_x, pos_y, texto, COR_PRINCIPAL_ALEATORIA + 8, FONT_20)
    
    #
    
    def desenhar_todos_botoes_menu(self, offset_x, offset_entre_menus):
        centro_y = LARGURA_TELA * (3 / 4)
        
        self.desenhar_botao_entrada(centro_y, offset_entre_menus)
        self.desenhar_botoes_principal(centro_y, offset_entre_menus)
        if self.profundidade_menu >= 1:
            self.desenhar_botoes_submenus(centro_y, offset_entre_menus, offset_x)  
    
    def desenhar_botao_entrada(self, centro_y, offset_entre_menus):
        pos_y = centro_y - (ALTURA_DA_FONTE_11 / 2)
        self.desenhar_texto_dos_botoes(
            (0, pos_y), 
            LARGURA_TELA, self.frase_entrada, True, FONT_11,
            offset_x=offset_entre_menus,
            offset_y=0
        )
    
    def desenhar_botoes_principal(self, centro_y, offset_entre_menus):
        frases = self.frases_menu_principal
        espacamento = 30
        
        opcoes_ativas = self.quantidades_opcoes_menus["principal"]
        itens_visiveis = min(5, len(opcoes_ativas))
        altura_total = (itens_visiveis - 1) * (espacamento) + ALTURA_DA_FONTE_11
        
        pos_y = centro_y - altura_total / 2
        if self.profundidade_menu == 1:
            self.calcular_animacao_scroll(1, opcoes_ativas, itens_visiveis)
        
        for (frase, ativo) in zip(frases, opcoes_ativas):
            self.desenhar_texto_dos_botoes(
                (LARGURA_TELA, pos_y), 
                LARGURA_TELA, frase, ativo, FONT_11,
                espacamento=espacamento,
                profundidade_menu=1,
                offset_x=offset_entre_menus,
                offset_y=self.offset_menu["scroll"][1]
            )
            pos_y += espacamento
        
    def desenhar_botoes_submenus(self, centro_y, offset_entre_menus, offset_x):
        frases = self.frases_submenus
        proximo_menu = list(frases.keys())[self.opcao_atual_menu[1]]
        espacamento = frases[proximo_menu][1]
        
        frases_atuais = frases[proximo_menu][0]
        opcoes_ativas = self.quantidades_opcoes_menus[proximo_menu]
        itens_visiveis = min(5, len(opcoes_ativas))     
        altura_total =  (itens_visiveis - 1) * espacamento + ALTURA_DA_FONTE_11

        if self.profundidade_menu == 2:
            self.calcular_animacao_scroll(2, opcoes_ativas, itens_visiveis)
        
        somas_y = [0, 9, 9, 9, 0, 0]
        somar_y = somas_y[self.opcao_atual_menu[1]]
        
        pos_y = centro_y - (altura_total / 2) 
        for (frase, ativo) in zip(frases_atuais, opcoes_ativas):
            self.desenhar_texto_dos_botoes(
                ((LARGURA_TELA * 2), pos_y), 
                LARGURA_TELA, frase, ativo, FONT_11,
                somar_y=somar_y,
                espacamento=espacamento,
                profundidade_menu=2,
                offset_x=offset_entre_menus + offset_x,
                offset_y=self.offset_menu["scroll"][2]
            )
            pos_y += espacamento
    
    #//// PAUSE ////
    
    def desenhar_shapes_fundo_pause(self, offset_x):
        formato = self.pos_shapes_fundo_pause
        y_soma = 0 
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        y = self.tipo_shapes_fundo_pause[y_soma]
                        y_soma += 1
                        self.desenhar_shape_como_letra(
                            (-self.distancia_do_pause + offset_x) + (i_coluna * TILE),
                            (i_linha * TILE), 
                            (COR_PRINCIPAL_ALEATORIA - 1, y)
                        )   
    
    #
    
    def desenhar_tudo_pause(self, offset_x):
        centro_y = LARGURA_TELA * (3 / 4)
        extra_x = 2
        
        self.desenhar_shapes_fundo_pause(offset_x)
        self.desenhar_botao_titulo(extra_x, offset_x)
        self.desenhar_botoes_pause(centro_y, extra_x, offset_x)
    
    def desenhar_botao_titulo(self, extra_x, offset_x):
        if self.frase_titulo_pause == "PAUSED":
            pos_y = (LARGURA_TELA/4) - (ALTURA_DA_FONTE_11/2)
        else:
            pos_y = (LARGURA_TELA/4) - ALTURA_DA_FONTE_11
        
        self.desenhar_texto_dos_botoes(
            (-self.distancia_do_pause, pos_y),
            (self.distancia_do_pause + extra_x), self.frase_titulo_pause, True, FONT_11,
            offset_x=-offset_x,
            offset_y=0,
            min=-2, max=3
        )
    
    def desenhar_botoes_pause(self, centro_y, extra_x, offset_x):
        frases = self.frases_pause
        espacamento = 30
        
        opcoes_ativas = self.quantidades_opcoes_pause
        itens_visiveis = min(5, len(opcoes_ativas))
        altura_total = (itens_visiveis - 1) * (espacamento) + ALTURA_DA_FONTE_11
        
        self.calcular_animacao_scroll(1, opcoes_ativas, itens_visiveis)
        
        pos_y = centro_y - altura_total / 2
        for (frase, ativo) in zip(frases, opcoes_ativas):
            self.desenhar_texto_dos_botoes(
                (-self.distancia_do_pause, pos_y), 
                (self.distancia_do_pause + extra_x), frase, ativo, FONT_11,
                espacamento=espacamento,
                offset_x=-offset_x,
                offset_y=0)
            pos_y += espacamento        
        
    #//// RECTS ////
    
    def calcular_comprimento_rect_direito(self):
        extra = 0
        comprimento = TILE * (self.shapes_visiveis * (self.distancia_entre_shapes_proximos + extra) + (self.distancia_inicial_shapes_proximos + extra))
        return comprimento
    
    def desenhar_rect(self, pos_x, pos_y, largura, comprimento, cor, *, mov_x=0, mov_esquerda=0, mov_direita=0, mov_y=0):
        px.rect(
            (TILE * (mov_esquerda + mov_direita + mov_x)) + pos_x, 
            (TILE * mov_y) + pos_y, 
            largura, comprimento, 
            cor
        )
    
    #
    
    def desenhar_todos_rects(self, mov_esquerda, mov_direita, mov_y, *, offset_x):
        margem = 4
        largura_final = BOARD_X - (margem * 2)
        self.rects_da_esquerda(margem, largura_final, mov_esquerda, mov_y, offset_x)
        self.rects_da_direita(margem, largura_final, mov_direita, mov_y, offset_x)
    
    def rects_da_esquerda(self, margem, largura, mov_esquerda, mov_y, offset_x):
        if self.shape_segurado != None:
            imagem_do_shape_segurado = SHAPES[self.shape_segurado]["imagem_pos"] + 1
        else:
            imagem_do_shape_segurado = 0
        
        self.desenhar_rect(
            margem + offset_x, 0, 
            largura, 4, 
            imagem_do_shape_segurado, 
            mov_esquerda=mov_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset_x, margem, 
            largura, largura, 
            0, 
            mov_esquerda=mov_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset_x, largura + (margem * 2), 
            largura, self.comprimento_rect_esquerdo_1, 
            0, 
            mov_esquerda=mov_esquerda,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            margem + offset_x, largura + self.comprimento_rect_esquerdo_1 + (margem * 3), 
            largura, self.comprimento_rect_esquerdo_2, 
            0, 
            mov_esquerda=mov_esquerda,
            mov_y=mov_y
        )
    
    def rects_da_direita(self, margem, largura, mov_direita, mov_y, offset_x):
        pos_x = ((TILE * 10) + BOARD_X) + margem
        comprimento_dir = self.calcular_comprimento_rect_direito()
        
        self.desenhar_rect(
            pos_x + offset_x, 0, 
            largura, 4,
            SHAPES[self.proximos_shapes[0]]["imagem_pos"] + 1,
            mov_direita=mov_direita,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            pos_x + offset_x, margem, 
            largura, comprimento_dir,
            0,
            mov_direita=mov_direita,
            mov_y=mov_y
        )
        
        self.desenhar_rect(
            pos_x + offset_x, comprimento_dir + (margem * 2), 
            largura, self.comprimento_rect_direito,
            0,
            mov_direita=mov_direita,
            mov_y=mov_y
        )

    #//// TEXTOS ////
    
    def desenhar_texto(self, pos, largura, frase, cor, *, mov_esquerda=0, mov_direita=0, mov_y, offset_x=0):
        pos_x, pos_y = pos
        px.text(
            (TILE * (mov_esquerda + mov_direita)) + pos_x + CENTRALIZAR(FONT_10, frase, largura) + offset_x, 
            (TILE * mov_y) + pos_y, 
            frase, cor, FONT_10
        )
    
    #
    
    def desenhar_todos_textos(self, mov_esquerda, mov_direita, mov_y, *, offset_x):
        cor = CORES_ALEATORIAS_TETRIS
        self.textos_da_esquerda((ALTURA_DA_FONTE_10 / 2), BOARD_X, cor, mov_esquerda, mov_y, offset_x)
        self.textos_da_direita((ALTURA_DA_FONTE_10 / 2), BOARD_X, mov_direita, mov_y, offset_x)
    
    def textos_da_esquerda(self, altura_da_fonte, largura, cor, mov_esquerda, mov_y, offset_x):
        espaco = 8
        espacamento = altura_da_fonte + espaco
        espacamento_entre_valores = altura_da_fonte + 3
        offset_fonte = 1
        
        pos_y_1 = 80 - offset_fonte
        
        frases_esqueda_1 = [
            (f"{self.tempo_formatado()}", None),
            ("LINES", f"{self.linhas_limpas}"),
            ("LEVEL",  f"{self.nivel_atual}"),
            ("SCORE", f"{self.pontos_atual}"),
        ]
        
        pos_y_1 += espaco
        for index, (frase, valor) in enumerate(frases_esqueda_1):
            self.desenhar_texto((0, pos_y_1), largura, frase, cor[index], mov_esquerda=mov_esquerda, mov_y=mov_y, offset_x=offset_x)
            
            if valor != None:
                pos_y_1 += espacamento_entre_valores
                self.desenhar_texto((0, pos_y_1), largura, valor, cor[index], mov_esquerda=mov_esquerda, mov_y=mov_y, offset_x=offset_x)
            pos_y_1 += espacamento
        self.comprimento_rect_esquerdo_1 = pos_y_1 - 80 + offset_fonte
        
        #/
        
        margem =  4
        pos_y_2 = (80 - offset_fonte) + self.comprimento_rect_esquerdo_1 + margem
        
        cor_combo = cor[4] if self.combo_atual >= 1 else 0
        cor_streak = cor[5] if self.back_to_back_atual >= 1 else 0
        
        frases_esqueda_2 = [
            ("COMBO", f"{self.combo_atual}x"),
            ("STREAK", f"{self.back_to_back_atual}x")
        ]
        
        pos_y_2 += espaco
        for (frase, valor) in frases_esqueda_2:
            cor_final = cor_combo if frase == "COMBO" else cor_streak        
            self.desenhar_texto((0, pos_y_2), largura, frase, cor_final, mov_esquerda=mov_esquerda, mov_y=mov_y, offset_x=offset_x)
            pos_y_2 += espacamento_entre_valores
            self.desenhar_texto((0, pos_y_2), largura, valor, cor_final, mov_esquerda=mov_esquerda, mov_y=mov_y, offset_x=offset_x)
            pos_y_2 += espacamento
        self.comprimento_rect_esquerdo_2 = pos_y_2 - ((80 - offset_fonte) + self.comprimento_rect_esquerdo_1 + margem)
    
    def textos_da_direita(self, altura_da_fonte, largura, mov_direita, mov_y, offset_x):
        espaco = 8
        espacamento = altura_da_fonte + espaco
        
        pos_x = ((TILE * 10) + BOARD_X)
        comprimento_dir = self.calcular_comprimento_rect_direito()
        pos_y = comprimento_dir 
        
        match self.modo_do_jogo:
            case "marathon_150": frase = "MARATHON"
            case "40_lines": frase = "40 LINES"
            case "ultra": frase = "ULTRA"
            case "crazy": frase = "CRAZY"
            case "zen": frase = "ZEN"
        
        pos_y += espacamento
        self.desenhar_texto((pos_x, pos_y), largura, frase, COR_PRINCIPAL_ALEATORIA, mov_direita=mov_direita, mov_y=mov_y, offset_x=offset_x)
        self.comprimento_rect_direito = pos_y - comprimento_dir + (espacamento / 2)
   
    #//// TEXTOS - STATUS E POPUPS ////
            
    def desenhar_texto_estatisticas(self, status, pos_x=0, pos_y=0, *, mov_y, offset_x):
        frases_status = status
        cor = CORES_ALEATORIAS_TETRIS
        cores = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 1,
            5: 1,
            6: 2,
            7: 2,
            8: 3,
            9: 3,
            10: 3,
            11: 3,
            12: 4,
            13: 4,
            14: 5,
            15: 5,
            16: 6,
            17: 6,
        }
            
        espacamento = 17
        espacamento_entre_valores = 13

        altura_total = (len(frases_status)) * espacamento - (espacamento / 2)
        meio_da_tela = ((TILE * LINHAS) / 2) - (altura_total / 2)
        
        pos_y += meio_da_tela
        
        for index, (chave, valor) in enumerate(status.items()):
            cor_index = cores[index]
            px.text((pos_x + espacamento_entre_valores) + offset_x, pos_y + (mov_y * TILE), f"{chave}:", cor[cor_index], FONT_10)
            px.text((pos_x + espacamento_entre_valores) + offset_x + FONT_10.text_width(f"{chave}:"), pos_y + (mov_y * TILE), valor, cor[cor_index], FONT_10)
            pos_y += espacamento
    
    def desenhar_popups(self, mov_x, offset_x):
        largura = TILE * LINHAS
        duracao_max = 130
        
        pos_inicial = 210
        extra = 30
        range_animacao = pos_inicial + ALTURA_DA_FONTE_10 + extra
            
        constante = 3 
        bit = 8
                
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
            
            progresso = (duracao_max - duracao) / duracao_max # 1.0 a 0.0
            fator = (progresso/2) + 1 * (progresso ** constante)
            pos_y = round((pos_inicial / bit) - int(fator * range_animacao) / bit) * bit
            
            p = 1
            if 0.4 < progresso:
                p -= progresso
            
            px.dither(p)
            px.text((mov_x * TILE) + CENTRALIZAR(FONT_10, frase, largura) + offset_x, pos_y, frase, cor, FONT_10)
            px.dither(1)
            
            if not self.esta_pausado:
                evento[2] -= 1
            
            if duracao == 0:
                self.sequencia_dos_eventos.remove(evento)
    
    #//// OFFSET - TETO ////

    def posicao_y_acima_do_teto(self, formato):
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    match self.shape_pos_atual[1] + i_linha:
                        case -3: return -3
                        case -2: return -2
                        case -1: return -1
        return 0
    
    def calcular_offset_teto(self):
        pos_y_alto = self.posicao_y_acima_do_teto(self.pegar_formato())
        if pos_y_alto < 0:
            return abs(pos_y_alto)
        return 0
    
    def calcular_offset_teto_gameover(self):
        for linha_i in range(CORRECAO_ALTURA):
            for espaco in self.mapa[linha_i]:
                if espaco != VAZIO:
                    return CORRECAO_ALTURA - linha_i
        return 0
    
    #//// FUNCOES DE DESENHAR - PYXEL ////
    
    def desenhar_fundo(self, pos, spritesheet_pos, tamanho, *, mov_x, mov_y, offset_x, colkey=None):
        pos_x, pos_y = pos
        spritesheet_x, spritesheet_y = spritesheet_pos
        largura, comprimento = tamanho
        px.bltm(
            (TILE * mov_x) + pos_x + offset_x,
            (TILE * mov_y) + pos_y, 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            (TILE * largura), (TILE * comprimento),
            colkey=colkey,
        )
    
    def desenhar_shape(self, coluna_x, linha_y, spritesheet_pos, *, mov_x, mov_y, offset_x, offset_y):
        spritesheet_x, spritesheet_y = spritesheet_pos
        px.blt(
            (TILE * (coluna_x + mov_x)) + offset_x + BOARD_X, 
            (TILE *  (linha_y + mov_y + offset_y)), 
            0, 
            (TILE * spritesheet_x), (TILE * spritesheet_y), 
            TILE, TILE,
            colkey=0
        )

    #//// DESENHAR SHAPES - PRINCIPAIS ////
    
    def desenhar_shape_fantasma(self, formato, mov_x, mov_y, offset_x, offset_y):
        if not self.mostrar_fantasma_config:
            return
        
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        pos_x, pos_y = self.shape_pos_fantasma            
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            pos_x + i_coluna,
                            pos_y + i_linha, 
                            (spritesheet_x, 1),
                            mov_x=mov_x,
                            mov_y=mov_y,
                            offset_x=offset_x,
                            offset_y=offset_y
                        )
    
    def desenhar_shape_atual(self, formato, pos, mov_x, mov_y, offset_x, offset_y):
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        pos_x, pos_y = pos
        
        self.visual_pos_x, self.visual_pos_y = self.calcular_animacao_shapes(True, pos_x, pos_y, self.visual_pos_x, self.visual_pos_y)
        
        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            self.visual_pos_x + i_coluna,
                            self.visual_pos_y + i_linha, 
                            (spritesheet_x, 0),
                            mov_x=mov_x,
                            mov_y=mov_y,
                            offset_x=offset_x,
                            offset_y=offset_y
                        )
    
    def desenhar_shapes_fixados(self, mapa, mov_x, mov_y, offset_x, offset_y):
        for linha in range(0, ALTURA_DO_JOGO):
            for coluna in range(COLUNAS):
                if mapa[linha][coluna] != VAZIO:
                    cor = mapa[linha][coluna]
                    spritesheet_x = COR_IMAGEM[cor]
                    
                    self.desenhar_shape(
                        coluna,
                        linha - CORRECAO_ALTURA,
                        (spritesheet_x, 0),
                        mov_x=mov_x,
                        mov_y=mov_y,
                        offset_x=offset_x,
                        offset_y=offset_y
                    )
    
    #//// DESENHAR SHAPES - PROXIMOS E SEGURADOS ////
    
    def desenhar_shapes_proximos(self, proximos_shapes, mov_direita, mov_y, offset_x, offset_y):
        ajustar_valor_x = 10.5
        ajustar_valor_y = 0.25 + 0.5
        acrescimo_distancia = ajustar_valor_y
        
        for proximo_shape in proximos_shapes:
            aumentar = 0.5 if proximo_shape in SHAPES_1_DE_LARGURA else 0
            
            spritesheet_x = SHAPES[proximo_shape]["imagem_pos"]
            formato = SHAPES_PROXIMOS_SEGURADO[proximo_shape]["formato"]
 
            for i_linha, e_linha in enumerate(formato):
                for i_coluna, _ in enumerate(e_linha):
                    if formato[i_linha][i_coluna] == 1:
                        self.desenhar_shape(
                            ajustar_valor_x     + i_coluna + SHAPES_PROXIMOS_SEGURADO[proximo_shape]["centralizado"][0],
                            acrescimo_distancia + i_linha  + aumentar,
                            (spritesheet_x, 0),
                            mov_x=mov_direita,
                            mov_y=mov_y,
                            offset_x=offset_x,
                            offset_y=offset_y
                        )
            acrescimo_distancia += self.distancia_entre_shapes_proximos
    
    def desenhar_shape_segurado(self, shape_segurado, mov_esquerda, mov_y, offset_x, offset_y):
        ajustar_valor_x = -3.5
        
        inicio, fim = 0.25, 4.5
        ajustar_valor_y = inicio + (fim / 2) - 1
        
        aumentar = -0.5 if self.shape_segurado in SHAPES_1_DE_LARGURA else 0
        
        spritesheet_x = SHAPES[shape_segurado]["imagem_pos"]
        formato = SHAPES[shape_segurado]["formato"]

        for i_linha, e_linha in enumerate(formato):
            for i_coluna, _ in enumerate(e_linha):
                if formato[i_linha][i_coluna] == 1:
                    self.desenhar_shape(
                        ajustar_valor_x + i_coluna + SHAPES_PROXIMOS_SEGURADO[shape_segurado]["centralizado"][1], 
                        ajustar_valor_y + i_linha + aumentar, 
                        (spritesheet_x, 0),
                        mov_x=mov_esquerda,
                        mov_y=mov_y,
                        offset_x=offset_x,
                        offset_y=offset_y
                    )
    
    #//// ANIMACAO - LINHA LIMPA E HARD DROP ////
    
    def desenhar_animacao_limpar_linha(self, mov_x, mov_y, offset_x, offset_y):
        def _animacao_de_limpar_linha(start, end, constante, *, constante_na_pos_x=0):
            for localizacao in self.localizacao_linhas_limpas:
                for pos_x in range(start, end - constante):
                    self.desenhar_shape(
                        pos_x + constante_na_pos_x,
                        localizacao,
                        (spritesheet_x, 0),
                        mov_x=mov_x,
                        mov_y=mov_y, 
                        offset_y=offset_y,
                        offset_x=offset_x,
                    )
        
        spritesheet_x = SHAPES[self.shape_atual]["imagem_pos"]
        partes = 7
        tempo_divido = self.are_duracao // partes

        if not self.esta_pausado:
            if self.tempo_animacao_limpar_linha > tempo_divido * (self.constante_animacao_limpar_linha + 1):
                self.constante_animacao_limpar_linha += 1
            else:
                self.tempo_animacao_limpar_linha += 1
            
        constante = self.constante_animacao_limpar_linha
        if self.tipo_t_spin == None:
            _animacao_de_limpar_linha(0,       COLUNAS // 2, constante, constante_na_pos_x=constante)
            _animacao_de_limpar_linha(COLUNAS // 2, COLUNAS, constante)
        else:
            _animacao_de_limpar_linha(0,       COLUNAS // 2, constante)
            _animacao_de_limpar_linha(COLUNAS // 2, COLUNAS, constante, constante_na_pos_x=constante)
    
    def desenhar_animacao_hard_drop(self, mov_x, mov_y, offset_x):
        diminuicao = 2.1
        duracao_total = 0.4
        duracao_diminuicao = 0.4
        duracao_max = 20
        
        for variaveis in self.estados_animacao_hard_drop:
            (formato, pos), duracao = variaveis[0], variaveis[1]
            
            if duracao <= 0:
                self.estados_animacao_hard_drop.remove(variaveis)
                continue
            
            largura = set()
            for linha in formato:
                for i, cel in enumerate(linha):
                    if cel == 1:
                        largura.add(i)
            
            lar_max = max(largura)
            lar_min = min(largura)
            #
            um_por_linha = 0
            linha_com_mais_um = 0
            for index, linha in enumerate(formato):
                if linha.count(1) >= um_por_linha:
                    um_por_linha = linha.count(1)
                    linha_com_mais_um = index
            
            largura = lar_max - lar_min + 1
            comprimento = (pos[1] + linha_com_mais_um)      
            
            x = BOARD_X + ((pos[0] + lar_min) * TILE)    
            fator = duracao_diminuicao * (1 - duracao / duracao_max)
            
            px.dither(duracao_total - fator)
            self.desenhar_rect(
                x + offset_x, self.calcular_offset_teto() * TILE ,
                largura * TILE, comprimento * TILE,
                8,
                mov_x=mov_x,
                mov_y=mov_y,
            )
            px.dither(1)
            
            variaveis[1] -= diminuicao
    
    #//// ANIMACAO - INTERPOLAÇÃO ////
    
    def calcular_animacao_scroll(self, profundidade_menu, opcoes_ativas, itens_visiveis):
        if len(opcoes_ativas) > 5:
            if self.opcao_atual_menu[profundidade_menu] > (len(opcoes_ativas) - 3):
                scroll = max(0, len(opcoes_ativas) - 5)
            else:
                scroll = max(0, self.opcao_atual_menu[profundidade_menu] - (itens_visiveis - 3))   
            
            velocidade = 0.1
            scroll = min(scroll, len(opcoes_ativas) - itens_visiveis)
            valor = self.offset_menu["scroll"][profundidade_menu]
            self.offset_menu["scroll"][profundidade_menu] = self.calcular_interpolacao(valor, scroll, velocidade, 0.01)
    
    def calcular_animacao_entre_menu(self):
        destino_x = (self.profundidade_menu * LARGURA_TELA)
        velocidade = 0.1
        valor = self.offset_menu["entre_menus"]
        self.offset_menu["entre_menus"] = self.calcular_interpolacao(valor, destino_x, velocidade, 1)
    
    def calcular_animacao_entre_menu_e_jogo(self):
        destino_x = LARGURA_TELA
        velocidade = 0.1
        valor = self.offset_menu["entre_menu_e_jogo"]
        self.offset_menu["entre_menu_e_jogo"] = self.calcular_interpolacao(valor, destino_x, velocidade, 1)
    
    def calcular_animacao_gameover_slide(self):
        condicao_animacao_offset_teto = (self.offset_em_jogo["teto"] != self.calcular_offset_teto_gameover() and not self.clicou_em_resetar_partida)
        condicao_animacao_hard_drop_e_popups = (len(self.estados_animacao_hard_drop) > 0 or len(self.sequencia_dos_eventos) > 0)
        if self.mov_em_jogo["mov_hard_drop"] > 0 or condicao_animacao_offset_teto or condicao_animacao_hard_drop_e_popups:
            self.mov_slide_gameover = 0
            return
        
        self.velocidade_slide_gameover = min(self.velocidade_slide_gameover + 0.001, 0.05)
        velocidade = self.velocidade_slide_gameover
        valor = self.mov_slide_gameover
        
        if not self.clicou_em_resetar_partida:
            destino_y = (LINHAS + 1)
            self.mov_slide_gameover = min(self.calcular_interpolacao(valor, destino_y, velocidade, 0.01), destino_y)  
        else:
            destino_y = 0
            self.mov_slide_gameover = max(self.calcular_interpolacao(valor, destino_y, velocidade, 0.01), destino_y)
    
    #
    
    def calcular_animacao_shapes(self, sinalizador, pos_x, pos_y, visual_pos_x, visual_pos_y):
        vel_x = self.visual_vel_x  # lateral mais suave
        vel_y = self.visual_vel_y  # queda mais rápida
        
        if sinalizador:
            visual_pos_x = self.calcular_interpolacao(visual_pos_x, pos_x, vel_x, 0.1)
            visual_pos_y = self.calcular_interpolacao(visual_pos_y, pos_y, vel_y, 0.1)
            return visual_pos_x, visual_pos_y
        return pos_x, pos_y
    
    def calcular_animacao_pausado(self):
        if not self.esta_pausado or self.esta_despausando:
            destino_x = 0
        elif self.esta_pausado:
            destino_x = self.distancia_do_pause 

        velocidade = 0.1
        valor = self.offset_em_jogo["pause"]
        self.offset_em_jogo["pause"] = self.calcular_interpolacao(valor, destino_x, velocidade, 1)
    
    def calcular_animacao_offset_teto(self, offset_abs):
        destino_y = offset_abs
        velocidade = 0.3
        valor = self.offset_em_jogo["teto"]
        self.offset_em_jogo["teto"] = self.calcular_interpolacao(valor, destino_y, velocidade, 0.1)
        return self.offset_em_jogo["teto"]
    
    def calcular_animacao_status(self, sianlizador, offset_tipo):
        if sianlizador:
            destino_x = (LARGURA_TELA / 2)
        else:
            destino_x = 0

        velocidade = 0.13
        valor = offset_tipo
        return self.calcular_interpolacao(valor, destino_x, velocidade, 1)
    
    #
    
    def valores_offset_entre_menu_e_jogo(self):
        self.calcular_animacao_entre_menu_e_jogo()
        if self.confirmacao_valor["voltar"] == 1:
            # MENU <--- JOGO
            backup = self.offset_em_jogo["pause"]
            offset_x = self.offset_menu["entre_menu_e_jogo"] + backup
            offset_x_do_menu = LARGURA_TELA - self.offset_menu["entre_menu_e_jogo"]
        else:
            # MENU ---> JOGO
            offset_x = LARGURA_TELA - self.offset_menu["entre_menu_e_jogo"]    
            offset_x_do_menu = self.offset_menu["entre_menu_e_jogo"]
        return offset_x, offset_x_do_menu
    
    #//// ANIMACAO - GERAL ////
    
    def calcular_valores_das_animacoes(self):
        inicio = self.movimento_inicio_config
        constante = self.movimento_constante_config
        
        if self.foi_esquerda:
            self.mov_em_jogo["mov_direita"] = 0
            if self.mov_em_jogo["mov_esquerda"] > -self.movimento_duracao:
                self.mov_em_jogo["mov_esquerda"] += -(inicio + abs(self.mov_em_jogo["mov_esquerda"]) * constante)
                self.mov_em_jogo["mov_esquerda"] = max(self.mov_em_jogo["mov_esquerda"], -self.movimento_duracao)
                self.mov_em_jogo["mov_x"] = self.mov_em_jogo["mov_esquerda"]
        else:
            if self.mov_em_jogo["mov_esquerda"] < 0:
                self.mov_em_jogo["mov_esquerda"] -= -(inicio + abs(self.mov_em_jogo["mov_esquerda"]) * constante)
                self.mov_em_jogo["mov_x"] = self.mov_em_jogo["mov_esquerda"]
                
                if abs(self.mov_em_jogo["mov_esquerda"]) < 0.5:
                    self.mov_em_jogo["mov_esquerda"] = 0
                    self.mov_em_jogo["mov_x"] = 0
        
        if self.foi_direita:
            self.mov_em_jogo["mov_esquerda"] = 0
            if self.mov_em_jogo["mov_direita"] < self.movimento_duracao:
                self.mov_em_jogo["mov_direita"] += (inicio + abs(self.mov_em_jogo["mov_direita"]) * constante)
                self.mov_em_jogo["mov_direita"] = min(self.mov_em_jogo["mov_direita"], self.movimento_duracao)
                self.mov_em_jogo["mov_x"] = self.mov_em_jogo["mov_direita"]
        else:
            if self.mov_em_jogo["mov_direita"] > 0:
                self.mov_em_jogo["mov_direita"] -= (inicio + abs(self.mov_em_jogo["mov_direita"]) * constante)
                self.mov_em_jogo["mov_x"] = self.mov_em_jogo["mov_direita"]
                
                if abs(self.mov_em_jogo["mov_direita"]) < 0.5:
                    self.mov_em_jogo["mov_direita"] = 0
                    self.mov_em_jogo["mov_x"] = 0   
        
        if self.acionou_hard_drop:
            if self.mov_em_jogo["mov_hard_drop"] < (self.movimento_duracao - 1): # diminui 1
                self.mov_em_jogo["mov_hard_drop"] += (inicio + abs(self.mov_em_jogo["mov_hard_drop"]) * constante)
                self.mov_em_jogo["mov_hard_drop"] = min(self.mov_em_jogo["mov_hard_drop"], (self.movimento_duracao - 1)) # diminui 1
            else:
                self.acionou_hard_drop = False
        else:
            if self.mov_em_jogo["mov_hard_drop"] > 0:
                self.mov_em_jogo["mov_hard_drop"] -= (inicio + abs(self.mov_em_jogo["mov_hard_drop"]) * constante)
            else:
                self.mov_em_jogo["mov_hard_drop"] = 0
    
    def valores_movimentos(self):
        mov_x = TRANSFORMAR_EM_DECIMAL(self.mov_em_jogo["mov_x"])
        mov_esquerda = TRANSFORMAR_EM_DECIMAL(self.mov_em_jogo["mov_esquerda"])
        mov_direita = TRANSFORMAR_EM_DECIMAL(self.mov_em_jogo["mov_direita"])
        mov_hard_drop = TRANSFORMAR_EM_DECIMAL(self.mov_em_jogo["mov_hard_drop"])
        return mov_x, mov_esquerda, mov_direita, mov_hard_drop, self.mov_slide_gameover
    
    #//// ENCAPSULAMENTO - GERAL ////
    
    def desenhar_shape_segurado_e_proximos(self, mov_esquerda, mov_direita, mov_y, offset_x, offset_y=0):
        self.desenhar_shapes_proximos(self.proximos_shapes, mov_direita, mov_y, offset_x, offset_y)
        if self.shape_segurado != None:
            self.desenhar_shape_segurado(self.shape_segurado, mov_esquerda, mov_y, offset_x, offset_y)
    
    def desenhar_tabuleiro_e_teto(self, mov_x, mov_y, offset_x, offset_y):
        self.desenhar_fundo((BOARD_X, 0), (0, 0), (COLUNAS, LINHAS), mov_x=mov_x, mov_y=mov_y, offset_x=offset_x)
        if offset_y > 0:
            px.dither(0.6)
            self.desenhar_fundo((BOARD_X, 0), (0, LINHAS * 2), (COLUNAS, offset_y), mov_x=mov_x, mov_y=mov_y, offset_x=offset_x)
            px.dither(1)
    
    def desenhar_todos_rects_textos(self, offset_x):
        mov_x, mov_esquerda, mov_direita, mov_hard_drop, mov_slide_gameover = self.valores_movimentos()
        self.desenhar_todos_rects(mov_esquerda, mov_direita, mov_slide_gameover, offset_x=offset_x)
        self.desenhar_todos_textos(mov_esquerda, mov_direita, mov_slide_gameover, offset_x=offset_x)

    #
    
    def desenhar_tudo_da_partida(self, offset_x, offset_y_teto, mov_x, mov_y):
        self.desenhar_tabuleiro_e_teto(mov_x, mov_y, offset_x, offset_y_teto)
        if self.acionou_hard_drop or len(self.estados_animacao_hard_drop) > 0:
            self.desenhar_animacao_hard_drop(mov_x, mov_y, offset_x)
        if not self.esta_em_are and self.desenhar_shape_apos_colisao:
            self.desenhar_shape_fantasma(self.pegar_formato(), mov_x, mov_y, offset_x, offset_y_teto)
            self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual, mov_x, mov_y, offset_x, offset_y_teto)
        if self.limpou_linha:
            self.desenhar_animacao_limpar_linha(mov_x, mov_y, offset_x, offset_y_teto)
        self.desenhar_shapes_fixados(self.mapa, mov_x, mov_y, offset_x, offset_y_teto)
    
    def desenhar_tudo_em_jogo(self, offset_x):
        offset_y_teto = self.calcular_animacao_offset_teto(self.calcular_offset_teto())
        mov_x, mov_esquerda, mov_direita, mov_hard_drop, mov_slide_gameover = self.valores_movimentos()
        self.desenhar_tudo_da_partida(offset_x, offset_y_teto, mov_x, mov_hard_drop)
        
        self.desenhar_shape_segurado_e_proximos(mov_esquerda, mov_direita, 0, offset_x)
        self.desenhar_popups(mov_x, offset_x)
          
    def desenhar_tudo_em_game_over(self, offset_x):
        offset_y_teto = self.calcular_animacao_offset_teto(self.calcular_offset_teto_gameover())
        mov_x, mov_esquerda, mov_direita, mov_hard_drop, mov_slide_gameover = self.valores_movimentos()
        if mov_hard_drop > 0:
            self.desenhar_tudo_da_partida(offset_x, offset_y_teto, mov_x, mov_hard_drop)
        else:
            self.desenhar_tudo_da_partida(offset_x, offset_y_teto, mov_x, mov_slide_gameover)
        
        if self.clicou_em_resetar_partida:
            self.desenhar_shape_fantasma(self.pegar_formato(), mov_x, mov_slide_gameover, offset_x, offset_y_teto)
            self.desenhar_shape_atual(self.pegar_formato(), self.shape_pos_atual, mov_x, mov_slide_gameover, offset_x, offset_y_teto)
        
        self.desenhar_shape_segurado_e_proximos(mov_esquerda, mov_direita, mov_slide_gameover, offset_x)
        self.desenhar_popups(mov_x, offset_x)
        
        px.dither(0.9)
        self.desenhar_rect(BOARD_X + offset_x, ((-LINHAS - 1) * TILE), (COLUNAS * TILE), LARGURA_TELA, 0, mov_y=mov_slide_gameover)
        px.dither(1)
        self.desenhar_texto_estatisticas(self.informacoes_status_da_partida, BOARD_X, ((-LINHAS - 1) * TILE), mov_y=mov_slide_gameover, offset_x=offset_x)
    
    #//// ENCAPSULAMENTO - MENU E PAUSE ////
    
    def desenhar_menu(self, offset_x):
        self.calcular_animacao_entre_menu() 
        
        px.dither(0.1)
        px.rect(-offset_x, (LARGURA_TELA/2), LARGURA_TELA, (LARGURA_TELA/2), 8)
        px.dither(1)
        
        if self.menu_ativo == "recentes" and len(self.historico_partidas) == 0:
            px.dither(0.1)
            px.rect((LARGURA_TELA - offset_x), (LARGURA_TELA/2), LARGURA_TELA, (LARGURA_TELA/2), 8)
            px.dither(0.4)
            px.rect((LARGURA_TELA - offset_x), 0, LARGURA_TELA, (LARGURA_TELA/2), 8)
            px.dither(1)  
        
        self.desenhar_todos_botoes_menu(offset_x, self.offset_menu["entre_menus"])
        
        px.rect(-offset_x, 0, LARGURA_TELA, (LARGURA_TELA/2), 0)
        px.dither(0.4)
        px.rect(-offset_x, 0, LARGURA_TELA, (LARGURA_TELA/2), 8)
        px.dither(1)
        
        self.desenhar_titulo_menu(offset_x)
        
        if self.menu_ativo == "recentes":
            if len(self.historico_partidas) > 0:
                status = self.historico_partidas[self.opcao_atual_menu[2] - 1]
                self.desenhar_rect((LARGURA_TELA - offset_x), 0, (COLUNAS * TILE), LARGURA_TELA, 0)
                self.desenhar_texto_estatisticas(status, LARGURA_TELA, 0, mov_y=0, offset_x=-offset_x)
    
    def desenhar_pause(self, offset_x):
        if self.mov_em_jogo["mov_esquerda"] < 0:
            self.foi_esquerda = False
            
        px.rect((-self.distancia_do_pause + offset_x), 0, self.distancia_do_pause, LARGURA_TELA, 0)
        
        px.dither(0.1)
        px.rect((-self.distancia_do_pause + offset_x), (LARGURA_TELA/2), self.distancia_do_pause, LARGURA_TELA, 8)
        px.dither(1)
        
        px.dither(0.4)
        px.rect((-self.distancia_do_pause + offset_x), 0, self.distancia_do_pause, (LARGURA_TELA/2), COR_PRINCIPAL_ALEATORIA + 8)
        px.dither(1)
        
        self.desenhar_tudo_pause(offset_x)
        
        self.offset_em_jogo["status"] = self.calcular_animacao_status(self.mostrar_status_pause, self.offset_em_jogo["status"])
        offset_entre_menu_e_jogo = self.offset_menu["entre_menu_e_jogo"]
        offset_x_status = self.offset_em_jogo["status"]
        self.desenhar_rect(LARGURA_TELA + (offset_entre_menu_e_jogo - offset_x_status), 0, (COLUNAS * TILE), LARGURA_TELA, 0)
        self.desenhar_texto_estatisticas(self.informacoes_status_da_partida, LARGURA_TELA, 0, mov_y=0, offset_x=(offset_entre_menu_e_jogo - offset_x_status))
    
    #//// //// DESENHAR TUDO //// ////
    
    def desenhar(self):
        px.cls(0)
        
        #! ("em_menu", "entre_menu_e_jogo", "em_jogo", "game_over")
        
        if self.estado_atual_do_jogo in ("em_jogo", "game_over"):
            self.calcular_valores_das_animacoes()
            if self.estado_atual_do_jogo == "game_over":
                self.calcular_animacao_gameover_slide()

        #
        
        offset_x = 0
        offset_x_do_menu = 0
        
        if self.estado_atual_do_jogo == "em_menu":
            if self.opcao_atual_menu[2] == 0:
                self.mostrar_status_menu = False
            self.offset_menu["status"] = self.calcular_animacao_status(self.mostrar_status_menu, self.offset_menu["status"])
            offset_x_do_menu = self.offset_menu["status"]
        
        if self.estado_atual_do_jogo == "entre_menu_e_jogo":
            offset_x, offset_x_do_menu = self.valores_offset_entre_menu_e_jogo()
        
        if self.estado_atual_do_jogo in ("em_jogo", "game_over"):
            if self.esta_pausado:
                self.calcular_animacao_pausado()
                offset_x = self.offset_em_jogo["pause"]
    
        #
        
        if self.estado_atual_do_jogo in ("em_menu", "entre_menu_e_jogo"):
           self.desenhar_menu(offset_x_do_menu)
        
        if self.estado_atual_do_jogo in ("entre_menu_e_jogo", "em_jogo", "game_over"):
            px.dither(0.5)
            px.rect(offset_x, 0, LARGURA_TELA, LARGURA_TELA, 8)
            px.dither(1)
            self.desenhar_shapes_fundo_em_jogo(offset_x)
        
        if self.estado_atual_do_jogo in ("entre_menu_e_jogo", "em_jogo", "game_over"):
            self.desenhar_todos_rects_textos(offset_x)
        
        if self.estado_atual_do_jogo == "em_jogo" or (self.estado_atual_do_jogo == "entre_menu_e_jogo" and self.mov_slide_gameover == 0):
            self.desenhar_tudo_em_jogo(offset_x)
        
        if self.estado_atual_do_jogo == "game_over" or (self.estado_atual_do_jogo == "entre_menu_e_jogo" and self.mov_slide_gameover > 0):
            self.desenhar_tudo_em_game_over(offset_x)
        
        #
        
        if self.esta_pausado:
            self.desenhar_pause(offset_x)
    
        # self.tempo_inical_test_fim = time.perf_counter()
        # print(f"{((self.tempo_inical_test_fim - self.tempo_fps_ms) * 1000):.2f} MS")
        
Jogo()