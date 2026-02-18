import pyxel as px

COR_PECA = {
    "T": 0,
    "I": 1,
    "QUADRADO": 2,
    
    "L_1": 3,
    "l_2": 4,
    
    "Z_1": 5,
    "Z_2": 6,
}


class Jogo:
    def __init__(self, size):
        self.size = size
        self.size_screen = size * 16
        
        px.init(self.size_screen, self.size_screen, title="Tetrico", fps=60, display_scale=2)
        px.load("my_resource.pyxres")
        
        self.x_atual = 6
        self.y_atual = 0
        
        self.map = [["" for x in range(10)] for x in range(20)]
        px.tilemaps[0].set(0, 0, ["0"]) 
        
        px.run(self.update, self.draw)

    def update(self):
        if px.btnp(px.KEY_LEFT, hold=True) and self.x_atual > 5:
            self.x_atual -= 1
        if px.btnp(px.KEY_RIGHT, hold=True) and self.x_atual < 14:
            self.x_atual += 1
        if px.btnp(px.KEY_DOWN) and self.y_atual < 19:
            self.y_atual += 1

    def draw(self):
        px.cls(0)
        
        px.bltm(80, 0, 0, 0, 0, 16 * 10, 16 * 20)
        
        self.draw_block(self.x_atual, self.y_atual)

    def draw_block(self, bx, by):
        
        sx = COR_PECA["T"] * 16  # posição x no spritesheet
        px.blt(bx * 16, by * 16, 0, sx, 0, 16, 16, 0)
        
        


Jogo(20)