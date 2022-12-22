import pygame
from random import randrange
from os import environ
from sys import platform as _sys_platform


class LifeBar:
    def __init__(self, life, mana):
        self.life = life
        self.mana = mana
        self.life_max = life
        self.mana_max = mana
        self.person = None

    def life_damage(self, x) -> None:
        value = self.life + x
        if value <= 0:
            self.life = 0
            self.person.dead()
        elif value < self.life_max:
            self.life = value
            self.person.replace_sprite(f"Hurt_{self.person.virado}")

            self.person.animate = True

    def mana_damage(self, x) -> None:
        value = self.mana + x
        if value <= 0:
            self.mana = 0
        elif value < self.mana_max:
            self.mana = value


class AdmBattles:
    def __init__(self, enemys, players):
        self.enemys = enemys
        self.players = players
        self.rects = []

    def update(self) -> None:
        self.rects = []
        for player in self.players:
            if "Attack 1" in player.sprite_name:
                damage = player.force * damages['Attack 1']
                width = (player.scale * 34)
                height = (player.scale * 8)
                if "Left" in player.sprite_name:
                    self.rects.append([
                        pygame.rect.Rect(player.rect.left, player.rect.top + (player.scale * (86 / 2)), width, height),
                        damage, ])
                elif "Right" in player.sprite_name:
                    self.rects.append([
                        pygame.rect.Rect(player.rect.left + width, player.rect.top + (player.scale * (86 / 2)), width,
                                         height),
                        damage, ])
        for enemy in self.enemys:
            for rect in self.rects:
                if enemy.rect.colliderect(rect[0]):
                    enemy.life_bar.life_damage(-rect[1])


class Person(pygame.sprite.Sprite):
    def __init__(self, name="Knight_1", virado="Right", scale=1.0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        dic_sounds = fr"{path}Sounds/person/{name}/"
        self.sounds = {
            "atk_1": pygame.mixer.Sound(fr"{dic_sounds}atk_1.ogg"),
            "Walk": pygame.mixer.Sound(fr"{dic_sounds}Walk.ogg"),
        }

        self.scale = scale
        self.sprite_dim = (68 * self.scale, 86 * self.scale)
        dic_images = fr"{path}Images/person/{name}/"
        self.images = {
            "Idle_Left": [pygame.image.load(fr"{dic_images}Idle_Left.png").convert_alpha(), 4],
            "Idle_Right": [pygame.image.load(fr"{dic_images}Idle_Right.png").convert_alpha(), 4],
            "Walk_Left": [pygame.image.load(fr"{dic_images}Walk_Left.png").convert_alpha(), 8],
            "Walk_Right": [pygame.image.load(fr"{dic_images}Walk_Right.png").convert_alpha(), 8],
            "Attack 1_Left": [pygame.image.load(fr"{dic_images}Attack 1_Left.png").convert_alpha(), 5],
            "Attack 1_Right": [pygame.image.load(fr"{dic_images}Attack 1_Right.png").convert_alpha(), 5],
            "Protect_Left": [pygame.image.load(fr"{dic_images}Protect_Left.png").convert_alpha(), 5],
            "Protect_Right": [pygame.image.load(fr"{dic_images}Protect_Right.png").convert_alpha(), 5],
            "Dead_Left": [pygame.image.load(fr"{dic_images}Dead_Left.png").convert_alpha(), 6],
            "Dead_Right": [pygame.image.load(fr"{dic_images}Dead_Right.png").convert_alpha(), 6],
            "Hurt_Left": [pygame.image.load(fr"{dic_images}Hurt_Left.png").convert_alpha(), 2],
            "Hurt_Right": [pygame.image.load(fr"{dic_images}Hurt_Right.png").convert_alpha(), 2],

        }
        self.sprite_name = None
        self.__i = 4
        self.__index = 0
        self.sprites = []
        self.replace_sprite(f"Idle_{virado}")
        self.sprite = self.sprites[0]

        self.rect = self.sprite.get_rect()

        self.coords = [largura / 2, altura / 2]
        self.rect.left, self.rect.top = self.coords
        self._vx, self._vy = 0, 0

        self.velocidade = 5
        self.virado = virado
        self.animate = False
        self.force = 2
        self.live = True

        self.life_bar = LifeBar(life=100, mana=50)
        self.life_bar.person = self

    @property
    def vx(self):
        return self._vx

    @vx.setter
    def vx(self, value):
        if not self.animate:
            self._vx = value

    @property
    def vy(self):
        return self._vy

    @vy.setter
    def vy(self, value):
        if not self.animate:
            self._vy = value

    def replace_sprite(self, name) -> None:
        self.sprite_name = name
        i = self.images[self.sprite_name][1]
        self.sprites = []
        sprite_sheet = pygame.transform.scale(self.images[self.sprite_name][0],
                                              (self.sprite_dim[0] * i, self.sprite_dim[1]))
        self.__i = i - 1

        for i in range(i):
            self.sprites.append(sprite_sheet.subsurface((i * self.sprite_dim[0], 0), self.sprite_dim))
        self.__index = randrange(0, i)
        if "Right" in self.sprite_name:
            self.virado = "Right"
        elif "Left" in self.sprite_name:
            self.virado = "Left"
            self.sprites.reverse()

    def update(self) -> None:
        self.sprite = self.sprites[self.__index]
        self.__index += 1
        if self.__index > self.__i:
            self.__index = 0
            if self.animate:
                self.stop_animate()

            if not self.live:
                self.__index = self.__i

    def move(self) -> None:
        if self.vx == 0 and self.vy == 0 and not self.animate and self.live:
            self.replace_sprite(f"Idle_{self.virado}")
        self.coords = [self.coords[0] + self.vx, self.coords[1] + self.vy]
        self.rect.left, self.rect.top = self.coords

    def moving_to_left(self) -> None:
        if not self.animate:
            self.replace_sprite("Walk_Left")
            self.vx = -self.velocidade

    def moving_to_right(self) -> None:
        if not self.animate:
            self.replace_sprite("Walk_Right")
            self.vx = self.velocidade

    def moving_to_up(self) -> None:
        if not self.animate:
            self.replace_sprite(f"Walk_{self.virado}")
            self.vy = -self.velocidade

    def moving_to_down(self) -> None:
        if not self.animate:
            self.replace_sprite(f"Walk_{self.virado}")
            self.vy = self.velocidade

    def stop_moving_y(self) -> None:
        self.vy = 0

    def stop_moving_x(self) -> None:
        self.vx = 0

    def defende(self) -> None:
        self.stop_moving_x()
        self.stop_moving_y()
        self.animate = True
        self.vx, self.vy = 0, 0
        self.replace_sprite(f"Protect_{self.virado}")

    def attack(self) -> None:
        self.som("atk_1")
        self.vx, self.vy = 0, 0
        self.animate = True
        self.replace_sprite(f"Attack 1_{self.virado}")

    def stop_animate(self) -> None:
        self.animate = False
        if self.vx == 0 and self.vy == 0 and self.live:
            self.replace_sprite(f"Idle_{self.virado}")

    def som(self, name_sound) -> None:
        self.sounds[name_sound].play().set_volume(.2)

    def dead(self) -> None:
        if self.live:
            self.replace_sprite(f"Dead_{self.virado}")
            self.live = False
            self.stop_animate()


class Player(Person):
    pass


class Enemy(Person):
    pass


class Wave:
    def __init__(self, num_enemy=1) -> None:
        self.anemys = []
        for enemy in range(num_enemy):
            self.anemys.append(Enemy(virado="Left"))

    def update(self) -> None:
        for enemy in self.anemys:
            enemy.update()

    def move(self) -> None:
        for enemy in self.anemys:
            enemy.move()


class Level1:
    def __init__(self, player: Player) -> None:
        dir_images = fr"{path}Images/maps/PNG/game_background_1/layers/"
        self.battleground = pygame.transform.scale(
            pygame.image.load(fr"{dir_images}battleground.png").convert_alpha(),
            (largura, altura))
        self.ground_decor = pygame.transform.scale(
            pygame.image.load(fr"{dir_images}ground_decor.png").convert_alpha(),
            (largura, altura))
        self.front_decor = pygame.transform.scale(
            pygame.image.load(fr"{dir_images}front_decor.png").convert_alpha(),
            (largura, altura))
        self.back_land = pygame.transform.scale(
            pygame.image.load(fr"{dir_images}back_land.png").convert_alpha(),
            (largura, altura))
        self.back_decor = pygame.transform.scale(
            pygame.image.load(fr"{dir_images}back_decor.png").convert_alpha(),
            (largura, altura))
        self.player = player
        self.tick_ant = pygame.time.get_ticks()

        self.wave = Wave()

        self.adm_battles = AdmBattles(self.wave.anemys, [self.player])

        self.old_coords = self.player.coords
        self.invisible_walls = pygame.rect.Rect(0.05 * largura, 0.38 * altura, 0.9 * largura, 0.45 * altura)

    def update(self, window) -> None:
        # map_back
        window.blit(self.battleground, (0, 0))
        window.blit(self.ground_decor, (0, 0))
        window.blit(self.back_land, (0, 0))
        window.blit(self.back_decor, (0, 0))

        # time_update_animates
        tick = pygame.time.get_ticks()
        if (tick - self.tick_ant) >= 90:  # 90ms
            self.player.update()
            self.wave.update()
            self.tick_ant = tick

        # move_person
        self.wave.move()
        self.player.move()
        self.blit(window)

        # map_front
        window.blit(self.front_decor, (0, 0))

        # block_player_move
        self.check_player()

        # life_bar

        self.adm_battles.update()

    def check_player(self) -> None:
        if not self.invisible_walls.colliderect(self.player.rect):
            self.player.coords = self.old_coords[:]
        self.old_coords = self.player.coords[:]

    def blit(self, window) -> None:
        # list_blit = sorted(self.wave.anemys + [self.player], key=lambda y: y.coords[1] + y.scale * 86)
        for person in self.wave.anemys:
            window.blit(person.sprite, person.coords)
        window.blit(self.player.sprite, self.player.coords)


def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    sair = False

    player = Player(scale=1)
    level = Level1(player)

    leftpress, rightpress, uppress, downpress = (False, False, False, False)

    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if not level.player.animate:
                        level.player.attack()
                if event.key == pygame.K_s:
                    if not level.player.animate:
                        level.player.defende()
                if event.key == pygame.K_d:
                    if not level.player.animate:
                        level.player.dead()
                if event.key == pygame.K_LEFT:
                    leftpress = True
                    level.player.moving_to_left()
                if event.key == pygame.K_RIGHT:
                    rightpress = True
                    level.player.moving_to_right()
                if event.key == pygame.K_UP:
                    uppress = True
                    level.player.moving_to_up()
                if event.key == pygame.K_DOWN:
                    downpress = True
                    level.player.moving_to_down()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftpress = False
                    if rightpress:
                        level.player.moving_to_right()
                    else:
                        level.player.stop_moving_x()
                if event.key == pygame.K_RIGHT:
                    rightpress = False
                    if leftpress:
                        level.player.moving_to_left()
                    else:
                        level.player.stop_moving_x()

                if event.key == pygame.K_UP:
                    uppress = False
                    if downpress:
                        level.player.moving_to_down()
                    else:
                        level.player.stop_moving_y()

                if event.key == pygame.K_DOWN:
                    downpress = False
                    if uppress:
                        level.player.moving_to_up()
                    else:
                        level.player.stop_moving_y()

        level.update(window)

        pygame.display.update()
        clock.tick(framerate)
    pygame.quit()


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('linux', 'linux2', 'linux3'):
        return "linux"
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'


plataform = platform()
if plataform == "android":
    path = "/data/data/sword.pgame/files/app/"
elif plataform == "linux":
    path = "./"
elif plataform == "win":
    path = ""

largura = 1080
altura = 720
framerate = 30

damages = {
    "Attack 1": 1
}

main()
