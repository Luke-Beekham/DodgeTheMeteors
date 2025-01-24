import pygame
import random
import os

pygame.init()

win =  pygame.display.set_mode((1300, 650))


run = True

# Get the path of the current file
current_file_path = __file__

# Get the directory containing the current file
current_dir = os.path.dirname(current_file_path)
print(current_dir)

ImagesFolder = current_dir + "/Images/"
SoundsFolder = current_dir + "/SoundEffects/"



GameOverScreen = pygame.image.load(ImagesFolder + "BackGroundGameOver.png").convert()
MainMenuScreen = pygame.image.load(ImagesFolder + "BackGroundStart.png").convert()
GameBackgroundScreen = pygame.image.load(ImagesFolder + "Background.png").convert()

pygame.display.set_caption("Dodge The Meteors")


start = False

class Music:
    def __init__(self, music, playTime,vol):
        self.music = music
        self.vol = vol
        self.played = False
        self.playedTime = playTime
        self.lastPlayedTime = 0

    def play(self,currentTime):    
        if not self.played or (currentTime - self.lastPlayedTime > self.playedTime):
            pygame.mixer.init()
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play()

            self.played = True
            self.lastPlayedTime = currentTime
    def stop(self):
        if self.played:
            pygame.mixer.music.stop() 
            self.played = False

class Sound:
    Channel = -1
    def __init__(self, sound, playTime,vol):
        self.sound = pygame.mixer.Sound(sound)
        self.vol = self.sound.set_volume(vol)
        self.played = False
        self.playedTime = playTime
        self.lastPlayedTime = 0
        Sound.Channel += 1
        self.Channel = pygame.mixer.Channel(Sound.Channel)
        

    def play(self):
        currentTime = pygame.time.get_ticks()
        # if not self.played or (currentTime - self.lastPlayedTime > self.playedTime):
        self.Channel.play(self.sound)
        self.played = True
        self.lastPlayedTime = currentTime
    def stop(self):
        if self.played:
            self.sound.stop()
            self.played = False
                               
                 
  

MainMenuMusic = Music(SoundsFolder + "MainMenu.wav", 20000,1)
GameTrackMusic = Music(SoundsFolder + "GameTrack.wav", 60000,0.5)
GameOverMusic = Music(SoundsFolder + "GameOver.wav", 10000,1)

class Text:
    def __init__(self, x, y, text, font, color):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.textSurface = font.render(text, True, color,(0,0,0))
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (x, y)
    
    def draw(self, win):
        if start == False: return
        win.blit(self.textSurface, self.textRect)
    
    def updateText(self,newText):
        self.text = newText 
        self.textSurface = self.font.render(self.text, True, self.color,(0,0,0))
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (self.x, self.y)
        


velocityFont = pygame.font.Font('freesansbold.ttf', 16)

velocityText = Text(100, 50, 'Velocity: 0', velocityFont, (0,255,0))

livesFont = pygame.font.Font('freesansbold.ttf',16)

livesText = Text(100,100,'Lives: 5',livesFont,(255,0,0))

timeLivedFont = pygame.font.Font('freesansbold.ttf',16)

timeLivedText = Text(100,150,'Time Lived: 0',timeLivedFont,(3, 173, 252))




class Object:
    MeteorCrashSound = Sound(SoundsFolder +"MeteorCrash.wav",1000,0.5)
    Meteor = pygame.image.load(ImagesFolder+"Meteor.png").convert_alpha()
    ObjectWarning = pygame.image.load(ImagesFolder+"ObjectWarning.png").convert_alpha()
    ObjectList = []
    secondsToMakeNewObject = 10
    currentTick = 0
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.surface = Object.Meteor
        self.velocity = 0
        self.ticksToMove = 30 + Object.currentTick
        self.health = 5
        self.warning = 0
        Object.ObjectList.append(self)
    
    def removeItself(self):
        Object.ObjectList.remove(self)
        Object.MeteorCrashSound.play()
    
    def draw(self, win):
        if start == False: return
        if self.warning == 1:
            win.blit(Object.ObjectWarning, (self.x, 100))
        else:
            self.rect = (self.x, self.y, self.width, self.height)
            win.blit(self.surface, self.rect)
        

    def isCloseToPlayer(self, plr):
        if self.x < plr.x + plr.width and self.x + self.width > plr.x:
            if self.y < plr.y + plr.height and self.y + self.height > plr.y:
                return True
    
    def fall(self):
        if start == False: return
        if self.y < 550:
            self.velocity += 1
            self.y += self.velocity
        else:
            self.removeItself()
            Object.makeObject(50, 50, (0,0,0))
    

    @classmethod
    def makeObject(cls,width, height, color):
        y = 100
        x = random.randint(0, 1300 - width)
        obj = cls(x, y, width, height, color)
        return obj
    @classmethod
    def drawObjects(cls, win):
        
        for obj in cls.ObjectList:
            obj.draw(win)
    
    @classmethod
    def checkCollision(cls, plr):
        for obj in cls.ObjectList:
            if obj.isCloseToPlayer(plr):
                return True,obj
        return False,None
    
    @classmethod
    def fallObjects(cls,currentTick):
        if start == False: return
        for obj in cls.ObjectList:
            if currentTick >= obj.ticksToMove:
                if obj.warning == 0:
                    obj.warning = 1
                    obj.ticksToMove += 1000

                else:
                    obj.warning = 2
                    obj.ticksToMove += 30
                    obj.fall()
    
    @classmethod
    def StopFalling(cls):
        for obj in Object.ObjectList:
            obj.removeItself()
    




class Player:
    dashSound = Sound(SoundsFolder + "DashSound.wav",1000,0.5)
    dashBackgroundSurface = pygame.Surface((120, 50))
    dashBackgroundSurface.fill((0, 0, 0))

    dashRectSurface = pygame.Surface((100, 30))
    dashRectSurface.fill((0, 0, 200))
    
    playerOwSound = Sound(SoundsFolder + "Ow.wav",1000,0.4)

    player_image = pygame.image.load(ImagesFolder+"StickBoi.png").convert_alpha()

    Folder = ImagesFolder + "StickBoiAnimation/"
    
    #Folder = R"C:\Users\4236696\Desktop\Cool Code\Practice\python\pygame\DodgeTheMeteors\Images\StickBoiAnimation/"

    playerLeftRunImage1 = pygame.image.load(Folder +"StickBoiLeftRun1.png").convert_alpha()
    playerLeftRunImage2 = pygame.image.load(Folder +"StickBoiLeftRun2.png").convert_alpha()
    playerLeftRunImage3 = pygame.image.load(Folder +"StickBoiLeftRun3.png").convert_alpha()
    playerLeftRunImage4 = pygame.image.load(Folder +"StickBoiLeftRun4.png").convert_alpha()

    playerRightRunImage1 = pygame.image.load(Folder +"StickBoiRightRun1.png").convert_alpha()
    playerRightRunImage2 = pygame.image.load(Folder +"StickBoiRightRun2.png").convert_alpha()
    playerRightRunImage3 = pygame.image.load(Folder +"StickBoiRightRun3.png").convert_alpha()
    playerRightRunImage4 = pygame.image.load(Folder +"StickBoiRightRun4.png").convert_alpha()
    playerRightRunImages = [playerRightRunImage1, playerRightRunImage2, playerRightRunImage3, playerRightRunImage4]


    playerLeftRunImages = [playerLeftRunImage1, playerLeftRunImage2, playerLeftRunImage3, playerLeftRunImage4]
    
    playerDedImage = pygame.image.load(Folder +"DedStickBoi.png").convert_alpha()
    
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 0
        self.maxVelocity = 10
        self.velocityDirection = "left"
        self.walkCount = 0
        self.ticksToMove = 35
        self.lives = 5
        self.canMove = True
        self.isInvincible = False
        self.ticksToDash = 7000
        self.hasSpeedPowerUp = False
        self.hasShieldPowerUp = False
        self.savedCurrentTick = 0
        

    def draw(self, win):
        if start == False: return
        Frame = None
        if self.lives <= 0:
            Frame = Player.playerDedImage
        elif self.velocity > 1:
            if self.velocityDirection == "left":
                Frame = Player.playerLeftRunImages[self.walkCount]

            else:
                Frame = Player.playerRightRunImages[self.walkCount]
        else:
            Frame = Player.player_image
            
        win.blit(Frame, (self.x, self.y))
        
    
    def increaseVelocity(self,direction):
        if self.velocity > self.maxVelocity and not(self.hasSpeedPowerUp):
            self.isInvincible = True
        if self.velocity == 0:
            self.velocityDirection = direction 
        else:
            if self.velocityDirection != direction and not(self.hasSpeedPowerUp):
                self.velocity = 0
        if self.velocity == self.maxVelocity and not(self.hasShieldPowerUp):
            self.isInvincible = False
        if self.velocity < self.maxVelocity and self.velocityDirection == direction:
            self.velocity += 0.5
            if not(self.hasShieldPowerUp):
                self.isInvincible == False
        elif self.velocity > self.maxVelocity and self.velocityDirection == direction and not(self.hasSpeedPowerUp):
            self.velocity -= 0.5

    def decreaseVelocity(self):
        if self.hasSpeedPowerUp: return
        if self.velocity > 0:
            self.velocity -= 1
        if self.velocity <= self.maxVelocity and not(self.hasShieldPowerUp):
            self.isInvincible = False
    
    def increaseWalkCount(self):
        if self.walkCount +1 >= 4:
            self.walkCount = 0
        else:
            self.walkCount += 1
    
    def move(self,direction=str):
        if not(self.canMove): return 
        self.increaseWalkCount()
        if direction == "left":
            if not(self.x <= 0):
                self.increaseVelocity("left")
                self.x -= self.velocity
        elif direction == "right":
            if not(self.x >= 1300 - self.width):
                self.increaseVelocity("right")
                self.x += self.velocity
    
    def removeLife(self,livesLost):
        if self.isInvincible: return
        self.lives -= livesLost
        livesText.updateText(f"Lives: {self.lives}")
        Player.playerOwSound.play()
        if self.lives <= 0:
            plr.canMove = False
            Object.StopFalling()
    
    def dash(self,currentTick):
        if currentTick >= self.ticksToDash:
            self.velocity = 20
            #self.ticksToDash += currentTick - self.ticksToDash
            self.savedCurrentTick = currentTick
            Player.dashSound.play()
        # self.maxVelocity = 20
    
    @classmethod
    def dashRectUpdate(cls,currentTick):
        dashRectWidth = ((currentTick -plr.savedCurrentTick)/( plr.ticksToDash)) * 100
        #print(f"dashRectWidth {dashRectWidth} CurrentTick {currentTick} plr.savedCurrentTick {plr.savedCurrentTick} plr.ticksToDash {plr.ticksToDash} ")
        if dashRectWidth > 100:
            dashRectWidth = 100
        cls.dashRectSurface = pygame.Surface((dashRectWidth, 30))
        if dashRectWidth == 100:
            cls.dashRectSurface.fill((0,255,0))
        else:
            cls.dashRectSurface.fill((255, 0, 0))

    @classmethod
    def dashRectDraw(cls):
        if start == True:   
            win.blit(Player.dashBackgroundSurface, (50,200))
            win.blit(Player.dashRectSurface, (60,210))

class PowerUps():

    PowerUpSound = Sound(SoundsFolder + "PowerUpSound.wav",2000,0.4)  

    redBullImage = pygame.image.load(ImagesFolder + "RedBull.png").convert_alpha()
    medKitImage = pygame.image.load(ImagesFolder + "MedKit.png").convert_alpha()
    shieldImage = pygame.image.load(ImagesFolder + "Shield.png").convert_alpha()

    PowerUpsList = []
    def __init__(self,x=int,y=int,width=int, height=int,type=str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.rect = (x, y, width, height)
        self.tickToDeactivate = 10000
        self.activated = False
        match self.type:
            case "M":
                self.surface = PowerUps.medKitImage
            case "R":
                self.surface = PowerUps.redBullImage
            case "S":
                self.surface = PowerUps.shieldImage
        PowerUps.PowerUpsList.append(self)
            
    @classmethod
    def makePowerUp(cls):
        x = random.randint(0,1300)
        y = 550
        width = 25
        height = 25
        type = random.randint(0,2)
        match type:
            case 0:
                type = "M"
            case 1:
                type = "R"
            case 2:
                type = "S"

        PowerUp = PowerUps(x,y,width,height,type)
    
    @classmethod
    def maybeMakePowerUp(cls):
        chance = random.randint(0,1000)
        if chance == 0:
            cls.makePowerUp()
    
    def isPowerUpNearPlayer(self,plr):
        if self.x < plr.x + plr.width and self.x + self.width > plr.x:
            if self.y < plr.y + plr.height and self.y + self.height > plr.y:
                return True
    
    @classmethod
    def maybePowerUpsActvate(cls,plr,currentTick):
        for PowerUp in PowerUps.PowerUpsList:
            if PowerUp.activated:
                if currentTick >= PowerUp.tickToDeactivate:
                    plr.hasSpeedPowerUp = False
                    plr.hasShieldPowerUp = False
                    PowerUp.removeItself()
            elif PowerUp.isPowerUpNearPlayer(plr):
                PowerUps.PowerUpSound.play()
                PowerUp.activated = True
                PowerUp.tickToDeactivate += currentTick
                if PowerUp.type == "M":
                    plr.lives += 1
                    livesText.updateText(f"Lives: {plr.lives}")
                elif PowerUp.type == "R":
                    plr.velocity = 20
                    plr.hasSpeedPowerUp = True
                elif PowerUp.type == "S":
                    plr.isInvincible = True
                    plr.hasShieldPowerUp = True
    
    def draw(self):
        if start == False or self.activated: return
        win.blit(self.surface,self.rect)
    
    @classmethod
    def drawPowerUps(cls):
        for PowerUp in cls.PowerUpsList:
            PowerUp.draw()
    
    def removeItself(self):
        PowerUps.PowerUpsList.remove(self)
        

Object.makeObject(50, 50, (0,0,0))

plr = Player(50, 550, 50, 50, (0, 0, 0))

clock = pygame.time.Clock()
initalTick = None
lastCurrentTick = 0
while run:
    
    currentTick = pygame.time.get_ticks()
    lastCurrentTick = currentTick
    if start:
        currentTick -= initalTick
        Object.currentTick = currentTick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        

    keys = pygame.key.get_pressed()
    if start == False:
        MainMenuMusic.play(currentTick)

        if any(keys):
            start = True
            MainMenuMusic.stop()
            initalTick = pygame.time.get_ticks()

            Object.currentTick = currentTick - initalTick
            
    else:
        
        if keys[pygame.K_f]:
            Object.StopFalling()
        if keys[pygame.K_l]:
            plr.removeLife(1)
        if keys[pygame.K_SPACE]:
            plr.dash(currentTick)
        if keys[pygame.K_s] and plr.lives <= 0:
            plr.lives = 5
            livesText.updateText(f"Lives: {plr.lives}")
            plr.canMove = True

            initalTick = pygame.time.get_ticks()

            Object.currentTick = currentTick - initalTick

            plr.ticksToMove = 35

            GameOverMusic.stop()
            # object = Object.makeObject(50, 50, (0,0,0))
            Object.secondsToMakeNewObject = 10



        if currentTick >= plr.ticksToMove:
            plr.ticksToMove += 35
            if keys[pygame.K_LEFT]:
                plr.move("left")
            elif keys[pygame.K_RIGHT]:
                plr.move("right")
            else:
                plr.decreaseVelocity()

    if start == False:
        win.blit(MainMenuScreen, (0,0))
    elif plr.lives > 0:
        GameTrackMusic.play(currentTick)
        win.blit(GameBackgroundScreen, (0,0))
        PowerUps.maybeMakePowerUp()
        PowerUps.maybePowerUpsActvate(plr,currentTick)
        timeLivedText.updateText(f"Time Lived: {currentTick//1000}")
            
        
    else:
        win.blit(GameOverScreen, (0,0))                                                             
        GameTrackMusic.stop()
        GameOverMusic.play(currentTick)
        Object.StopFalling()


    plr.draw(win)
    velocityText.updateText(f"Velocity: {plr.velocity}")
    velocityText.draw(win)

    livesText.draw(win)

    
    timeLivedText.draw(win)

    Player.dashRectUpdate(currentTick)
    Player.dashRectDraw()

    PowerUps.drawPowerUps()

    if currentTick//1000 >= Object.secondsToMakeNewObject and start:
        Object.secondsToMakeNewObject += 10
        object = Object.makeObject(50, 50, (0,0,0))
    
    Object.fallObjects(currentTick)
    Object.drawObjects(win)

    action,obj = Object.checkCollision(plr) 
    if action:
        plr.removeLife(1)
        if plr.lives > 0:
            obj.removeItself()
            Object.makeObject(50, 50, (0,0,0))

    if plr.isInvincible:
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 100,0, 50))  # RGBA color with alpha
        win.blit(overlay, (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()