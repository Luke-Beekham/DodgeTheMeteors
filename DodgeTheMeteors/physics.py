import pygame
import random
import os
import asyncio

pygame.init()





async def main():
    win =  pygame.display.set_mode((1300, 650))

    run = True

    scaleFactor = 1 

    # Get the path of the current file
    current_file_path = __file__

    # Get the directory containing the current file
    current_dir = os.path.dirname(current_file_path)
    print(current_dir)
    ImagesFolder = current_dir + "/Images/1300X650/"
    SoundsFolder = current_dir + "/SoundEffects/"


    
    def loadImages(ImagesFolder):
        global imageDict
        AnimationFolder = ImagesFolder + "/StickBoiAnimation/"
        GameOverScreen = pygame.image.load(ImagesFolder + "BackGroundGameOver.png").convert()
        MainMenuScreen = pygame.image.load(ImagesFolder + "BackGround Menu.png").convert()
        GameBackgroundScreen = pygame.image.load(ImagesFolder + "Background.png").convert()
        SettingScreen = pygame.image.load(ImagesFolder + "BackGround Settings.png").convert()
        Meteor = pygame.image.load(ImagesFolder + "Meteor.png").convert_alpha()
        ObjectWarning = pygame.image.load(ImagesFolder + "ObjectWarning.png").convert_alpha()
        player_image = pygame.image.load(ImagesFolder + "StickBoi.png").convert_alpha()
        playerLeftRunImage1 = pygame.image.load(AnimationFolder + "StickBoiLeftRun1.png").convert_alpha()
        playerLeftRunImage2 = pygame.image.load(AnimationFolder + "StickBoiLeftRun2.png").convert_alpha()
        playerLeftRunImage3 = pygame.image.load(AnimationFolder + "StickBoiLeftRun3.png").convert_alpha()
        playerLeftRunImage4 = pygame.image.load(AnimationFolder + "StickBoiLeftRun4.png").convert_alpha()
        playerRightRunImage1 = pygame.image.load(AnimationFolder + "StickBoiRightRun1.png").convert_alpha()
        playerRightRunImage2 = pygame.image.load(AnimationFolder + "StickBoiRightRun2.png").convert_alpha()
        playerRightRunImage3 = pygame.image.load(AnimationFolder + "StickBoiRightRun3.png").convert_alpha()
        playerRightRunImage4 = pygame.image.load(AnimationFolder + "StickBoiRightRun4.png").convert_alpha()
        playerDedImage = pygame.image.load(AnimationFolder + "DedStickBoi.png").convert_alpha()
        redBullImage = pygame.image.load(ImagesFolder + "RedBull.png").convert_alpha()
        medKitImage = pygame.image.load(ImagesFolder + "MedKit.png").convert_alpha()
        shieldImage = pygame.image.load(ImagesFolder + "Shield.png").convert_alpha()
        TutoralScreen = pygame.image.load(ImagesFolder + "BackGroundTutoral.png").convert_alpha()
        TutoralScreen1 = pygame.image.load(ImagesFolder + "BackGroundTutoral1.png").convert_alpha()
        TutoralScreen2 = pygame.image.load(ImagesFolder + "BackGroundTutoral2.png").convert_alpha()
        TutoralScreen3 = pygame.image.load(ImagesFolder + "BackGroundTutoral3.png").convert_alpha()
        TutoralScreen4 = pygame.image.load(ImagesFolder + "BackGroundTutoral4.png").convert_alpha()
        TutoralScreen5 = pygame.image.load(ImagesFolder + "BackGroundTutoral5.png").convert_alpha()
        TutoralScreen6 = pygame.image.load(ImagesFolder + "BackGroundTutoral6.png").convert_alpha()
        CutScene1 = pygame.image.load(ImagesFolder + "CutScene1.png").convert_alpha()
        CutScene2 = pygame.image.load(ImagesFolder + "CutScene2.png").convert_alpha()
        CutScene3 = pygame.image.load(ImagesFolder + "CutScene3.png").convert_alpha()
        CutScene4 = pygame.image.load(ImagesFolder + "CutScene4.png").convert_alpha()
        CutScene5 = pygame.image.load(ImagesFolder + "CutScene5.png").convert_alpha()





        imageDict = {
            "GameOverScreen" : GameOverScreen,
            "MainMenuScreen" : MainMenuScreen,
            "GameBackgroundScreen" : GameBackgroundScreen,
            "SettingScreen" : SettingScreen,
            "Meteor": Meteor,
            "ObjectWarning": ObjectWarning,
            "player_image": player_image,
            "playerLeftRunImage1": playerLeftRunImage1,
            "playerLeftRunImage2": playerLeftRunImage2,
            "playerLeftRunImage3": playerLeftRunImage3,
            "playerLeftRunImage4": playerLeftRunImage4,
            "playerRightRunImage1": playerRightRunImage1,
            "playerRightRunImage2": playerRightRunImage2,
            "playerRightRunImage3": playerRightRunImage3,
            "playerRightRunImage4": playerRightRunImage4,
            "playerDedImage": playerDedImage,
            "redBullImage": redBullImage,
            "medKitImage": medKitImage,
            "shieldImage": shieldImage,
            "TutoralScreen" : TutoralScreen,
            "TutoralScreen1" : TutoralScreen1, 
            "TutoralScreen2" : TutoralScreen2,
            "TutoralScreen3" : TutoralScreen3,
            "TutoralScreen4" : TutoralScreen4,
            "TutoralScreen5" : TutoralScreen5,
            "TutoralScreen6" : TutoralScreen6,
            "CutScene1" : CutScene1,
            "CutScene2" : CutScene2,
            "CutScene3" : CutScene3,
            "CutScene4" : CutScene4,
            "CutScene5" : CutScene5
        }


    loadImages(ImagesFolder)

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
            self.x = x * scaleFactor
            self.y = y * scaleFactor
            self.text = text
            self.font = font
            self.color = color
            self.textSurface = font.render(text, True, color,(0,0,0))
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (x, y)
        
        def draw(self, win):
            if start == False and not(isTutoral): return
            win.blit(self.textSurface, self.textRect)
        
        def updateText(self,newText):
            self.text = newText 
            self.textSurface = self.font.render(self.text, True, self.color,(0,0,0))
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)
            
    def MakeTexts(ScaleFactor):
        global velocityText
        global livesText
        global timeLivedText

        size = int(16*ScaleFactor)

        velocityFont = pygame.font.Font('freesansbold.ttf', size)

        velocityText = Text(100, 50, 'Velocity: 0', velocityFont, (0,255,0))

        livesFont = pygame.font.Font('freesansbold.ttf',size)

        livesText = Text(100,100,'Lives: 5',livesFont,(255,0,0))

        timeLivedFont = pygame.font.Font('freesansbold.ttf',size)

        timeLivedText = Text(100,150,'Time Lived: 0',timeLivedFont,(3, 173, 252))

    MakeTexts(1)

    class Object:
        MeteorCrashSound = Sound(SoundsFolder +"MeteorCrash.wav",1000,0.5)
        ObjectList = []
        secondsToMakeNewObject = 10
        currentTick = 0
        def __init__(self, x, y, width, height, color):
            self.x = x * scaleFactor
            self.y = y * scaleFactor
            self.width = width * scaleFactor
            self.height = height * scaleFactor
            self.color = color
            self.rect = (x, y, width, height)
            self.surface = imageDict["Meteor"]
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
                win.blit(imageDict["ObjectWarning"], (self.x, 100))
            else:
                self.rect = (self.x, self.y, self.width, self.height)
                win.blit(imageDict["Meteor"], self.rect)
            

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
        
        #Folder = R"C:\Users\4236696\Desktop\Cool Code\Practice\python\pygame\DodgeTheMeteors\Images\StickBoiAnimation/"    
        def __init__(self, x, y, width, height, color):
            self.x = x * scaleFactor
            self.y = y * scaleFactor
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
            if start == False and not isTutoral: return
            Frame = None
            if self.lives <= 0:
                Frame = imageDict["playerDedImage"]
            elif self.velocity > 1:
                if self.velocityDirection == "left":
                    Frame = imageDict[f"playerLeftRunImage{self.walkCount+1}"]

                else:
                    Frame = imageDict[f"playerRightRunImage{self.walkCount+1}"]
            else:
                Frame = imageDict["player_image"]
                
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
                self.ticksToDash = currentTick + 7000
                self.savedCurrentTick = currentTick
                Player.dashSound.play()
            # self.maxVelocity = 20
        
        @classmethod
        def dashRectUpdate(cls,currentTick):
            try:

                dashRectWidth = ((currentTick-plr.savedCurrentTick)/( plr.ticksToDash-plr.savedCurrentTick)) * 100
            except ZeroDivisionError:
                dashRectWidth = 100
            if dashRectWidth > 100:
                dashRectWidth = 100
            else:
                pass
                #print(f"dashRectWidth {dashRectWidth} CurrentTick {currentTick} plr.savedCurrentTick {plr.savedCurrentTick} plr.ticksToDash {plr.ticksToDash} ")
            cls.dashRectSurface = pygame.Surface((dashRectWidth*scaleFactor, 30*scaleFactor))
            if dashRectWidth == 100:
                cls.dashRectSurface.fill((0,255,0))
            else:
                cls.dashRectSurface.fill((255, 0, 0))

        @classmethod
        def dashRectDraw(cls):
            if start == True or isTutoral:   
                win.blit(Player.dashBackgroundSurface, (50*scaleFactor,200*scaleFactor))
                win.blit(Player.dashRectSurface, (60*scaleFactor,210*scaleFactor))

    class PowerUps:

        PowerUpSound = Sound(SoundsFolder + "PowerUpSound.wav",2000,0.4)  

        PowerUpsList = []
        def __init__(self,x=int,y=int,width=int, height=int,type=str):
            self.x = x * scaleFactor
            self.y = y * scaleFactor
            self.width = width
            self.height = height
            self.type = type
            self.rect = (x, y, width, height)
            self.tickToDeactivate = 10000
            self.activated = False
            match self.type:
                case "M":
                    self.surface = imageDict["medKitImage"]
                case "R":
                    self.surface = imageDict["redBullImage"]
                case "S":
                    self.surface = imageDict["shieldImage"]
            PowerUps.PowerUpsList.append(self)
        

        @classmethod
        def makeSpecificPowerUp(cls,type):
            x = random.randint(0,1300)
            y = 550
            width = 25
            height = 25
            PowerUp = PowerUps(x,y,width,height,type)
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
            if (start == False and not(isTutoral)) or self.activated: return
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
    old_width = 1300
    old_height = 600

    orgImageDict = imageDict.copy()

    setting = False

    isTutoral = False

    isTutoralTickOnce = False

    tutoralPowerUpRedBull = True
    tutoralPowerUpMedKit = True
    tutoralPowerUpShield = True

    OnceWipe = True

    isStory = False

    storyTick = 0

    while run:   
        currentTick = pygame.time.get_ticks()
        lastCurrentTick = currentTick
        if start:
            currentTick -= initalTick
            Object.currentTick = currentTick
            if OnceWipe:
                plr.ticksToMove = currentTick
                plr.ticksToDash = currentTick
                plr.savedCurrentTick = currentTick
                OnceWipe = False
        elif isTutoral and not(isTutoralTickOnce):
            currentTick -= initalTick
            initalTick = currentTick
            isTutoralTickOnce = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and start == False and not(isTutoral) and not(isStory):
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                x = mouse_pos[0]
                y = mouse_pos[1]
                if not setting:
                    if x >= 978 * scaleFactor and y >=263 * scaleFactor and y <= 341 * scaleFactor:
                        start = True
                        MainMenuMusic.stop()
                        initalTick = pygame.time.get_ticks()
                        Object.currentTick = currentTick - initalTick
                    elif x >= 9 * scaleFactor and x <=316 * scaleFactor and y >= 371 * scaleFactor and y <= 437 * scaleFactor:
                        setting = True
                    elif x >= 931 * scaleFactor and x <=1290 * scaleFactor and y >=407 * scaleFactor and y <=471 * scaleFactor:
                        initalTick = pygame.time.get_ticks()
                        isTutoral = True
                    elif x >= 935 * scaleFactor and x <= 1290 * scaleFactor and y >= 545 * scaleFactor and y <=605 * scaleFactor:
                        isStory = True
                        storyTick = currentTick

                elif setting:
                    if x >= 120 * scaleFactor and x <=556 * scaleFactor and y >=260 * scaleFactor and y <=315 * scaleFactor:
                        win =  pygame.display.set_mode((1300, 650),pygame.RESIZABLE)
                        ImagesFolder = current_dir + "/Images/1300X650/"
                        loadImages(ImagesFolder)
                        scaleFactor = 1
                        plr.y = 550
                        MakeTexts(scaleFactor)
                        livesText.updateText(f"Lives: {plr.lives}")

                        Player.dashBackgroundSurface = pygame.Surface((120*scaleFactor, 50*scaleFactor))
                        Player.dashBackgroundSurface.fill((0, 0, 0))

                        Player.dashRectSurface = pygame.Surface((100*scaleFactor, 30*scaleFactor))
                        Player.dashRectSurface.fill((0, 0, 200))
                    elif x >=117 * scaleFactor and x <=569 * scaleFactor and y >=358 * scaleFactor and y <=412 * scaleFactor:
                        pass
                        #win =  pygame.display.set_mode((1920, 960),pygame.RESIZABLE)
                    elif x >= 116 * scaleFactor and x <=568 * scaleFactor and y >=451 * scaleFactor and y <=499 * scaleFactor:
                        win =  pygame.display.set_mode((650, 325))
                        ImagesFolder = current_dir + "/Images/650X325/"
                        loadImages(ImagesFolder)
                        scaleFactor = 0.5
                        plr.y *= scaleFactor
                        MakeTexts(scaleFactor)
                        livesText.updateText(f"Lives: {plr.lives}")

                        Player.dashBackgroundSurface = pygame.Surface((120*scaleFactor, 50*scaleFactor))
                        Player.dashBackgroundSurface.fill((0, 0, 0))

                        Player.dashRectSurface = pygame.Surface((100*scaleFactor, 30*scaleFactor))
                        Player.dashRectSurface.fill((0, 0, 200))

                        
                        

                    elif x >= 739 * scaleFactor and x <= 1263 * scaleFactor and y >=512 * scaleFactor and y <= 591 * scaleFactor:
                        setting = False
                    

            # if event.type == pygame.VIDEORESIZE:
                
            #     new_width = event.dict['size'][0]

            #     new_height = event.dict['size'][1]
            #     ScaleFactor_width = new_width / 1300
            #     ScaleFactor_height = new_height / 650
            #     old_width = new_width
            #     old_height = new_height
                

            #     newOrgImageDict = orgImageDict.copy()
            #     for key in newOrgImageDict:
            #         original_image = newOrgImageDict[key]
            #         current_image = imageDict[key]
                    
            #         newImageWidth = int(original_image.get_width() * ScaleFactor_width)
            #         newImageHeight = int(original_image.get_height() * ScaleFactor_height)
            #         scaled_image = pygame.transform.scale(newOrgImageDict[key], (newImageWidth, newImageHeight))
            #         imageDict[key] = scaled_image


            #     win =  pygame.display.set_mode((new_width, new_height),pygame.RESIZABLE)
            #     print(f"ImageDict Width: {imageDict['GameBackgroundScreen'].get_width()} OriginalImageWidth: {orgImageDict['GameBackgroundScreen'].get_width()} ScaleFactor_width: {ScaleFactor_width}")

            

        keys = pygame.key.get_pressed()
        if start == False and not(isTutoral) and not(isStory):
            MainMenuMusic.play(currentTick)  
        elif MainMenuMusic.played:
            MainMenuMusic.stop()
        if isTutoral or start == True:
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
            if setting:
                win.blit(imageDict["SettingScreen"],(0,0))
            elif isTutoral:
                i = int(currentTick//10000)
                match i:
                    case 6:
                        isTutoral = False
                    case 2:
                        if tutoralPowerUpRedBull:
                            PowerUps.makeSpecificPowerUp("R")
                            tutoralPowerUpRedBull = False
                    case 3:
                        if tutoralPowerUpMedKit:
                            PowerUps.makeSpecificPowerUp("M")
                            tutoralPowerUpMedKit = False
                    case 4:
                        if tutoralPowerUpShield:
                            PowerUps.makeSpecificPowerUp("S")
                            tutoralPowerUpShield = False
                if not(i >= 6):
                    win.blit(imageDict[f"TutoralScreen{i+1}"],(0,0))

                PowerUps.maybePowerUpsActvate(plr,currentTick)
            elif isStory:
                if currentTick  -storyTick >= 50000:
                    isStory = False
                elif currentTick -storyTick >= 40000 :
                    win.blit(imageDict["CutScene5"],(0,0))
                elif currentTick -storyTick >= 30000 :
                    win.blit(imageDict["CutScene4"],(0,0))
                elif currentTick -storyTick >= 20000 :
                    win.blit(imageDict["CutScene3"],(0,0))
                elif currentTick -storyTick >= 10000 :
                    win.blit(imageDict["CutScene2"],(0,0))
                else:
                    win.blit(imageDict["CutScene1"],(0,0))
            else:
                win.blit(imageDict["MainMenuScreen"], (0,0))
        elif plr.lives > 0:
            GameTrackMusic.play(currentTick)
            win.blit(imageDict["GameBackgroundScreen"], (0,0))
            PowerUps.maybeMakePowerUp()
            
            timeLivedText.updateText(f"Time Lived: {currentTick//1000}")
                
            
        else:
            win.blit(imageDict["GameOverScreen"], (0,0))                                                             
            GameTrackMusic.stop()
            GameOverMusic.play(currentTick)
            Object.StopFalling()


        plr.draw(win)
        velocityText.updateText(f"Velocity: {plr.velocity}")
        velocityText.draw(win)

        livesText.draw(win)

        await asyncio.sleep(0)
        
        timeLivedText.draw(win)

        Player.dashRectUpdate(currentTick)
        Player.dashRectDraw()

        PowerUps.drawPowerUps()
        PowerUps.maybePowerUpsActvate(plr,currentTick)

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

asyncio.run(main())