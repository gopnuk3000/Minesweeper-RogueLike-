class GoldFlag:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def used(self, x, y):
        a = []
        a.append((x, y))
        for i in range(self.width):
            for j in range(self.height):
                if x != i and y != j:
                    pass
                else:
                    a.append((i, j))
        return a
