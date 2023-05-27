from pygame import *
import sys


class Boss(sprite.Sprite):
    def __init__(self, x, y):
        self.health = 3
        self.cooldown = 0
        self.atk = None
        self.mayAttack = True
        self.width = 400
        self.height = 635
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.imageReg = image.load("boss.png")
        self.imageWeak = image.load("bossWeak.png")
        self.imageBlock = image.load("atk.png")
        self.image = self.imageReg
        self.rect = Rect(x, y, self.width, self.height)
        self.attackType = 1
        self.attackCount = 0
        self.attackList = []

    def attack(self, target, group):
        if self.cooldown < 1:
            if self.mayAttack:
                self.attackCount += 1
                if self.attackType == 1:
                    self.attackList.clear()
                    self.image = self.imageReg
                    self.atk = BossAttackBasic(self.rect.x + self.rect.width / 2, self.rect.y + self.height / 2 - 300, target)
                    group.add(self.atk)
                    self.attackList.append(self.atk)
                    self.mayAttack = False
                elif self.attackType == -1:
                    x = 25000
                    y = 25000
                    self.attackList.clear()
                    for i in range(5):
                        self.atk = bossAttackWave(self.rect.x + self.rect.width / 2, self.rect.y + self.height / 2 - 300, x, y, self.imageBlock)
                        y -= 25000
                        x += 25000
                        self.attackList.append(self.atk)
                        group.add(self.atk)
                        self.mayAttack = False
                if self.attackCount % 2 == 0:
                    self.image = self.imageWeak
                    self.cooldown = 240000
                self.attackType *= -1


global boss
boss = Boss(7650, 3105)


class BossAttackBasic(sprite.Sprite):
    def __init__(self, x, y, target):
        self.lastClock = time.get_ticks()
        self.message = None
        self.width = 85
        self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("atk.png")
        self.rect = Rect(x, y, self.width, self.height)
        self.xSpeed = (abs(self.rect.x - target.rect.x)) / 300 * 144 / 1000
        self.ySpeed = (abs(self.rect.y - target.rect.y)) / 300 * 144 / 1000

    def move(self, platforms, target, group, sc, FPS, FPS_NUMBER):
        currentClock = time.get_ticks()
        elapsedMs = currentClock - self.lastClock
        self.lastClock = currentClock
        self.rect.x += self.xSpeed * elapsedMs
        self.rect.y += self.ySpeed * elapsedMs
        if self.rect.colliderect(target):
            while True:
                for e in event.get():
                    if e.type == KEYDOWN and e.key == K_ESCAPE:
                        sys.exit()
                sc.blit(image.load("lose.png"), (0, 0))
                display.update()
                FPS.tick(FPS_NUMBER)
        for p in platforms:
            if self.rect.colliderect(p):
                boss.mayAttack = True
                group.remove(self)
                self.kill()


class bossAttackWave(sprite.Sprite):
    def __init__(self, x, y, targetX, targetY, imageBlock):
        self.lastClock = time.get_ticks()
        self.message = None
        self.width = 85
        self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = imageBlock
        self.rect = Rect(x, y, self.width, self.height)
        self.xSpeed = targetX / 7000 * 144 / 1000
        self.ySpeed = targetY / 7000 * 144 / 1000

    def move(self, platforms, target, group, sc, FPS, FPS_NUMBER):
        currentClock = time.get_ticks()
        elapsedMs = currentClock - self.lastClock
        self.lastClock = currentClock
        self.rect.x += self.xSpeed * elapsedMs
        self.rect.y += self.ySpeed * elapsedMs
        if self.rect.colliderect(target):
            while True:
                for e in event.get():
                    if e.type == KEYDOWN and e.key == K_ESCAPE:
                        sys.exit()
                sc.blit(image.load("lose.png"), (0, 0))
                display.update()
                FPS.tick(FPS_NUMBER)
        for p in platforms:
            if self.rect.colliderect(p):
                boss.mayAttack = True
                group.remove(self)
                self.kill()
