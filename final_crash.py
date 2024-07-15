import pygame as pg
import sys
import time
import random

def crash():
    global state, crashflag, pushFlag, vx
    second = 5 #5秒以内
    total = 0 #時間計測で使用
    vx = 30 #ターゲットのx方向の速度
    state = 1 #初期の状態を示す
    crashflag = False #ターゲットに触れたらTrue
    pushFlag = False #1回クリックしたらTrue（複数回反応するのを防ぐ）

    screen = pg.display.set_mode((800, 600)) #ディスプレイの大きさをセット

    virus_img = pg.image.load("images/virus.png") #ターゲットの画像
    virus_img = pg.transform.scale(virus_img, (70, 70)) #画像のスケールを変換
    virusrect = pg.Rect(200, 250, 70, 70)

    #手の画像
    handimg = pg.image.load("images/hand.png")
    handrect = pg.Rect(360, 180, 120, 240)

    #クリア後の画像
    grade = pg.image.load("images/grade.png")

    def gamestage():
        global state, crashflag, pushFlag, vx
        
        #ターゲットが壁に当たったら左右に動くように処理
        if crashflag == False: #ターゲットに触れていないとき
            if virusrect.x < 5 or virusrect.x > 800-70: #左右の壁に当たったら
                vx = -vx #逆方向に動く
            virusrect.x = virusrect.x + vx

            #ターゲットが画面内で上下に動くように処理
            if (virusrect.x>= 0 and virusrect.x < 200) or (virusrect.x>= 400 and virusrect.x < 600):
                virusrect.y = virusrect.y + 11
            elif (virusrect.x>= 200 and virusrect.x < 400) or (virusrect.x>= 600 and virusrect.x < 800-70):
                virusrect.y = virusrect.y - 9
            screen.blit(virus_img, virusrect) #virusrectの上に画像を張り付ける

            #手の位置の設定
            (mx, my) = pg.mouse.get_pos()
            #手の画像の中心とカーソルの位置が同期するようにする
            handrect.x = mx - 65
            handrect.y = my - 60
            screen.blit(handimg, handrect)

            #ターゲットにクリックしたときの処理
            mdown = pg.mouse.get_pressed()
            (mx, my) = pg.mouse.get_pos()
            if mdown[0]: #左クリックしたら
                cat = pg.mixer.Sound("sounds/cat.mp3")
                cat.set_volume(0.2) #音の大きさを0.2にする（0から1まで）
                cat.play()
                if virusrect.collidepoint(mx, my) and pushFlag == False: #手がターゲットに触れたら
                    poka = pg.mixer.Sound("sounds/poka.wav")
                    poka.set_volume(1) #音の大きさを1にする（0から1まで）
                    poka.play()
                    crashflag = True #ターゲットに触れた印
                    pushFlag = True #1回クリックした印
                    state = 2 #状態を2に更新（クリア）   
                else:
                    pushFlag = False
        
        if second <= 0:
            state = 3 #状態を3に更新（失敗）
        
        if crashflag == True: #ターゲットに触れたら
            lost_img = pg.transform.rotate(virus_img, 180) #ターゲットがひっくり返る
            screen.blit(lost_img, virusrect) #背景画面を変える
            #叩いたら手が震えるようにする
            (mx, my) = pg.mouse.get_pos()
            handrect.x = mx - 65 + random.randint(-3, 3) #左右に小刻みに震える
            handrect.y = my - 60 + random.randint(-3, 3) #上下に小刻みに震える
            screen.blit(handimg, handrect)

    while True: #常に表示
        if second > 0:
            start = time.perf_counter()

        screen.fill(pg.Color("WHITE")) #背景画面を白く
        if crashflag == True:
            screen.blit(grade, (0,0))
        
        if state == 1 or (second > 0): #通常
            gamestage()
        elif state == 2 and (second <= 0): #クリア
            pg.mixer.Sound("sounds/shine.mp3").play()
            return True
        elif state == 3: #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False
        
        font = pg.font.Font("ipaexg.ttf", 40)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("BLACK"))
        screen.blit(text, (20, 20))

        font = pg.font.Font("ipaexg.ttf", 50) 
        texting = font.render("コロナをつぶせ！", True, pg.Color("BLACK"))
        screen.blit(texting, (200, 100))

        if second == 3 and crashflag == False:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("3", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))
        
        if second == 2 and crashflag == False:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("2", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))

        if second == 1 and crashflag == False:
            font = pg.font.Font("ipaexg.ttf", 200) 
            texting = font.render("1", True, pg.Color("RED"))
            screen.blit(texting, (320, 200))

        pg.display.update()
        pg.time.Clock().tick(60) #1秒間に100回以下で表示

        if second > 0:
            end = time.perf_counter()
            p_time = end - start
            total += p_time

            if total >= 1:
                second -= 1
                total = 0

        #終了の定型文
        for event in pg.event.get():
            if event.type == pg.QUIT: #終了のイベントなら
                pg.quit() #pygame（写真の表示など）を終了して
                sys.exit() #プログラムを閉じる
