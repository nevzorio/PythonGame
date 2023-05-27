import pygame.time
from pygame import *
import pyganim
from boss import boss

MOVE_SPEED = 4 * 144 / 1000
WIDTH = 170
HEIGHT = 250
JUMP_POWER = 3
GRAVITY = 0.065 * 144 / 1000
ANIMATION_DELAY = 100
ANIMATION_RIGHT = [('l2.png'),
            ('r1.png')]
ANIMATION_LEFT = [('l1.png'),
            ('r2.png')]
ANIMATION_JUMP_LEFT = [('static.png', 1)]
ANIMATION_JUMP_RIGHT = [('static.png', 1)]
ANIMATION_STAY = [('static.png', 1)]
ANIMATION_STAY_LEFT = [('static.png', 1)]
COLOR = "#888888"


class Knight(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.interaction = False
        self.vertVelocity = 0
        self.speed = MOVE_SPEED
        self.leftRotated = False
        self.xOffset = 0
        self.startPosX = x
        self.startPosY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.yOffset = 0
        self.onGround = True
        self.image.set_colorkey(Color(COLOR))
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStayLeft = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStayLeft.play()
        self.boltAnimStayLeft.blit(self.image, (0, 0))

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.punchAnim = pyganim.PygAnimation([("punch.png", 1)])
        self.punchAnim.play()
        self.lastClock = pygame.time.get_ticks()

    def update(self, left, right, up, platforms):
        currentClock = pygame.time.get_ticks()
        elapsedMs = currentClock - self.lastClock
        self.lastClock = currentClock
        if left:
            self.leftRotated = True
            self.xOffset = -self.speed * elapsedMs
            self.image.fill(Color(COLOR))
            if up and not self.rect.colliderect(boss):
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            elif not self.rect.colliderect(boss):
                self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.leftRotated = False
            self.xOffset = self.speed * elapsedMs
            self.image.fill(Color(COLOR))
            if up and not self.rect.colliderect(boss):
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            elif not self.rect.colliderect(boss):
                self.boltAnimRight.blit(self.image, (0, 0))
        if not (left or right):
            self.xOffset = 0
            if not up and not self.rect.colliderect(boss):
                self.image.fill(Color(COLOR))
                if not self.leftRotated:
                    self.boltAnimStay.blit(self.image, (0, 0))
                else:
                    self.boltAnimStayLeft.blit(self.image, (0, 0))
        if not self.onGround:
            self.yOffset = self.vertVelocity * elapsedMs + GRAVITY * elapsedMs * elapsedMs / 2
            self.vertVelocity += GRAVITY * elapsedMs
        self.onGround = False

        self.rect.y += self.yOffset
        self.collide(0, self.yOffset, platforms)

        self.rect.x += self.xOffset
        self.collide(self.xOffset, 0, platforms)
        if up:
            if self.onGround:
                self.vertVelocity = -JUMP_POWER
                self.image.fill(Color(COLOR))
                if not self.leftRotated and not self.rect.colliderect(boss):
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                elif not self.rect.colliderect(boss):
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
        if self.rect.colliderect(boss):
            self.punchAnim.blit(self.image, (0, 0))

    def collide(self, xVelocity, yVelocity, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):

                if xVelocity > 0:
                    self.rect.right = p.rect.left

                if xVelocity < 0:
                    self.rect.left = p.rect.right

                if yVelocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vertVelocity = 0
                    self.yOffset = 0

                if yVelocity < 0:
                    self.vertVelocity = 0
                    self.rect.top = p.rect.bottom
                    self.yOffset = 0
