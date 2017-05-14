"""Root Finding Methods:
A collection of methods to find roots of equations.
"""
import sympy
from equations_util import *
import numpy

def regula_falsi(f, xl, xu, max_err=1e-5, max_iter=100):
    if f(xl) * f(xu) > 0:
        raise ValueError("Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        yl = f(xl)
        yu = f(xu)
        xr = (xl * yu - xu * yl) / (yu - yl)
        yr = f(xr)
        err = abs(xr - prev_xr)
        if yr * yu < 0:
            xl = xr
        elif yr * yl < 0:
            xu = xr
        else:
            err = 0
        prev_xr = xr
        output = output.col_join(sympy.Matrix([[xr, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def bisection(f, xl, xu, max_err=1e-5, max_iter=100):
    if f(xl) * f(xu) > 0:
        raise ValueError("Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        yl = f(xl)
        yu = f(xu)
        xr = (xl + xu) / 2
        yr = f(xr)
        err = abs(xr - prev_xr)
        if yr * yu < 0:
            xl = xr
        elif yr * yl < 0:
            xu = xr
        else:
            err = 0
        prev_xr = xr
        output = output.col_join(sympy.Matrix([[xr, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def newton(f, f_diff, xi, max_err=1e-5, max_iter=100):
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        output = output.col_join(sympy.Matrix([[root, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def newton_mod1(f, f_diff, xi, m, max_err=1e-5, max_iter=100):
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - m * fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        output = output.col_join(sympy.Matrix([[root, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def newton_mod2(f, f_diff, f_diff2, xi, max_err=1e-5, max_iter=100):
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        f_diff_xi2 = f_diff2(xi)
        root = xi - f_diff_xi * fxi / (f_diff_xi ** 2 - fxi * f_diff_xi2)
        err = abs((root - xi))
        xi = root
        output = output.col_join(sympy.Matrix([[root, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def secant(f, xi, xi_prev, max_err=1e-5, max_iter=100):
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        fxi = f(xi)
        fxi_prev = f(xi_prev)
        root = xi - fxi * (xi_prev - xi) / (fxi_prev - fxi)
        err = abs((root - xi))
        xi_prev = xi
        xi = root
        output = output.col_join(sympy.Matrix([[root, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)

def fixed_point(f, xi, max_err=1e-5, max_iter=100):
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(1, max_iter):
        root = xi - f(xi)
        err = abs((root - xi))
        xi = root
        output = output.col_join(sympy.Matrix([[root, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)

if __name__ == '__main__':
    # print("""Please Select A Method:
    # 1) Newton-Raphson Method
    # 2) Secant Method
    # 3) Bisection Method
    # 4) Regula-Falsi Method
    # 5) Modified Newton(With Known Multiplicity)
    # 6) Modified Newton(With Unknown Multiplicity)""")
    eqn = input("Please Enter The Equation: ")  # Test Code (Just Enter x^2 - 4)
    # var = input("Please Enter The Name of The Variable: ")#Test Code (Use x as a symbol)
    # symbol = sympy.symbols(var)
    expr = sympy.sympify(eqn)
    free_symbols = expr.free_symbols
    if len(free_symbols) != 1:
        raise ValueError("The Expression Contains More Than One Variable")
    symbol = free_symbols.pop()
    expr_diff = sympy.diff(expr, symbol)
    expr_diff2 = sympy.diff(expr_diff, symbol)
    f = sympy.utilities.lambdify(symbol, expr)
    g = sympy.utilities.lambdify(symbol, expr_diff)
    h = sympy.utilities.lambdify(symbol, expr_diff2)
    # f = lambda x: x ** 3 - 2 * x ** 2 - 4 * x + 8
    # g = lambda x: 3 * x ** 2 - 4 * x - 4
    # h = lambda x: 6 * x - 4
    #output = regula_falsi(f, 1.5, 2.2, 1e-5, 100)
    #print_table("Regula-Falsi", output[:, 0], f, output[:, 1], symbol)
    #output = bisection(f, 1.5, 2.2, 1e-5, 100)
    #print_table("Bisection", output[:, 0], f, output[:, 1], symbol)
    output = newton(f, g, 2.2)
    print_table("Newton-Raphson", output[:, 0], f, output[:, 1], symbol)
    #output = fixed_point(f, 0.1)
    #print_table("Fixed Point", output[:, 0], f, output[:, 1], symbol)
    output = secant(f, 1.5, 2.2)
    print_table("Secant", output[:, 0], f, output[:, 1], symbol)
    output = newton_mod1(f, g, 2.2, 2)
    print_table("Newton-Raphson Mod#1", output[:, 0], f, output[:, 1], symbol)
    output = newton_mod2(f, g, h, 2.2)
    print_table("Newton-Raphson Mod#2", output[:, 0], f, output[:, 1], symbol)
