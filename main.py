from modules.interface import *
from modules.functions import *
from modules.database import *
from modules.elements import *

window = Window()
geometry = Geometry()
finit_elements = FinitElements()
cursor = window.field.get_cursor()

current_line = None
current_id_lines = []
current_area = {}

hint = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            cursor.move(x, y)
            # print(cursor.get_coords())
            geometry_object = geometry.highlight_object(cursor.get_coords())
            window.field.draw(window.screen)
            window.show_hint.draw(window.screen, cursor, geometry_object, hint)
            # Добавить информацию об объекте

        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed_tab = find_pressed_button(window.menu.tabs)
            if check_buttons(event.pos, window.menu.tabs):
                for tab in window.menu.tabs:
                    tab.press(event.pos)

            elif check_buttons(event.pos, pressed_tab.buttons):
                for button in pressed_tab.buttons:
                    button.press(event.pos)
            pressed_button = find_pressed_button(pressed_tab.buttons)
            button_point = window.menu.tabs[0].buttons[0]
            button_line = window.menu.tabs[0].buttons[1]
            button_area = window.menu.tabs[0].buttons[2]
            button_mesh_line = window.menu.tabs[1].buttons[0]
            button_choose_material = window.menu.tabs[1].buttons[2]
            button_temperature = window.menu.tabs[2].buttons[0]
            button_set_temperature = window.menu.tabs[2].buttons[1]
            # create point
            if pressed_button == button_point:
                coords = cursor.get_coords()
                geometry.add_point(coords)
            # create line
            if pressed_button == button_line:
                coords = cursor.get_coords()
                x, y = coords
                if x is not None and y is not None:
                    if check_point(coords, geometry):
                        if not current_line:
                            current_line = [find_point(coords, geometry)]
                            hint = ["Для завершения линии отметьте еще одну точку",
                                    f"Начало линии в точке c координатами {str(current_line[0])}"]
                        else:
                            current_line.append(find_point(coords, geometry))
                            coords1, coords2 = current_line
                            coords1, coords2 = current_line
                            x1, y1 = coords1
                            x2, y2 = coords2
                            id1 = DATABASE.get_id_point(x1, y1)
                            id2 = DATABASE.get_id_point(x2, y2)
                            geometry.add_line(id1, id2)
                            current_line = None
                            hint = None
            # create area
            if pressed_button == button_area:
                coords = cursor.get_coords()
                x, y = coords
                if x is not None and y is not None:
                    if check_line(coords, geometry):
                        line = find_line(coords, geometry)
                        current_id_lines.append(line.id)
                        id_points = DATABASE.get_id_points_from_line(line.id)
                        hint = [f"Для завершения площади отметьте еще несколько линий до замкнутого контура.",
                                f" Отмеченные линии: {', '.join(map(str, current_id_lines))}"]
                        for id_point in id_points:
                            if id_point not in current_area:
                                current_area[id_point] = False
                            else:
                                current_area[id_point] = True
                        if all(current_area.values()):
                            geometry.add_area(current_id_lines)
                            current_area = {}
                            current_id_lines = []
                            hint = None

            if pressed_button == button_mesh_line:
                coords = cursor.get_coords()
                x, y = coords
                if x is not None and y is not None:
                    if check_line(coords, geometry):
                        line = find_line(coords, geometry)
                        line.set_color(GREEN)
                        print('Введите количество элементов')
                        count_of_elements = int(input())
                        # dialog_window = DialogWindow()
                        # count_of_nodes = dialog_window.get_value()
                        coords_of_elements = mesh_line(line, count_of_elements)
                        list_of_nodes = []
                        list_of_finit_lines = []
                        for coords in coords_of_elements:
                            x, y = coords
                            finit_elements.add_node(coords)
                            list_of_nodes.append(finit_elements.get_node(coords))
                        
                        for i in range(len(list_of_nodes) - 1):
                            DATABASE.add_finit_line_into_db(list_of_nodes[i].id, list_of_nodes[i + 1].id)
                            finitline = FinitLine([list_of_nodes[i], list_of_nodes[i + 1]])
                            list_of_finit_lines.append(finitline)

                        line.set_finit_lines(list_of_finit_lines)
                        if line.material_id:
                            for finit_line in list_of_finit_lines:
                                id_finit_line = DATABASE.get_id_finit_line(finit_line.node1.id, finit_line.node2.id)
                                DATABASE.set_material_of_finit_line(id_finit_line, line.material_id)

            if pressed_button == button_choose_material:
                coords = cursor.get_coords()
                x, y = coords
                if x is not None and y is not None:
                    if check_line(coords, geometry):
                        line = find_line(coords, geometry)
                        print('Введите id материала')
                        material_id = int(input())
                        line.set_material(material_id)

            if pressed_button == button_set_temperature:
                coords = cursor.get_coords()
                x, y = coords
                if x is not None and y is not None:
                    if check_node(coords, finit_elements):
                        node = find_node(coords, finit_elements)
                        print('Введите температуру')
                        temperature = float(input())
                        DATABASE.set_temperature(node.id, temperature)

            if pressed_button == button_temperature:
                print('Введите коэффициент теплоотдачи с поверхности в окружающую среду')
                heat_transfer = float(input())
                print('Введите температуру окружающейй среды')
                environment_t = float(input())
                print('Введите мощность внутренних тепловых источников')
                heat_source_power = float(input())
                mke(geometry.get_geometry_objects()['lines'], heat_transfer, environment_t, heat_source_power)

            window.menu.draw(window.screen)
            window.field.set_geometry_objects(geometry.get_geometry_objects())
            window.field.set_finit_elements(finit_elements.get_finit_elements())
            window.field.draw(window.screen)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_line = None
                current_area = None

    geometry.get_geometry_objects()
    pygame.display.flip()


# geometry.clear_database()
DATABASE.close()
pygame.quit()

