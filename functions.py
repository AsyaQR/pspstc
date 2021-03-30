from modules.database import *
from modules.matrix import *
from modules.constants import*


def split_line(lenght, *args):
    """
    Если аргумент один, то разбивается на равные по длине части
    Если аргументов несколько, то разбиение
    return tuple
    Example
    ---------------
    >>> split_line(10, 5)
    return (2.0, 4.0, 6.0, 8.0, 10.0)

    >>> split_line(10, 4)
    return (2.5, 5.0, 7.5, 10.0)

    >>> split_line(10, 4, 8, 2, 6)
    return (2.0, 6.0, 7.0, 10.0)

    >>> split_line(4, 8, 15, 16, 23, 42)
    return (0.3076923076923077, 0.8846153846153846, 1.5, 2.3846153846153846, 4.0)
    ---------------
    """

    if len(args) == 1:
        count_of_segment = args[0]
        lenght_of_segment = lenght / count_of_segment
        segments = [lenght_of_segment * i for i in range(1, count_of_segment + 1)]
    else:
        count_of_segment = len(args)
        lenght_of_segments = [lenght * args[i] / sum(args) for i in range(count_of_segment)]
        segments = [sum(lenght_of_segments[:i]) for i in range(1, count_of_segment + 1)]
    return tuple(segments)


def check_buttons(coords, buttons):
    x_pos, y_pos = coords
    for button in buttons:
        if button.x <= x_pos <= button.x + button.width:
            if button.y <= y_pos <= button.y + button.height:
                return True
            else:
                return False


def find_pressed_button(buttons):
    for button in buttons:
        if button.state == 'pressed':
            return button


def check_point(coords, geometry):
    x_pos, y_pos = coords
    for point in geometry.get_geometry_objects()['points']:
        x, y = point.x, point.y
        if x - 5 <= x_pos <= x + 5:
            if y - 5 <= y_pos <= y + 5:
                return True


def find_point(coords, geometry):
    x_pos, y_pos = coords
    for point in geometry.get_geometry_objects()['points']:
        x, y = point.x, point.y
        if x - 5 <= x_pos <= x + 5:
            if y - 5 <= y_pos <= y + 5:
                coords = point.x, point.y
                return coords


def check_node(coords, finit_elements):
    x_pos, y_pos = coords
    for node in finit_elements.get_finit_elements()['nodes']:
        x, y = node.x, node.y
        if x - 5 < x_pos < x + 5:
            if y - 5 < y_pos < y + 5:
                return True


def exactly_check_node(coords, finit_elements):
    x_pos, y_pos = coords
    for node in finit_elements.get_finit_elements()['nodes']:
        x, y = node.x, node.y
        if x == x_pos:
            if y == y_pos:
                return True


def find_node(coords, finit_elements):
    x_pos, y_pos = coords
    for node in finit_elements.get_finit_elements()['nodes']:
        x, y = node.x, node.y
        if x - 5 <= x_pos <= x + 5:
            if y - 5 <= y_pos <= y + 5:
                coords = node.x, node.y
                return node


def check_line(coords, geometry):
    x, y = coords
    result = False
    for line in geometry.get_geometry_objects()['lines']:
        x1, y1 = line.coords_start_point
        x2, y2 = line.coords_finish_point
        displacement = 5
        if x2 - x1 == 0:
            if ( x2 + displacement >= x >= x2 - displacement and
                 max(y1, y2) >= y >= min(y1, y2)):
                result = True
        elif y2 - y1 == 0:
            if ( y2 + displacement >= y >= y2 - displacement and
                 max(x1, x2) >= x >= min(x1, x2)):
                result = True
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
            if ( y <= x * k + b + displacement and
                 y >= x * k + b - displacement and
                 y <= x * k_orto + b_max and
                 y >= x * k_orto + b_min):
                result = True
    return result


def find_line(coords, geometry):
    x, y = coords
    result = None
    for line in geometry.get_geometry_objects()['lines']:
        x1, y1 = line.coords_start_point
        x2, y2 = line.coords_finish_point
        displacement = 5
        if x2 - x1 == 0:
            if ( x2 + displacement >= x >= x2 - displacement and
                 max(y1, y2) >= y >= min(y1, y2)):
                result = line
        elif y2 - y1 == 0:
            if ( y2 + displacement >= y >= y2 - displacement and
                 max(x1, x2) >= x >= min(x1, x2)):
                result = line
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
            if ( y <= x * k + b + displacement and
                 y >= x * k + b - displacement and
                 y <= x * k_orto + b_max and
                 y >= x * k_orto + b_min):
                result = line
    return result


def mesh_line(line, count_of_elements):
    x1, y1 = line.coords_start_point
    x2, y2 = line.coords_finish_point
    line_lenght = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    lenghts_of_elements = split_line(line_lenght, count_of_elements)
    coords_of_elements = None
    x_min = min(x1, x2)
    x_max = max(x1, x2)
    if x_min == x1:
        y_x_min = y1
        y_x_max = y2
    else:
        y_x_min = y2
        y_x_max = y1
    for i in range(len(lenghts_of_elements) + 1):
        if not coords_of_elements:
            coords_of_elements = []
            coords_of_elements.append((x1, y1))
        elif i == len(lenghts_of_elements):
            coords_of_elements.append((x2, y2))
        else:
            lenght = lenghts_of_elements[i - 1]
            x = x_min + lenght * ((x_max - x_min) / line_lenght)
            cos = (x_max - x_min) / line_lenght
            y = None
            
            if y_x_min <= y_x_max:
                y = y_x_min + lenght * (1 - cos ** 2) ** 0.5
            else:
                y = y_x_min - lenght * (1 - cos ** 2) ** 0.5
            '''
            if x1 >= x2 and y1 >= y2:
                y = max(y1, y2) - lenght * (1 - cos ** 2) ** 0.5
            elif x1 >= x2 and y1 <= y2:
                y = min(y1, y2) + lenght * (1 - cos ** 2) ** 0.5
            elif x1 <= x2 and y1 >= y2:
                y = max(y1, y2) - lenght * (1 - cos ** 2) ** 0.5
            else:
                y = min(y1, y2) + lenght * (1 - cos ** 2) ** 0.5
            '''
            coords_of_elements.append((x, y))
    return coords_of_elements

'''
x1, y1    x2, y2
y1 = kx1 + d => d = y1 - kx1 => d = y1 - x1(y2 - y1)/(x2 - x1)
y2 = kx2 + d => y2 = k(x2 - x1) + y1 => k = (y2 - y1)/(x2 - x1)
'''
def fill_polygon(screen, color, *points):
    points = [point for point in points]
    pygame.draw.polygon(screen, color, points)


def check_temperature(line):
    result = False
    for node in DATABASE.get_id_nodes_of_line(line.id):
        if DATABASE.get_temperature(node) != 0:
            result = True
            break
    return result


def find_index_temperature_node(line):
    for node_id in DATABASE.get_id_nodes_of_line(line.id):
        if DATABASE.get_temperature(node_id) != 0:
            return DATABASE.get_id_nodes_of_line(line.id).index(node_id)


def check_temperature_line(list_of_lines, done_lines):
    result = False
    for line in list_of_lines:
        if line not in done_lines:
            if check_temperature(line):
                result = True
                break
    return result


def find_temperature_line(list_of_lines, done_lines):
    for line in list_of_lines:
        if line not in done_lines:
            if check_temperature(line):
                return line


def temperature_mke_for_changed_line(line, heat_transfer, environment_t, heat_source_power):
    print('начали')
    results = []
    list_of_transcalency = []
    for id_finit_line in DATABASE.get_list_of_id_finit_lines(line.id):
        transcalency = DATABASE.get_transcalency_of_finit_line(id_finit_line)
        list_of_transcalency.append(transcalency)
    list_of_transcalency = list_of_transcalency[::-1]
    matrix = TemperatureMatrix(len(list_of_transcalency) + 1)
    matrix.fill(line.id, heat_transfer, environment_t, heat_source_power, 2)
    if matrix.determinant != 0:
        results = matrix.find_unknown()[::-1]
    for i in range(len(DATABASE.get_id_nodes_of_line(line.id))):
        DATABASE.set_temperature(DATABASE.get_id_nodes_of_line(line.id)[i], results[i])
    print('----------')
    print(results)
    print('----------')


def mke(list_of_lines, heat_transfer, environment_t, heat_source_power):
    done_lines = []
    while check_temperature_line(list_of_lines, done_lines):
        line = find_temperature_line(list_of_lines, done_lines)
        if find_index_temperature_node(line) == 0:
            line.temperature_mke(heat_transfer, environment_t, heat_source_power)
            done_lines.append(line)
        if find_index_temperature_node(line) == len(DATABASE.get_id_nodes_of_line(line.id)) - 1:
            temperature_mke_for_changed_line(line, heat_transfer, environment_t, heat_source_power)
            done_lines.append(line)
