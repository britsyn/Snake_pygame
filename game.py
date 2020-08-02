from config import Config
from snake import Snake
from apple import Apple
import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Wormy')
        self.apple = Apple()
        self.snake = Snake()

    def resetGame(self):
        del self.snake
        del self.apple
        self.snake = Snake()
        self.apple =Apple()

        return True

    def isGameOver(self):
        if (
            self.snake.WormCoordinates[self.snake.HEAD]['x'] == -1 or
            self.snake.WormCoordinates[self.snake.HEAD]['x'] == Config.CELLWIDTH or
            self.snake.WormCoordinates[self.snake.HEAD]['y'] == -1 or
            self.snake.WormCoordinates[self.snake.HEAD]['y'] == Config.CELLHEIGHT
        ):
            return self.resetGame()

        for wormBody in self.snake.WormCoordinates[1:]:
            if (
                wormBody['x'] == self.snake.WormCoordinates[self.snake.HEAD]['x'] and
                wormBody['y'] == self.snake.WormCoordinates[self.snake.HEAD]['y']
            ):
                return self.resetGame()

    def drawGrid(self):
        for x in range(0, Config.WINDOW_WIDTH, Config.CELLSIZE):
            pygame.draw.line(self.screen, Config.DARKGRAY, (x, 0), (x, Config.WINDOW_HEIGHT))

        for y in range(0, Config.WINDOW_HEIGHT, Config.CELLSIZE):
            pygame.draw.line(self.screen, Config.DARKGRAY, (0, y), (Config.WINDOW_WIDTH, y))

    def drawWarm(self):
        for coord in self.snake.WormCoordinates:
            x = coord['x'] * Config.CELLSIZE
            y = coord['y'] * Config.CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
            pygame.draw.rect(self.screen, Config.DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Config.CELLSIZE - 8, Config.CELLSIZE - 8)
            pygame.draw.rect(self.screen, Config.GREEN, wormInnerSegmentRect)

    def drawApple(self):
        x = self.apple.x * Config.CELLSIZE
        y = self.apple.y * Config.CELLSIZE
        appleRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
        pygame.draw.rect(self.screen, Config.RED, appleRect)

    def drawScore(self, score):
        scoreSurf = self.BASICFONT.render('Score: %s' % score, Config.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (Config.WINDOW_WIDTH - 120, 10)
        self.screen.blit(scoreSurf, scoreRect)

    def draw(self):
        self.screen.fill(Config.BG_COLOR)
        self.drawGrid()
        self.drawWarm()
        self.drawApple()
        self.drawScore(len(self.snake.WormCoordinates) - 3)
        pygame.display.update()
        self.clock.tick(Config.FPS)

    def handleKeyEvents(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.handleKeyEvents(event)

            self.snake.update(self.apple)
            self.draw()
            if self.isGameOver():
                break
