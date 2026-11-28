class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = 0
        self.y = 0

    def update(self, target_rect, level_width, level_height):
        desired_x = target_rect.centerx - self.screen_width // 2
        desired_y = target_rect.centery - self.screen_height // 2

        max_x = max(0, level_width - self.screen_width)
        max_y = max(0, level_height - self.screen_height)

        self.x = max(0, min(desired_x, max_x))
        self.y = max(0, min(desired_y, max_y))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)