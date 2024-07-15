import pygame as pg, sys
import random
import time

from pygame.constants import GL_CONTEXT_FLAGS

def block():
    global bv, vx, vy, state, score
    second = 25 #25秒以内
    total = 0
    bv = 8 #ボスの速度
    state = 1 #初期の状態
    score = 0 #スコア

    #ボール速度
    vx = 0 #x方向
    vy = -10 #y方向

    screen = pg.display.set_mode((800, 600))

    #バーを作る
    barrect = pg.Rect(400, 500, 140, 20)

    #ボールを作る
    ballimg = pg.image.load("images/eraser.png")
    ballimg = pg.transform.scale(ballimg, (40, 40))
    ballrect = pg.Rect(400, 450, 40, 40)

    #ブロックの画像
    midimg = pg.image.load("images/mid.png")
    midimg = pg.transform.scale(midimg, (90, 40))
    finalimg = pg.image.load("images/final.png")
    finalimg = pg.transform.scale(finalimg, (90, 40))

    #10個のブロックを作る
    blocks = []
    for yy in range(2):
        for xx in range(5):
            blocks.append(pg.Rect(160+xx*100, 100+yy*50, 80, 30)) #(left, top, width, height)

    #ボス画像と土台
    bossimg = pg.image.load("images/tsuishi.png")
    bossimg = pg.transform.scale(bossimg, (80, 60))
    bossrect = pg.Rect(50, 100, 80, 60)

    def gamestage():
        global vx, vy, bv, state, score

        screen.fill(pg.Color("DARKGREEN")) #背景の色

        (mx, my) = pg.mouse.get_pos() #クリックした場所

        barrect.x = mx - 70 #マウスのx座標の-50にバーを作る(バーのx座標の中心)
        pg.draw.rect(screen, pg.Color("ORANGE"), barrect) #バーを描画

        #ボールの処理
        if ballrect.y < 0: #上の壁に当たったら
            vy = -vy #逆方向に動く
        if ballrect.x < 0 or ballrect.x > 800 - 40: #左右の壁に当たったら
            vx = -vx #逆方向に動く
        if barrect.colliderect(ballrect): #ボールとバーがぶつかったら
            vx = ((ballrect.x + 15) - (barrect.x + 70)) / 4 #バーの中心 - ボールの中心
            vy = random.randint(-15, -10) #上方向の速度はランダム
            pg.mixer.Sound("sounds/pi.wav").play()
        if ballrect.y > 600: #画面の下に落ちたら
            state = 2 #状態を2に更新（失敗）

        ballrect.x += vx
        ballrect.y += vy
        screen.blit(ballimg, ballrect) #ボールを土台に張る

        n = 0 #ブロックのインデックス
        for block in blocks:
            if n % 2 == 0:
                screen.blit(midimg, block)
            elif n % 2 !=0:
                screen.blit(finalimg, block)
            if block.colliderect(ballrect): #ボールがブロックに当たったら
                pg.mixer.Sound("sounds/erase.wav").play()
                vy = -vy #ボールの速度を逆にする
                blocks[n] = pg.Rect(800, 600, 0, 0) #ブロックの座標を画面外に
                score += 1
            n += 1 #ここでインクリメントすると上手く消える

        if score == 10: #全てのブロックに当てたらボスが出る
            screen.blit(bossimg, bossrect)
            if bossrect.x <= 0 or bossrect.x >= 800-80:
                bv = -bv #逆方向に動く
            bossrect.x += bv 
            if bossrect.colliderect(ballrect): #ボスとボールが当たったら
                state = 3 #状態を3に更新（クリア）

    while True:
        if second > 0:
            start = time.perf_counter()
        
        if state == 1 and (second > 0): #通常
            gamestage()
        elif state == 2 or (second <= 0): #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False
        elif state == 3: #クリア
            pg.mixer.Sound("sounds/shine.mp3").play()
            return True
        
        #残り時間の表示
        font = pg.font.Font("ipaexg.ttf", 40)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("WHITE"))
        screen.blit(text, (20, 20))

        if second > 3:
            font = pg.font.Font("ipaexg.ttf", 50) 
            texting = font.render("テストをぜんぶけせ！", True, pg.Color("WHITE"))
            screen.blit(texting, (170, 260))

        if second == 3:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("3", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))
            pg.mixer.Sound("sounds/warning.mp3").play()
        
        if second == 2:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("2", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))

        if second == 1:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("1", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))
        
        pg.display.update()
        pg.time.Clock().tick(60)

        if second > 0:
            end = time.perf_counter()
            p_time = end - start
            total += p_time

            if total >= 1:
                second -= 1
                total = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()