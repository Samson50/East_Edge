import pygame, sys, shelve, story
from pygame.locals import *
from characters import *
from images import *
from room_data import *


class Option():
    def __init__(self, image, x):
        self.image = image
        self.x = x

    def show(self, surface, y):
        surface.blit(self.image, (self.x, y))


class Save(Option):
    def __init__(self, x):
        Option.__init__(self, pause_img, x)

    def run(self, cadet):
        # save values
        slot = shelve.open(story.saves[story.current_save])
        slot["file"] = "has-file"
        slot["restore"] = story.restore_steps
        slot["decisions"] = story.decisions
        slot["room"] = story.current_room
        slot["cdt-x"] = cadet.x
        slot["cdt-y"] = cadet.y
        slot.close()
        return False


class Pack(Option):
    def __init__(self, x):
        Option.__init__(self, pack_img, x)

    def run(self, cadet):
        return True

class Quit(Option):
    def __init__(self, x):
        Option.__init__(self, quit_img, x)

    def run(self, cadet):
        pygame.quit()
        sys.exit()


class PauseMenu():
    def __init__(self):
        self.options = [Save(250), Pack(250), Quit(250)]
        self.top = pause_top
        self.mid = pause_mid
        self.bottom = pause_bottom
        self.pointer = 0

    def get_events(self, cadet):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.pointer += 1
                if event.key == K_UP:
                    self.pointer -= 1
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_f:
                    return self.options[self.pointer].run(cadet)
        self.pointer %= len(self.options)
        return True

    def show(self, surface):
        surface.blit(self.top, (250,0))
        i = 0
        for option in self.options:
            surface.blit(self.mid, (250, 20+20*i))
            option.show(surface,20+i*20)
            i += 1
        surface.blit(self.bottom, (250,len(self.options)*20+20))
        surface.blit(pause_select, (250, 20+20*self.pointer))

        pygame.display.update()

    def run(self, surface, cadet):
        print "stuffs"
        paused = True
        while paused:
            paused = self.get_events(cadet)
            self.show(surface)

        return "Moving"














