import random
import pygame as pg
import sys

def main():
    # 秒数をclock変数に保存する
    clock = pg.time.Clock()

    # スクリーンを表示する
    pg.display.set_caption("逃げ！こうかとん")
    screen_sfc = pg.display.set_mode((1600, 900))
    screen_rct = screen_sfc.get_rect()

    # 背景の表示
    bgimg_sfc = pg.image.load("fig/pg_bg.jpg")
    bgimg_rct = bgimg_sfc.get_rect()
    screen_sfc.blit(bgimg_sfc, bgimg_rct)

    # こうかとん
    kkimg_sfc = pg.image.load("fig/6.png")
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0)
    kkimg_rct = kkimg_sfc.get_rect()
    kkimg_rct.center = 500, 300
    kkimg_sfc.blit(kkimg_sfc, kkimg_rct)

    # 爆弾
    bsize = 20
    bom_sfc = pg.Surface((bsize, bsize))
    bom_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_sfc, (255, 0, 0), (bsize/2, bsize/2), bsize/2)
    bom_rct = bom_sfc.get_rect()
    bom_rct.centerx = random.randint(0, screen_rct.width)
    bom_rct.centery = random.randint(0, screen_rct.height)
    vx, vy = +1, +1

    # ポイント(0:表示しない、1:ポイント表示かつゲットしていない、2：ポイント取得後)
    point = 0
    comment = "" # スターを取得するとクリアしたときにSPECIAL CLEARに変化する

    # スター
    star_sfc = pg.Surface((100, 100))
    star_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(star_sfc, (255, 255, 0), (50, 50), 50)
    star_rct = star_sfc.get_rect()
    rx = random.randint(0, screen_rct.width)
    ry = random.randint(0, screen_rct.height)
    star_rct.centerx = rx
    star_rct.centery = ry
    # スターにP
    s_fonto = pg.font.Font(None, 100)
    s_txt = s_fonto.render("P", True, (30, 30, 30))

    while True:
        # 背景を表示する
        screen_sfc.blit(bgimg_sfc, bgimg_rct)

        # 秒数を表示する
        fonto = pg.font.Font(None, 80)
        txt = fonto.render(str(pg.time.get_ticks()/1000), True, (0, 0, 0))
        screen_sfc.blit(txt, (50, 50))

        # 30秒経過したらクリアと表示する
        if int(pg.time.get_ticks()) > 10000:
            Cfonto = pg.font.Font(None, 80)
            Ctxt = Cfonto.render(f"{comment}CLEAR", True, (0, 0, 0))
            screen_sfc.blit(Ctxt, (50, 150))
        # 1秒ごとに爆弾が大きくなる
        if((int(pg.time.get_ticks()) % 1000) < 100):
            bsize += 0.5
            bom_sfc = pg.Surface((bsize, bsize))
            star_sfc.set_colorkey((0, 0, 0))
            pg.draw.circle(bom_sfc, (255, 0, 0), (bsize/2, bsize/2), bsize/2)
        # 5秒経過後スターが表示される
        if(int(pg.time.get_ticks()) > 5000 and point==0):
            point = 1 
            
        # ×を押したときに終了する
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 

        # キーによってこうかとんを移動させる
        key_status = pg.key.get_pressed()

        if key_status[pg.K_UP]    == True: kkimg_rct.centery -= 1
        if key_status[pg.K_DOWN]  == True: kkimg_rct.centery += 1
        if key_status[pg.K_LEFT]  == True: kkimg_rct.centerx -= 1
        if key_status[pg.K_RIGHT] == True: kkimg_rct.centerx += 1
        if check_bound(kkimg_rct, screen_rct) != (1, 1):
            if key_status[pg.K_UP]    == True: kkimg_rct.centery += 1
            if key_status[pg.K_DOWN]  == True: kkimg_rct.centery -= 1
            if key_status[pg.K_LEFT]  == True: kkimg_rct.centerx += 1
            if key_status[pg.K_RIGHT] == True: kkimg_rct.centerx -= 1
        if kkimg_rct.colliderect(bom_rct):
            return
        if kkimg_rct.colliderect(star_rct):
            point=2
            
        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        # 爆弾を移動させる
        bom_rct.move_ip(vx, vy)

        # 爆弾が壁にぶつかったとき反射する
        yoko, tate = check_bound(bom_rct, screen_rct)
        vx *= yoko
        vy *= tate

        # 爆弾を生成する
        screen_sfc.blit(bom_sfc, bom_rct)

        # 1の時にスターを表示、2:コメントを加える
        if point == 1:
            screen_sfc.blit(star_sfc, star_rct)    # スターを表示する
            screen_sfc.blit(s_txt, (rx-15, ry-27)) # 文字Pを表示する
        if point == 2:
            comment = "SPECIAL"

        pg.display.update()
        clock.tick(1000)


def check_bound(rct, scr_rct):

    yoko, tate = +1, +1
    if rct.left < scr_rct.left or scr_rct.right < rct.right:
        yoko = -1 # 範囲外
    if rct.top < scr_rct.top or scr_rct.bottom < rct.bottom:
        tate = -1 # 範囲外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()