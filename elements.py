from modules.constants import *
from modules.database import *
from modules.functions import *
import pygame


class FinitElements:
    def __init__(self):
        self.finit_elements = {'nodes': [],
                              'temperature_finit_lines': [],
                              'finit_areas': []}

    def add_node(self, coords):
        x, y = coords
        if x is not None and y is not None:
            if not exactly_check_node(coords, self):
                DATABASE.add_node_into_db(coords)
                node = Node(coords)
                self.finit_elements['nodes'].append(node)

    # def add_temperature_finit_line(self, nodes, transcalency):


    def get_node(self, coords):
        x, y = coords
        for node in self.finit_elements['nodes']:
            if x == node.x and y == node.y:
                return node

    def get_finit_elements(self):
        return self.finit_elements

    def get_nodes(self):
        return self.finit_elements['nodes']


class Node:
    def __init__(self, coords):
        self.id = DATABASE.get_id_node(coords)
        self.x, self.y = coords
        self.color = DATABASE.get_color_node(self.id)

    def draw(self, display, field):
        x = self.x + field.x
        y = -self.y + field.height + field.y
        pygame.draw.circle(display, self.color, (int(x), int(y)), 2)

    def __str__(self):
        return f"({self.x}, {self.y})"


class FinitLine:
    def __init__(self, nodes):
        node1, node2 = nodes
        self.node1, self.node2 = node1, node2
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        self.transcalency = None

    def set_material(self, material_id):
        self.transcalency = DATABASE.get_lambda(material_id)

