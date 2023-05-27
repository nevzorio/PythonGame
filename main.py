import pygame
from blocks import *
from knight import *
from boss import *

FPS_NUMBER = 144

windowWidth = 1200
windowHeight = 1080
geometry = (windowWidth, windowHeight)
bgColor = "#002549"
blocks = Blocks(-100, -100)
timer = pygame.time.Clock()
knight = Knight(85, 255)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+windowWidth/ 2, -t+windowHeight / 2

    l = min(0, l)
    l = max(-(camera.width-windowWidth), l)
    t = max(-(camera.height-windowHeight), t)
    t = min(0, t)

    return Rect(l, t, w, h)


# class Background(pygame.sprite.Sprite):
#     def __init__(self, image_file, location):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load("bg.png")
#         self.rect = self.image.get_rect()
#         self.rect.left, self.rect.top = location


def main():
    left = right = up = 0
    pygame.init()
    sc = pygame.display.set_mode(geometry)
    entities = pygame.sprite.Group()
    platforms = []
    blocks.generate_blocks(sc, entities, platforms)
    entities.add(knight)
    entities.add(boss)
    pygame.display.set_caption("Dead Maze")
    bg = Surface(geometry)
    # bg = Background('bg.png', [0, 0])

    game_started = False

    bg.fill(Color(bgColor))

    FPS = time.Clock()


    total_level_width = len(blocks.blockList[0]) * blocks.width
    total_level_height = len(blocks.blockList) * blocks.height

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                game_started = True
        if game_started:
            break
        sc.blit(image.load("start.png"), (0, 0))
        display.update()
        FPS.tick(FPS_NUMBER)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise(SystemExit, "QUIT")
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYDOWN and event.key == K_UP:
                up = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            # if event.type == KEYDOWN and event.key == K_s:
            #     knight.speed *= 6
            # if event.type == KEYDOWN and event.key == K_w:
            #     knight.speed /= 6
            if event.type == KEYDOWN and event.key == K_e:
                knight.interaction = True
            if event.type == KEYUP and event.key == K_e:
                knight.interaction = False
        sc.blit(bg, (0, 0))
        knight.update(left, right, up, platforms)
        camera.update(knight)
        if knight.rect.x > 5610:
            boss.attack(knight, entities)
            for atk in boss.attackList:
                atk.move(platforms, knight, entities, sc, FPS, FPS_NUMBER)
            if boss.rect.colliderect(knight) and boss.cooldown > 0:
                boss.cooldown = 0
                knight.punchAnim.play()
                boss.health -= 1
                if boss.health < 1:
                    while True:
                        for e in pygame.event.get():
                            if e.type == KEYDOWN and e.key == K_ESCAPE:
                                sys.exit()
                        sc.blit(image.load("victory.png"), (0, 0))
                        display.update()
                        FPS.tick(FPS_NUMBER)
        if blocks.trapdoorlever.collide_player(knight):
            entities.remove(blocks.trapdoorlever)
        blocks.jumpBoost.collide_player(knight)
        if blocks.key.rect.colliderect(knight):
            blocks.npc.message.kill()
            blocks.npc.kill()
        blocks.key.collide_player(knight, entities)
        blocks.npc.collide_player(knight, entities)
        for i in blocks.doorList:
            i.collide_player(knight)
        for e in entities:
            sc.blit(e.image, camera.apply(e))
        # fpsText = pygame.font.Font(None, 100).render(str(round(FPS.get_fps())), True, "#990000")
        # sc.blit(fpsText, [0, 0])
        pygame.display.update()
        FPS.tick(FPS_NUMBER)


main()
