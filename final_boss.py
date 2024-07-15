import pygame as pg
import sys
import time
import random

def boss():
    global state, bv, clearFlag, enemyFlag, bulletFlag
    second = 8 #8秒以内
    total = 0 #時間計測で使用
    bv = 10 #ボスの横方向のスピード
    state = 1 #初期の状態
    clearFlag = False #クリアしたらTrue
    enemyFlag = False #enemyが画面にいたらTrue
    bulletFlag = False #1回弾を打ったらTrue

    screen = pg.display.set_mode((800, 600))
    
    myimg = pg.image.load("images/banzai.png") #プレイヤー
    myimg = pg.transform.scale(myimg, (120, 120)) #スケールの変更
    myrect = pg.Rect(400, 470, 120, 120) #貼り付ける板

    bossimg = pg.image.load("images/lastboss.png") #ボス
    bossimg = pg.transform.scale(bossimg, (100, 100))
    bossrect = pg.Rect(50, 75, 100, 100)

    bulletimg = pg.image.load("images/sheet.png") #弾
    bulletimg = pg.transform.scale(bulletimg, (64, 64))
    bulletrect = pg.Rect(900, -100, 64, 64)

    enemyimg = pg.image.load("images/mail.png") #敵
    enemyimg = pg.transform.scale(enemyimg, (64, 72))
    enemyrect = pg.Rect(-100, 50, 64, 72)

    naitei = pg.image.load("images/naitei.png") #クリア画面

    def gamestage():
        global state, bv, clearFlag, enemyFlag, bulletFlag

        screen.fill(pg.Color("WHITE"))
        if clearFlag == True: #クリア後の画面表示
            screen.fill(pg.Color("WHITE"))
            screen.blit(naitei, (0,0))
            font = pg.font.Font("ipaexg.ttf", 40) 
            text = font.render("おめでとう！", True, pg.Color("RED"))
            screen.blit(text, (480, 480))

        (mx, my) = pg.mouse.get_pos() #マウスの場所
        mdown = pg.mouse.get_pressed() #クリックしたボタン

        if clearFlag == False:
            myrect.x = mx - 120/2 #マウスがプレイヤーの中心になるようにする
            screen.blit(myimg, myrect)

            #弾の動きの処理
            if bulletFlag == False:
                if mdown[2] and bulletrect.y < 0: #右クリックかつ画面の上から出たら
                    bulletrect.x = myrect.x + 120/2 - 64/2 #プレイヤーの中心から弾が出るように
                    bulletrect.y = myrect.y #プレイヤーのy座標から弾が出るように
                    pg.mixer.Sound("sounds/special.wav").play()
                if bulletrect.y >= -120/2: #弾が画面に残っていたら
                    bulletrect.y -= 28 #弾を上へ進める
                    screen.blit(bulletimg, bulletrect)
                    if bulletrect.y <= -120/2:
                        bulletFlag = True

            #ボスの動きの処理
            if bossrect.x == 340: #画面の中心でボスの速度をランダムに変える
                if bv < 0:
                    bv = random.randrange(-40, -10, 10)
                elif bv > 0:
                    bv = random.randrange(10, 40, 10)
            if bossrect.x <= -20 or bossrect.x >= 800-100: #左右の壁の部分に着いたら
                bv = -bv #逆方向に動く
            bossrect.x += bv 
            screen.blit(bossimg, bossrect)
            if bossrect.colliderect(bulletrect): #ボスと弾が当たったら
                pg.mixer.Sound("sounds/up.wav").play()
                clearFlag = True #クリアした印

            #ボスから発射される敵の処理
            if enemyFlag == False: #敵が画面にいないとき
                pg.mixer.Sound("sounds/apper.wav").play()
                if bv > 0: #ボスが右方向に動くとき
                    enemyrect.x = bossrect.x + 100/2 #ボスから出す
                elif bv < 0: #ボスが左方向に動くとき
                    enemyrect.x = bossrect.x - 100/2
            if enemyrect.y <= 600: #画面の下に到達するまで
                enemyFlag = True
                enemyrect.y += 25
                if enemyrect.y >= bossrect.y + 100/2: #ボスのy座標より50下へ来たら
                    screen.blit(enemyimg, enemyrect) #画面に出力
            if enemyrect.y > 600: #画面の下に来たら
                enemyFlag = False
                enemyrect.y = 50 #初期化（ボスのy座標へ）
            if enemyrect.colliderect(myrect): #enemyがプレイヤーと当たったら
                state = 2 #状態を2に更新（失敗）
            if enemyrect.colliderect(bulletrect): #弾とenemyimgが当たったら 
                enemyFlag = False
                enemyrect.y = 50 ##初期化（ボスのy座標へ）
                pg.mixer.Sound("sounds/piko.wav").play()

    while True:
        if second > 0: #残り時間が0秒より大きかったら
            start = time.perf_counter() #計測スタート

        if (state == 1) and (second > 0): #通通常
            gamestage()
        elif (clearFlag == True) and (second <= 0): #クリア
            pg.mixer.Sound("sounds/defeatboss.mp3").play()
            time.sleep(0.5)
            return True
        elif (state == 2) or (second <= 0): #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False

        #残り時間
        font = pg.font.Font("ipaexg.ttf", 30)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("BLACK"))
        screen.blit(text, (20, 20))

        if clearFlag == False: #クリアしていないときは以下の文字を出力
            font = pg.font.Font("ipaexg.ttf", 30)
            text = font.render("履歴書は1枚しかないぞ", True, pg.Color(255,51,0))
            screen.blit(text, (470, 20))

            if second > 3:
                font = pg.font.Font("ipaexg.ttf", 35) 
                text = font.render("右クリックで面接官に履歴書を受け取らせよう", True, pg.Color("BLUE"))
                screen.blit(text, (35, 260))

            if second == 3:
                font = pg.font.Font("ipaexg.ttf", 200) 
                text = font.render("3", True, pg.Color("RED"))
                screen.blit(text, (330, 200))
            
            if second == 2:
                font = pg.font.Font("ipaexg.ttf", 200) 
                text = font.render("2", True, pg.Color("RED"))
                screen.blit(text, (330, 200))

            if second == 1:
                font = pg.font.Font("ipaexg.ttf", 200) 
                text = font.render("1", True, pg.Color("RED"))
                screen.blit(text, (330, 200))

        pg.display.update()
        pg.time.Clock().tick(60) #フレームレートは60

        if second > 0: #残り時間が0秒より大きかったら
            end = time.perf_counter() #計測終了
            p_time = end - start #1つの処理にかかった時間を求める
            total += p_time #1つの処理にかかった時間を累計

            if total >= 1: #累計時間が1秒を超えたら
                second -= 1 #残り時間を1秒減らす
                total = 0 #累計時間をリセット

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
