# Solving systems of linear equations with NumPy
> small program illustrating how to solve systems of linear equations with NumPy


The program asks for the number of equations in the systems, and it expects the user to provide the corresponding coefficients.

For example, for the following system of linear equations:

$
\begin{cases}
x_3 = 3 \\
-2 x_2 - 2 x_3 = 0 \\
-x_2  - 2_4 = 6 \\
x_1 - x_2 + 2 x_2 + x_3 = 9 \\
\end{cases}
$

it expects the following input:

```bash
Enter the coefficients of equation 1 separated by a space (a1x1 + a2x2 + a3x3 + ... + anxn = b): 0 0 1 0 3
Enter the coefficients of equation 2 separated by a space (a1x1 + a2x2 + a3x3 + ... + anxn = b): 0 -2 -2 0 0
Enter the coefficients of equation 3 separated by a space (a1x1 + a2x2 + a3x3 + ... + anxn = b): 1 -1 0 -2 6
Enter the coefficients of equation 4 separated by a space (a1x1 + a2x2 + a3x3 + ... + anxn = b): 1 -1 2 1 9
```