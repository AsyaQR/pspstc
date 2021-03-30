import pygame
from modules.constants import *
from modules.geometry import *
from modules.functions import *


class Window:
    def __init__(self):
        # initialization of screen from pygame
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.screen.fill(BLACK)
        self.init_ui()

    def init_ui(self):
        # initialization of objects for window
        y_coords = split_line(HEIGHT, 1, 7, 2)
        # Create Menu
        self.menu = Menu((0, 0), (WIDTH, int(y_coords[0])))

        tab_geometry = Tab(self.screen, 'Геометрия')
        button_point = Button(self.screen, 'Точка')
        button_line = Button(self.screen, 'Линия')
        button_area = Button(self.screen, 'Площадь')

        tab_ke = Tab(self.screen, 'КЭ')
        button_mesh_line = Button(self.screen, 'Разбить линию')
        button_mesh_area = Button(self.screen, 'Разбить площадь')
        button_choose_material = Button(self.screen, 'Выбрать материал')

        tab_mke = Tab(self.screen, 'МКЭ')
        button_temperature = Button(self.screen, 'Температурный МКЭ')
        button_set_temperature = Button(self.screen, 'Задать температуру')
        button_test23 = Button(self.screen, 'Тестовая кнопка 3')
        button_test24 = Button(self.screen, 'Тестовая кнопка 4')

        self.menu.add_tab(tab_geometry)
        self.menu.add_button(tab_geometry, button_point)
        self.menu.add_button(tab_geometry, button_line)
        self.menu.add_button(tab_geometry, button_area)

        self.menu.add_tab(tab_ke)
        self.menu.add_button(tab_ke, button_mesh_line)
        self.menu.add_button(tab_ke, button_mesh_area)
        self.menu.add_button(tab_ke, button_choose_material)

        self.menu.add_tab(tab_mke)
        self.menu.add_button(tab_mke, button_temperature)
        self.menu.add_button(tab_mke, button_set_temperature)
        self.menu.add_button(tab_mke, button_test23)
        self.menu.add_button(tab_mke, button_test24)

        self.menu.tabs[0].state = 'pressed'
        self.menu.tabs[0].buttons[0].state = 'pressed'

        self.menu.draw(self.screen)

        # Create Field
        self.field = Field((0, int(y_coords[0])), (WIDTH, int(y_coords[1])))
        self.field.draw(self.screen)

        # Create ShowHint
        self.show_hint = ShowHint((0, int(y_coords[1])), (WIDTH, int(y_coords[2])))


class DialogWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((200, 200))
        self.screen.fill(YELLOWGREEN)
        self.init_ui()

    def init_ui(self):
        pass


class Menu:
    def __init__(self, coords1, coords2):
        self.x, self.y = coords1
        x2, y2 = coords2
        self.width = x2 - self.x
        self.height = y2 - self.y
        self.tabs_height = self.height * 0.4
        self.lenghts_of_tabs = []
        self.tabs = []

    def add_tab(self, tab):
        self.tabs.append(tab)

        if len(self.tabs) == 0:
            tab.x, tab.y = self.x, self.y
        else:
            tab.x = sum(self.lenghts_of_tabs) + self.x
            tab.y = self.y

        self.lenghts_of_tabs.append(tab.width)

    def add_button(self, tab, button):
        tab.add_button(button)

    def draw(self, display):
        pygame.draw.rect(display, WHITE, (self.x, self.y, self.width, self.height))
        quantity_of_tabs = len(self.tabs)
        height_of_tabs = self.tabs_height
        for i in range(quantity_of_tabs):
            tab = self.tabs[i]
            tab.draw(sum(self.lenghts_of_tabs[:i]) + 10 * i, 0, height_of_tabs)

        for tab in self.tabs:
            if tab.state == 'pressed':
                quantity_of_buttons = len(tab.buttons)
                height_of_button = self.height - self.tabs_height
                for i in range(quantity_of_buttons):
                    button = tab.buttons[i]
                    button.draw(sum(tab.lenghts_of_buttons[:i]) + 10 * i, self.y + self.tabs_height, height_of_button)


class Button:
    def __init__(self, display, text):
        self.display = display
        self.text = text
        self.state = 'unpressed'

        font_size = 20
        self.font = pygame.font.SysFont('serif', font_size)
        self.width, self.height = self.font.size(text)
        self.x, self.y = None, None

    def press(self, press_pos):
        x_press, y_press = press_pos
        if self.x + self.width >= x_press >= self.x and self.y + self.height >= y_press >= self.y:
            self.state = 'pressed'
        else:
            self.state = 'unpressed'

    def draw(self, x, y, height):
        self.x, self.y = x, y

        if self.state == 'unpressed':
            self.display.fill(WHITE, (x, y, self.width + 10, height))

        if self.state == 'pressed':
            self.display.fill(YELLOWGREEN, (x, y, self.width + 10, height))

        pygame.draw.rect(self.display, GREY, (x, y, self.width + 10, height), 1)

        text = self.font.render(self.text, 1, BLACK)
        self.display.blit(text, (x + 5, y + self.height * 0.01))


class Tab(Button):
    def __init__(self, display, text):
        super().__init__(display, text)
        self.buttons = []
        self.lenghts_of_buttons = []

    def add_button(self, button):
        self.buttons.append(button)

        if len(self.buttons) == 0:
            button.x, button.y = self.x, self.y + self.height
        else:
            button.x = sum(self.lenghts_of_buttons) + self.x
            button.y = self.y + self.height

        self.lenghts_of_buttons.append(button.width)

    def press(self, press_pos):
        x_press, y_press = press_pos
        if self.x + self.width >= x_press >= self.x and self.y + self.height >= y_press >= self.y:
            self.state = 'pressed'
            self.buttons[0].state = 'pressed'
        else:
            self.state = 'unpressed'
            for button in self.buttons:
                button.state = 'unpressed'


class Field:
    def __init__(self, coords1, coords2):
        self.x, self.y = coords1
        x2, y2 = coords2
        self.width = x2 - self.x
        self.height = y2 - self.y
        self.scale = 1
        self.grid_size = 20
        self.cursor = Cursor(self)
        self.geometry_objects = {}
        self.finit_elements = {}

    def draw(self, display):
        display.fill(WHITE, (self.x, self.y, self.width, self.height))
        for i in range(self.height // (self.scale * self.grid_size)):
            point1 = self.x, self.y + self.scale * self.grid_size * i
            point2 = self.x + self.width, self.y + self.scale * self.grid_size * i
            pygame.draw.line(display, VERYLIGHTBLUE, point1, point2, 1)

        for i in range(self.width // (self.scale * self.grid_size)):
            point1 = self.x + self.scale * self.grid_size * i, self.y
            point2 = self.x + self.scale * self.grid_size * i, self.y + self.height
            pygame.draw.line(display, VERYLIGHTBLUE, point1, point2, 1)

        for list_of_geometry_objects in self.geometry_objects.values():
            for geometry_object in list_of_geometry_objects:
                geometry_object.draw(display, self)
                if isinstance(geometry_object, Line):
                    geometry_object.draw_temperature_mke(display, self)

        for list_of_finit_elements in self.finit_elements.values():
            for finit_element in list_of_finit_elements:
                finit_element.draw(display, self)


    def set_geometry_objects(self, geometry_objects):
        self.geometry_objects = geometry_objects

    def set_finit_elements(self, finit_elements):
        self.finit_elements = finit_elements

    def get_cursor(self):
        return self.cursor


class Cursor:
    def __init__(self, field):
        self.x, self.y = None, None
        self.field = field

    def move(self, x, y):
        field = self.field
        if field.x <= x <= field.x + field.width and field.y <= y <= field.y + field.height:
            self.x = abs(x - field.x)
            self.y = abs(y - field.height - field.y)
        else:
            self.x, self.y = None, None

    def get_coords(self):
        return self.x, self.y


class ShowHint:
    def __init__(self, coords1, coords2):
        self.x, self.y = coords1
        x, y = coords2
        self.width = x - self.x
        self.height = y - self.y

        font_size = 20
        self.font = pygame.font.SysFont('serif', font_size)

    def draw(self, display, cursor, geometry_object, hint):
        display.fill(WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.line(display, VERYLIGHTBLUE, (self.x, self.y), (self.x + self.width, self.y))

        font_size = 15
        self.font = pygame.font.SysFont('serif', font_size)

        x, y = cursor.x, cursor.y
        if x is None:
            x = ' '
        if y is None:
            y = ' '

        width1, height1 = self.font.size(str(x))
        text1 = self.font.render(str(x), 1, BLACK)
        width2, height2 = self.font.size(str(y))
        text2 = self.font.render(str(y), 1, BLACK)

        pygame.draw.rect(display, GREY, (self.x, self.y, width1 + 10, height1 + 10), 1)
        pygame.draw.rect(display, GREY, (self.x + width1 + 10, self.y, width2 + 10, height2 + 10), 1)

        display.blit(text1, (self.x + 5, self.y + 5))
        display.blit(text2, (self.x + width1 + 15, self.y + 5))

        if str(geometry_object) == "None":
            geometry_object_str = ' '
        else:
            geometry_object_str = str(geometry_object)
        text3 = self.font.render(geometry_object_str, 1, BLACK)
        width3, height3 = self.font.size(geometry_object_str)
        display.blit(text3, (self.x + 5, self.y + height1 + 15))
        pygame.draw.rect(display, GREY, (self.x, self.y + height1 + 10, width3 + 10, height3 + 10), 1)
        if hint:
            text4_str = hint[0]
            text5_str = hint[1]
        else:
            text4_str = ' '
            text5_str = ' '
        text4 = self.font.render(text4_str, 1, BLACK)
        width4, height4 = self.font.size(text4_str)
        display.blit(text4, (self.x + 5, self.y + height1 + height3 + 25))
        pygame.draw.rect(display, GREY, (self.x, self.y + height1 + height3 + 20, width4 + 10, height4 + 10), 1)
        text5 = self.font.render(text5_str, 1, BLACK)
        width5, height5 = self.font.size(text5_str)
        display.blit(text5, (self.x + 5, self.y + height1 + height3 + height4 + 35))
        pygame.draw.rect(display, GREY, (self.x, self.y + height1 + height3 + height4 + 30, width5 + 10, height5 + 10), 1)
