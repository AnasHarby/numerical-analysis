"""Root Finding Methods:
A collection of methods to find roots of equations.
"""
import numpy
from part1_output import Output
import matplotlib.pyplot
import timeit
from equations_util import *
from math import log2, ceil


def regula_falsi(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 2:
        raise ValueError("Error! Invalid number of arguments")
    xl, xu = min(arguments[0], arguments[1]), max(arguments[0], arguments[1])
    f = expr_to_lambda(expr)
    if f(xl) * f(xu) > 0:
        raise ValueError(
            "Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Regula-Falsi", f, expr_to_lambda(diff(expr)))
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xl)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
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
        cur_xi = numpy.append(cur_xi, xr)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        yl = f(xl)
        yu = f(xu)
        x_next = (xl * yu - xu * yl) / (yu - yl)
        output.error_bound = abs(x_next - prev_xr)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, xr)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def bisection(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 2:
        raise ValueError("Error! Invalid number of arguments")
    xl, xu = min(arguments[0], arguments[1]), max(arguments[0], arguments[1])
    f = expr_to_lambda(expr)
    if f(xl) * f(xu) > 0:
        raise ValueError(
            "Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Bisection", f, lambda x: x / 2)
    output.error_bound = ceil(abs(log2(abs(xu - xl)) - log2(max_err)))
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xl)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
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
        cur_xi = numpy.append(cur_xi, xr)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, xr)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def newton(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 1:
        raise ValueError("Error! Invalid number of arguments")
    xi = arguments[0]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson", f, f_diff)
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xi)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        cur_xi = numpy.append(cur_xi, root)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        x_next = xi - fxi / fxi_diff
        output.error_bound = abs(x_next - xi)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, root)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def newton_mod1(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 2:
        raise ValueError("Error! Invalid number of arguments")
    xi, m = arguments[0], arguments[1]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson Mod#1", f, f_diff)
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xi)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - m * fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        cur_xi = numpy.append(cur_xi, root)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        x_next = xi - m * fxi / fxi_diff
        output.error_bound = abs(x_next - xi)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, root)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def newton_mod2(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 1:
        raise ValueError("Error! Invalid number of arguments")
    xi = arguments[0]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    f_diff2 = expr_to_lambda(diff(expr_diff))
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson Mod#2", f, f_diff)
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xi)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        f_diff_xi2 = f_diff2(xi)
        root = xi - f_diff_xi * fxi / (f_diff_xi ** 2 - fxi * f_diff_xi2)
        err = abs((root - xi))
        xi = root
        cur_xi = numpy.append(cur_xi, root)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        f_diff_xi2 = f_diff2(xi)
        x_next = xi - f_diff_xi * fxi / (f_diff_xi ** 2 - fxi * f_diff_xi2)
        output.error_bound = abs(x_next - xi)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, root)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def secant(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 2:
        raise ValueError("Error! Invalid number of arguments")
    xi, xi_prev = arguments[0], arguments[1]
    f = expr_to_lambda(expr)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Secant", f, expr_to_lambda(diff(expr)))
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xi)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_prev = f(xi_prev)
        root = xi - fxi * (xi_prev - xi) / (fxi_prev - fxi)
        err = abs((root - xi))
        xi_prev = xi
        xi = root
        cur_xi = numpy.append(cur_xi, root)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        fxi = f(xi)
        fxi_prev = f(xi_prev)
        x_next = xi - fxi * (xi_prev - xi) / (fxi_prev - fxi)
        output.error_bound = abs(x_next - xi)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, root)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def fixed_point(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 1:
        raise ValueError("Error! Invalid number of arguments")
    xi = arguments[0]
    f = expr_to_lambda(expr)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Fixed-Point", f, lambda x: x - f(x))
    cur_xi = numpy.empty(0, dtype=numpy.float64)
    cur_err_i = numpy.empty(0, dtype=numpy.float64)
    cur_xi = numpy.append(cur_xi, xi)
    cur_err_i = numpy.append(cur_err_i, float('NaN'))
    begin = timeit.default_timer()
    for i in range(0, max_iter):
        root = xi - f(xi)
        err = abs((root - xi))
        xi = root
        cur_xi = numpy.append(cur_xi, root)
        cur_err_i = numpy.append(cur_err_i, err)
        if err <= max_err:
            break
    end = timeit.default_timer()
    try:
        x_next = xi - f(xi)
        output.error_bound = abs(x_next - xi)
    except (ZeroDivisionError, OverflowError):
        output.error_bound = 0
    output.execution_time = abs(end - begin)
    output.roots = numpy.append(output.roots, root)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe(
        cur_xi, output.function, cur_err_i, symbol))
    return output


def birge_vieta(expr, arguments, max_err=1e-5, max_iter=50):
    if len(arguments) != 1:
        raise ValueError("Error! Invalid number of arguments")
    xi = arguments[0]
    output = Output()
    symbol = get_symbol(expr)
    _init_output(output, "Birge-Vieta", expr_to_lambda(expr),
                 expr_to_lambda(diff(expr)))
    poly = sympy.Poly(expr, expr.free_symbols)
    a = poly.all_coeffs()
    m = len(a) - 1
    n = m + 1
    i = 1
    begin = timeit.default_timer()
    while m > 0:
        cur_xi = numpy.empty(0, dtype=numpy.float64)
        cur_err_i = numpy.empty(0, dtype=numpy.float64)
        cur_xi = numpy.append(cur_xi, xi)
        cur_err_i = numpy.append(cur_err_i, float('NaN'))
        b = numpy.zeros(m + 1, dtype=numpy.float64)
        c = numpy.zeros(m + 1, dtype=numpy.float64)
        err = 0
        for _ in range(0, max_iter):
            find_coeffs(a, b, c, xi)
            root = xi - b[m] / c[m - 1]
            err = abs((root - xi))
            xi = root
            cur_xi = numpy.append(cur_xi, xi)
            cur_err_i = numpy.append(cur_err_i, err)
            if err <= max_err:
                break
        a = b[0: -1]
        m = len(a) - 1
        output.dataframes.append(create_dataframe(
            cur_xi, output.function, cur_err_i, symbol, i))
        i += 1
        output.roots = numpy.append(output.roots, xi)
        output.errors = numpy.append(output.errors, err)
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    return output


def illinois(expr, arguments, max_err=1e-5, max_iter=50):
    delta = 0.1
    if len(arguments) == 3:
        delta = arguments[2]
    elif len(arguments) != 2:
        raise ValueError("Error! Invalid number of arguments")
    start, end = arguments[0], arguments[1]
    i = 0
    f = expr_to_lambda(expr)

    symbol = get_symbol(expr)
    counter = 0
    output = Output()
    _init_output(output, "Illinois", f, expr_to_lambda(diff(expr)))
    begin_time = timeit.default_timer()

    while start + i * delta < end:
        xl, xu = start + i * delta, start + (i + 1) * delta
        f_xl, f_xu = f(xl), f(xu)
        if f_xl * f_xu > 0:
            i += 1
            continue

        prev_xi = err = 0
        cur_xi = cur_err_i = numpy.empty(0, dtype=numpy.float64)
        cur_xi = numpy.append(cur_xi, xl)
        cur_err_i = numpy.append(cur_err_i, float('NaN'))
        for _ in range(0, max_iter):
            if f_xl == 0:
                cur_xi = numpy.append(cur_xi, xl)
                cur_err_i = numpy.append(cur_err_i, 0.0)
                break
            elif f_xu == 0:
                cur_xi = numpy.append(cur_xi, xu)
                cur_err_i = numpy.append(cur_err_i, 0.0)
                i += 1
                break
            step = f_xl * (xl - xu) / (f_xu - f_xl)
            xi = xl + step
            f_xi = f(xi)
            err = abs(xi - prev_xi)
            if f_xi * f_xu < 0:
                xl, f_xl = xu, f_xu
            else:
                f_xl /= 2
            xu, f_xu = xi, f_xi
            prev_xi = xi
            cur_xi = numpy.append(cur_xi, xi)
            cur_err_i = numpy.append(cur_err_i, err)
            if err <= max_err:
                break

        output.dataframes.append(create_dataframe(
            cur_xi, output.function, cur_err_i, symbol, counter))
        i += 1
        output.roots = numpy.append(output.roots, prev_xi)
        output.errors = numpy.append(output.errors, err)
        counter += 1

    end_time = timeit.default_timer()
    output.execution_time = abs(end_time - begin_time)
    return output


def _init_output(output: Output, method_name: str, f, f_bound):
    output.roots = []
    output.errors = []
    output.title = method_name
    output.function = f
    output.boundary_function = f_bound


def find_coeffs(a, b, c, xi):
    m = len(a) - 1
    c[0] = b[0] = a[0]
    for i in range(1, m + 1):
        b[i] = a[i] + xi * b[i - 1]
        c[i] = b[i] + xi * c[i - 1]


if __name__ == '__main__':
    # print("""Please Select A Method:
    # 1) Newton-Raphson Method
    # 2) Secant Method
    # 3) Bisection Method
    # 4) Regula-Falsi Method
    # 5) Modified Newton(With Known Multiplicity)
    # 6) Modified Newton(With Unknown Multiplicity)""")
    out = birge_vieta(sympy.sympify(
        "x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3])
    print(out.title + ":", out.execution_time)
    for df in out.dataframes:
        print(df)
    # out = newton(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    # out = newton_mod1(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3, 2])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    # out = newton_mod2(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    # out = secant(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3, -5])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    # out = bisection(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3, -5])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    # out = regula_falsi(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), [-3, -5])
    # print(out.title + ":", out.execution_time)
    # for df in out.dataframes:
    #     print(df)
    out = illinois(sympy.sympify("(x - 0) * ( x - 1) * (x - 2) * ( x - 3) * (x - 4) * (x - 5) * (x - 6) * (x - 7) * ("
                                 "x - 8) * (x - 9)"), [-1.0001, 10])
    print(out.title + ":", out.execution_time)
    for df in out.dataframes:
        print(df)
        # print(birge_vieta(sympy.sympify("x ** 4 - 9 * x ** 3 - 2 * x ** 2 + 120 * x - 130"), -3))
        # eqn = input("Please Enter The Equation: ")  # Test Code (Just Enter x^2 - 4)
        # var = input("Please Enter The Name of The Variable: ")#Test Code (Use x as a symbol)
        # symbol = sympy.symbols(var)
        # expr = sympy.sympify(eqn)
        # free_symbols = expr.free_symbols
        # if len(free_symbols) != 1:
        #    raise ValueError("The Expression Contains More Than One Variable")
        # symbol = free_symbols.pop()
        # expr_diff = sympy.diff(expr, symbol)
        # expr_diff2 = sympy.diff(expr_diff, symbol)
        # f = sympy.utilities.lambdify(symbol, expr)
        # g = sympy.utilities.lambdify(symbol, expr_diff)
        # h = sympy.utilities.lambdify(symbol, expr_diff2)
        # f = lambda x: x ** 3 - 2 * x ** 2 - 4 * x + 8
        # g = lambda x: 3 * x ** 2 - 4 * x - 4
        # h = lambda x: 6 * x - 4
