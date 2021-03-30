import pygame
from modules.constants import *
from modules.database import *
from modules.matrix import *
from modules.functions import *


def check_point(coords, coords_of_points):
    x, y = coords
    result = False
    for coord_of_point in coords_of_points:
        if coord_of_point[0] - 5 <= x <= coord_of_point[0] + 5:
            if coord_of_point[1] - 5 <= y <= coord_of_point[1] + 5:
                result = True
    return result


def check_line_to_add_into_db(point_id1, point_id2, geometry):
    result = True
    point1 = min([point_id1, point_id2])
    point2 = max([point_id1, point_id2])
    for line in geometry.geometry_objects['lines']:
        points_from_line = DATABASE.get_id_points_from_line(line.id)
        if points_from_line[0] == point1 and points_from_line[1] == point2:
            result = False
    return result


class Geometry:
    def __init__(self):
        self.geometry_objects = {'points': [],
                                 'lines': [],
                                 'areas': []}

    def add_point(self, coords):
        # добавляем точку в словарь, если это возможно*
        x, y = coords
        coords_of_points = []
        for point in self.geometry_objects['points']:
            coords_of_points.append((point.x, point.y))
        if x is not None or y is not None:
            if not check_point(coords, coords_of_points):
                DATABASE.add_point_into_db(x, y)
                id = DATABASE.get_id_point(x, y)
                self.geometry_objects['points'].append(Point(id))

    def add_line(self, point_id1, point_id2):
        x1, y1 = DATABASE.get_coords_point(point_id1)
        x2, y2 = DATABASE.get_coords_point(point_id2)
        if x1 != x2 or y1 != y2:
            if check_line_to_add_into_db(point_id1, point_id2, self):
                DATABASE.add_line_into_db(point_id1, point_id2)
                id = DATABASE.get_id_line(point_id1, point_id2)
                self.geometry_objects['lines'].append(Line(id))

    def add_area(self, list_of_lines_id):
        DATABASE.add_area_into_db(list_of_lines_id)
        id = DATABASE.get_id_area(list_of_lines_id)
        self.geometry_objects['areas'].append(Area(id))

    def highlight_object(self, event_pos):
        x_cursor, y_cursor = event_pos
        if x_cursor is not None or y_cursor is not None:
            for list_of_geometry_objects in self.geometry_objects.values():
                for geometry_object in list_of_geometry_objects:

                    if isinstance(geometry_object, Point):
                        x_go, y_go = geometry_object.get_coords()
                        if x_go - 5 <= x_cursor <= x_go + 5 and y_go - 5 <= y_cursor <= y_go + 5:
                            geometry_object.set_color(ORANGE)
                            return geometry_object
                        else:
                            geometry_object.set_color(BLACK)

                    if isinstance(geometry_object, Line):
                        x_go, y_go = geometry_object.get_coords()
                        x1, y1 = x_go
                        x2, y2 = y_go
                        displacement = 5
                        if x2 - x1 == 0:
                            if ( x2 + displacement >= x_cursor >= x2 - displacement and 
                                 max(y1, y2) >= y_cursor >= min(y1, y2) ):
                                geometry_object.set_color(ORANGE)
                                return geometry_object
                            else:
                                geometry_object.set_color(BLACK)
                        elif y2 - y1 == 0:
                            if ( y2 + displacement >= y_cursor >= y2 - displacement and 
                                 max(x1, x2) >= x_cursor >= min(x1, x2) ):
                                geometry_object.set_color(ORANGE)
                                return geometry_object
                            else:
                                geometry_object.set_color(BLACK)
                        else:
                            k = (y2 - y1) / (x2 - x1)
                            b = y1 - x1 * k
                            displacement *= (k ** 2 + 1) ** 0.5
                            k_orto = -1 / k
                            if y1 == max(y1, y2):
                                y_up, x_up = y1, x1
                                y_down, x_down = y2, x2
                            else:
                                y_up, x_up = y2, x2
                                y_down, x_down = y1, x1
                            b_max = y_up - x_up * k_orto
                            b_min = y_down - x_down * k_orto
                            if ( y_cursor <= x_cursor * k + b + displacement and
                                 y_cursor >= x_cursor * k + b - displacement and
                                 y_cursor <= x_cursor * k_orto + b_max and
                                 y_cursor >= x_cursor * k_orto + b_min):
                                geometry_object.set_color(ORANGE)
                                return geometry_object
                            else:
                                geometry_object.set_color(BLACK)
                    else:
                        geometry_object.set_initial_color()
        return None

    def get_geometry_objects(self):
        return self.geometry_objects


class Point:
    def __init__(self, id):
        self.id = id
        self.x, self.y = DATABASE.get_coords_point(id)
        self.color = DATABASE.get_color_point(id)

    def draw(self, display, field):
        x = self.x + field.x
        y = -self.y + field.height + field.y
        pygame.draw.circle(display, self.color, (x, y), 2)

    def set_color(self, color):
        self.color  = color

    def set_initial_color(self):
        self.color = DATABASE.get_color_point(self.id)

    def get_color(self):
        return self.color

    def get_coords(self):
        return self.x, self.y

    def __str__(self):
        return f"Точка {self.id}"


class Line:
    def __init__(self, id):
        self.id = id
        self.coords_start_point = DATABASE.get_coords_line(id)[0]
        self.coords_finish_point = DATABASE.get_coords_line(id)[1]
        self.color = DATABASE.get_color_line(id)
        self.material_id = None
        self.list_of_nodes = []

    def draw(self, display, field):
        x1, y1 = self.coords_start_point
        x1 = x1 + field.x
        y1 = -y1 + field.height + field.y
        x2, y2 = self.coords_finish_point
        x2 = x2 + field.x
        y2 = -y2 + field.height + field.y
        pygame.draw.line(display, self.color, (x1, y1), (x2, y2), 1)

    def set_finit_lines(self, list_of_finit_lines):
        list_of_id_finit_lines = []
        for finit_line in list_of_finit_lines:
            id_finit_line = DATABASE.get_id_finit_line(finit_line.node1.id, finit_line.node2.id)
            list_of_id_finit_lines.append(id_finit_line)

        DATABASE.set_finit_lines(self.id, list_of_id_finit_lines)

    def set_material(self, material_id):
        list_of_id_finit_lines = DATABASE.get_list_of_id_finit_lines(self.id)
        if list_of_id_finit_lines:
            for id_finit_line in list_of_id_finit_lines:
                DATABASE.set_material_of_finit_line(id_finit_line, material_id)

    def set_color(self, color):
        self.color = color

    def set_initial_color(self):
        self.color = DATABASE.get_color_line(self.id)

    def get_coords(self):
        return self.coords_start_point, self.coords_finish_point

    def __str__(self):
        return f"Линия {self.id}"

    def add_nodes(self, list_of_nodes):
        for node in list_of_nodes:
            self.list_of_nodes.append(node)

    def temperature_mke(self, heat_transfer, environment_t, heat_source_power):
        print('начали')
        results = []
        list_of_transcalency = []
        for id_finit_line in DATABASE.get_list_of_id_finit_lines(self.id):
            transcalency = DATABASE.get_transcalency_of_finit_line(id_finit_line)
            list_of_transcalency.append(transcalency)
        matrix = TemperatureMatrix(len(list_of_transcalency) + 1)
        matrix.fill(self.id, heat_transfer, environment_t, heat_source_power, 1)
        print(matrix.determinant)
        if matrix.determinant != 0:
            results = matrix.find_unknown()    
        for i in range(len(DATABASE.get_id_nodes_of_line(self.id))):
            DATABASE.set_temperature(DATABASE.get_id_nodes_of_line(self.id)[i], results[i])
        print('----------')
        print(results)
        print('----------')

    def draw_temperature_mke(self, display, field):
        list_of_coords_chart = []
        list_of_coords_local = []
        run = True
        if DATABASE.get_list_of_id_finit_lines(self.id) is None:
            run = False
        else:
            for node_id in DATABASE.get_id_nodes_of_line(self.id):
                if DATABASE.get_temperature(node_id) == 0:
                    run = False
                    break
        if run:
            x1, y1 = self.coords_start_point
            x2, y2 = self.coords_finish_point
            lenght = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            x_pos1 = min(x1, x2)
            x_pos2 = max(x1, x2)
            if x_pos1 == x1:
                y_pos1 = y1
                y_pos2 = y2
            else:
                y_pos1 = y2
                y_pos2 = y1
            sinus_of_line_slope = abs(y1 - y2) / lenght
            cosinus_of_line_slope = (1 - sinus_of_line_slope ** 2) ** 0.5

            for node_id in DATABASE.get_id_nodes_of_line(self.id):
                temperature_draw = DATABASE.get_temperature(node_id) / 10
                x_1, y_1 = DATABASE.get_coords_node(node_id)
                x_1 = x_1 + field.x
                y_1 = -y_1 + field.height + field.y
                if y_pos1 < y_pos2:
                    x_2 = x_1 - temperature_draw * sinus_of_line_slope
                else:
                    x_2 = x_1 + temperature_draw * sinus_of_line_slope
                y_2 = y_1 - temperature_draw * cosinus_of_line_slope
                pygame.draw.line(display, BLACK, (x_1, y_1), (x_2, y_2))
                list_of_coords_chart.append((x_2, y_2))
                list_of_coords_local.append((x_1, y_1))
            '''
            for i in range(len(list_of_coords_chart) - 1):
                x_start, y_start = list_of_coords_chart[i]
                x_finish, y_finish = list_of_coords_chart[i + 1]
                pygame.draw.line(display, BLACK, (x_start, y_start), (x_finish, y_finish))
            '''
            # Color
            temperature_to_color = {}
            temperatures = DATABASE.get_all_temperatures(field.geometry_objects['lines'])
            max_temperature = max(temperatures)
            min_temperature = min(temperatures)
            step = (max_temperature - min_temperature) / 14
            for i in range(14):
                temperature_to_color[step * i + min_temperature] = LIST_OF_COLORS[i]

            number = 0
            for finit_line in DATABASE.get_list_of_id_finit_lines(self.id):
                color = WHITE
                node1, node2 = DATABASE.get_id_nodes_of_finit_line(finit_line)
                temperature = (DATABASE.get_temperature(node1) + DATABASE.get_temperature(node2)) / 2
                for i in range(13):
                    temperatures_in_dict = list(temperature_to_color.keys())
                    if temperatures_in_dict[i] <= temperature <= temperatures_in_dict[i + 1]:
                        color = temperature_to_color[temperatures_in_dict[i]]
                        break
                coords1 = list_of_coords_local[number]
                coords2 = list_of_coords_local[number + 1]
                coords3 = list_of_coords_chart[number + 1]
                coords4 = list_of_coords_chart[number]
                fill_polygon(display, color, coords1, coords2, coords3, coords4)
                number += 1

                for i in range(len(list_of_coords_chart) - 1):
                    x_start, y_start = list_of_coords_chart[i]
                    x_finish, y_finish = list_of_coords_chart[i + 1]
                    pygame.draw.line(display, BLACK, (x_start, y_start), (x_finish, y_finish))

                for i in range(len(list_of_coords_chart)):
                    x_start, y_start = list_of_coords_chart[i]
                    x_finish, y_finish = list_of_coords_local[i]
                    pygame.draw.line(display, BLACK, (x_start, y_start), (x_finish, y_finish))

