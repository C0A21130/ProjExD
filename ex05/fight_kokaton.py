from ctypes import pointer
import pygame as pg
import sys
import random


# スクリーンのクラス
class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect

    # 画面に表示するメソッド
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


# こうかとんを作成するためのクラス
class Bird:
    def __init__(self, img, size, xy):
        self.sfc = pg.image.load(img)    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.center = xy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen, bomb):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]: 
            self.rct.centery -= 1
        if key_states[pg.K_DOWN]: 
            self.rct.centery += 1
        if key_states[pg.K_LEFT]: 
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT]: 
            self.rct.centerx += 1
        if key_states[pg.K_SPACE ]:
            self.attack(scr, bomb)
        # こうかとんが画面外にでているか確認
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP] : 
                self.rct.centery += 1
            if key_states[pg.K_DOWN] : 
                self.rct.centery -= 1
            if key_states[pg.K_LEFT] : 
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT] : 
                self.rct.centerx -= 1
        self.blit(scr)
    
    # ビームを表示する関数
    def attack(self, scr, bomb, coment):
        b = Beam(self.rct)
        b.blit(scr)
        # b.check(bomb, coment)
        
# ビームを表示するクラス
class Beam:
    def __init__(self, me):
        self.sfc = pg.image.load("fig/beam.png")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.3)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.center = (me.centerx - 500, me.centery)

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def check(self, bomb, coment):
        if self.rct.colliderect(bomb.rct):
            coment.point = 3

#　爆弾を作成するクラス
class Bomb:
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), 10)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


# メッセージを表示するクラス
class Coment:
    def __init__(self):
        self.txt = ""
        self.point = 0

    # メダルを取得したか確認するクラス
    def check(self):
        if (self.point==1):
            self.tex = "CLEAR"
        if (self.point==2):
            self.txt = "SPECIAL CLEAR"
        if (self.point==3):
            self.txt = "HIT CLEAR"
        if (self.point == 0):
            self.txt = int(pg.time.get_ticks())/1000

    def blit(self, scr):
        Cfonto = pg.font.Font(None, 80)
        Ctxt = Cfonto.render(f"{self.txt}", True, (0, 0, 0))
        if (self.point==1):
            Ctxt = Cfonto.render("CLEAR", True, (0, 0, 0))
        scr.sfc.blit(Ctxt, (50, 150))


# メダルの上に文字を表示する
class MedalTxt:
    def __init__(self, txt):
        s_fonto = pg.font.Font(None, 100)
        self.s_txt = s_fonto.render(txt, True, (30, 30, 30))

    def push(self):
        return self.s_txt


# メダルを表示するクラス
class Medal:
    def __init__(self, scr, point):
        self.txt = ""
        self.point = point
        self.rx = random.randint(0, scr.rct.width)
        self.ry = random.randint(0, scr.rct.height)
        self.sfc = pg.Surface((100, 100))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, (255, 255, 0), (50, 50), 50)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = self.rx
        self.rct.centery = self.ry
    
    def blit(self,scr):
        medal_txt = MedalTxt("P")
        scr.sfc.blit(self.sfc, self.rct)    # スターを表示する
        scr.sfc.blit(medal_txt.push(), (self.rx-15, self.ry-27)) # 文字Pを表示する


def main():
    clock = pg.time.Clock()

    # スクリーンと背景画像
    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    # こうかとん
    kkt = Bird("fig/6.png", 2.0, (900, 400))

    # 爆弾
    bomb = Bomb((255, 0, 0), 10, (1, 1), scr)

    # メダル
    medal = Medal(scr, 1)

    # メッセージ
    coment = Coment()

    while True:
        # スクリーンの表示
        scr.blit()

        # 終わりボタンを押したときに画面を終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        # こうかとんを毎時間移動する
        kkt.update(scr, bomb)

        # 爆弾を毎時間移動する
        bomb.update(scr)

        # 爆弾を表示する
        bomb.blit(scr)

        # メダル
        medal.blit(scr)
        
        # ポイントが0のときは変化しない
        if coment.point==0:
            coment.point = 0
        # もしメダルを撮れていないで10秒たつとCLEAが表示される
        if ((int(pg.time.get_ticks()) > 10000) and (coment.point==0)):
            coment.point = 1
            coment.check()
            coment.blit(scr)

        # こうかとんが爆弾にぶつかった際に終了させる
        if kkt.rct.colliderect(bomb.rct):
            return
        # こうかとんがメダルを入手したらSPECIAL CLEARにする
        if kkt.rct.colliderect(medal.rct):
            coment.point = 2

        # コインを取得したか確認する
        coment.check()
        # メッセージを表示する
        coment.blit(scr)

        pg.display.update()
        clock.tick(1000)


# こうかとんか爆弾が画面にぶつかったことを検知する関数
def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()