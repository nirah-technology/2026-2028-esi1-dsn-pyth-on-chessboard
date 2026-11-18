import pygame

pygame.init()


class WindowGame:
    def __init__(self) -> None:
        self.__build_ui()

    def __build_ui(self):
        self.__screen = pygame.display.set_mode((800, 600))
        self.__clock = pygame.time.Clock()
        self.__is_running: bool = False

    def display(self):
        self.__is_running = True

        while self.__is_running:
            # Game logic

            # Event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_running = False

            # Display logic
            self.__screen.fill((50, 50, 50))
            margin = 100
            self.__player_surface = pygame.draw.rect(
                self.__screen, (255, 255, 255), pygame.Rect(margin, margin, 100, 100)
            )
            pygame.display.flip()

            self.__clock.tick(60)

        pygame.quit()
