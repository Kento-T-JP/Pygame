import pygame as pg, sys
import random

#他のファイルにあるプログラムを読み込み
import final_maze
import final_block
import final_bar
import final_chase
import final_crash
import final_shooting
import final_boss

pg.init()
page = 0 #現在のページ（画面の状態を初期化）

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("MINI GAMEs")

#背景の画像
img1 = pg.image.load("images/root1.png") #セレクト画面
img2 = pg.image.load("images/root2.png") #ゲームオーバー1
img3 = pg.image.load("images/root3.png") #セレクト画面
img4 = pg.image.load("images/root4.png") #ゲームオーバー2
img5 = pg.image.load("images/root5.png") #クリア画面
img6 = pg.image.load("images/caution.png") #ボス直前の警告画面
img7 = pg.image.load("images/lastdame.png") #ボス戦のゲームオーバー画面

titleimg = pg.image.load("images/flower1.png") #タイトルの背景画像

next_img = pg.image.load("images/nextbtn.png") #nextのボタン

replay_img = pg.image.load("images/replaybtn.png") #replayのボタン

boss_img = pg.image.load("images/bossbtn.png") #ボス戦に進むボタン

again_img_eva = pg.image.load("images/playagain.png") #ボス戦のplay againボタン（ヱヴァンゲリヲン風）

again_img = pg.image.load("images/playlastgame.png") #直前に戻るボタン

pg.mixer.Sound("sounds/world.mp3").play(-1) #BGM、-1を引数にして無限ループ（音楽は新世界）

pushFlag = False #クリックするたびに変わる（一瞬で複数回反応するのを防ぐため）

bossFlag = False #ボス戦まで到達したらTrue

shake = 10 #画面を揺らす回数（ボス戦の前に使用）
tick = 60 #画面の更新回数（ボス戦の前に使用）

def button_to_jump(btn, newpage):
    global page, pushFlag, shake #グローバル変数にして全体に影響

    mdown = pg.mouse.get_pressed() #マウスのボタンの種類
    (mx, my) = pg.mouse.get_pos() #マウスの位置
    if mdown[0]:
        #ボタンをクリック かつ pushplagがFalseのとき
        if btn.collidepoint(mx, my) and pushFlag == False:
            pg.mixer.Sound("sounds/kyuin.mp3").play() #ボタンを押した音
            page = newpage #ページ（画面）を遷移
            pushFlag = True #クリックした印
            shake = 10 #（処理の関係上）画面が遷移したらリセット
        else:
            pushFlag = False #（処理の関係上）Falseにする

def title0(): #タイトル画面
    screen.blit(titleimg, (0,0))
    font = pg.font.Font("ipaexg.ttf", 50) 
    texting = font.render("俺のゲーム（大学編）", True, pg.Color("BLACK"))
    screen.blit(texting, (170, 230))
    btn0 = screen.blit(next_img, (330, 458))
    button_to_jump(btn0, 1) #select1に遷移

    if bossFlag == True: #ボス戦まで到達していたら
        btn1 = screen.blit(boss_img, (280, 520))
        button_to_jump(btn1, 19) #ボス戦前まで遷移

def select1(): #セレクト画面
    screen.blit(img1, (0,0))
    btn1 = screen.blit(next_img, (90, 220)) #90, 200の座標につける
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 2) #btn1はmaze2へ行く設定にする
    button_to_jump(btn2, 3) #btn2はgameover3へ行く設定にする
    button_to_jump(btn3, 0) #1つ前のページに戻る

def maze2(): #迷路ゲーム
    global page
    state = final_maze.maze() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 3 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 4 #次のステージへ

def gameover3(): #ゲームオーバー
    screen = pg.display.set_mode((800, 600))
    screen.blit(img2, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタンは最初に戻る
    button_to_jump(btn2, 1) #1つ前のページに戻る

def select4(): #セレクト画面
    screen = pg.display.set_mode((800, 600))
    screen.blit(img3, (0,0))
    btn1 = screen.blit(next_img, (90, 220))
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 5) #btn1はgameover5へ行く設定にする
    button_to_jump(btn2, 6) #btn2はblock6へ行く設定にする
    button_to_jump(btn3, 2) #1つ前のページに戻る

def gameover5(): #ゲームオーバー
    screen.blit(img4, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタン
    button_to_jump(btn2, 4) #1つ前のページに戻る

def block6(): #ブロック崩しゲーム
    global page
    state = final_block.block() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 5 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 7 #次のステージへ

def select7(): #セレクト画面
    screen.blit(img1, (0,0))
    btn1 = screen.blit(next_img, (90, 220))
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 8) #btn1はbar8へ行く設定にする
    button_to_jump(btn2, 9) #btn2はgameover9へ行く設定にする
    button_to_jump(btn3, 6) #1つ前のページに戻る

def bar8(): #ボール跳ね返しゲーム
    global page
    state = final_bar.bar() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 9 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 10 #次のステージへ

def gameover9(): #ゲームオーバー
    screen.blit(img2, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタンのみ
    button_to_jump(btn2, 7) #1つ前のページに戻る

def select10(): #セレクト画面
    screen.blit(img3, (0,0))
    btn1 = screen.blit(next_img, (90, 220)) #90, 200の座標につける
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 11) #btn1はgameover11へ行く設定にする
    button_to_jump(btn2, 12) #btn2はchase12へ行く設定にする
    button_to_jump(btn3, 8) #1つ前のページに戻る

def gameover11(): #ゲームオーバー
    screen.blit(img4, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタン
    button_to_jump(btn2, 10) #1つ前のページに戻る

def chase12(): #敵から逃げてゴールにたどり着くゲーム
    global page
    state = final_chase.chase() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 11 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 13 #次のステージへ

def select13(): #セレクト画面
    screen.blit(img1, (0,0))
    btn1 = screen.blit(next_img, (90, 220)) #90, 200の座標につける
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 14) #btn1はcrash14へ行く設定にする
    button_to_jump(btn2, 15) #btn2はgameover15へ行く設定にする
    button_to_jump(btn3, 12) #1つ前のページに戻る

def crash14(): #素早く動くオブジェクトにタッチするゲーム
    global page
    state = final_crash.crash() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 15 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 16 #次のステージへ

def gameover15(): #ゲームオーバー
    screen.blit(img2, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタン
    button_to_jump(btn2, 13) #1つ前のページに戻る

def select16(): #セレクト画面
    screen.blit(img1, (0,0))
    btn1 = screen.blit(next_img, (90, 220)) #90, 200の座標につける
    btn2 = screen.blit(next_img, (590, 220))
    btn3 = screen.blit(again_img, (360, 390))
    button_to_jump(btn1, 17) #btn1はgameover17へ行く設定にする
    button_to_jump(btn2, 18) #btn2はshooting18へ行く設定にする
    button_to_jump(btn3, 14) #1つ前のページに戻る

def gameover17(): #ゲームオーバー
    screen.blit(img4, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    btn2 = screen.blit(again_img, (30, 507))
    button_to_jump(btn1, 0) #リプレイボタン
    button_to_jump(btn2, 16) #1つ前のページに戻る

def shooting18(): #シューティングゲーム
    global page
    state = final_shooting.shooting() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 17 #ゲームオーバー
    elif state == True: #成功→次のステージへ
        page = 19 #次のステージへ

def go_to_boss19(): #ボスへの挑戦前の画面
    global shake, tick
    screen = pg.display.set_mode((800, 600))
    if shake == 10:
        pg.mixer.Sound("sounds/warning.mp3").play()
    if shake > 0:
        tick = 5 #画面の更新回数を60から5に減らして画面が揺れる演出をする準備をする
        shake = shake - 1 #揺らす回数を0まで減らす
        bx = random.randint(-20, 20) #左右に揺らす
        by = random.randint(-10, 10) #上下に揺らす
    elif shake == 0: #画面が揺れないようにする
        bx = 0 
        by = 0
        tick = 60 #画面の更新回数を60に戻す
    screen.blit(img6, [0+bx, 0+by]) #画面が揺れる
    btn1 = screen.blit(boss_img, (575+bx, 526+by)) #ボス戦へのボタンも揺らす
    btn2 = screen.blit(again_img, (30+bx, 515+by)) #１つ戻るボタンも揺らす
    btn3 = screen.blit(replay_img, (630+bx, 5+by)) #リプレイボタンも揺らす
    button_to_jump(btn1, 20) #リプレイボタン
    button_to_jump(btn2, 16) #1つ前のページに戻る
    button_to_jump(btn3, 0) #最初に戻る

def boss20(): #ボス戦（シューティングゲーム系）
    global page
    state = final_boss.boss() #クリアしたらTrueを返す、失敗したらFalseを返す関数
    if state == False: #失敗→ゲームオーバー
        page = 21 #ゲームオーバー
    elif state == True: #成功
        page = 22 #クリア

def gameover21(): #ゲームオーバー
    screen.blit(img7, (0,0))
    btn1 = screen.blit(again_img_eva, (325, 420))
    button_to_jump(btn1, 20) #リプレイボタン


def clear22(): #クリア画面
    screen.blit(img5, (0,0))
    btn1 = screen.blit(replay_img, (600, 520))
    button_to_jump(btn1, 0) #リプレイボタン

while True:
    if page == 0:
        title0()

    elif page == 1:
        select1()

    elif page == 2:
        maze2()
    
    elif page == 3:
        gameover3()

    elif page == 4:
        select4()
    
    elif page == 5:
        gameover5()
    
    elif page == 6:
        block6()

    elif page == 7:
        select7()
    
    elif page == 8:
        bar8()

    elif page == 9:
        gameover9()
    
    elif page == 10:
        select10()
    
    elif page == 11:
        gameover11()

    elif page == 12:
        chase12()

    elif page == 13:
        select13()
    
    elif page == 14:
        crash14()

    elif page == 15:
        gameover15()
    
    elif page == 16:
        select16()

    elif page == 17:
        gameover17()

    elif page == 18:
        shooting18()
    
    elif page == 19:
        bossFlag = True #ボス戦まで到達したのでTrue
        go_to_boss19()

    elif page == 20:
        boss20()

    elif page == 21:
        gameover21()

    elif page == 22:
        clear22()

    pg.display.update()
    pg.time.Clock().tick(tick)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

