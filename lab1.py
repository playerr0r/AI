# Путь коня. 
# На шахматной доске NxN, несколько клеток из которой вырезано, заданы две клетки. Построить минимальный путь коня из одной клетки в другую. 

# https://scask.ru/m_book_ii.php?id=21

# Размер доски
N = 8
# Координаты клеток, вырезанных из доски
ex = [[4, 1], [6, 7], [2, 1], [1, 0], [6, 4], [0, 3], [5, 4], [4, 5], [0, 4], [6, 6], [4, 6], [3, 4], [4, 0], [7, 4], [7, 5], [2, 3], [1, 6], [3, 7], [4, 2], [5, 6], [5, 3], [5, 1], [1, 5], [7, 0], [0, 5], [1, 4], [5, 0], [5, 2], [6, 1], [4, 3], [7, 4]]

# Координаты начальной и конечной клеток
sx, sy = 0, 0
fx, fy = 5, 5

# Проверка, находится ли клетка в списке вырезанных
def isExcluded(x, y):
    for i in ex:
        if i[0] == x and i[1] == y:
            return True
    return False

# Проверка, находится ли клетка в пределах доски
def isOnBoard(x, y):
    return x >= 0 and x < N and y >= 0 and y < N

# Проверка, можно ли попасть в клетку
def isAccessible(x, y):
    return isOnBoard(x, y) and not isExcluded(x, y)

# Проверка, является ли клетка конечной
def isFinal(x, y):
    return x == fx and y == fy


#TODO: глубину нужно ограничивать

# поиск пути с ограничением помощью поиска в глубину
def findPathDepthLimited():
    print("Depth Limited")
    # Список клеток, доступных для хода
    queue = [[sx, sy]]
    # Список клеток, по которым уже ходили
    visited = []
    # Список клеток, из которых можно попасть в текущую
    parents = [[None, None] for i in range(N * N)]
    # Пока есть доступные клетки
    while len(queue) > 0:
        # Берем первую клетку из очереди
        x, y = queue.pop(0)
        # Если клетка является конечной, то возвращаем путь
        if isFinal(x, y):
            path = []
            while x != sx or y != sy:
                path.append([x, y])
                x, y = parents[y * N + x]
            path.append([sx, sy])
            path.reverse()
            return path
        # Добавляем клетку в список посещенных
        visited.append([x, y])
        # Для каждого возможного хода
        for dx, dy in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]:
            # Если клетка доступна и не посещена
            if isAccessible(x + dx, y + dy) and [x + dx, y + dy] not in visited:
                # Добавляем клетку в список доступных
                queue.append([x + dx, y + dy])
                # Запоминаем, откуда можно попасть в эту клетку
                parents[(y + dy) * N + (x + dx)] = [x, y]
        # print(visited)
    return None


# поиск пути с помощью оптимального алгоритма перебора А*
def findPathAStar():
    print("A*")
    # Список клеток, доступных для хода
    queue = [[sx, sy]]
    # Список клеток, по которым уже ходили
    visited = []
    # Список клеток, из которых можно попасть в текущую
    parents = [[None, None] for i in range(N * N)]
    # Список расстояний от начальной клетки до текущей
    g = [0 for i in range(N * N)]
    # Список расстояний от текущей клетки до конечной
    h = [0 for i in range(N * N)]
    # Список суммарных расстояний от начальной до конечной через текущую клетку
    f = [0 for i in range(N * N)]
    # Пока есть доступные клетки
    while len(queue) > 0:
        # Берем первую клетку из очереди
        x, y = queue.pop(0)
        # Если клетка является конечной, то возвращаем путь
        if isFinal(x, y):
            path = []
            while x != sx or y != sy:
                path.append([x, y])
                x, y = parents[y * N + x]
            path.append([sx, sy])
            path.reverse()
            return path
        # Добавляем клетку в список посещенных
        visited.append([x, y])
        # Для каждого возможного хода
        for dx, dy in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]:
            # Если клетка доступна и не посещена
            if isAccessible(x + dx, y + dy) and [x + dx, y + dy] not in visited:
                # Добавляем клетку в список доступных
                queue.append([x + dx, y + dy])
                # Запоминаем клетку, из которой можно попасть в текущую
                parents[(y + dy) * N + x + dx] = [x, y]
                # Запоминаем расстояние от начальной клетки до текущей
                g[y * N + x] = g[y * N + x] + 1
                # Запоминаем расстояние от текущей клетки до конечной
                h[y * N + x] = abs(fx - x) + abs(fy - y)
                # Запоминаем суммарное расстояние от начальной до конечной через текущую клетку
                f[y * N + x] = g[y * N + x] + h[y * N + x]
        # Сортируем список доступных клеток по расстоянию от начальной до конечной
        queue.sort(key=lambda i: f[i[1] * N + i[0]])
        # print(visited)
    return None


# поиск пути с помощью поиска в ширину
def findPathBFS():
    print("Breadth-first search")
    # Список клеток, доступных для хода
    queue = [[sx, sy]]
    # Список клеток, по которым уже ходили
    visited = []
    # Список клеток, из которых можно попасть в текущую
    parents = [[None, None] for i in range(N * N)]
    # Пока есть доступные клетки
    while len(queue) > 0:
        # Берем первую клетку из очереди
        x, y = queue.pop(0)
        # Если клетка является конечной, то возвращаем путь
        if isFinal(x, y):
            path = []
            while x != sx or y != sy:
                path.append([x, y])
                x, y = parents[y * N + x]
            path.append([sx, sy])
            path.reverse()
            return path
        # Добавляем клетку в список посещенных
        visited.append([x, y])
        # Для каждого возможного хода
        for dx, dy in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]:
            # Если клетка доступна и не посещена
            if isAccessible(x + dx, y + dy) and [x + dx, y + dy] not in visited:
                # Добавляем клетку в список доступных
                queue.append([x + dx, y + dy])
                # Запоминаем клетку, из которой можно попасть в текущую
                parents[(y + dy) * N + x + dx] = [x, y]
        # print(visited)
    return None


# Вывод пути
def printPath(path):
    # Для каждой клетки
    for i in range(N):
        for j in range(N):
            # Если клетка вырезана
            if isExcluded(j, i):
                print('O', end=' ')
            # Если клетка доступна
            elif isAccessible(j, i):
                # Если клетка является конечной
                if isFinal(j, i):
                    print('F', end=' ')
                # Если клетка является начальной
                elif [j, i] == [sx, sy]:
                    print('S', end=' ')
                # Если клетка входит в путь
                if [j, i] in path:
                    print('X', end=' ')
                else:
                    print('.', end=' ')
        print()
    print()


printPath(path = findPathDepthLimited())
printPath(path = findPathBFS())
printPath(path = findPathAStar())