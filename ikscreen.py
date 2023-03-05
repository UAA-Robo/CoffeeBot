from pygame.display import set_mode, set_caption
from pygame.font import Font
from pygame.time import Clock
import pygame.draw
from model import Model


class IKScreen:
    """
    this class configures the screen and gives us an object to blit to

    # Window Initialization
    SCREEN_HEIGHT = 520
    SCREEN_WIDTH = 1525
    """

    def __init__(self,
                 screen_height=1020,
                 screen_width=1525,
                 caption="Robot Simulation",
                 fps=180,
                 ):
        self._screen = (screen_width, screen_height)
        self._caption = caption

        self.caption = caption

        self.font = Font("Fonts/LEMONMILK-Medium.otf", 30)

        self.fps = fps
        self.clock = Clock()

        """
        Rendering Constants
        
        """
        # immutable in program constants... we can change these here but not in real time (yet)
        self.scaling = 1
        self.YOffset, self.XOffset = self.screen
        self.YOffset = (self.YOffset - 20) / 2
        self.XOffset = 265
        self.XHorizontalOffset = 510

        self.screen_width, self.screen_height = self.screen

        self.window = set_mode(self._screen)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen_size):
        x, y = screen_size
        self.screen_size((x, y))
        self.window = set_mode(self._screen_size)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption = caption
        set_caption(self._caption)

    def draw_text(self, text, _x, _y, color=(255, 255, 255)):
        # Draws Text on screen at x, y
        img = self.font.render(text, True, color)
        self.window.blit(img, (_x, _y))

    def draw_arm_piece(self, arm_start_x, arm_start_y, arm_end_x, arm_end_y, color=(255, 255, 255),
                       offset_1=0,
                       offset_2=0):
        pygame.draw.line(self.window,
                         color,
                         (arm_start_x * self.scaling + offset_1, arm_start_y * self.scaling + offset_2),
                         (arm_end_x * self.scaling + offset_1, arm_end_y * self.scaling + offset_2), 2)

    def draw_circle(self, x, y, color, offset_1=0, offset_2=0):
        pygame.draw.circle(self.window, color,
                           (offset_1 + x * self.scaling, y * self.scaling + offset_2), 8 * self.scaling)

    def render(self, model: Model):
        # Rendering
        # Fill screen with black
        self.clock.tick(self.fps)

        self.window.fill((0, 0, 0))

        # X / Y Plane Top View

        # draw the background
        pygame.draw.rect(self.window, (50, 50, 50), (10, 10, self.XHorizontalOffset - 15, self.screen_height - 20))

        # draw the line from the elbow to the hand
        self.draw_arm_piece(model.elbowX, model.elbowY, model.handX, model.handY, offset_1=self.XOffset,
                            offset_2=self.YOffset)
        # draw the hand - a red circle
        self.draw_circle(model.handX, model.handY, color=(255, 0, 0), offset_1=self.XOffset, offset_2=self.YOffset)

        # draw the arm piece from the elbow to the base
        self.draw_arm_piece(model.elbowX, model.elbowY, model.baseX, model.baseY, offset_1=self.XOffset,
                            offset_2=self.YOffset)

        # draw the base - blue circle
        self.draw_circle(model.baseX, model.baseY, (0, 0, 255), offset_1=self.XOffset, offset_2=self.YOffset)
        # draw the elbow, a green circle
        self.draw_circle(model.elbowX, model.elbowY, (0, 255, 0), offset_1=self.XOffset, offset_2=self.YOffset)



        # Z / Y Plane Front View
        ZYOffset = self.XHorizontalOffset + 265
        # draw the background
        pygame.draw.rect(self.window, (50, 50, 50),
                         (self.XHorizontalOffset + 5, 10, self.XHorizontalOffset - 15, self.screen_height - 20))

        # draw the line from the elbow to the hand
        self.draw_arm_piece(model.elbowX, model.elbowY, model.handX, model.handY,
                            offset_1=ZYOffset,
                            offset_2=self.YOffset)
        # draw the hand - a red circle
        self.draw_circle(model.handX, model.handY, color=(255, 0, 0),
                         offset_1=ZYOffset,
                         offset_2=self.YOffset)

        # draw the arm piece from the elbow to the base
        self.draw_arm_piece(model.elbowX, model.elbowY, model.baseX, model.baseY,
                            offset_1=ZYOffset,
                            offset_2=self.YOffset)

        # draw the base - blue circle
        self.draw_circle(model.baseX, model.baseY, (0, 0, 255),
                         offset_1=ZYOffset,
                         offset_2=self.YOffset)

        # draw the elbow, a green circle
        self.draw_circle(model.elbowX, model.elbowY, (0, 255, 0),
                         offset_1=ZYOffset,
                         offset_2=self.YOffset)

        # X / Z Plane Side View
        XZOffset = self.XHorizontalOffset * 2 + 265
        pygame.draw.rect(self.window, (50, 50, 50),
                         (self.XHorizontalOffset * 2, 10, self.XHorizontalOffset - 15, self.screen_height - 20))

        # draw the line from the elbow to the hand
        self.draw_arm_piece(model.elbowX, model.elbowY, model.handX, model.handY,
                            offset_1=XZOffset,
                            offset_2=self.YOffset)
        # draw the hand - a red circle
        self.draw_circle(model.handX, model.handY, color=(255, 0, 0),
                         offset_1=ZYOffset,
                         offset_2=self.YOffset)

        # draw the arm piece from the elbow to the base
        self.draw_arm_piece(model.elbowX, model.elbowY, model.baseX, model.baseY,
                            offset_1=XZOffset,
                            offset_2=self.YOffset)

        # draw the base - blue circle
        self.draw_circle(model.baseX, model.baseY, (0, 0, 255),
                         offset_1=XZOffset,
                         offset_2=self.YOffset)

        # draw the elbow, a green circle
        self.draw_circle(model.elbowX, model.elbowY, (0, 255, 0),
                         offset_1=XZOffset,
                         offset_2=self.YOffset)

        # Text at top of screen
        self.draw_text(f"Top View X / Y", 20, 10)
        self.draw_text(f"Front View Y / Z", self.XHorizontalOffset + 15, 10)
        self.draw_text(f"Side View X / Z", self.XHorizontalOffset * 2 + 10, 10)

        # Updates Screen
        pygame.display.update()
