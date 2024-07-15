import pygame as pg, sys
import random
import time

def shooting():
    global state, score, specialFlag, clearFlag
    second = 20 #20秒以内
    total = 0 #時間計測で使用
    state = 1 #初期の状態
    score = 0 #スコア
    specialFlag = False #1度特別な弾を打ったらTrue
    clearFlag = False #クリアしたかどうか

    screen = pg.display.set_mode((800, 600))

    myimg = pg.image.load("images/gakusei.png") #プレイヤー
    myimg = pg.transform.scale(myimg, (70, 80)) #スケールの変更
    myrect = pg.Rect(400, 500, 70, 80) #貼り付ける板の大きさは(70, 70)で揃える

    penimg = pg.image.load("images/pen.png") #弾
    penimg = pg.transform.scale(penimg, (32, 32))
    penrect = pg.Rect(900, -100, 32, 32) #画面外に弾の土台を準備する

    specialimg = pg.image.load("images/energy.png") #スペシャル攻撃
    specialimg = pg.transform.scale(specialimg, (175, 175))
    specialrect = pg.Rect(900, -200, 175, 175)

    sotsugyou = pg.image.load("images/sotsugyou.png") #クリア後の画面

    #敵の初期設定
    reportimg = pg.image.load("images/report.png")
    reportimg = pg.transform.scale(reportimg, (50, 50))
    reports = [] #レポートの土台(rect)を入れる
    for i in range(10): #10個の敵を作る
        ux = random.randint(0+25, 800-25) #画面の端から端まで
        uy = -100 * i #画面の外（上）に準備
        reports.append(pg.Rect(ux, uy, 50, 50))

    #画面スクロール
    sakuraimg = pg.image.load("images/sakura.png") #桜の画像
    sakuraimg = pg.transform.scale(sakuraimg, (12, 12))
    sakuras = []
    for i in range(60): #60個のサクラの画像
        sakura = pg.Rect(random.randint(0, 800), 10 * i, 30, 30)
        sakura.w = random.randint(5, 8) #wは落ちるスピードに相当
        sakuras.append(sakura)

    def gamestage():
        global state, score, specialFlag, clearFlag
        screen.fill(pg.Color(102,204,51))
        pg.draw.polygon(screen, pg.Color(204,153,102), [(300,600), (500, 600), (400, -100)]) #道になるように三角形を出力

        if clearFlag == True: #クリア後の画面表示
            screen.fill(pg.Color("WHITE"))
            screen.blit(sotsugyou, (0,0))

        (mx, my) = pg.mouse.get_pos() #マウスの場所
        mdown = pg.mouse.get_pressed() #クリックしたボタン

        #背景の桜を出力
        for sakura in sakuras:
            sakura.y += sakura.w #画面の下方向に動かす
            screen.blit(sakuraimg, sakura)
            if sakura.y > 600: #画面の下に行ったら
                sakura.x = random.randint(0, 800) #x方向はランダムに設定
                sakura.y = 0

        myrect.x = mx - 70/2 #マウスがプレイヤーの画像の中心になるようにする
        screen.blit(myimg, myrect) #プレイヤーを出力

        #通常の弾
        if mdown[0] and penrect.y < 0: #左クリック、画面の上から出たら
            penrect.x = myrect.x + 70/2 - 32/2 #プレイヤーの中心から弾が出るように
            penrect.y = myrect.y
            pg.mixer.Sound("sounds/shot.wav").play()
        if penrect.y >= 0: #弾が画面に残っていたら
            penrect.y -= 15 #弾を上へ進める
            screen.blit(penimg, penrect)

        #特別な弾(1回限り)
        if specialFlag == False: #specialFlagがFalseのとき使える
            if mdown[2] and specialrect.y < 0: #右クリック、画面の下に準備してあったら
                specialrect.x = myrect.x + 70/2 - 175/2 #プレイヤーの中心から弾が出るように
                specialrect.y = myrect.y - 120
                pg.mixer.Sound("sounds/special.wav").play()
            if specialrect.y >= -175: #弾が画面に残っていたら
                specialrect.y -= 7 #弾を上へ進める
                specialrect.x = myrect.x + 50/2 - 175/2 #カーソルの動きと連動する
                if specialrect.y < -175:
                    specialFlag = True
                screen.blit(specialimg, specialrect)

        #report（敵）を下に動かす
        if clearFlag == False: #クリア後の処理を軽くするため
            for report in reports: #配列reportsの中身（10個）を使う
                if report.y <= 600: #画面の下に到達するまで
                    report.y += 5
                    screen.blit(reportimg, report) #reportはRect
                if report.y > 600: #画面の下に来たら
                    #初期化
                    report.x = random.randint(0+25, 800-25)
                    report.y = -100
                if report.colliderect(myrect): #reportがプレイヤーと当たったら
                    state = 2
                    pg.mixer.Sound("sounds/down.wav").play()
                #通常の弾とreportが当たったら
                if report.colliderect(penrect): 
                    report.y = -100 #画面外へ消える
                    report.x = random.randint(0+25, 800-25)
                    penrect.y = -100 #画面外へ消える
                    pg.mixer.Sound("sounds/piko.wav").play()
                    score += 100 #100点入る
                #特別な弾とreportが当たったら
                if report.colliderect(specialrect): #弾とreportが当たったら
                    report.y = -100 #画面外へ消える
                    report.x = random.randint(0+25, 800-25)
                    pg.mixer.Sound("sounds/piko.wav").play()
                    score += 100 #100点入る
        
        score = score + 10 #当たらずに動いていたら+10
        if score >= 10000: #クリアしたことを示す
            clearFlag = True

        font = pg.font.Font("ipaexg.ttf", 30) #ページ数の表示
        text = font.render("ページ数："+str(score), True, pg.Color("BLACK"))
        screen.blit(text, (20, 20))

    while True:
        if second > 0:
            sakurat = time.perf_counter()

        if (state == 1) and (second > 0): #通常
            gamestage()
        elif (state == 2) or (score < 10000): #失敗
            pg.mixer.Sound("sounds/down.wav").play()
            return False
        elif (second <= 0) and (score >= 10000): #クリア
            pg.mixer.Sound("sounds/shine.mp3").play()
            time.sleep(0.5)
            return True

        #残り時間の表示
        font = pg.font.Font("ipaexg.ttf", 30)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("BLACK"))
        screen.blit(text, (20, 50))

        if specialFlag == False: #スペシャル攻撃を行っていないとき
            font = pg.font.Font("ipaexg.ttf", 30)
            text = font.render("右クリックで必殺技", True, pg.Color("BLUE"))
            screen.blit(text, (480, 20))

        if second > 3:
            font = pg.font.Font("ipaexg.ttf", 50) 
            text = font.render("卒論を10000ページかけ！", True, pg.Color(255,51,0))
            screen.blit(text, (130, 260))

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
        pg.time.Clock().tick(60)

        if second > 0:
            end = time.perf_counter()
            p_time = end - sakurat
            total += p_time

            if total >= 1:
                second -= 1
                total = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

