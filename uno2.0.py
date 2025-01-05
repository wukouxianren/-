import os
from PIL import Image, ImageTk
import tkinter as tk
import random
import pygame
import time
pygame.mixer.init()
zhuapai_sound=pygame.mixer.Sound('zhuapai3.0.wav')
chupai_sound=pygame.mixer.Sound('chuapi.wav')
#牌组---------------------------------------------
card=[None]*108
for i in range(108):
    card[i]=i
card_calor=['红','黄','蓝','绿','红','黄','蓝','绿']
card_number=[0,1,2,3,4,5,6,7,8,9,10]
card_action=['+2','+4','反转','电击','跳过']
card_rest=[]
add=0
player_now=random.randint(0,3)
judge_position=0
card_type={}
for i in range(80):
    card_type[i]={}
    card_type[i]['number']=card_number[i%10]
    card_type[i]['color']=card_calor[i//10]
    card_type[i]['action']='N'
for i in range(80,104):
    card_type[i]={}
    card_type[i]['number']=card_number[10]
    card_type[i]['color']=card_calor[(i-80)//3]
    card_type[i]['action']=card_action[i%3]
for i in range(104,108):
    card_type[i]={}
    card_type[i]['number']=card_number[10]
    card_type[i]['color']='super'
    card_type[i]['action']=card_action[3] if i-104>=2 else card_action[4]
#图片调整--------------------------------------------------------
def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths
image_paths=get_file_paths("uno3.0")
image=[]
#print(image_paths)
root=tk.Tk()
root.geometry("500x500")
buttons=[]
def resize_image(image_path, size):
    global image_paths
    global root
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)
image_size = (120, 180)
for i in range(109):
    image.append(resize_image(image_paths[i], image_size))
    #玩家------------------------------------------------------
player={
    0:{'hurt':0,'card':[]},
    1:{'hurt':0,'card':[]},
    2:{'hurt':0,'card':[]},
    3:{'hurt':0,'card':[]}
}
#牌组运动---------------------------------------------
def wash_card():
    random.shuffle(card)
    #return card
def license_card():
    for i in range(4):
        for j in range(8):
            player[i]['card'].append(card[i*8+j])
    for i in range(32,108):
        card_rest.append(card[i])
def get_card():
    player[player_now%4]['card'].append(card_rest.pop(-1))
    zhuapai_sound.play()
    time.sleep(0.3)
    #return card 
def send_card(a):
    x=player[player_now%4]['card'][a]
    card_rest.insert(0,card_rest)
    card_rest[0]=x
    player[player_now%4]['card'].pop(a)
    chupai_sound.play()
def sort_card():
    global player_now
    for i in range(len(player[player_now%4]['card'])):
        if 40<=player[(player_now)%4]['card'][i]<80:
            player[(player_now)%4]['card'][i]=player[(player_now)%4]['card'][i]-40
    for i in range(len(player[player_now%4]['card'])):
        for j in range(len(player[player_now%4]['card'])-i-1):
            if player[player_now%4]['card'][j]>player[player_now%4]['card'][j+1]:
                player[player_now%4]['card'][j],player[player_now%4]['card'][j+1]=player[player_now%4]['card'][j+1],player[player_now%4]['card'][j]
def clean(a):
    return list(set(a))
def show_card(s):
    if isinstance(s,list):
        for i in range(len(s)):
            print(i,end=' ')
            print(card_type[s[i]])
    else:
        print(card_type[s])
    return s
def chupai(allchoice):
    global player
    global player_now
    global add
    choice=eval(input())
    if choice==100:
        get_card()
        player_now=player_now+1 if judge_position==0 else player_now-1
    elif 0<=choice<len(player[player_now%4]['card']):
        if player[player_now%4]['card'][choice] in allchoice and card_type[player[player_now%4]['card'][choice]]['action']=='N':
            send_card(choice)
            player_now=player_now+1 if judge_position==0 else player_now-1
        elif (player[player_now%4]['card'][choice] in allchoice) is False:
            print('输入错误，请重新输入')
            chupai(allchoice)
        else:
            send_card(choice)
            player_now=player_now+1 if judge_position==0 else player_now-1
            if card_type[card_rest[0]]['action']=='电击':
                player[player_now%4]['hurt']=1
            elif card_type[card_rest[0]]['action']=='+2':
                player[player_now%4]['hurt']=2
                add+=1
            elif card_type[card_rest[0]]['action']=='+4':
                player[player_now%4]['hurt']=3
                add+=1
            else:
                panduan(card_rest[0])    
    else:
        print('输入错误，请重新输入')
        chupai(allchoice)
   
#功能牌的功能实现--------------------------------------------
#+2
def add_two():
    global add
    player[player_now%4]['hurt']=0
    for i in range(2*add):
        get_card()
    add=0
    return player
#+4
def add_four():
    global add
    player[player_now%4]['hurt']=0
    for i in range(4*add):
        get_card()
    add=0
    return player
#反转
def reverse():
    global judge_position
    judge_position=1 if judge_position==0 else 0
    return judge_position
#跳过
def skip():
    global player
    global player_now
    a=player[player_now%4]['hurt']
    player[player_now%4]['hurt']=0

    player_now=player_now+1 if judge_position==0 else player_now-1
    player[player_now%4]['hurt']=a
    return player
#电击
def stun_gun():
    player[player_now%4]['hurt']=0
    for i in range(random.randint(1,10)):
        get_card()
    return player 
def panduan(a):
    if card_type[a]['action']=='+2':
        add_two()
    if card_type[a]['action']=='+4':
        add_four()
    if card_type[a]['action']=='反转':
        reverse()
    if card_type[a]['action']=='电击':
        stun_gun()
    return player
#出牌规则----------------------------------------------
def rule(allchoice):
    #super
    for i in range(len(player[player_now%4]['card'])):
        if card_type[player[player_now%4]['card'][i]]['action']=='跳过':
            allchoice.append(player[player_now%4]['card'][i])
    #judge number
    for i in range(len(player[player_now%4]['card'])):
        if (card_type[player[player_now%4]['card'][i]]['number']==card_type[card_rest[0]]['number']) and (card_type[player[player_now%4]['card'][i]]['number']!=10):
            allchoice.append(player[player_now%4]['card'][i])
    #judge color
    for i in range(len(player[player_now%4]['card'])):
        if card_type[player[player_now%4]['card'][i]]['color']==card_type[card_rest[0]]['color']:
            allchoice.append(player[player_now%4]['card'][i])
        if card_type[player[player_now%4]['card'][i]]['color']=='super':
            allchoice.append(player[player_now%4]['card'][i])
        if card_type[card_rest[0]]['color']=='super':
            allchoice.append(player[player_now%4]['card'][i])
    #judge action
    for i in range(len(player[player_now%4]['card'])):
        if (card_type[player[player_now%4]['card'][i]]['action']==card_type[card_rest[0]]['action']) and (card_type[player[player_now%4]['card'][i]]['action']!='N'):
            allchoice.append(player[player_now%4]['card'][i])
    print(allchoice)
    return allchoice
def judge_skip():
    global player_now
    global judge_position
    for i in range(len(player[player_now%4]['card'])):
        if card_type[player[player_now%4]['card'][i]]['action']=='跳过':
            print("是否跳过？（是1/否2）")
            choice=eval(input())
            if choice==1:
                zz=random.randint(1,len(card_rest))
                x=player[player_now%4]['card'][i]
                card_rest.insert(zz,card_rest)
                card_rest[zz]=x
                player[player_now%4]['card'].pop(i)
                skip()
                return 0
            elif choice==2:
                print('不跳过，承受攻击')
                panduan(card_rest[0])
                input("请按任意键继续...")
                player_now=player_now+1 if judge_position==0 else player_now-1
                return 0
            else:
                print('输入错误，请重新输入')
                judge_skip()
    print('受到底牌攻击')
    panduan(card_rest[0])
    input("请按任意键继续...")
    player_now=player_now+1 if judge_position==0 else player_now-1
def judge_add2():
                global add
                global player_now

                allchoice2=[]
                for i in range(len(player[player_now%4]['card'])):
                    if card_type[player[player_now%4]['card'][i]]['action']=='+2':
                        allchoice2.append(player[player_now%4]['card'][i])
                if len(allchoice2)==0:
                    judge_skip()
                else:
                    print('请选择要出的牌：（仅需输入序号即可）,选择承受攻击请输入100')
                    choice=eval(input())
                    if choice==100:
                        panduan(card_rest[0])
                        player_now=player_now+1 if judge_position==0 else player_now-1
                    elif player[player_now%4]['card'][choice] in allchoice2:
                        send_card(choice)
                        add+=1
                        player[player_now%4]['hurt']=0
                        player_now=player_now+1 if judge_position==0 else player_now-1
                        player[player_now%4]['hurt']=2
                    
                    else:
                        print('输入错误，请重新输入')
                        judge_add2()
def judge_add4():
                global add
                global player_now
                allchoice2=[]
                for i in range(len(player[player_now%4]['card'])):
                    if card_type[player[player_now%4]['card'][i]]['action']=='+4':
                        allchoice2.append(player[player_now%4]['card'][i])
                if len(allchoice2)==0:
                    judge_skip()
                else:
                    print('请选择要出的牌：（仅需输入序号即可）,选择承受攻击请输入100')
                    choice=eval(input())
                    if choice==100:
                        panduan(card_rest[0])
                        player_now=player_now+1 if judge_position==0 else player_now-1
                    elif player[player_now%4]['card'][choice] in allchoice2:
                        send_card(choice)
                        add+=1
                        player[player_now%4]['hurt']=0
                        player_now=player_now+1 if judge_position==0 else player_now-1
                        player[player_now%4]['hurt']=3
                    
                    else:
                        print('输入错误，请重新输入')
                        judge_add4()    
def judge_min():
    global player
    global player_now
    xx=int(100)
    min=0
    for i in range(4):
        if len(player[i]['card'])<xx:
            xx=len(player[i]['card'])
            min=i 
    return min 
#窗口测试--------------------------------------------------------
#游戏开始----------------------------------------------
def prepare():
    wash_card()
    license_card()
    sort_card()
    #print(f'玩家{player_now%4}的牌是：')
    #show_card(player[player_now%4]['card'])
    #print('牌组剩余的牌是：')
    #show_card(card_rest)
    print('游戏开始')
#游戏进行-------------------------------------------------
def play_under():
    global judge_position
    global add
    global player_now
    
    while len(card_rest)>0:
        print(f'玩家{player_now%4}的牌是：')
        #sort_card()
        show_card(player[player_now%4]['card'])
        print('底牌是：')
        show_card(card_rest[0])#以上用显示按钮换
        if player[player_now%4]['hurt']==0:
            allchoice=[]
            allchoice=rule(allchoice)
            if len(allchoice)==0:  
                print('无牌可出，自动摸牌')
                input("请按任意键继续...")
                get_card()
                player_now=player_now+1 if judge_position==0 else player_now-1
            else:
                print('请选择要出的牌：（仅需输入序号即可）,不出请输入100')
                chupai(allchoice)#改成按键，案件反馈用牌编号如果可以出再次打印按钮，反之在窗口打印错误并在玩家确认后再次打印按钮
        elif player[player_now%4]['hurt']!=0:
            if player[player_now%4]['hurt']==1:
                judge_skip()#判断按钮存在
            elif player[player_now%4]['hurt']==2:
                judge_add2()
            elif player[player_now%4]['hurt']==3:
                judge_add4()
            #根据原有函数适度增改                  
        if (len(player[(player_now-1)%4]['card'])==0) or (len(player[(player_now+1)%4]['card'])==0):
            print('游戏结束')
            print("*********************************************")
            print("\n"*5)
            winner=(player_now-1)%4 if len(player[(player_now-1)%4]['card'])==0 else (player_now+1)%4
            print(f'玩家{winner}赢了')#胜利界面打印
            print("\n"*5)
            print("*********************************************")
            break
        if len(card_rest)<0:
            print('底牌摸完，游戏结束')
            print(f'玩家{judge_min()}赢了')#胜利界面打印
            break                     
def judge_win():
    global player
    global player_now
    if len(player[player_now%4]['card'])==0:
        win_window=tk.Toplevel(root)
        win_window.geometry("500x500")
        label=tk.Label(win_window,text='you win')
        label.pack()
        return
    if len(card_rest)<=0:
        a=judge_min()
        win_window=tk.Toplevel(root)
        win_window.geometry("500x500")
        label=tk.Label(win_window,text="玩家{}赢了".format(a))
        label.pack()
        return
def click_skip():
    global player
    global player_now
    global add
    global judge_position
    global card_rest
    if player[player_now%4]['hurt']==0:
        get_card()
        judge_win()
        player_now=player_now+1 if judge_position==0 else player_now-1
    elif player[player_now%4]['hurt']!=0:
        panduan(card_rest[0])
        judge_win()
        player_now=player_now+1 if judge_position==0 else player_now-1
    label=tk.Label(root,text='玩家{}'.format(player_now%4),height=1,width=5,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=800,y=650)
    x=0
    for i in range(3):
        x+=len(player[(player_now+i)%4]['card'])
    for i in range(x+1):
        others[i].place_forget()
    print_others()
    for i in range(len(buttons)):
        buttons[i].place_forget()
    sort_card()
    for i in range(len(player[player_now%4]['card'])):
        buttons[i].configure(image=image[player[player_now%4]['card'][i]],command=lambda i=i:button_click(i))
        buttons[i].place(x=(1560-len(player[player_now%4]['card'])*50+50)/2+i*50,y=700)
        
        #buttons[i].grid(row=i//16,column=i%16)
def chupai_on(allchoice,xx):
    global player
    global player_now
    global add
    global judge_position
    global buttons
    global root
    choice=xx
    if player[player_now%4]['card'][choice] in allchoice and card_type[player[player_now%4]['card'][choice]]['action']=='N':
        send_card(choice)
        judge_win()
        player_now=player_now+1 if judge_position==0 else player_now-1
    elif (player[player_now%4]['card'][choice] in allchoice) is False:
        error_window=tk.Toplevel(root)
        error_window.geometry("150x100")
        label=tk.Label(error_window,text='输入错误，请重新输入')
        label.place(x=0,y=0)
    else:
        send_card(choice)
        judge_win()
        player_now=player_now+1 if judge_position==0 else player_now-1
        if card_type[card_rest[0]]['action']=='电击':
            player[player_now%4]['hurt']=1
        elif card_type[card_rest[0]]['action']=='+2':
            player[player_now%4]['hurt']=2
            add+=1
        elif card_type[card_rest[0]]['action']=='+4':
            player[player_now%4]['hurt']=3
            add+=1
        else:
            panduan(card_rest[0])   
def button_click(xx):
    global player
    global player_now
    global buttons
    global judge_position
    global add
    if player[player_now%4]['hurt']==0:
            allchoice=[]
            allchoice=rule(allchoice)
            if len(allchoice)==0:
                nocard_window=tk.Toplevel(root)
                nocard_window.geometry("150x100")
                label=tk.Label(nocard_window,text='无牌可出，自动摸牌')
                label.place(x=0,y=0)
                get_card()
                judge_win()
                player_now=player_now+1 if judge_position==0 else player_now-1
            else:
                chupai_on(allchoice,xx)
    elif player[player_now%4]['hurt']!=0:
            if player[player_now%4]['hurt']==1:
                if card_type[player[player_now%4]['card'][xx]]['action']=='跳过':
                    zz=random.randint(1,len(card_rest))
                    x=player[player_now%4]['card'][xx]
                    card_rest.insert(zz,card_rest)
                    card_rest[zz]=x
                    player[player_now%4]['card'].pop(xx)
                    judge_win()
                    skip()
                else:
                    error_window=tk.Toplevel(root)
                    error_window.geometry("150x100")
                    label=tk.Label(error_window,text='输入错误，可选择跳过承受攻击')
                    label.place(x=0,y=0)
            elif player[player_now%4]['hurt']==2:
                if card_type[player[player_now%4]['card'][xx]]['action']=='+2':
                    send_card(xx)
                    judge_win()
                    add+=1
                    player[player_now%4]['hurt']=0
                    player_now=player_now+1 if judge_position==0 else player_now-1
                    player[player_now%4]['hurt']=2
                elif card_type[player[player_now%4]['card'][xx]]['action']=='跳过':
                    zz=random.randint(1,len(card_rest))
                    x=player[player_now%4]['card'][xx]
                    card_rest.insert(zz,card_rest)
                    card_rest[zz]=x
                    player[player_now%4]['card'].pop(xx)
                    judge_win()
                    skip()
                else:
                    error_window=tk.Toplevel(root)
                    error_window.geometry("150x100")
                    label=tk.Label(error_window,text='输入错误，可选择跳过承受攻击')
                    label.place(x=0,y=0)
            elif player[player_now%4]['hurt']==3:
                if card_type[player[player_now%4]['card'][xx]]['action']=='+4':
                    send_card(xx)
                    judge_win()
                    add+=1
                    player[player_now%4]['hurt']=0
                    player_now=player_now+1 if judge_position==0 else player_now-1
                    player[player_now%4]['hurt']=3
                elif card_type[player[player_now%4]['card'][xx]]['action']=='跳过':
                    zz=random.randint(1,len(card_rest))
                    x=player[player_now%4]['card'][xx]
                    card_rest.insert(zz,card_rest)
                    card_rest[zz]=x
                    player[player_now%4]['card'].pop(xx)
                    judge_win()
                    skip()
                else:
                    error_window=tk.Toplevel(root)
                    error_window.geometry("150x100")
                    label=tk.Label(error_window,text='输入错误，可选择跳过承受攻击')
                    label.place(x=0,y=0)
    else:
        error_window=tk.Toplevel(root)
        error_window.geometry("150x100")
        label=tk.Label(error_window,text='错误oqjndvsifebfjsbdnvs')
        label.place(x=0,y=0)
    label=tk.Label(root,text='玩家{}'.format(player_now%4),height=1,width=5,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=800,y=650)
    x=0
    for i in range(3):
        x+=len(player[(player_now+i)%4]['card'])
    for i in range(x+1):
        others[i].place_forget()
    print_others()
    if random.randint(0,1)==1:
        dipai=tk.Label(root,image=image[card_rest[0]])
        dipai.place(x=800,y=380) 
    else:
        dipai=tk.Label(root,image=image[card_rest[0]])
        dipai.place(x=780,y=380)             
    for i in range(len(buttons)):
        buttons[i].place_forget()
    sort_card()
    for i in range(len(player[player_now%4]['card'])):
        buttons[i].configure(image=image[player[player_now%4]['card'][i]],command=lambda i=i:button_click(i))
        buttons[i].place(x=(1560-len(player[player_now%4]['card'])*50+50)/2+i*50,y=700)
        
        #buttons[i].grid(row=i//16,column=i%16)
others=[]
def print_others():
    global player_now
    global player
    global others
    global judge_position
    x=0
    for i in range(3):
        x+=len(player[(player_now+i)%4]['card'])
    for i in range(x+1):
        others.append(tk.Label(root,image=image[-1]))
    for j in range(len(player[(player_now+1 if judge_position==0 else player_now-1)%4]['card'])):
        others[j].place(x=40,y=((800-(len(player[(player_now+1 if judge_position==0 else player_now-1)%4]['card']))*40-130)/2+j*40))
    for p in range(len(player[(player_now+2 if judge_position==0 else player_now-2)%4]['card'])):
        others[p+len(player[(player_now+1 if judge_position==0 else player_now-1)%4]['card'])].place(x=(1560-len(player[(player_now+2 if judge_position==0 else player_now-2)%4]['card'])*50+50)/2+p*50,y=0)
    for m in range(len(player[(player_now+3 if judge_position==0 else player_now-3)%4]['card'])):
        others[m+len(player[(player_now+1 if judge_position==0 else player_now-1)%4]['card'])+len(player[(player_now+2 if judge_position==0 else player_now-2)%4]['card'])].place(x=1540,y=((800-(len(player[(player_now+3 if judge_position==0 else player_now-3)%4]['card']))*40-130)/2+m*40))
    label=tk.Label(root,text='玩',height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=1450,y=300)
    label=tk.Label(root,text='家',height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=1450,y=329)
    label=tk.Label(root,text=(player_now+3 if judge_position==0 else player_now-3)%4,height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=1450,y=358)
    label=tk.Label(root,text='玩',height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=180,y=300)
    label=tk.Label(root,text='家',height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=180,y=329)
    label=tk.Label(root,text=(player_now+1 if judge_position==0 else player_now-1)%4,height=1,width=2,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=180,y=358)
    label=tk.Label(root,text='玩家{}'.format((player_now+2 if judge_position==0 else player_now-2)%4),height=1,width=5,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=800,y=200)
def play_on():
    global judge_position
    global add
    global player_now
    #背景---------------------------------
    image11 = Image.open("bg.png")  
    image11 = image11.resize((1710, 890), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image11)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0,y=0)
    #底牌和一些信息-------------------------------------------
    label=tk.Label(root,text='玩家{}'.format(player_now%4),height=1,width=5,font=('宋体',20), bg="SystemButtonFace")
    label.place(x=800,y=650)
    di=[]
    for i in range(7):
        di.append(tk.Label(root,image=image[-1]))
        di[i].place(x=560+5*i,y=230+2*i)
    dipai=tk.Label(root,image=image[card_rest[0]])
    dipai.place(x=780,y=380)
    button_skip=tk.Button(root,text='跳过',command=click_skip,height=2,width=15)
    button_skip.place(x=1450,y=780)
    #其他玩家-------------------------------------------------
    
    print_others()
    #手牌----------------------------------------------------
    sort_card()
    for i in range(len(player[player_now%4]['card'])):
        buttons.append(tk.Button(root,image=image[player[player_now%4]['card'][i]],command=lambda i=i:button_click(i),borderwidth=0,highlightthickness=0))
        buttons[i].place(x=(1560-len(player[player_now%4]['card'])*50+50)/2+i*50,y=690)
        #buttons[i].grid(row=0,column=i)
    for i in range(8,80):
        buttons.append(tk.Button(root,image=image[107]))
        buttons[i].place(x=1000,y=1000)
    root.mainloop()
def main():
    prepare()
    #play_under()
    play_on()
main()