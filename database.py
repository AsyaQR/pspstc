import sqlite3
from modules.constants import *


class DateBase:
    def __init__(self):
        # self.db = sqlite3.connect("C:/Users/Specter/YandexDisk/[Work]/[Projects]/УИРы/МКЭ/Project/main/data/data.db")
        self.db = sqlite3.connect("data/data.db")

    # Point
    def add_point_into_db(self, x, y):
        query = f"INSERT INTO points(x, y) VALUES ({x}, {y})"
        self.db.execute(query)
        self.db.commit()

    def get_id_point(self, x, y):
        query = f"SELECT id FROM points WHERE x={x} AND y={y}"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_coords_point(self, id):
        query = f"SELECT x, y FROM points WHERE id={id}"
        x, y = self.db.execute(query).fetchone()
        return x, y

    def get_color_point(self, id):
        query = f"SELECT color FROM points WHERE id={id}"
        color = self.db.execute(query).fetchone()[0]
        return str_to_color(color)

    def set_color_point(self, color):
        color = color_to_str(color)
        query = f"INSERT INTO points(color) VALUES('{color}')"
        self.db.execute(query)
        self.db.commit()


    def get_point(self, id):
        query = f"SELECT x, y, color FROM points WHERE id={id}"
        x, y, color = self.db.execute(query).fetchone()
        return x, y, color

    # Line
    def add_line_into_db(self, point_id1, point_id2):
        point1 = min([point_id1, point_id2])
        point2 = max([point_id1, point_id2])
        id_points = ';'.join(map(str, [point1, point2]))
        query = f"INSERT INTO lines(id_points) VALUES('{id_points}')"
        self.db.execute(query)
        self.db.commit()

    def get_id_line(self, point_id1, point_id2):
        point1 = min([point_id1, point_id2])
        point2 = max([point_id1, point_id2])
        id_points = ';'.join(map(str, [point1, point2]))
        query = f"SELECT id FROM lines WHERE id_points='{id_points}'"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_id_points_from_line(self, id):
        query = f"SELECT id_points FROM lines WHERE id={id}"
        id_points = map(int, self.db.execute(query).fetchone()[0].split(';'))
        return list(id_points)

    def get_coords_line(self, id):
        result = []
        query = f"SELECT id_points FROM lines WHERE id={id}"
        id_points = map(int, self.db.execute(query).fetchone()[0].split(';'))
        for id_point in id_points:
            coords = self.get_coords_point(id_point)
            result.append(coords)
        return result

    def get_color_line(self, id):
        query = f"SELECT color FROM lines WHERE id={id}"
        color = self.db.execute(query).fetchone()[0]
        return str_to_color(color)

    def set_color_line(self, color):
        color = color_to_str(color)
        query = f"INSERT INTO lines(color) VALUES('{color}')"
        self.db.execute(query)
        self.db.commit()

    def set_finit_lines(self, id, list_of_id_finit_lines):
        id_finit_lines = ';'.join(map(str, list_of_id_finit_lines))
        query = f"UPDATE lines SET id_finit_lines='{id_finit_lines}' WHERE id={id}"
        self.db.execute(query)
        self.db.commit()

    def get_list_of_id_finit_lines(self, id):
        query = f"SELECT id_finit_lines FROM lines WHERE id={id}"
        if self.db.execute(query).fetchone()[0]:
            id_finit_lines = map(int, self.db.execute(query).fetchone()[0].split(';'))
            return list(id_finit_lines)

    def get_id_nodes_of_line(self, id):
        id_of_nodes = []
        finit_lines = self.get_list_of_id_finit_lines(id)
        for i in range(len(finit_lines)):
            if i == 0:
                id_of_nodes.append(DATABASE.get_id_nodes_of_finit_line(finit_lines[i])[0])
                id_of_nodes.append(DATABASE.get_id_nodes_of_finit_line(finit_lines[i])[1])
            else:
                id_of_nodes.append(DATABASE.get_id_nodes_of_finit_line(finit_lines[i])[1])
        return list(id_of_nodes)

    def get_known_temperature(self, id):
        for node_id in self.get_id_nodes_of_line(id):
            if self.get_temperature(node_id) != 0:
                return self.get_temperature(node_id)

    def get_temperature_of_line(self, id):
        result = []
        for node in self.get_id_nodes_of_line(id):
            result.append(self.get_temperature(node))
        return result

    # Area
    def add_area_into_db(self, lines_id):
        lines_id = sorted(lines_id)
        id_lines = ';'.join(map(str, lines_id))
        query = f"INSERT INTO areas(id_lines) VALUES('{id_lines}')"
        self.db.execute(query)
        self.db.commit()

    def get_id_area(self, lines_id):
        lines_id = sorted(lines_id)
        id_lines = ';'.join(map(str, lines_id))
        query = f"SELECT id FROM areas WHERE id_lines='{id_lines}'"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_list_of_coords(self, id):
        query = f"SELECT id_lines FROM areas WHERE id={id}"
        id_lines = map(int, self.db.execute(query).fetchone()[0].split(';'))

        list_of_coords_of_area = []
        for id_line in id_lines:
            list_of_coords_of_line = self.get_coords_line(id_line)
            for coords_of_line in list_of_coords_of_line:
                if coords_of_line not in list_of_coords_of_area:
                    list_of_coords_of_area.append(coords_of_line)
        return list_of_coords_of_area

    def get_color_area(self, id):
        query = f"SELECT color FROM areas WHERE id={id}"
        color = self.db.execute(query).fetchone()[0]
        return str_to_color(color)

    # Node
    def add_node_into_db(self, coords):
        x, y = coords
        query = f"INSERT INTO nodes(x, y) VALUES({x}, {y})"
        self.db.execute(query)
        self.db.commit()

    def get_id_node(self, coords):
        x, y = coords
        query = f"SELECT id FROM nodes WHERE x={x} AND y={y}"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_coords_node(self, id):
        query = f"SELECT x, y FROM nodes WHERE id={id}"
        x, y = self.db.execute(query).fetchone()
        return x, y

    def get_color_node(self, id):
        query = f"SELECT color FROM nodes WHERE id={id}"
        color = self.db.execute(query).fetchone()[0]
        return str_to_color(color)

    def set_temperature(self, id, temperature):
        query = f"UPDATE nodes SET temperature={temperature} WHERE id={id}"
        self.db.execute(query)
        self.db.commit()

    def get_temperature(self, id):
        query = f"SELECT temperature FROM nodes WHERE id={id}"
        temperature = self.db.execute(query).fetchone()[0]
        return temperature

    def get_all_temperatures(self, lines):
        temperatures = []
        for line in lines:
            if self.get_list_of_id_finit_lines(line.id) is not None:
                for node_id in self.get_id_nodes_of_line(line.id):
                    temperatures.append(self.get_temperature(node_id))
        return temperatures

    # Materials
    def add_material_into_db(self, material):
        query = f"INSERT INTO materials(material) VALUES('{material}')"
        self.db.execute(query)
        self.db.commit()

    def set_transcalensy(self, id, transcalensy):
        query = f"UPDATE materials SET lambda={transcalensy} WHERE id={id}"
        self.db.execute(query)
        self.db.commit()

    def get_id_material(self, material):
        query = f"SELECT id FROM materials WHERE material='{material}'"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_name_material(self, id):
        query = f"SELECT material FROM materials WHERE id={id}"
        name = self.db.execute(query).fetchone()[0]
        return name

    def get_lambda(self, id):
        query = f"SELECT lambda FROM materials WHERE id={id}"
        transcalensy = self.db.execute(query).fetchone()[0]
        return transcalensy

    def get_list_of_materials(self):
        query = f"SELECT material FROM materials"
        materials = self.db.execute(query).fetchone()[0]

    # Finit lines
    def add_finit_line_into_db(self, node_id1, node_id2):
        id_nodes = ';'.join(map(str, [node_id1, node_id2]))
        query1 = f"INSERT INTO finit_lines(id_nodes) VALUES('{id_nodes}')"
        self.db.execute(query1)
        self.db.commit()
        x1, y1 = self.get_coords_node(node_id1)
        x2, y2 = self.get_coords_node(node_id2)
        h = (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) / 100
        id = self.get_id_finit_line(node_id1, node_id2)
        query2 = f"UPDATE finit_lines SET h={h} WHERE id={id}"

        self.db.execute(query2)
        self.db.commit()

    def set_material_of_finit_line(self, id, material_id):
        query = f"UPDATE finit_lines SET id_material={material_id} WHERE id={id}"
        self.db.execute(query)
        self.db.commit()

    def get_id_finit_line(self, node_id1, node_id2):
        id_nodes = ';'.join(map(str, [node_id1, node_id2]))
        query = f"SELECT id FROM finit_lines WHERE id_nodes='{id_nodes}'"
        id = self.db.execute(query).fetchone()[0]
        return id

    def get_transcalency_of_finit_line(self, id_finit_line):
        query = f"SELECT id_material FROM finit_lines WHERE id='{id_finit_line}'"
        material = self.db.execute(query).fetchone()[0]
        transcalensy = self.get_lambda(material)
        return transcalensy

    def get_h_of_finit_line(self, id):
        query = f"SELECT h FROM finit_lines WHERE id='{id}'"
        h = self.db.execute(query).fetchone()[0]
        return h

    def get_id_nodes_of_finit_line(self, id):
        query = f"SELECT id_nodes FROM finit_lines WHERE id={id}"
        if self.db.execute(query).fetchone()[0]:
            id_nodes = map(int, self.db.execute(query).fetchone()[0].split(';'))
            return list(id_nodes)

    # Work database
    def clear(self):
        query = f"DELETE from points"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='points'"
        self.db.execute(query)
        self.db.commit()

        query = f"DELETE from lines"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='lines'"
        self.db.execute(query)
        self.db.commit()

        query = f"DELETE from areas"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='areas'"
        self.db.execute(query)
        self.db.commit()

        query = f"DELETE from nodes"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='nodes'"
        self.db.execute(query)
        self.db.commit()

        query = f"DELETE from finit_lines"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='finit_lines'"
        self.db.execute(query)
        self.db.commit()

        '''
        query = f"DELETE from materials"
        self.db.execute(query)
        query = f"DELETE from sqlite_sequence WHERE name='materials'"
        self.db.execute(query)
        self.db.commit()
        '''



    def close(self):
        self.db.close()


DATABASE = DateBase()
# DATABASE.clear()
