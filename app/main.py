from PIL import Image
import numpy as np
import random as rand
import itertools as tools


class Solver:
    def __init__(self, filename: str, number_of_verts: int):
        image = Image.open(filename)
        self.pixels = np.asarray(image)
        self.x_size = self.pixels.shape[0]
        self.y_size = self.pixels.shape[1]
        self.number_of_vertices = number_of_verts
        self.list_of_dark_points = []
        self.dark_points_count = 0
        self.number_of_took = 0
        self.list_of_picked = []
        self.lines_list = []
        self.list_of_unrepeated_lines = []
        self.edges = []

    def get_dark_points(self):

        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[x])):
                if self.pixels[x][y][0] == self.pixels[x][y][1] == self.pixels[x][y][2]:
                    self.list_of_dark_points.append((x, y))
        self.dark_points_count = len(self.list_of_dark_points)

    def selection(self):
        self.number_of_took = int(self.dark_points_count / 1000)
        for i in range(self.number_of_took):
            self.list_of_picked.append(rand.choice(self.list_of_dark_points))
        self.list_of_picked = list(set(self.list_of_picked))

    def create_lines_from_selection(self):
        for pair_of_points in tools.product(self.list_of_picked, repeat=2):
            if pair_of_points[0] == pair_of_points[1]:
                continue
            coeff_a = pair_of_points[0][1] - pair_of_points[1][1]
            coeff_b = pair_of_points[1][0] - pair_of_points[0][0]
            coeff_c = pair_of_points[0][0] * pair_of_points[1][1] - pair_of_points[0][1] * pair_of_points[1][0]
            equation = [coeff_a, coeff_b, coeff_c]
            self.lines_list.append(equation)

    def take_unrepeated_lines(self):
        while len(self.lines_list) != 0:
            equation = self.lines_list[-1]
            self.lines_list.pop()
            is_unique = True
            for other_eq in self.lines_list:
                scalar1 = equation[0] * other_eq[1] - other_eq[0] * equation[1]
                scalar2 = equation[0] * other_eq[2] - other_eq[0] * equation[2]
                scalar3 = equation[1] * other_eq[2] - other_eq[1] * equation[2]
                if abs(scalar1) < 0.02 * other_eq[0] * other_eq[1] and abs(scalar2) < 0.02 * other_eq[0] * other_eq[
                    0] and abs(
                    scalar3) < 0.02 * other_eq[1] * other_eq[2]:
                    is_unique = False
                    break
            if is_unique:
                self.list_of_unrepeated_lines.append(equation)

    def find_edges(self):
        for line in self.list_of_unrepeated_lines:
            cur_max_in_a_row = 0
            cur_x = 0
            while cur_x < self.x_size:
                cur_y = 0
                if line[1] == 0:
                    cur_y = cur_x
                else:
                    cur_y = -line[2] - cur_x * line[0]
                if [cur_x, cur_y] in self.list_of_dark_points:
                    cur_max_in_a_row += 1
                else:
                    cur_max_in_a_row = 0
                if cur_max_in_a_row == 15:
                    self.edges.append(line)
                    break

    def find_answer(self):
        set_of_points = set()
        for pair_of_edges in tools.product(self.edges, repeat=2):
            if pair_of_edges[0] == pair_of_edges[1]:
                continue
            main_det = pair_of_edges[0][0] * pair_of_edges[1][1] - pair_of_edges[1][0] * pair_of_edges[0][1]
            x_det = pair_of_edges[0][2] * pair_of_edges[1][1] - pair_of_edges[1][0] * pair_of_edges[0][2]
            y_det = pair_of_edges[0][0] * pair_of_edges[1][2] - pair_of_edges[1][2] * pair_of_edges[0][1]
            point = (int(x_det / main_det), int(y_det / main_det))
            set_of_points.add(point)
        print(f"Number of intersections is {len(set_of_points) - self.number_of_vertices}")

    def make_solve(self):
        self.get_dark_points()
        self.selection()
        self.create_lines_from_selection()
        self.take_unrepeated_lines()
        self.find_edges()
        self.find_answer()


if __name__ == "__main__":
    filename = input()
    number_of_vertices = int(input())
    solver = Solver(filename,number_of_vertices)
    solver.find_answer()