import pygame as pg
import sys

def main():
    # 時間の生成
    clock = pg.time.Clock()

    #画面の表示
    pg.display.set_caption("初めてのPygame")  # タイトルバーに「初めてのPygame」を表示する
    screen = pg.display.set_mode((800, 600)) # 縦：800、幅：600の画面が表示される

    # 画像の表示
    tori_img = pg.image.load("fig/6.png") # surfaceを生成する
    tori_rect = tori_img.get_rect() # rectを生成する
    tori_rect.center = 700, 400
    screen.blit(tori_img, tori_rect) # rectにしたがってimgをsurfaceに貼り付ける
    pg.display.update()

    clock.tick(0.2)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()