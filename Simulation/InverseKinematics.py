import math

def solve_inverse_kinematics(constants:list[float], coordinates:list[float], iterations:float, learning_rate:float):
    """
    TODO docstring
    """
    L1 = constants[0]
    L2 = constants[1]

    a = coordinates[0]
    b = coordinates[1]
    theta1 = 0
    theta2 = 0

    a_error = 0
    b_error = 0

    error = 0
    previous_error = 0
    error_derivative = 0


    for i in range(iterations):
        a_error = a - (L1 * math.cos(theta1) + L2 * math.cos(theta2))
        b_error = b - (L1 * math.sin(theta1) + L2 * math.sin(theta2))

        error = (a_error + b_error)/2

        error_derivative = error - previous_error
        previous_error = error


        theta1 = theta1 - learning_rate * error_derivative
        theta2 = theta2 - learning_rate * error_derivative

        print(f"--Iteration {i}-- Error:{error}, theta1: {theta1}, theta2: {theta2}")



if __name__ == "__main__":
    #stuff
    solve_inverse_kinematics([2, 2], [2,3], 200, 0.01)