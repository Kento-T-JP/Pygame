import pygame as pg, sys
import random
import time

from pygame.constants import GL_CONTEXT_FLAGS

def bar():
    global itemFlag, state
    second = 20 #20秒以内
    total = 0 #時間計測で使用
    state = 1 #初期の状態
    itemFlag = False #上から落ちてくるアイテムをゲットしたらTrue

    screen = pg.display.set_mode((800, 600))
    img1 = pg.image.load("images/plus.png")
    img2 = pg.image.load("images/kakeru.png")
    img3 = pg.image.load("images/minus.png")
    img4 = pg.image.load("images/waru.png")

    #バーを作る
    global barrect
    barrect = pg.Rect(400, 500, 100, 20)

    #ボールを作る
    ballimg = pg.image.load("images/credit.png")
    ballimg = pg.transform.scale(ballimg, (70, 50))
    ballrect = pg.Rect(400, 450, 70, 50)
    ballrect2 = pg.Rect(400, 450, 70, 50)
    ballrect3 = pg.Rect(400, 450, 70, 50)

    #アイテム
    itemimg = pg.image.load("images/zenkyu.png")
    itemimg = pg.transform.scale(itemimg, (80, 60))
    itemrect = pg.Rect(370, -100, 80, 60)

    #ボール速度の定義（グローバル変数）
    global vx, vy, vx2, vy2, vx3, vy3
    vx = random.randint(-10, 10) #x方向はランダムに決める
    vy = -10
    vx2 = random.randint(-10, 10) #x方向はランダムに決める
    vy2 = -10
    vx3 = random.randint(-10, 10)
    vy3 = -15

    def gamestage():
        global vx, vy, vx2, vy2, vx3, vy3
        global barrect, itemFlag, state

        #背景画面の出力
        screen.fill(pg.Color("SLATEBLUE"))
        screen.blit(img1, (100,100))
        screen.blit(img2, (270,300))
        screen.blit(img3, (440,100))
        screen.blit(img4, (610,300))

        (mx, my) = pg.mouse.get_pos() #マウスの位置

        if itemFlag == False: #アイテムをゲットする前
            barrect.x = mx - 50 #マウスのx座標の-50にバーを作る(バーのx座標の中心)
            pg.draw.rect(screen, pg.Color("CYAN"), barrect) #バーを出力
        else: #アイテムをゲットした後
            itemrect.y = 700 #アイテムを消す
            barrect = pg.Rect(400, 500, 300, 20) #バーを大きくする
            barrect.x = mx - 150 #マウスをバーのx座標の中心に
            pg.draw.rect(screen, pg.Color("GOLD"), barrect) #バーを出力

        #ボール1つ目
        if ballrect.y < 0: #上の壁に当たったら
            vy = -vy #逆方向に動く
        if ballrect.x < 0 or ballrect.x > 800 - 70: #左右の壁に当たったら
            vx = -vx #逆方向に動く
        if barrect.colliderect(ballrect): #ボールとバーがぶつかったら
            vx = random.randint(-15, 15)
            vy = random.randint(-10, -5) #上方向の速度はランダム
            pg.mixer.Sound("sounds/doko.wav").play()
        if ballrect.y > 600: #画面の下に落ちたら
            state = 2 #状態を2に更新（失敗）
        ballrect.x += vx #ボールの速度ベクトルのx成分
        ballrect.y += vy #ボールの速度ベクトルのy成分
        screen.blit(ballimg, ballrect) #ボールを土台に張る

        #ボール2つ目
        if second <= 14: #14秒以下になったらボール2つ目を出す
            if ballrect2.y < 0: #上の壁に当たったら
                vy2 = -vy2 #逆方向に動く
            if ballrect2.x < 0 or ballrect2.x > 800 - 70: #左右の壁に当たったら
                vx2 = -vx2 #逆方向に動く
            if barrect.colliderect(ballrect2): #ボールとバーがぶつかったら
                vx2 = random.randint(-15, 15)
                vy2 = random.randint(-15, -10) #上方向の速度はランダム
                pg.mixer.Sound("sounds/doko.wav").play()
            if ballrect2.y > 600: #画面の下に落ちたら
                state = 2 #状態を2に更新（失敗）
            ballrect2.x += vx2
            ballrect2.y += vy2
            screen.blit(ballimg, ballrect2)

        #ボール3つ目
        if second <= 7: #7秒以下になったらボール2つ目を出す
            if ballrect3.y < 0: #上の壁に当たったら
                vy3 = -vy3 #逆方向に動く
            if ballrect3.x < 0 or ballrect3.x > 800 - 70: #左右の壁に当たったら
                vx3 = -vx3 #逆方向に動く
            if barrect.colliderect(ballrect3): #ボールとバーがぶつかったら
                vx3 = random.randint(-15, 15)
                vy3 = random.randint(-20, -15) #上方向の速度はランダム
                pg.mixer.Sound("sounds/doko.wav").play()
            if ballrect3.y > 600: #画面の下に落ちたら
                state = 2 #状態を2に更新（失敗）
            ballrect3.x += vx3
            ballrect3.y += vy3
            screen.blit(ballimg, ballrect3)

        #アイテムの処理
        if second <= 15: #残り時間が15秒になったらアイテムを落とす
            if itemrect.y <= 600: #画面の下に到達するまで
                    itemrect.y += 4
                    screen.blit(itemimg, itemrect)
            if itemrect.y > 600: #画面の下に来たら
                    itemrect.y = 700 #アイテムを消す
            if itemrect.colliderect(barrect): #アイテムがバーと当たったら
                pg.mixer.Sound("sounds/magic.wav").play()
                itemFlag = True #アイテムをゲットした印

    while True:
        if second > 0:
            start = time.perf_counter()

        if (state == 1) and (second > 0): #通常
            gamestage()
        elif state == 2: #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False
        elif second <= 0: #クリア
            pg.mixer.Sound("sounds/shine.mp3").play()
            return True
        
        #残り時間の表示
        font = pg.font.Font("ipaexg.ttf", 40)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("BLACK"))
        screen.blit(text, (20, 20))

        if second > 3:
            font = pg.font.Font("ipaexg.ttf", 50) 
            texting = font.render("単位をおとすな！", True, pg.Color("BLACK"))
            screen.blit(texting, (210, 230))

        if second == 3:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("3", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))
        
        if second == 2:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("2", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))

        if second == 1:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("1", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))
        
        pg.display.update()
        pg.time.Clock().tick(60) #1秒間に60回以下画面を更新

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