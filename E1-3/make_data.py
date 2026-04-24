import json


def make_cross(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    center = n // 2

    for i in range(n):
        matrix[center][i] = 1
        matrix[i][center] = 1

    return matrix


def make_x(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        matrix[i][i] = 1
        matrix[i][n - 1 - i] = 1

    return matrix


data = {
    "filters": {},
    "patterns": {}
}

for size in [3, 5, 13, 25]:
    cross = make_cross(size)
    x_shape = make_x(size)

    data["filters"][f"size_{size}"] = {
        "cross": cross,
        "x": x_shape
    }

    data["patterns"][f"size_{size}_1"] = {
        "input": cross,
        "expected": "+"
    }

    data["patterns"][f"size_{size}_2"] = {
        "input": x_shape,
        "expected": "x"
    }

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("data.json 생성 완료")