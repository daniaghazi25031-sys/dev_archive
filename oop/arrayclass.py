class matrex:
    def __init__(self, data):
        self.data = data
        self.row = len(data)
        self.col = len(data[0])

    def __str__(self):
        output = ""
        for row in self.data:
            output += "| " + " ".join(map(str, row)) + " |\n"
        return output

    def add(self, other):
        result = []
        for i in range(self.row):
            newrow = []
            for j in range(self.col):
                sumv = self.data[i][j] + other.data[i][j]
                newrow.append(sumv)
            result.append(newrow)
        return matrex(result)

    def mul(self, other):
        x = [[0 for _ in range(other.col)] for _ in range(self.row)]
        for i in range(self.row):
            for j in range(other.col):
                for k in range(self.col):
                    x[i][j] += self.data[i][k] * other.data[k][j]
        return matrex(x)

m_list = [[4, 3, 5], [33, 2, 6]]
g_list = [[4, 6], [6, 5], [1, 2]]

m = matrex(m_list)
g = matrex(g_list)


result_mul = g.mul(m)
print("Multiplication Result:")
print(result_mul)
m2 = matrex([[1, 1, 1], [1, 1, 1]])
result_add = m.add(m2)
print("Addition Result:")
print(result_add)

