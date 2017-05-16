import timeit

import sympy
import numpy
from part1_output import Output
from equations_util import create_dataframe_part2
import timeit

import equations_util
from part1_output import Output


def _eliminate(system: sympy.Matrix, i, j):
    """
    Performs forward eliminates on a row inside a system of linear equations.
    :param system: linear equations system.
    :param i: index of the base row.
    :param j: index of the row to be eliminated.
    :var system: a mutable matrix can be passed (reference passing)
    :return: an augmented square matrix after eliminating the row.
    """
    n = system.shape[1]
    c = system[j, i] / system[i, i]
    for k in range(0, n):
        system[j, k] -= c * system[i, k]
    return system


def _back_sub(tri_mat: sympy.Matrix, index_map=None):
    """
    Performs back substitution on an augmented upper triangular matrix.
    :param tri_mat: augmented triangular matrix.
    :return: a [n, 1] matrix containing result.
    """
    n = tri_mat.shape[0]
    x = sympy.zeros(n, 1)
    if index_map is None:
        index_map = numpy.array(range(n), dtype=numpy.int)
    for i in range(n - 1, -1, -1):
        s = 0
        for j in range(i + 1, n):
            s += tri_mat[index_map[i], j] * x[j]
        x[i] = (tri_mat[index_map[i], n] - s) / tri_mat[index_map[i], i]
    return x


def _forward_sub(a: sympy.Matrix, b:sympy.Matrix, index_map=None):
    """
    Performs forward substitution on a lower triangular matrix.
    :param a: triangular matrix, the coefficients of the variables.
    :param b: r.h.s of the equations.
    :param index_map: an array specifying the actual position of each row.
    :return: a [n, 1] matrix containing result.
    """
    n = a.shape[0]
    y = sympy.zeros(n, 1)
    if index_map is None:
        index_map = numpy.array(range(n), dtype=numpy.int)
    y[index_map[0]] = b[index_map[0]]
    for i in range(1, n):
        sum = b[index_map[i]]
        for j in range(0, i):
            sum -= a[index_map[i], j] * y[index_map[j]]
        y[index_map[i]] = sum
    return y


def _get_max_elem(system, i):
    n = system.shape[0]
    max_mag, max_ind = abs(system[i, i]), i
    for j in range(i + 1, n):
        if abs(system[j, i]) > max_mag:
            max_mag, max_ind = abs(system[j, i]), j
    return max_ind


def gauss(system: sympy.Matrix, symbol_list: list):
    """
    Performs gauss elimination with partial pivoting on a system of
    linear equations.
    :param system: system of linear equations.
    :param symbol_list: list of symbols used in the equations.
    :return: a [n, 1] matrix containing result.
    """
    output = Output()
    output.title = "Gaussian-Elimination"
    n = system.shape[0]
    begin = timeit.default_timer()
    # iterate over columns
    for i in range(0, n):
        # find maximum magnitude and index in this column
        max_ind = _get_max_elem(system, i)
        # swap current row with the row found to have the maximum element
        system.row_swap(max_ind, i)
        # forward elimination, iterate over remaining rows and eliminate
        for j in range(i + 1, n):
            _eliminate(system, i, j)
    # perform back substitution.
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    output.dataframes.append(equations_util.create_equ_sys_df(symbol_list, _back_sub(system)))
    return output


def gauss_jordan(system: sympy.Matrix, symbol_list):
    """
    Performs gauss jordan elimination with partial pivoting on a system of
    linear equations.
    :param system: system of linear equations.
    :param symbol_list: list of symbols used in the equations.
    :return: a [n, 1] matrix (vector) containing result.
    """
    system = system.as_mutable()
    n = system.shape[0]
    output = Output()
    output.title = "Gauss Jordan"
    begin = timeit.default_timer()
    # iterate over rows
    for i in range(0, n):
        # find maximum magnitude and index in this column
        max_ind = _get_max_elem(system, i)
        # swap current row with the row found to have the maximum element
        system.row_swap(max_ind, i)
        # normalize current row
        system.row_op(i, lambda u, v: u / system[i, i])
        # forward elimination, iterate over remaining rows and eliminate
        for j in range(i + 1, n):
            _eliminate(system, i, j)
        # forward elimination, iterate over previous rows and eliminate
        for j in range(i - 1, -1, -1):
            _eliminate(system, i, j)
    # return last column
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    output.dataframes.append(equations_util.create_equ_sys_df(symbol_list, sympy.Matrix(system.col(system.shape[0]))))
    return output


def _decompose(a, indexMap):
    n = a.shape[0]
    # iterating over columns
    for i in range(0, n):
        # find maximum magnitude and index in this column
        max_ind = _get_max_elem(a, i)
        indexMap[i], indexMap[max_ind] = indexMap[max_ind], indexMap[i]
        for j in range(i + 1, n):
            # store the factor in-place in matrix a
            factor = a[indexMap[j], i] / a[indexMap[i], i]
            a[indexMap[j], i] = factor
            # eliminate the current row by the calculated factor
            for k in range(i + 1, n):
                a[indexMap[j], k] -= factor * a[indexMap[i], k]
    return a, indexMap


def lu_decomp(system: sympy.Matrix, symbol_list):
    # TODO: Check for sigularity.
    system = system.as_mutable()
    output = Output()
    output.title = "LU Decomposition"
    begin = timeit.default_timer()
    n = system.shape[0]
    a = system[:, :n]
    b = system[:, n]
    indexMap = numpy.array(range(n), dtype=numpy.int)
    a, indexMap = _decompose(a, indexMap)
    y = _forward_sub(a, b, indexMap)
    output.dataframes.append(equations_util.create_equ_sys_df(symbol_list, _back_sub(a.row_join(y), indexMap)))
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    return  output


def jacobi(A: sympy.Matrix, symbols: list, b=None, max_iter=100, max_err=1e-5, x=None):
    """Jacobi Iterative Method for Solving A System of Linear Equations:
    takes a system of linear equations and returns an approximate solution
    for the system using Jacobi's approximation.

    Keyword arguments:
    A: sympy.Matrix -- The augmented matrix representing the system if b = None
    else the coefficients matrix. A is an [n, n] matrix.
    symbols: list of sympy.Symbol representing the variables' names.
    b: sympy.Matrix -- The r.h.s matrix of the system. b is an n-dimensional
    vector.
    max_iter: int -- The maximum number of iterations to perform.
    max_err: float -- The maximum allowed error.
    x: sympy.Matrix -- The initial value for the variables. x is an n-dimensional
    vector.

    return:
    1) The n-dimensional vector x containing the final approximate solution.
    2) The [n, number_of_iterations] matrix x_hist containing the values
    of x during each iteration.
    3) The numpy array err_hist containing the values of the error during each iteration.
    """
    n = len(symbols)
    output = Output()
    output.title = "Jacobi"
    if b is None:
        A, b = [A[:, :-1], A[:, -1]]
    if x is None:
        x = sympy.Matrix.zeros(n, 1)
    D = A.multiply_elementwise(sympy.Matrix.eye(n))
    x_prev = x[:, :]
    err_hist = [float('NaN')]
    x_hist = sympy.Matrix(x)
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        x = D.inv() * (b - (A - D) * x)
        x_hist = x_hist.row_join(x)
        #print("XHIST:\n", x_hist)
        diff = (x - x_prev).applyfunc(abs)
        err = numpy.amax(numpy.array(diff).astype(numpy.float64))
        err_hist.append(err)
        x_prev = x[:, :]
        if err < max_err:
            break
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    output.roots = numpy.array(x[:]).astype(numpy.float64)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe_part2(x_hist, err_hist, symbols))
    return output


def gauss_seidel(A: sympy.Matrix, symbols: list, b=None, max_iter=100, max_err=1e-5, x=None):
    """Gauss-Seidel Iterative Method for Solving A System of Linear Equations:
    takes a system of linear equations and returns an approximate solution
    for the system using Gauss-Seidel approximation.

    Keyword arguments:
    A: sympy.Matrix -- The augmented matrix representing the system if b = None
    else the coefficients matrix. A is an [n, n] matrix.
    symbols: list of sympy.Symbol representing the variables' names.
    b: sympy.Matrix -- The r.h.s matrix of the system. b is an n-dimensional
    vector.
    max_iter: int -- The maximum number of iterations to perform.
    max_err: float -- The maximum allowed error.
    x: sympy.Matrix -- The initial value for the variables. x is an n-dimensional
    vector.

    return:
    1) The n-dimensional vector x containing the final approximate solution.
    2) The [n, number_of_iterations] matrix x_hist containing the values
    of x during each iteration.
    3) The numpy array err_hist containing the values of the error during each iteration.
    """
    n = len(symbols)
    output = Output()
    output.title = "Gauss-Seidel"
    if b is None:
        A, b = [A[:, :-1], A[:, -1]]
    if x is None:
        x = sympy.Matrix.zeros(n, 1)
    x_prev = x[:, :]
    err_hist = [float('NaN')]
    x_hist = sympy.Matrix(x)
    begin = timeit.default_timer()
    for _ in range(0, max_iter):
        for i in range(0, n):
            xi_new = b[i]
            for j in range(0, n):
                if i != j:
                    xi_new -= A[i, j] * x[j]
                x[i] = xi_new / A[i, i]
        x_hist = x_hist.row_join(x)
        diff = (x - x_prev).applyfunc(abs)
        err = numpy.amax(numpy.array(diff).astype(numpy.float64))
        err_hist.append(err)
        x_prev = x[:, :]
        if err < max_err:
            break
    end = timeit.default_timer()
    output.execution_time = abs(end - begin)
    output.roots = numpy.array(x[:]).astype(numpy.float64)
    output.errors = numpy.append(output.errors, err)
    output.dataframes.append(create_dataframe_part2(x_hist, err_hist, symbols))
    return output
