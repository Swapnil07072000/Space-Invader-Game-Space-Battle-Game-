#Space Battle Game

#Importing
import pygame as p
import pygame_menu as pm
import os
import time
import random


p.init()
p.font.init()

WIDTH,HEIGHT=750,650
WIN=p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Space Battle Game")

#Load Images
RED_SPACE_SHIP=p.image.load(os.path.join("Images","Final_Enemy_Red_Space_Ship.png"))
GREEN_SPACE_SHIP=p.image.load(os.path.join("Images","Final_Enemy_Green_Space_Ship.png"))
BLUE_SPACE_SHIP=p.image.load(os.path.join("Images","Final_Enemy_Blue_Space_Ship.png"))
PURPLE_SPACE_SHIP=p.image.load(os.path.join("Images","Final_Enemy_Purple_Space_Ship.png"))



#Player ship
YELLOW_SPACE_SHIP=p.image.load(os.path.join("Images","Final_Player_Space_Ship.png"))


#Lasers
RED_LASER=p.image.load(os.path.join("Images","Final_Enemy_Red_Missile.png"))
GREEN_LASER=p.image.load(os.path.join("Images","Final_Enemy_Green_Missile.png"))
BLUE_LASER=p.image.load(os.path.join("Images","Test2.png"))
YELLOW_LASER=p.image.load(os.path.join("Images","Final_Enemy_Yellow_Missile.png"))
PURPLE_LASER=p.image.load(os.path.join("Images","Final_Enemy_Purple_Missile.png"))

#Background
BG=p.transform.scale(p.image.load(os.path.join("Images","Game_Background.png")),(WIDTH,HEIGHT))

#Laser
class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=p.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def off_screen(self,height):
        return not (self.y<=height and self.y>=0)

    def collision(self,obj):
        return collide(self,obj)

#Ship
class Ship:
    COOLDOWN=30
    
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0
        

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-=10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter>=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self,x,y,lives=5,health=100):
        super().__init__(x,y,health)
        self.ship_img=YELLOW_SPACE_SHIP
        self.laser_img=YELLOW_LASER
        self.mask=p.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def scoreBD(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            return True
        
        
    def healthbar(self,window):
        p.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        p.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))
        
    
class Enemy(Ship):
    COLOR_MAP={
        "red":(RED_SPACE_SHIP,RED_LASER),
        "green":(GREEN_SPACE_SHIP,GREEN_LASER),
        "blue":(BLUE_SPACE_SHIP,BLUE_LASER),
        "purple":(PURPLE_SPACE_SHIP,PURPLE_LASER)
        }
    def __init__(self,x,y,color,health=100): 
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.COLOR_MAP[color]
        self.mask=p.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y+=vel

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x-20,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1



    
def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None

def won1():
    try:
        title='GREAT WIN'
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('YOU WON ! ! !',500,500,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=50,font_name=f2)
        menu.add.label(t1)
        menu.add.button('PLAY AGAIN',selectD,font_size=40,font_name=f2)
        #menu.add.button('RETURN TO MAIN MENU',menus,font_size=40,font_name=f2)
        menu.add.button('EXIT',out,font_size=40,font_name=f2)
        menu.mainloop(screen)

    except:
        v="Error"

def lost1():
    try:
        title='PLAY AGAIN !!!'
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('YOU LOST ! ! !',500,500,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=50,font_name=f2)
        menu.add.label(t1)
        menu.add.button('PLAY',selectD,font_size=40,font_name=f2)
        menu.add.button('RETURN TO MAIN MENU',menus,font_size=40,font_name=f2)
        menu.add.button('EXIT',out,font_size=40,font_name=f2)
        menu.mainloop(screen)
    except:
        v="Error"

def wquit():
    try:
        title='YOU PRESSED ESC !!!'
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('Want to Quit ! ! !',500,500,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=50,font_name=f2)
        menu.add.label(t1)
        menu.add.button('PLAY',selectD,font_size=40,font_name=f2)
        menu.add.button('RETURN TO MAIN MENU',menus,font_size=40,font_name=f2)
        menu.add.button('EXIT',out,font_size=40,font_name=f2)
        menu.mainloop(screen)
    except:
        v="Error"
    

def pause():
    try:
        size=[750,650]
        #f2="bernardcondensed"
        screen=p.display.set_mode(size)
        #menu=pm.Menu('PAUSED',500,500,theme=pm.themes.THEME_BLUE)
        clock=p.time.Clock()
        counter,text=10,'10'.rjust(3)
        p.time.set_timer(p.USEREVENT,1000)
        font=p.font.SysFont('comicsans',200)
        run=True
        while run:
            for event in p.event.get():
                if event.type==p.USEREVENT:
                    if counter>0:
                        counter-=1
                        text=str(counter).rjust(3)
                    else:
                        menu=pm.Menu('PAUSED',500,500,theme=pm.themes.THEME_BLUE)
                        menu.add.button('EXIT',out,font_size=40,font_name=f2)
                        menu.mainloop(screen)
                if event.type==p.QUIT:
                    run=False
            #menu.add.button('EXIT',out,font_size=40,font_name=f2)
            screen.fill((255,255,255))
            screen.blit(font.render(text,True,(0,0,0)),(300,250))
            p.display.flip()
            clock.tick(60)
            #menu.mainloop(screen)
    except:
        v="Error"
    

#Main function
def main_menu(enemy_vel,laser_vel, wave_length,d,Lev):
    run=True
    FPS=60
    level=0
    lives=5
    score=0
    score1=100
    main_font=p.font.SysFont("comicsans",50)
    lost_font=p.font.SysFont("comicsans",60)
    enemies=[]
    wave_length=wave_length
    enemy_vel=enemy_vel
    player_vel=5
    laser_vel=laser_vel
    player=Player(300,630)
    clock=p.time.Clock()
    lost=False
    lost_count=0

    def redraw_window():
        WIN.blit(BG,(0,0))

            
        #Draw Text
        lives_label=main_font.render(f"Lives: {lives}",1,(255,255,255))
        level_label=main_font.render(f"Level: {level}",1,(255,255,255))
        score_label=main_font.render(f"Score: {score}",1,(255,255,255))
        win_score=main_font.render(f"Win Score: {score1}",1,(255,255,255))
        Level=main_font.render(f"Difficult Level: {Lev}",1,(255,255,255))

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))
        WIN.blit(score_label,(10,40))
        WIN.blit(win_score,(WIDTH-win_score.get_width()-10,40))
        WIN.blit(Level,(10,70))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost1()
            

        p.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count>FPS*3:
                run=False
            else:
                continue

        if len(enemies)==0:
            level+=1
            if d=='e':
                lives+=1
                player.health=(player.health/2)+50
                wave_length+=2
                
            if d=='m':
                score1+=10
                lives+=1
                player.health=(player.health/2)+30
                
            if d=='h':
                score1+=20
                enemy_vel+=1
                laser_vel+=1
             
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500,-100),random.choice(["red","blue","green","purple"]))
                enemies.append(enemy)
        
        for event in p.event.get():
            if event.type==p.QUIT:
                p.quit()
                p.init()

        keys=p.key.get_pressed()
        #Left 
        if keys[p.K_a] and  player.x-player_vel>0:
            player.x-=player_vel
        #Right
        if keys[p.K_d] and player.x+player_vel+player.get_width()<WIDTH:
            player.x+=player_vel
        #Up
        if keys[p.K_w] and player.y-player_vel>0:
            player.y-=player_vel
        #Down
        if keys[p.K_s] and player.y+player_vel+player.get_height()+10<HEIGHT:
            player.y+=player_vel
        #Shoot
        if keys[p.K_SPACE]:
            player.shoot()
        #Esc
        if keys[p.K_ESCAPE]:
            wquit()
        #Pause
        if keys[p.K_TAB]:
            pause()
            
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,2*60)==1:
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)
            
            if enemy.y+enemy.get_height()>HEIGHT:
                lives-=1
                if d=='m' or d=='h':
                    score=score-10
                enemies.remove(enemy)

        if player.scoreBD(-laser_vel,enemies):
            score=score+10
        if score==score1:
            won1()
        



def out():
    p.quit()
    pm.quit()

def decide(d1):
    try:
        s=['e','m','h']
        for i in s:
            if d1=='e':
                main(d='e')
            elif d1=='m':
                main(d='m')
            elif d1=='h':
                main(d='h')
            else:
                print('Not Found')
    except:
        v="Error"

def selectD():
    try:
        title='SELECT DIFFICULTY'
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('SELECT',750,650,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=100,font_name=f2)
        menu.add.label(t1)
        menu.add.button('EASY',lambda:decide('e'),font_size=80,font_name=f2)
        menu.add.button('MEDIUM',lambda:decide('m'),font_size=80,font_name=f2)
        menu.add.button('HARD',lambda:decide('h'),font_size=80,font_name=f2)
        menu.add.button('RETURN',menus,font_size=80,font_name=f2)
        menu.mainloop(screen)
    except:
        v="Error"

def aboutus():
    try:
        title=" My Name is 'Pawar Swapnil Uttam'. "\
               "This is my Final Year Project on the Topic: SPACE BATTLE GAME."
               
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('ABOUT US',750,650,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=40,font_name=f2)
        menu.add.label(t1)
        menu.add.button('RETURN',menus,font_size=80,font_name=f2)
        menu.mainloop(screen)
    except:
        v="Error"
    
def menus():
    try:
        title='MAIN MENU'
        t1=''
        f=p.font.SysFont("comicsans",70)
        f1="gillsans"
        f2="bernardcondensed"
        f3="lucidafaxregular"
        f4="calisto"
        size=[750,650]
        screen=p.display.set_mode(size)
        menu=pm.Menu('Welcome',750,650,theme=pm.themes.THEME_BLUE)
        menu.add.label(title,max_char=-1,selectable=False,font_size=100,font_name=f2)
        menu.add.label(t1)
        menu.add.button('PLAY',selectD,font_size=80,font_name=f2)
        menu.add.button('QUIT',out,font_size=80,font_name=f2)
        menu.add.button('ABOUT US',aboutus,font_size=80,font_name=f2)
        menu.mainloop(screen)
    except:
        v="Error" 
 

    
def main(d):
    title_font=p.font.SysFont("comicsans",70)
    run=True
    while run:
        WIN.blit(BG,(0,0))
        title_label=title_font.render("SPACE BATTLE GAME",1,(255,255,255))
        WIN.blit(title_label,(WIDTH/2-title_label.get_width()/2,350))
        p.display.update()
        
        for event in p.event.get():
            if event.type==p.QUIT:
                run=False
            if event.type==p.MOUSEBUTTONDOWN:
                if d=='e':
                    main_menu(enemy_vel=3,laser_vel=6, wave_length=2,d='e',Lev='Easy')
                if d=='m':
                    main_menu(enemy_vel=3,laser_vel=6, wave_length=4,d='m',Lev='Medium')
                if d=='h':
                    main_menu(enemy_vel=4,laser_vel=7, wave_length=5,d='h',Lev='Hard')
                
    p.quit()
    pm.quit()

                                 
#Game start
if __name__=="__main__":
    menus()   
#main_menu()
