import numpy as np
from modules.database import *

def rewrite_matrix(change_matrix, matrix, degree):
    for i in range(degree):
        for j in range(degree):
            change_matrix[i][j] = matrix[i][j]


class TemperatureMatrix:
    def __init__(self, degree):
        self.degree = degree

        self.matrix = np.zeros(pow(self.degree, 2)).reshape(self.degree, self.degree)
        self.free_member_matrix = np.zeros(self.degree)
        self.determinant = None

    def fill(self, line_id, heat_transfer, environment_t, heat_source_power, way):
        if way == 1:
            list_of_id_elements = DATABASE.get_list_of_id_finit_lines(line_id)
        elif way == 2:
            list_of_id_elements = DATABASE.get_list_of_id_finit_lines(line_id)[::-1]
        known_temperature = DATABASE.get_known_temperature(line_id)
        for i in range(self.degree):
            if i == 0:
                self.matrix[i][i] = 1

                self.free_member_matrix[i] = known_temperature

            elif i == self.degree - 1:
                element_id = list_of_id_elements[i - 1]
                transcalency = DATABASE.get_transcalency_of_finit_line(element_id)
                h = DATABASE.get_h_of_finit_line(element_id)
                self.matrix[i][i - 1] = -transcalency / h
                self.matrix[i][i] = (transcalency / h) + heat_transfer

                self.free_member_matrix[i] = heat_transfer * environment_t

            else:
                element_id1 = list_of_id_elements[i - 1]
                element_id2 = list_of_id_elements[i]
                transcalency1 = DATABASE.get_transcalency_of_finit_line(element_id1)
                transcalency2 = DATABASE.get_transcalency_of_finit_line(element_id2)
                h1 = DATABASE.get_h_of_finit_line(element_id1)
                h2 = DATABASE.get_h_of_finit_line(element_id2)
                self.matrix[i][i - 1] = -transcalency1 / h1
                self.matrix[i][i] = transcalency1 / h1 + transcalency2 / h2
                self.matrix[i][i + 1] = -transcalency2 / h2

                self.free_member_matrix[i] = heat_source_power * (h1 + h2) / 2

        self.determinant = np.linalg.det(self.matrix)


    def find_unknown(self):
        temperatures = []
        changeable_matrix = np.zeros(pow(self.degree, 2)).reshape(self.degree, self.degree)
        rewrite_matrix(changeable_matrix, self.matrix, self.degree)
        for i in range(self.degree):
            for j in range(self.degree):
                changeable_matrix[j][i] = self.free_member_matrix[j]
            temperatures.append(np.linalg.det(changeable_matrix) / self.determinant)
            rewrite_matrix(changeable_matrix, self.matrix, self.degree)
        return(temperatures)

    def print(self):
        string = []
        for i in range(self.degree):
            for j in range(self.degree):
                string.append(self.matrix[i][j])
            print('   '.join(map(str, string)))
            string = []

        print(self.free_member_matrix)
