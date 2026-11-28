import pygame

from game import settings


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 40, 60)
        self.speed = settings.PLAYER_SPEED
        self.reset(x, y)

    def reset(self, x, y):
        self.rect.topleft = x, y
        self.x, self.y = float(x), float(y)
        self.velocity_y = 0
        self.on_ground = False
        self.airborne_jump = False
        self.direction = 1
        self.walk_time = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = -settings.JUMP_SPEED
            self.on_ground = False
            self.airborne_jump = True

    def update(self, dt, platforms, level_width, direction):
        if direction:
            self.direction = direction

        old_x = self.rect.x
        self.move_horizontal(direction * self.speed * dt, platforms, level_width)
        self.walk_time = self.walk_time + dt if old_x != self.rect.x else 0

        self.velocity_y = min(
            self.velocity_y + settings.GRAVITY * dt,
            settings.MAX_FALL_SPEED,
        )
        self.move_vertical(self.velocity_y * dt, platforms)

    def move_horizontal(self, distance, platforms, level_width):
        self.x = max(0, min(self.x + distance, level_width - self.rect.width))
        self.rect.x = round(self.x)

        hits = [platform for platform in platforms if self.rect.colliderect(platform)]
        if hits and distance:
            if distance > 0:
                self.rect.right = min(platform.left for platform in hits)
            else:
                self.rect.left = max(platform.right for platform in hits)
            self.x = float(self.rect.x)

    def move_vertical(self, distance, platforms):
        self.y += distance
        self.rect.y = round(self.y)

        hits = [platform for platform in platforms if self.rect.colliderect(platform)]
        if hits and distance:
            if distance > 0:
                self.rect.bottom = min(platform.top for platform in hits)
            else:
                self.rect.top = max(platform.bottom for platform in hits)
            self.y = float(self.rect.y)
            self.velocity_y = 0

        self.check_ground(platforms)

    def check_ground(self, platforms):
        probe = self.rect.move(0, 1)
        self.on_ground = self.velocity_y >= 0 and probe.collidelist(platforms) != -1
        if self.on_ground:
            self.airborne_jump = False
