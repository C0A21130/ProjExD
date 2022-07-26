import sys                     # sysモジュールを読み込む
import pygame as pg            # pygameモジュールをpgとして読み込む
import random
from random import randint     # randomモジュール内にあるrandint関数を読み込む

BARS_NUM = 5  # 落ちてくる障害物の最大数

# 弾数の実装のための変数
rz_num = 10

# メインの画面を生成するクラス
class Screen:
    def __init__(self, title, wh, image):   # wh:幅高さタプル, image:背景画像ファイル名
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)      # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.bgi_sfc = pg.image.load(image)     # Surface
        self.bgi_rct = self.bgi_sfc.get_rect()  # Rect  

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


# 自身の操作するPlayerを生成するクラス
class Player:
    # image:画像ファイル名, size:拡大率, xy:初期座標タプル, hp:体力
    def __init__(self, image, size, xy, hp):
        self.sfc = pg.image.load(image)                        # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)    # Surface
        self.rct = self.sfc.get_rect()                         # Rect
        self.rct.center = xy
        self.hp = hp
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr: Screen):
        key_states = pg.key.get_pressed()
        if key_states[pg.K_LEFT]:
            self.rct.centerx -= 1.0
        if key_states[pg.K_RIGHT]:
            self.rct.centerx += 1.0
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_LEFT]:
                self.rct.centerx += 1.0
            if key_states[pg.K_RIGHT]:
                self.rct.centerx -= 1.0
        self.blit(scr)


# 上から落ちてくるバーを生成するクラス
class Bar:
    def __init__(self, size, color, scr: Screen):
        self.sfc = pg.Surface(size)
        pg.Surface.fill(self.sfc, color)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
        self.rct.centery = -randint(0, 500)
        self.w, self.h = size
        self.rct.width = randint(80, self.w)
        self.vy  = 1.2
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
        
    def update(self, scr: Screen):
        self.rct.move_ip(0, self.vy)
        if self.rct.centery > scr.rct.height:
            self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
            self.rct.centery = -randint(0, 500)
            self.rct.width = randint(80, self.w)
        scr.sfc.blit(self.sfc, self.rct)


#レーザーを描画:金
class Razer: 
    def __init__(self,size,color,rz_num,scr:Screen,player):
        self.vy = -1
        self.sfc = pg.Surface(size)
        pg.Surface.fill(self.sfc, color)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = player.rct.centerx
        self.rct.centery = player.rct.centery
        self.w, self.h = size
        self.a = 0

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(0, self.vy)
        scr.sfc.blit(self.sfc, self.rct)


# メダルを生成するクラス:安野
class Medal:
    def __init__(self, scr):
        self.sfc = pg.Surface((100, 100))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, (255, 255, 0), (50, 50), 50)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr, time):
        self.rct.move_ip(0, 1)
        self.blit(scr)
        if (time % 15 < 0.01) and (not (-self.rct.width < self.rct.centery < scr.rct.width)):
            self.rct.centerx = randint(self.rct.width, scr.rct.width-self.rct.width)
            self.rct.centery = random.randint(-2000, -100)

    # メダルがプレイやーかレーザーにぶつかったときにスコアを増やすように命令する
    def check_hit(self, player, scr):
        if self.rct.colliderect(player.rct):
            self.rct.centerx = randint(self.rct.width, scr.rct.width-self.rct.width)
            self.rct.centery = random.randint(-2000, -100)
            return True
        return False


# ゲームに登場するItemを生成するクラス:岡田
class Item:
    def __init__(self, r, color, scr: Screen):
        self.sfc = pg.Surface((r*2, r*2))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (r, r), r)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
        self.rct.centery = randint(-2000, -100)
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
        
    def update(self, scr: Screen):
        self.rct.move_ip(0, 1)
        scr.sfc.blit(self.sfc, self.rct)


# テキストを表示するクラス:安野
class Text:
    # txt:表示する文字、xy:表示する位置のタプル
    def __init__(self, text, xy):
        self.font = pg.font.Font(None, 80)
        self.text = text
        self.xy = xy
    
    def blit(self, scr):
        coment = self.font.render(self.text, True, (0,0,0))
        scr.sfc.blit(coment, self.xy)


# ものが障害物にぶつかったことを感知する関数
def check_bound(rct, scr_rct):
    
    # [1] rct: こうかとん or 爆弾のRect
    # [2] scr_rct: スクリーンのRect

    yoko, tate = 1, 1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right:
        yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom:
        tate = -1 # 領域外
    return yoko, tate


# ダメージの演出をする関数:横井
def damage(surface, scale):
    GB = min(255, max(0, round(255 * (1-scale))))
    surface.fill((255, GB, GB), special_flags = pg.BLEND_MULT)


# BGMを再生する関数：山本
def sound():
    pg.mixer.init(frequency = 44100)    
    pg.mixer.music.load("fig/test.mp3")
    pg.mixer.music.play(1)              


def main():
    # グローバル変数:岡田
    global rz_num
    
    # スコアに関する変数:横井
    point = 0
    score = 0
    # 時間に関する変数:岡田
    time = 0
    # 弾数に関する変数:岡田
    inv_point = 0  # 無敵ゲージを0で初期化
    inv = False    # 無敵かどうかの判定する変数
    st = 0         # 無敵の開始時刻を保存する変数

    clock = pg.time.Clock() # 時間計測用のオブジェクト

    # BGMを再生する関数の呼び出し:山本
    sound()

    # スクリーンの生成
    screen = Screen("", (700, 900), "fig/pg_bg.jpg")
    screen.blit()                                    

    # 操作するキャラクターの生成
    player = Player("fig/5.png", 1.5, (350, 848), 500)
    
    # 落ちてくるバーの生成
    bars = [Bar((120, 30), (0,0,0), screen) for i in range(BARS_NUM)]

    # メダルを生成:安野
    medal = Medal(screen)

    #レーザーを弾の数(rz_num)だけ生成:金
    rz_list=[Razer((10,20),(255,0,0),rz_num,screen,player) for i in range(rz_num)]
    x=0

    # 画面に表示するテキストを生成:横井
    time_text = Text(f"Time:{time: .1f}", (10, 10))
    hp_text = Text(f"HP:{player.hp}", (500, 10))
    score_text = Text(f"Score:{0}", (10, 80))
    rz_num_text = Text(f"rz_num:{rz_num}", (10, 150))
    over_text = Text("GAME OVER", (170, 450)) 

    # 弾数を追加するアイテムを生成:岡田
    rz_plus = Item(15, (255, 0, 0), screen)

    # ライフを回復するアイテムを生成:岡田
    heal = Item(15, (0, 128, 0), screen)

    # 無敵ゲージを生成:
    inv_text = Text("X"*inv_point, (10, 220))

    # 常にゲームを再生し続ける
    while True:
        screen.blit()

        # スコア計算の処理:横井
        score = int(time)*500+point*3000  
        
        # プレイヤーを更新するメソッドを呼び出す
        player.update(screen)

        # メダルを更新するメソッドを呼び出す:安野
        medal.update(screen, time)

        # バーを表示する
        for bar in bars:
            bar.update(screen)

            # ダメージ判定を受けたときの処理:横井
            if player.rct.colliderect(bar.rct) and (not inv): 
                damage(screen.sfc, 0.5) # 画面を赤く変化させる
                player.hp -= 1 

        # 時間を画面上に表示する:横井
        time_text.text = f"Time:{time: .1f}"
        time_text.blit(screen)

        # 残りのHPを画面上に表示する:横井
        hp_text.text = f"HP:{player.hp}"
        hp_text.blit(screen)

        # スコアの結果を表示する:横井
        score_text.text = f"Score:{score}"
        score_text.blit(screen)

        # 弾数を表示する:岡田
        rz_num_text.text = f"Shots:{rz_num}"
        rz_num_text.blit(screen)

        # 無敵ゲージを表示する:岡田
        if inv_point == 10:
            inv_text.text = "O"*inv_point
        else:
            inv_text.text = "X"*inv_point
        inv_text.blit(screen)
        
        # HPが0以下のときゲームを終了してそれ以外ならゲームを続行する:横井
        if player.hp <= 0:
            player.hp = 0
            player = Player("fig/8.png", 1.5, (350, 390), 0)
            over_text.blit(screen)
            bars.clear()
        else:
            time = float(pg.time.get_ticks()/1000)

        # メダルが操作プレイヤーと衝突したときにポイントを１増やす:安野
        if medal.check_hit(player, screen):
            point+=1

        # 25秒おきに弾数追加アイテムを表示:岡田
        if 0 <= time % 25 <= 0.01: # 25秒おき
            rz_plus = Item(10, (255, 0, 0), screen)
            # 障害物と被らないようにする
            for bar in bars: 
                while rz_plus.rct.colliderect(bar.rct):
                    rz_plus = Item(10, (255, 0, 0), screen)
        rz_plus.update(screen)

        # 40秒おきに回復アイテムを表示:岡田
        if 0 <= time % 40 <= 0.01:
            heal = Item(10, (0, 128, 0), screen)
            # 障害物と被らないようにする
            for bar in bars: 
                while heal.rct.colliderect(bar.rct):
                    heal = Item(10, (0, 128, 0), screen)
        heal.update(screen)


        # 弾数追加アイテムとプレイヤーがぶつかったときにアイテムを画面から消して弾数を追加:岡田
        if player.rct.colliderect(rz_plus.rct):
            rz_num += 3
            for i in range(3):
                rz_list.append(Razer((10,20),(255,0,0),rz_num,screen,player))
            rz_plus.rct.centerx = -30

        # 回復アイテムとプレイヤーがぶつかったときにアイテムを画面から消して体力を回復:岡田
        if player.rct.colliderect(heal.rct): 
            player.hp += 100
            heal.rct.centerx = -30

      
        # メダルとプレイヤーがぶつかったときにメダルを画面から消す:安野
        if player.rct.colliderect(medal.rct):
            medal.rct.centerx = -100

        #レーザーが発射され、バーに当たるとバーとレーザーのｘ座標を変える:金
        if x>0: 
            rz.update(screen)
            for bar in bars:
                if rz.rct.colliderect(bar.rct):
                    rz.rct.centerx=1000
                    bar.rct.centerx=-1000
                    if inv_point < 10:
                        inv_point += 1

        # 無敵は10秒継続:岡田
        if time - st > 10:  
            inv = False

        # 無敵中に画面を黄色にする:岡田
        if inv:  
            screen.sfc.fill((255, 255, 0), special_flags = pg.BLEND_MULT)

        # 画面のばつボタンをクリックしたときに終了する
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:

                # 無敵タイムを開始する処理:岡田
                if event.key == pg.K_LSHIFT and inv_point == 10:
                    inv_point = 0
                    inv = True
                    st = time  # 無敵の開始時刻を保存
            
                # スペースキーを押したときに弾を打つ:金
                if event.key == pg.K_SPACE:
                    x+=1
                    if len(rz_list)>0:
                        rz=rz_list.pop(0)
                        rz.rct.centerx = player.rct.centerx
                        rz_num -= 1
                        rz.update(screen)
        
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    # sys.exit()
