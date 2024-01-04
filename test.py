import pygame

class test:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.screen.fill((255, 192, 203))
        pygame.display.flip()

    def updateUi(self):
        font = pygame.font.Font(None, 36)
        text = font.render("42", True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 150))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    def step(self):
        self.updateUi()
        print("works")

if __name__ == "__main__":
    theTest = test()
    while True:
        theTest.step()