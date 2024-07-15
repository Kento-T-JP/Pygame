import pygame as pg, sys
import random
import time

def maze():
    global goalFlag, cardFlag, pl_x, pl_y
    second = 12 #12秒以内
    total = 0 #時間計測で使用
    pl_x = 1 #プレイヤーのx座標
    pl_y = 1 #プレイヤーのy座標
    MAZE_W = 10 #迷路の横幅（列の数）
    MAZE_H = 7 #迷路の縦幅（行の数）
    W = 80 #1マスのサイズ（横）
    H = 80 #1マスのサイズ（縦）
    maze = [] #ダンジョンの枠組み
    cardFlag = False #カードをゲットしたらTrue
    goalFlag = False #ゴールしたらTrue

    screen = pg.display.set_mode((800, 560))
    clock = pg.time.Clock()

    imgPlayer = pg.image.load("images/player.png") #プレイヤーの画像
    imgPlayer = pg.transform.scale(imgPlayer, (80, 80))
    myrect = pg.Rect(80, 80, 80, 80)

    #背景の画像
    imgWall = pg.image.load("images/wall.png") #壁
    imgWall = pg.transform.scale(imgWall, (80, 80))
    imgFloor = pg.image.load("images/floor.png") #床
    imgFloor = pg.transform.scale(imgFloor, (80, 80))
    starimg = pg.image.load("images/castle.png") #スタートの位置の画像
    starimg = pg.transform.scale(starimg, (80, 80))
    goalimg = pg.image.load("images/univ.png") #ゴールの位置の画像
    goalimg = pg.transform.scale(goalimg, (80, 80))

    cardimg = pg.image.load("images/card.png") #カード（アイテム）の画像
    cardimg = pg.transform.scale(cardimg, (70, 70))
    cardRect = pg.Rect(80*(MAZE_W-2), 80, 80, 80)

    #迷路の配列（空）を作る
    for y in range(MAZE_H):
        maze.append([0]*MAZE_W) #9行11列の行列

    #ランダムに迷路を作る関数
    def make_maze():
        #壁をランダムで作る時に方向を指定するために定義
        XP = [0, 1, 0, -1] #(上、右、下、左)の方向
        YP = [-1, 0, 1, 0] #(上、右、下、左)の方向

        #0が通路, 1が壁、xが横方向（列）, yが縦方向（行）
        for x in range(MAZE_W):
            maze[0][x] = 1 #1行目は1
            maze[MAZE_H-1][x] = 1 #6行目は1
        
        for y in range(MAZE_H-1):
            maze[y][0] = 1 #1列目は1
            maze[y][MAZE_W-1] = 1 #10列目は1
    #ここまでで外側が一周壁になる

        for y in range(1, MAZE_H-1): #2行目から6行目
            for x in range(1, MAZE_W-1): #2列目から9列目
                maze[y][x] = 0 #内側は全て0

        for y in range(2, MAZE_H-2, 2): #3, 5行目
            for x in range(2, MAZE_W-1, 2): #3, 5, 7, 9列目
                maze[y][x] = 1 #奇数番目は1
    #これで奇数番目に壁ができた（壁のチェック柄のような感じ）

        for y in range(2, MAZE_H-2, 2): #3, 5行目
            for x in range(2, MAZE_W-2, 2): #カード（アイテム）を置く9列目にはランダムに壁を作らない（3, 5, 7列目）
                d = random.randint(0, 3) #0から3までの乱数
                if x > 2: #3だったら
                    d = random.randint(0, 2)
                maze[y+YP[d]][x+XP[d]] = 1 
                #一番左の通路は4方向にランダムで壁を作る
                #左以外は3方向にランダムで壁を作る（袋小路ができてしまうから）

    #画面に迷路やプレイヤーなどを出力
    def draw(screen):
        global goalFlag, cardFlag
        CYAN = [0, 255, 255] #スタートの色
        RED = [255, 0, 0] #ゴールの色

        #迷路を描画
        for y in range(MAZE_H):
            for x in range(MAZE_W):
                X = x*W #描画を行う座標（左端）
                Y = y*H #描画を行う座標（上）
                if maze[y][x] == 0: #通路
                    screen.blit(imgFloor, [X, Y])
                if maze[y][x] == 1: #壁
                    screen.blit(imgWall, [X, Y])
                if (x == 1) and (y == 1): #スタート
                    pg.draw.rect(screen, CYAN, [X, Y, W, H])
                    screen.blit(starimg, [X, Y])
                if (x == MAZE_W-2) and (y == MAZE_H-2): #ゴール
                    pg.draw.rect(screen, RED, [X, Y, W, H])
                    screen.blit(goalimg, [X, Y])

        #カード（アイテム）を拾ったかの判定
        if cardRect.colliderect(myrect): #プレイヤーがアイテムに触れたら
            pg.mixer.Sound("sounds/card.mp3").play()
            cardFlag = True #カードをゲットした印
            #アイテムの座標を画面外にしてカードを消す
            cardRect.x = 800
            cardRect.y = 600

            #ゴールに着いてからクリアするようにする（順番が逆にならないようにする）
            if goalFlag == True:
                goalFlag = False

        #プレイヤーとカードを描写
        screen.blit(imgPlayer, myrect)
        screen.blit(cardimg, cardRect)

    #プレイヤーの動きを設定
    def move_player():
        global pl_x, pl_y, goalFlag
        key = pg.key.get_pressed() #押されたキーを取得
        if key[pg.K_UP] == 1: #上方向のキーなら
            if maze[pl_y-1][pl_x] != 1: #壁(1)に当たらなければ
                pl_y = pl_y - 1 #上に動く（y方向に-1する）
                myrect.y -= H #上に１ブロック分動く（画面上の座標の設定）
                pg.mixer.Sound("sounds/walk.wav").play() #足音
        if key[pg.K_DOWN] == 1: #下方向なら
            if maze[pl_y+1][pl_x] != 1:
                pl_y = pl_y + 1 
                myrect.y += H
                pg.mixer.Sound("sounds/walk.wav").play()
        if key[pg.K_LEFT] == 1: #左方向なら
            if maze[pl_y][pl_x-1] != 1:
                pl_x = pl_x - 1 
                myrect.x -= W
                pg.mixer.Sound("sounds/walk.wav").play()
        if key[pg.K_RIGHT] == 1: #右方向なら
            if maze[pl_y][pl_x+1] != 1:
                pl_x = pl_x + 1 
                myrect.x += W
                pg.mixer.Sound("sounds/walk.wav").play()

        if pl_x == MAZE_W-2 and pl_y == MAZE_H-2: #ゴールしたら
            goalFlag = True #ゴールした印

    make_maze() #迷路を作る（ランダムに変わらないようにループの外に出す）

    while True:
        if second > 0: #残り時間が0秒より大きかったら
            start = time.perf_counter() #計測スタート

        #クリアしたかどうかの判定
        if (goalFlag == True) and (cardFlag == True): #アイテムをゲットしてゴールしたら
            pg.mixer.Sound("sounds/shine.mp3").play()
            return True #True（成功）を返す
        elif second <= 0: #制限時間オーバーのとき
            pg.mixer.Sound("sounds/down.wav").play()
            return False #False（失敗）を返す

        move_player() #プレイヤーを動かす
        draw(screen) #画面への描画を行う

        #残り時間を表示
        font = pg.font.Font("ipaexg.ttf", 40)
        text = font.render("のこり"+str(second)+"秒", True, pg.Color("WHITE"))
        screen.blit(text, (25, 20))

        font = pg.font.Font("ipaexg.ttf", 40) 
        texting = font.render("学生証を拾って赤色へいけ！", True, pg.Color("WHITE"))
        screen.blit(texting, (270, 20))

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
        clock.tick(10) #1秒間に10回以下更新

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
