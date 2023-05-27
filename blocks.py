from pygame import *

trapdoorList = []
npcDoorList = []
theGatesHaveOpened = False


class Blocks(sprite.Sprite):
    def __init__(self, x, y):
        self.doorList = None
        self.trapdoorlever = None
        self.jumpBoost = None
        self.key = None
        self.npc = None
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("block.png")
        self.rect = Rect(x, y, self.width, self.height)
        self.blockList = [
            "----------------------------------------------------------------------------------------------------------",
            "-                                                                -                       -----------------",
            "-                                                                -                       -----------------",
            "-                                                                -                       -----------------",
            "-                                                                -                       -----------------",
            "-                                                                -                       -----------------",
            "-TTT------                                                       -                       -----------------",
            "-TTTTTTTT-                                                       -                       -----------------",
            "-TTTTTTTT-                                                       -                       -----------------",
            "-TTTTTTTT---                                 ----------          -                       -----------------",
            "-TTTTTTTT-                                            -          -                       -----------------",
            "-TTTTTTTT-                            ---             -          -                       -----------------",
            "-TTTTTTTT-                      --                    -          -                       -----------------",
            "-TTTTTTTT----------------------------------------------          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-        ---                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT--         -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-        ---                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-        ---                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                       -----------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                ------------------------",
            "-TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                ------------------------",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                ------------------------",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                ------------------------",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-l         -                ------------------------",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT------     -                ------------------------",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------------TTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------------TTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "----------------------------TTTTTTTTTTTTTTTTTTTTTTTTTT-     ------                --------               -",
            "----------------------------TTTTTTTTTTTTTTTTTTTTTTTTTT-          -                --------               -",
            "-MMMMMMMMMMMMMMMMMMMMMMMMMMMTTTTTTTTTTTTTTTTTnTTTTTTDD-          -                --------               -",
            "-MMMMMMMMMMMMMMMMMMMMMMMMMMMTTTTTTTTTTTTTTTTTTTTTTTTDD-          -                --------               -",
            "-MMMMkMMMMMMMMMMMMMMMMMMMMMMTTTTTTTTTTTTTTTTTTTTTTTTDD-     j    -                --------               -",
            "----------------------------------------------------------------------------------------------------------"
        ]

    def generate_blocks(self, sc, group, list):
        x = y = 0
        global trapdoorList, npcDoorList
        self.doorList = []
        self.wasBg = False
        for row in self.blockList:
            for column in row:
                if column == "-":
                    block = Blocks(x, y)
                    group.add(block)
                    list.append(block)
                    if len(list) == 1 and not self.wasBg:
                        block.image = image.load("bg.png")
                        self.wasBg = True
                        list.clear()
                if column == "T":
                    trapdoor = Trapdoor(x, y)
                    group.add(trapdoor)
                    trapdoorList.append(trapdoor)
                    list.append(trapdoor)
                if column == "M":
                    npcDoor = NpcDoor(x, y)
                    group.add(npcDoor)
                    npcDoorList.append(npcDoor)
                    list.append(npcDoor)
                if column == "l":
                    self.trapdoorlever = lever(x, y)
                    group.add(self.trapdoorlever)
                if column == "j":
                    self.jumpBoost = JumpBoost(x, y)
                    group.add(self.jumpBoost)
                if column == "D":
                    self.door = Door(x, y, len(self.doorList) + 1)
                    self.doorList.append(self.door)
                    group.add(self.door)
                    trapdoor = Trapdoor(x, y)
                    group.add(trapdoor)
                    trapdoorList.append(trapdoor)
                    list.append(trapdoor)
                if column == "k":
                    self.key = Key(x, y)
                    group.add(self.key)
                if column == "n":
                    self.npc = Npc(x, y)
                    group.add(self.npc)
                    trapdoor = Trapdoor(x, y)
                    group.add(trapdoor)
                    trapdoorList.append(trapdoor)
                    list.append(trapdoor)
                x += self.width
            y += self.height
            x = 0


class Trapdoor(sprite.Sprite):
    def __init__(self, x, y):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("block.png")
        self.rect = Rect(x, y, self.width, self.height)

    def open(self):
        self.rect.x = -90000


class NpcDoor(sprite.Sprite):
    def __init__(self, x, y):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("block.png")
        self.rect = Rect(x, y, self.width, self.height)

    def open(self):
        self.rect.x = -90000


class lever(sprite.Sprite):
    def __init__(self, x, y):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("lever.png")
        self.rect = Rect(x, y, self.width, self.height)

    def collide_player(self, knight):
        global trapdoorList
        if knight.interaction:
            if self.rect.colliderect(knight):
                for i in trapdoorList:
                    i.open()
                self.image = image.load("leverPressed.png")


class Key(sprite.Sprite):
    def __init__(self, x, y):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("key.png")
        self.rect = Rect(x, y, self.width, self.height)

    def collide_player(self, knight, group):
        global theGatesHaveOpened
        if self.rect.colliderect(knight):
            message = Message(3995, 3400, "level2.png")
            group.add(message)
            theGatesHaveOpened = True
            self.kill()


class JumpBoost(sprite.Sprite):
    def __init__(self, x, y):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("jumpboost.png")
        self.rect = Rect(x, y, self.width, self.height)

    def collide_player(self, knight):
        if self.rect.colliderect(knight) and knight.interaction:
            knight.rect.x -= 6 * 85
            knight.rect.y -= 35 * 85


class Door(sprite.Sprite):
    def __init__(self, x, y, number):
        self.width = self.height = 85
        self.geometry = (self.width, self.height)
        sprite.Sprite.__init__(self)
        self.image = image.load("door" + str(number) + ".png")
        self.rect = Rect(x, y, self.width, self.height)

    def collide_player(self, knight):
        global theGatesHaveOpened
        if self.rect.colliderect(knight) and knight.interaction and theGatesHaveOpened:
            knight.rect.x += 51 * 85


class Message(sprite.Sprite):
    def __init__(self, x, y, text_img):
        self.width = 1000
        self.height = 250
        sprite.Sprite.__init__(self)
        self.image = image.load(text_img)
        self.rect = Rect(x, y, self.width, self.height)


class Npc(sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.talked = False
        self.width = 170
        self.clock = None
        self.message = None
        self.height = 250
        sprite.Sprite.__init__(self)
        self.image = image.load("npc.png")
        self.rect = Rect(x, y, self.width, self.height)

    def show_massage(self, group):
        self.message = Message(self.x - 170, self.y - 85, "npc_dialogue.png")
        group.add(self.message)

    def collide_player(self, knight, group):
        global npcDoorList
        if self.rect.colliderect(knight) and knight.interaction and not self.talked:
            self.show_massage(group)
            for i in npcDoorList:
                i.open()
            self.talked = True
