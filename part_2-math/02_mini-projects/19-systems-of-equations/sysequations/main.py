"""
Solving system of linear equations with NumPy
"""

import numpy as np

if __name__ == "__main__":
    # Ask the user for the number of equations
    n = int(input("Enter the number of equations: "))

    # Ask the user for the coefficients of the equations
    A = []
    C = []
    for n in range(n):
        equation = input(
            (
                f"Enter the coefficients of equation {n + 1} "
                "separated by a space (a1x1 + a2x2 + a3x3 + ... + anxn = b): "
            )
        )
        coefficients = list(map(int, equation.split()))
        A.append(coefficients[:-1])
        C.append(coefficients[-1])

    # Convert the lists to NumPy arrays
    A = np.array(A)
    C = np.array(C)

    solutions = np.linalg.solve(A, C)
    print(f"The solutions are: {solutions}")
    print("=" * 50)
    for i, row in enumerate(A):
        for j, elem in enumerate(row):
            print(f"{elem}x{j + 1}", end=" + " if j < len(row) - 1 else "")
        print(f" = {C[i]}")
    for i in range(len(solutions)):
        print(f"x{i + 1} = {solutions[i]}")
    print("=" * 50)

