import pygame, os
import pygame.gfxdraw
import os, sys
from time import sleep

MODULE_PATH = os.path.join(os.getcwd(), "mod")
sys.path.append(MODULE_PATH)

# Custom module
from map import *
from color import *
from level import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, level, which):
        pygame.sprite.Sprite.__init__(self)
        global currentMap

        self.keys = None

        self.setting = {
            "ball": currentMap['ball'],
            "center": currentMap['ball']//2,
            "radius": currentMap['ball']//2 - 1,
            "velocity": {
                "600x400": {
                    "max_speed": 10,
                    "bounce": -2.4,
                    "head_bounce": 1,
                    "default": .14,
                    "linear": 3,
                    "skill":5,
                    "dist": 1.2
                },
                "900x600": {
                    "max_speed": 17,
                    "bounce": -3.5,
                    "head_bounce": 2,
                    "default": .2,
                    "linear": 5,
                    "skill": 5,
                    "dist": 1.5
                }
            }
        }

        self.setting_for_one = {
            "600x400": {
                "max_speed": 10,
                "bounce": -1.7,
                "head_bounce": 1,
                "default": .08,
                "linear": 3,
                "skill": 2,
                "dist": 1
            },
            "900x600": {
                "max_speed": 17,
                "bounce": -2.5,
                "head_bounce": 2,
                "default": .1,
                "linear": 5,
                "skill": 3,
                "dist": 1
            }
        }
        if which == 0:
            self.current_vel = self.setting_for_one[currentMap['type']]
        else:
            self.current_vel = self.setting['velocity'][currentMap['type']]


        # Loading Ball Image
        ballImg = pygame.Surface((self.setting['ball'], self.setting['ball']))
        pygame.gfxdraw.filled_circle(ballImg, self.setting['center'], self.setting['center'], self.setting['radius'], BALL)
        ballImg.convert_alpha()
        ballImg.set_colorkey(BLACK)

        self.image = ballImg

        # Set ball position
        self.initX = pos[0]
        self.initY = pos[1]

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.vx = 0
        self.vy = 0

        self.max_speed = self.current_vel['max_speed']
        self.cnt = 0

        self.isPause = False

        self.totalStar = starCount
        self.eatenStar = 0
        self.level = level

        self.stageClear = False
        self.which = which

        self.linear = False
        self.prevBlock = None

        self.changeCnt = 0

        self.hasBuff = False
        self.usingSkill = False

        if which != 2:
            self.left = pygame.K_a
            self.right = pygame.K_d
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT

    def respawn(self):
        self.rect.x = self.initX
        self.rect.y = self.initY
        self.vx = 0

    def update(self):
        self.keys = pygame.key.get_pressed()


        if self.keys[self.left]:
            self.rect.x -= self.current_vel['dist']
        if self.keys[self.right]:
            self.rect.x += self.current_vel['dist']

        if self.keys[self.left] or self.keys[self.right]:
            if self.linear:
                self.vx = 0
                self.linear = False

        self.rect.x += self.vx
        self.rect.y += self.vy

        if not self.linear:
            self.vy += self.current_vel['default']
        else:
            self.vy = 0
        self.check_block()

        if self.vy >= self.max_speed:
            self.vy = self.max_speed

        if self.hasBuff:
            ballImg = pygame.Surface((self.setting['ball'], self.setting['ball']))
            pygame.gfxdraw.filled_circle(ballImg, self.setting['center'], self.setting['center'],
                                         self.setting['radius'], BUFFED_BALL)
            ballImg.convert_alpha()
            ballImg.set_colorkey(BLACK)

            self.image = ballImg
        else:
            ballImg = pygame.Surface((self.setting['ball'], self.setting['ball']))
            pygame.gfxdraw.filled_circle(ballImg, self.setting['center'], self.setting['center'],
                                         self.setting['radius'], BALL)
            ballImg.convert_alpha()
            ballImg.set_colorkey(BLACK)

            self.image = ballImg

    def useSkill(self):
        if self.hasBuff:
            self.hasBuff = False
            self.usingSkill = True
            if self.keys[self.right]:
                self.vx += self.current_vel['skill']
            if self.keys[self.left]:
                self.vx -= self.current_vel['skill']
        else:
            return

    def check_block(self):
        global remain_star_1p, remain_star_2p
        alpha = 10
        if self.which != 2:
            block_list = pygame.sprite.spritecollide(self, blockGroup, False)
            whichBlock = blockGroup
        else:
            block_list = pygame.sprite.spritecollide(self, blockGroup2, False)
            whichBlock = blockGroup2


        if block_list:
            for blocks in block_list:
                if blocks.rect.colliderect(self.rect):
                    # ball_sound.play()
                    if self.usingSkill:
                        self.vx = 0
                        self.usingSkill = False

                    if self.prevBlock:
                        if self.prevBlock.type == 'linear' and self.prevBlock != blocks:
                            self.linear = False
                            if self.vx > 0:
                                self.vx -= self.current_vel['linear']
                            if self.vx < 0:
                                self.vx += self.current_vel['linear']

                    if blocks.type == 'star':
                        whichBlock.remove(blocks)
                        self.eatenStar += 1
                        if self.eatenStar == self.totalStar[self.level]:
                            self.stageClear = True
                        if self.which != 2:
                            remain_star_1p[self.level] -= 1
                        else:
                            remain_star_2p[self.level] -= 1
                        return

                    if blocks.type == 'skill':
                        whichBlock.remove(blocks)
                        self.hasBuff = True
                        return

                    is_normal = True
                    if self.rect.bottom > blocks.rect.top + alpha:
                        is_normal = False
                        self.vy += self.current_vel['default']

                    # to blocks top
                    if self.rect.top > blocks.rect.bottom - 5:
                        is_normal = False
                        self.vy += self.current_vel['head_bounce']

                    # to blocks side
                    if self.rect.top < blocks.rect.bottom - 5 and self.rect.bottom > blocks.rect.top + alpha:
                        is_normal = False
                        if self.rect.left < blocks.rect.right - 5 and (self.keys[self.left]):
                            self.rect.left = blocks.rect.right
                        if self.rect.right > blocks.rect.left + 5 and (self.keys[self.right]):
                            self.rect.right = blocks.rect.left

                    if is_normal:
                        self.vy = self.current_vel['bounce']
                        if blocks.type == "easy":
                            whichBlock.remove(blocks)
                        if blocks.type == 'linear':
                            self.linear = True
                            self.rect.centery = blocks.rect.centery
                            if blocks.direction == 'l':
                                self.rect.right = blocks.rect.left - 10
                                self.vx = -self.current_vel['linear']
                            if blocks.direction == 'r':
                                self.rect.left = blocks.rect.right + 10
                                self.vx = self.current_vel['linear']
                    self.prevBlock = blocks


    def isDead(self):
        if self.rect.top > currentMap['worldY'] + 50:
            self.linear = False
            self.prevBlock = None

            self.hasBuff = False
            self.usingSkill = False

            return True
        else:
            return False

class NormalBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = normal_block
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.type = 'normal'


class EasyBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = easy_block
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.type = 'easy'


class Star(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = star
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.type = 'star'


class LinearBlock(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = linearBlock
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.type = 'linear'
        self.direction = direction

        if self.direction == 'l':
            self.image = pygame.transform.rotate(self.image,180)

class SkillBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = skillBlock
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.type = 'skill'

def getImage(image):
    convert_image = pygame.image.load(os.path.join(image_path, image)).convert()
    convert_image = pygame.transform.scale(convert_image, (currentMap['unit'], currentMap['unit']))
    convert_image.convert_alpha()
    convert_image.set_colorkey(BLACK)

    return convert_image


def getMap(level, isTwo, which=1):
    level = level - 1
    stage = levels[level]

    cross_line = 0

    playerGroup = pygame.sprite.Group()
    blockGroup = pygame.sprite.Group()

    player = None

    if isTwo:
        screen = pygame.display.set_mode([worldX, worldY])
    else:
        screen = pygame.display.set_mode([(worldX - 2) // 2, worldY])

    if which == 2:
        cross_line = ((worldX - 2) // 2) - 2

    x = y = 0
    for row in stage:
        for col in row:
            if col == "b":
                block = NormalBlock([cross_line + x, y])
                blockGroup.add(block)

            if col == "e":
                block = EasyBlock([cross_line + x, y])
                blockGroup.add(block)

            if col == "p":
                player = Ball([cross_line + x, y], level, which)
                playerGroup.add(player)

            if col == 's':
                starObj = Star([cross_line + x, y])
                blockGroup.add(starObj)

            if col == 'r':
                linearObj = LinearBlock([cross_line + x, y], 'r')
                blockGroup.add(linearObj)

            if col == 'l':
                linearObj = LinearBlock([cross_line + x, y], 'l')
                blockGroup.add(linearObj)

            if col == 'k':
                skillObj = SkillBlock([cross_line + x, y])
                blockGroup.add(skillObj)

            x += currentMap['unit']
        y += currentMap['unit']
        x = 0

    return {
        "screen": screen,
        "player": player,
        "playerGroup": playerGroup,
        "blockGroup": blockGroup,
        "msg": "staging"
    }


def drawTextBox(text, sizeX, sizeY, centerX, centerY, textColor, bgColor, fontSize = 22):
    font = pygame.font.Font(os.path.join(font_path, 'NanumGothic.ttf'), fontSize)

    text_surface = font.render(text, True, textColor)
    text_rect = text_surface.get_rect()
    text_box = pygame.Surface((sizeX, sizeY))
    text_box.fill(bgColor)
    text_box_center = (centerX - (sizeX // 2), centerY - (sizeY // 2))
    text_rect.center = (centerX, centerY)

    screen.blit(text_box, text_box_center)
    screen.blit(text_surface, text_rect)

def checkWhere(pos, centerX, centerY, width, height, cnt, offset):
    fromX = centerX - (width // 2)
    toX = centerX + (width // 2)
    fromY = centerY - (height // 2)
    toY = centerY + (height // 2)

    x = pos[0]
    y = pos[1]

    where = -1

    for i in range(cnt):
        if fromX <= x <= toX and fromY <= y - offset*i <= toY:
            where = i+1
            break

    return where

def isOnButton(where):
    drawTextBox(p_1, text_box_width, text_box_height, centerX, centerY, TEXT_COLOR, ACTIVE_TEXT_BOX) if where == 1 else drawTextBox(p_1, text_box_width, text_box_height, centerX, centerY, TEXT_COLOR, TEXT_BOX)
    drawTextBox(p_2, text_box_width, text_box_height, centerX, centerY + 60, TEXT_COLOR, ACTIVE_TEXT_BOX) if where == 2 else drawTextBox(p_2, text_box_width, text_box_height, centerX, centerY + 60, TEXT_COLOR, TEXT_BOX)
    drawTextBox(pref, text_box_width, text_box_height, centerX, centerY + 120, TEXT_COLOR, ACTIVE_TEXT_BOX) if where == 3 else drawTextBox(pref, text_box_width, text_box_height, centerX, centerY + 120, TEXT_COLOR, TEXT_BOX)
    drawTextBox(game_quit, text_box_width, text_box_height, centerX, centerY + 180, TEXT_COLOR, ACTIVE_TEXT_BOX) if where == 4 else drawTextBox(game_quit, text_box_width, text_box_height, centerX, centerY + 180, TEXT_COLOR, TEXT_BOX)

def reInitMap():
    global worldX, worldY, cross_line, screen, currentMap, centerX, centerY, normal_block, easy_block, star, linearBlock, skillBlock, pref, main_bg
    pref = currentMap['type']

    worldX = currentMap['worldX']
    worldY = currentMap['worldY']

    centerX = (worldX - 2) // 2
    centerY = worldY

    cross_line = (currentMap['worldX'] - 2) / 2

    normal_block = getImage('block1.png')
    easy_block = getImage('block2.png')

    star = getImage('star.png')

    linearBlock = getImage('block3.png')
    skillBlock = getImage('skill.png')

    screen = pygame.display.set_mode([worldX - 2, worldY * 2])
    big_main_bg = main_bg
    small_main_bg = pygame.transform.scale(main_bg, ((worldX - 2), worldY*2))
    if currentMap['type'] == '600x400':
        screen.blit(small_main_bg, (0,0))
    elif currentMap['type'] == '900x600':
        screen.blit(big_main_bg, (0,0))

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

FPS = 240
fpsClock = pygame.time.Clock()

worldX = currentMap['worldX']
worldY = currentMap['worldY']

cross_line = (currentMap['worldX'] - 2) / 2

screen = pygame.display.set_mode([worldX - 2, worldY*2])
pygame.display.set_caption("Bounce Ball")

# image
main_bg = pygame.image.load(os.path.join(image_path, "main.png"))

normal_block = getImage('block1.png')
easy_block = getImage('block2.png')

star = getImage('star.png')

linearBlock = getImage('block3.png')
skillBlock = getImage('skill.png')

# sound
# ball_sound = pygame.mixer.Sound('/Users/naker/Desktop/GameProto/bounce_ball/music/new.mp3')
# pygame.mixer.music.load('/Users/naker/Desktop/GameProto/bounce_ball/music/new.mp3')

# Start Menu
main_1p = False
main_2p = False

centerX = (worldX - 2) // 2
centerY = worldY

p_1 = "1인"
p_2 = "2인"
pref = currentMap['type']
game_quit = "게임 종료"

text_box_width = 140
text_box_height = 50

def main_start():
    global screen, currentMap, main_1p, main_2p, level, res, level_for_2p, res2, remain_star_1p, remain_star_2p, clear_1p, clear_2p
    start = True
    screen = pygame.display.set_mode([worldX - 2, worldY * 2])

    big_main_bg = main_bg
    small_main_bg = pygame.transform.scale(main_bg, ((worldX - 2), worldY * 2))
    if currentMap['type'] == '600x400':
        screen.blit(small_main_bg, (0, 0))
    elif currentMap['type'] == '900x600':
        screen.blit(big_main_bg, (0, 0))
    drawTextBox(p_1, text_box_width, text_box_height, centerX, centerY, TEXT_COLOR, TEXT_BOX)
    drawTextBox(p_2, text_box_width, text_box_height, centerX, centerY + 60, TEXT_COLOR, TEXT_BOX)
    drawTextBox(pref, text_box_width, text_box_height, centerX, centerY + 120, TEXT_COLOR, TEXT_BOX)
    drawTextBox(game_quit, text_box_width, text_box_height, centerX, centerY + 180, TEXT_COLOR, TEXT_BOX)

    while start:
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                btnNum = checkWhere(event.pos, centerX, centerY, text_box_width, text_box_height, 5, 60)
                isOnButton(btnNum)
            if event.type == pygame.MOUSEBUTTONDOWN:
                btnNum = checkWhere(event.pos, centerX, centerY, text_box_width, text_box_height, 5, 60)
                if btnNum == 4:
                    pygame.quit()
                    sys.exit()
                if btnNum == 1:
                    start = False
                    main_1p = True
                    main_2p = False
                if btnNum == 2:
                    start = False
                    main_1p = False
                    main_2p = True
                if btnNum == 3:
                    if pref == '600x400':
                        currentMap = MapSetting['900x600']
                    else:
                        currentMap = MapSetting['600x400']
                    reInitMap()

        pygame.display.flip()

main_start()

while True:
    level = 1
    res = getMap(level, False, 0)
    remain_star_1p = starCount[:]
    screen = res['screen']

    restart = False

    score_offset_x = 80
    score_offset_y = 25
    score_font_size = 16

    # 1 player
    while main_1p:
        fpsClock.tick_busy_loop(FPS)
        screen.fill(BG)
        if restart:
            main_start()
            level = 1
            res = getMap(level, False, 0)
            remain_star_1p = starCount[:]
            screen = res['screen']
            restart = False

        drawTextBox("Remain Star : {0}".format(remain_star_1p[level - 1]), score_offset_x, score_offset_y,
                    score_offset_x, score_offset_y, BLACK, BG, score_font_size)
        playerGroup = res['playerGroup']
        blockGroup = res['blockGroup']
        player = res['player']
        playerGroup.draw(screen)
        blockGroup.draw(screen)
        if not player.isPause:
            playerGroup.update()

        if player.isDead():
            res = getMap(level, False, 0)
            remain_star_1p[level - 1] = starCount[level - 1]
            player.respawn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.isPause = not player.isPause
                if event.key == pygame.K_LSHIFT:
                    player.useSkill()

        if player.stageClear:
            level += 1
            res = getMap(level, False, 0)

        if remain_star_1p[level - 1] == -1:
            playerGroup.empty()
            blockGroup.empty()

            end = True
            endWidth = (currentMap['worldX'] - 2) // 2
            endHeight = currentMap['worldY']
            endScreen = pygame.display.set_mode([endWidth, endHeight])

            level = 1
            res = getMap(level, False, 0)
            remain_star_1p = starCount[:]
            while end:
                endScreen.fill(BG)
                pygame.draw.rect(endScreen, BG, (0, 0, endWidth, endHeight))
                drawTextBox("Winner", 200, 50, endWidth // 2, endHeight // 2, BLACK, BG, fontSize=currentMap['end-font'])
                drawTextBox("Press Enter to go main menu", 200, 50, endWidth // 2, endHeight // 2 + currentMap['end-font'], BLACK,
                            BG, fontSize=currentMap['end-font'] // 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            end = False
                            restart = True

                pygame.display.flip()

        pygame.display.flip()

    # 2 player
    level = 1
    res = getMap(level, True, 1)
    level_for_2p = 1
    res2 = getMap(level, True, 2)
    remain_star_1p = starCount[:]
    remain_star_2p = starCount[:]
    rank_1p = 0
    rank_2p = 0

    end = False
    restart = False
    while main_2p:
        fpsClock.tick(FPS)
        screen.fill(BG)
        pygame.draw.rect(screen, BOUNDARY, (cross_line, 0, 2, worldY))

        if restart:
            main_start()
            level = 1
            res = getMap(level, True, 1)
            level_for_2p = 1
            res2 = getMap(level, True, 2)
            remain_star_1p = starCount[:]
            remain_star_2p = starCount[:]
            restart = False

        if remain_star_1p[level - 1] == -1 and remain_star_2p[level_for_2p - 1] == -1:
            end = True
            endWidth = currentMap['worldX']
            endHeight = currentMap['worldY']
            endScreen = pygame.display.set_mode([endWidth, endHeight])

            level = 1
            res = getMap(level, True, 1)
            level_for_2p = 1
            res2 = getMap(level, True, 2)
            remain_star_1p = starCount[:]
            remain_star_2p = starCount[:]

            while end:
                endScreen.fill(BG)
                pygame.draw.rect(endScreen, BOUNDARY,(cross_line, 0, 2, currentMap['worldY']))

                if rank_1p > rank_2p:
                    drawTextBox("Winner", 200, 50, endWidth // 4, endHeight // 2, BLACK, BG, fontSize=currentMap['end-font'])
                    drawTextBox("Press Enter to go main menu", 200, 50, endWidth // 4, endHeight // 2 + currentMap['end-font'],
                                BLACK,
                                BG, fontSize=currentMap['end-font'] // 2)
                    drawTextBox("Loser", 200, 50, endWidth // 4 + cross_line, endHeight // 2, BLACK, BG,
                                fontSize=currentMap['end-font'])
                    drawTextBox("Press Enter to go main menu", 200, 50, endWidth // 4 + cross_line,
                                endHeight // 2 + currentMap['end-font'],
                                BLACK,
                                BG, fontSize=currentMap['end-font'] // 2)
                else:
                    drawTextBox("Loser", 200, 50, endWidth // 4, endHeight // 2, BLACK, BG, fontSize=currentMap['end-font'])
                    drawTextBox("Press Enter to go main menu", 200, 50, endWidth // 4, endHeight // 2 + currentMap['end-font'],
                                BLACK,
                                BG, fontSize=currentMap['end-font'] // 2)
                    drawTextBox("Winner", 200, 50, endWidth // 4 + cross_line, endHeight // 2, BLACK, BG,
                                fontSize=currentMap['end-font'])
                    drawTextBox("Press Enter to go main menu", 200, 50, endWidth // 4 + cross_line,
                                endHeight // 2 + currentMap['end-font'],
                                BLACK,
                                BG, fontSize=currentMap['end-font'] // 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            end = False
                            restart = True

                pygame.display.flip()

            rank_1p = 0
            rank_2p = 0

        if remain_star_1p[level - 1] != -1:
            drawTextBox("Remain Star : {0}".format(remain_star_1p[level - 1]), score_offset_x, score_offset_y,
                        score_offset_x, score_offset_y, BLACK, BG, score_font_size)
        else:
            drawTextBox("Playground", score_offset_x, score_offset_y,
                        score_offset_x, score_offset_y, BLACK, BG, score_font_size)
            if rank_2p != 1:
                rank_1p = 1

        playerGroup = res['playerGroup']
        blockGroup = res['blockGroup']
        player = res['player']
        playerGroup.draw(screen)
        blockGroup.draw(screen)

        if remain_star_2p[level_for_2p - 1] != -1:
            drawTextBox("Remain Star : {0}".format(remain_star_2p[level_for_2p - 1]), score_offset_x, score_offset_y,
                        cross_line + score_offset_x, score_offset_y, BLACK, BG, score_font_size)
        else:
            drawTextBox("Playground", score_offset_x, score_offset_y,
                        cross_line + score_offset_x, score_offset_y, BLACK, BG, score_font_size)
            if rank_1p != 1:
                rank_2p = 1

        playerGroup2 = res2['playerGroup']
        blockGroup2 = res2['blockGroup']
        player2 = res2['player']
        playerGroup2.draw(screen)
        blockGroup2.draw(screen)


        if not player.isPause:
            playerGroup.update()
            playerGroup2.update()

        if player.isDead():
            player.respawn()
            res = getMap(level, True, 1)
            remain_star_1p[level - 1] = starCount[level - 1]
        if player2.isDead():
            player2.respawn()
            res2 = getMap(level_for_2p, True, 2)
            remain_star_2p[level_for_2p - 1] = starCount[level_for_2p - 1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.isPause = not player.isPause
                if event.key == pygame.K_LSHIFT:
                    player.useSkill()
                if event.key == pygame.K_RSHIFT:
                    player2.useSkill()

        if player.stageClear:
            level += 1
            res = getMap(level, True, 1)

        if player2.stageClear:
            level_for_2p += 1
            res2 = getMap(level_for_2p, True, 2)

        pygame.display.flip()

pygame.quit()
sys.exit()
