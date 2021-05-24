import pygame


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = pygame.Color(200, 255, 200)
WAYPOINT_COLOR = pygame.Color(0, 0, 200)
WAYPOINT_RADIUS = 5
WALKER_COLOR = pygame.Color(220, 40, 0)
WALKER_WIDTH = 3
WALKER_RADIUS = WAYPOINT_RADIUS + WALKER_WIDTH + 1
WALKER_SPEED = 200  # pixels per second
CRITICAL_DISTANCE = 5
FPS = 60
waypoints = [
    pygame.Vector2(200, 600),
    pygame.Vector2(600, 200),
    pygame.Vector2(1000, 400)
]


class Walker:
    def __init__(self):
        self.position = pygame.Vector2(waypoints[0])
        self.target = waypoints[1]
        self.current_target_index = 0
        self.velocity = pygame.Vector2(WALKER_SPEED)

    def update(self, dt):
        distance = self.target - self.position
        if distance.length() <= CRITICAL_DISTANCE:
            # Alternative: See if direction flipped. Avoids jumping over target
            # when speed is too high.
            self.current_target_index = (self.current_target_index + 1) % len(waypoints)
            self.target = waypoints[self.current_target_index]
        velocity = distance.normalize() * WALKER_SPEED
        self.position += velocity * dt


def run():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    walker = Walker()

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    waypoints.append(pygame.Vector2(event.pos))
                elif event.button == 3:
                    walker.position = pygame.Vector2(event.pos)

        walker.update(dt)

        window.fill(BACKGROUND_COLOR)
        for w in waypoints:
            pygame.draw.circle(
                window,
                WAYPOINT_COLOR,
                w,
                WAYPOINT_RADIUS
            )

        pygame.draw.circle(
            window,
            WALKER_COLOR,
            walker.position,
            WALKER_RADIUS,
            WALKER_WIDTH
        )
        pygame.display.flip()


run()
