import pygame as pg, sys
import random
import time

def chase():
    global rightFlag, state
    second = 15 #15秒以内
    state = 1 #ゲーム画面の切り替えで使用
    total = 0 #時間計測で使用
    rightFlag = True #キャラが右を向いているかどうか

    screen = pg.display.set_mode((800, 600))

    #主人公（プレイヤー）の画像
    myimgR = pg.image.load("images/playerR.png")
    myimgR = pg.transform.scale(myimgR, (40, 50))
    myimgL = pg.transform.flip(myimgR, True, False) #上下の反転はなし
    myrect = pg.Rect(50, 200, 40, 50) #主人公の土台

    #4方向の壁(left, top, width(横), height（縦）)
    walls = [pg.Rect(0, 0, 800, 20),
            pg.Rect(0, 0, 20, 600),
            pg.Rect(780, 0, 20, 600),
            pg.Rect(0, 580, 800, 20)]

    #トラップを作る
    trapimg = pg.image.load("images/shuniku.png")
    trapimg = pg.transform.scale(trapimg, (30, 30))
    traps = []
    #10個のトラップの（土台の）座標を作る
    for i in range(10):
        wx = 180 + i * 50
        wy = random.randint(80, 550) #整数の乱数
        traps.append(pg.Rect(wx, wy, 30, 30))

    #ゴール地点の表示
    goalrect = pg.Rect(750, 250, 30, 100)

    #敵の画像とその土台を作る
    enemyimgL = pg.image.load("images/sotsuron.png")
    enemyimgL = pg.transform.scale(enemyimgL, (70, 70))
    enemyimgR = pg.transform.flip(enemyimgL, True, False)
    enemyrect = pg.Rect(650, 200, 70, 70)

    def gamestage():
        global rightFlag, state

        screen.fill(pg.Color("DEEPSKYBLUE"))
        vx = 0 #プレイヤーのx方向の速度
        vy = 0 #プレイヤーのy方向の速度
        key = pg.key.get_pressed() #キーボードの入力を取得
        if key[pg.K_RIGHT]: #右方向を押したら
            vx = 4 #右方向に4勧める
            rightFlag = True #右向きをTrueに

        if key[pg.K_LEFT]: #左方向を押したら
            vx = -4
            rightFlag = False #右向きをFalseに
        
        if key[pg.K_UP]: #上方向を押したら
            vy = -4
        
        if key[pg.K_DOWN]: #下方向を押したら
            vy = 4

        #プレイヤーの動きを更新
        myrect.x += vx
        myrect.y += vy

        #衝突判定
        if myrect.collidelist(walls) != -1: #返り値が-1でないとき壁と接触していることになる
            #上の処理の移動を相殺して障害物と重ならないようにする
            myrect.x -= vx
            myrect.y -= vy
        
        if rightFlag: #右向きなら
            screen.blit(myimgR, myrect)
        else: #左向きなら
            screen.blit(myimgL, myrect)

        #for文で4つの壁を出力
        for wall in walls:
            pg.draw.rect(screen, pg.Color("DARKRED"), wall)

        #偶数個目のトラップを左右に動かす
        for trap in traps[0::2]: #0から2ずつインデックスを増加
            if second % 2 == 0: #残り時間が偶数の時
                trap.x += 1 #左方向に+1
            else:
                trap.x -= 2 #右方向に+2
        #奇数個目のトラップを上下に動かす
        for trap in traps[1::2]: #1から2ずつインデックスを増加
            if second % 2 == 0: #残り時間が偶数の時
                trap.y += 2 #下方向に+2
            else:
                trap.y -= 2 #上方向に+2

        #for文でトラップを出力
        for trap in traps:
            screen.blit(trapimg, trap) #土台に貼り付けて出力
        if myrect.collidelist(traps) != -1: #トラップと主人公がぶつかったら
            state = 2 #状態を2に更新（失敗）

        pg.draw.rect(screen, pg.Color("GOLD"), goalrect)
        if myrect.colliderect(goalrect): #ゴールに触れれば
            state = 3 #状態を2に更新（クリア）
        
        #敵の速度を定義して動かす
        ovx = 0
        ovy = 0
        if enemyrect.x < myrect.x: #主人公に近づくようにする
            ovx = 2
        else:
            ovx = -2
        if enemyrect.y < myrect.y: #主人公に近づくようにする
            ovy = 1
        elif enemyrect.y > myrect.y:
            ovy = -1
        else: #主人公と水平に一直線上の時
            ovy = 0 #上下に揺れないようにする
        #敵の動きを更新
        enemyrect.x += ovx
        enemyrect.y += ovy

        if ovx > 0: #右方向に動く時は右向き
            screen.blit(enemyimgR, enemyrect)
        else: #左方向に動く時は左向き
            screen.blit(enemyimgL, enemyrect)

        if myrect.colliderect(enemyrect): #敵に当たったら
            state = 2 #状態を2に更新（失敗）

    while True:
        if second > 0:
            start = time.perf_counter()
        
        if state == 1 and (second > 0): #通常
            gamestage()
        elif (state == 2) or (second <= 0): #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False
        elif state == 3: #成功
            pg.mixer.Sound("sounds/shine.mp3").play()
            return True

        font = pg.font.Font("ipaexg.ttf", 40)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("WHITE"))
        screen.blit(text, (25, 30))

        font = pg.font.Font("ipaexg.ttf", 50) 
        texting = font.render("", True, pg.Color("BLACK"))
        screen.blit(texting, (90, 260))

        if second > 3:
            font = pg.font.Font("ipaexg.ttf", 50) 
            texting = font.render("卒論をかわして先へすすめ！", True, pg.Color("WHITE"))
            screen.blit(texting, (90, 260))

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

