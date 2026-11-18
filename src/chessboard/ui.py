import pygame

pygame.init()


class WindowGame:
    def __init__(self) -> None:
        self.__build_ui()

    def __build_ui(self):
        self.__screen = pygame.display.set_mode((800, 600))
        self.__clock = pygame.time.Clock()
        self.__is_running: bool = False
        self.__cells: list[pygame.Rect] = []
        self.__background = None

    def draw_chessboard(self, surface: pygame.Surface):
        color_1 = (255, 255, 255)
        color_2 = (101, 67, 33)

        cell_size = 50

        for index_x in range(1, 9):
            for index_y in range(1, 9):
                if (index_x + index_y) % 2 == 0:
                    cell = pygame.draw.rect(
                        surface,
                        color_1,
                        (
                            index_x * cell_size,
                            index_y * cell_size,
                            cell_size,
                            cell_size,
                        ),
                    )
                else:
                    cell = pygame.draw.rect(
                        surface,
                        color_2,
                        (
                            index_x * cell_size,
                            index_y * cell_size,
                            cell_size,
                            cell_size,
                        ),
                    )
                self.__cells.append(cell)

    def display(self):
        self.__is_running = True

        background = None

        self.__screen.fill((0, 0, 0))
        self.__background = self.__screen.convert()

        self.draw_chessboard(self.__background)

        while self.__is_running:
            # Game logic

            # Event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_running = False

            # Display logic

            self.__screen.blit(self.__background, (0, 0))
            pygame.display.flip()

            self.__clock.tick(60)

        pygame.quit()
