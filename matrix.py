class MatrixError(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message)

class Matrix:
    def __init__(self, values, *args, **kwargs):
        self.__values = values

        # Check the matrix is valid
        lengths = set([len(row) for row in self.__values])
        if len(lengths) > 1:
            raise MatrixError("{} contains rows of differing lengths".format(
                repr(self)))

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if not (type(self[i][j]) == int or type(self[i][j]) == float):
                    raise TypeError("values should be ints or floats not {}".format(
                        type(self[i][j])))

    def __repr__(self, *args, **kwargs):
        return "<{}.{} object at {}>".format(
            self.__class__.__module__, self.__class__.__name__, hex(id(self)))

    def __str__(self, *args, **kwargs):
        # Find the maximum width of the values to rjust by
        widths = []
        for row in self.__values:
            for item in row:
                widths.append(len(str(item)))
        width = max(widths)

        # Format the string representation of the matrix
        output = "Matrix([[{}]])".format(str("]\n"+" "*8+"[").join([" ".join(
            [str(item).rjust(width, " ") for item in row])
            for row in self.__values]))
        return output

    @property
    def latex(self, *args, **kwargs):
        # Format the latex representation of the matrix
        output = "\\begin{bmatrix}\n"
        for row in self.__values:
            output += "\t{} \\\\\n".format(
                " & ".join([str(item) for item in row]))
        output += "\\end{bmatrix}"
        return output

    def __get__(self, *args, **kwargs):
        return self.__values

    def __getitem__(self, key):
        return self.__values[key]

    def __set__(self, values):
        self.__values = values

    def __setitem__(self, key, value):
        self.__values[key] = value

    def row(self, i):
        return self.__values[i]

    def column(self, i):
        return [row[i] for row in self.__values]

    def __add__(self, other):
        if type(other) == Matrix:
            if self.shape == other.shape:
                values = [[self[i][j] + other[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
            else:
                raise MatrixError("cannot add {} and {} with different orders of {}x{} and {}x{}".format(
                    repr(other), repr(self), *other.shape, *self.shape))
        elif type(other) == int or type(other) == float:
            values = [[self[i][j] + other for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot add {} to {}".format(
                other.__class__.__name__, self.__class__.__name__))
        return Matrix(values)

    def __radd__(self, other):
        try:
            return self.__add__(other)
        except TypeError:
            raise TypeError("cannot add {} to {}".format(
                self.__class__.__name__, other.__class__.__name__))

    def __iadd__(self, other):
        self = self.__add__(other)
        return self

    def __sub__(self, other):
        if type(other) == Matrix:
            if self.shape == other.shape:
                values = [[self[i][j] - other[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
            else:
                raise MatrixError("cannot subtract {} from {} with different orders of {}x{} and {}x{}".format(
                    repr(other), repr(self), *other.shape, *self.shape))
        elif type(other) == int or type(other) == float:
            values = [[self[i][j] - other for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot subtract {} from {}".format(
                other.__class__.__name__, self.__class__.__name__))
        return Matrix(values)

    def __rsub__(self, other):
        if type(other) == Matrix:
            if self.shape == other.shape:
                values = [[other[i][j] - self[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
            else:
                raise MatrixError("cannot subtract {} from {} with different orders of {}x{} and {}x{}".format(
                    repr(other), repr(self), *self.shape, *other.shape))
        elif type(other) == int or type(other) == float:
            values = [[other - self[i][j] for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot subtract {} from {}".format(
                self.__class__.__name__, other.__class__.__name__))
        return Matrix(values)

    def __isub__(self, other):
        self = self.__sub__(other)
        return self

    def __mul__(self, other):
        if type(other) == Matrix:
            if self.shape[1] == other.shape[0]:
                values = [[sum([self[i][m] * other[m][j]
                                for m in range(self.shape[1])])
                           for j in range(other.shape[1])]
                          for i in range(self.shape[0])]
            else:
                raise MatrixError("cannot multiply {} and {} with orders of {}x{} and {}x{}".format(
                    repr(self), repr(other), *self.shape, *other.shape))
        elif type(other) == int or type(other) == float:
            values = [[self[i][j] * other for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot multiply {} and {}".format(
                self.__class__.__name__, other.__class__.__name__))
        return Matrix(values)

    def __rmul__(self, other):
        if type(other) == Matrix:
            if other.shape[1] == self.shape[0]:
                values = [[sum([other[i][m] * self[m][j]
                                for m in range(other.shape[1])])
                           for j in range(self.shape[1])]
                          for i in range(other.shape[0])]
            else:
                raise MatrixError("cannot multiply {} and {} with orders of {}x{} and {}x{}".format(
                    repr(other), repr(self), *other.shape, *self.shape))
        elif type(other) == int or type(other) == float:
            values = [[self[i][j] * other for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot multiply {} and {}".format(
                other.__class__.__name__, self.__class__.__name__))
        return Matrix(values)

    def __imul__(self, other):
        self = self.__mul__(other)
        return self

    def __mod__(self, other):
        if type(other) == int or type(other) == float:
            values = [[self[i][j] % other for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise TypeError("cannot perform mod on {} with {}".format(
                self.__class__.__name__, other.__class__.__name__))
        return Matrix(values)

    def __imod__(self, other):
        self = self.__mod__(other)
        return self

    def sgn(self, x):
        # Calculate the sign of x
        if type(x) == int or type(x) == float:
            if x == 0:
                return 0
            else:
                return int(x / abs(x))
        else:
            raise TypeError("values should be ints or floats not {}".format(
                x.__class__.__name__))

    @property
    def inverse(self, *args, **kwargs):
        # Calculate inverse (M * M^-1 = I)
        if not self.is_singular():
            d = self.det
            for i in range(26):
                if (d * i) % 26 == 1:
                    break
            M = i * self.adjugate
        else:
            raise MatrixError("{} has no inverse as the determinant is 0".format(
                repr(self)))
        return M

    @property
    def inv(self, *args, **kwargs):
        return self.inverse

    @property
    def determinant(self, *args, **kwargs):
        # Calculate determinant
        if self.is_square():
            if self.shape == (1, 1):
                return self[0][0]
            elif self.shape == (2, 2):
                return self[0][0] * self[1][1] - self[0][1] * self[1][0]
            elif self.shape == (3, 3):
                return (self[0][0] * self[1][1] * self[2][2]
                        + self[0][1] * self[1][2] * self[2][0]
                        + self[0][2] * self[1][0] * self[2][1]
                        - self[0][2] * self[1][1] * self[2][0]
                        - self[0][1] * self[1][0] * self[2][2]
                        - self[0][0] * self[1][2] * self[2][1])
        else:
            raise MatrixError("{} must be square to have a determinant".format(
                repr(self)))

    @property
    def det(self, *args, **kwargs):
        return self.determinant

    def minor(self, i, j):
        # A matrix discluding the ith row and jth column
        values = []
        for n in range(self.shape[0]):
            if n != i:
                values.append([])
                for m in range(self.shape[1]):
                    if m != j:
                        values[-1].append(self[n][m])
        return Matrix(values)

    @property
    def matrix_of_minors(self, *args, **kwargs):
        # Create a matrix with the determinants of each matrix of minor
        values = []
        for i in range(self.shape[0]):
            values.append([])
            for j in range(self.shape[1]):
                values[-1].append(self.minor(i, j).det)
        return Matrix(values)

    @property
    def minors(self, *args, **kwargs):
        return self.matrix_of_minors

    @property
    def cofactor(self, *args, **kwargs):
        values = [[self[i][j] * (-1)**(i+j) for j in range(self.shape[1])]
                  for i in range(self.shape[0])]
        return Matrix(values)

    @property
    def transpose(self, *args, **kwargs):
        values = [[self[j][i] for j in range(self.shape[1])]
                  for i in range(self.shape[0])]
        return Matrix(values)

    @property
    def T(self, *args, **kwargs):
        return self.transpose

    @property
    def adjugate(self, *args, **kwargs):
        return self.minors.cofactor.T

    @property
    def identity(self, *args, **kwargs):
        if self.is_square():
            values = [[int(i == j) for j in range(self.shape[1])]
                      for i in range(self.shape[0])]
        else:
            raise MatrixError("{} must be square to have an identity matrix".format(
                repr(self)))
        return Matrix(values)

    @property
    def I(self, *args, **kwargs):
        return self.identity

    @property
    def shape(self, *args, **kwargs):
        return (len(self.__values), len(self.__values[0]))

    def is_square(self, *args, **kwargs):
        return self.shape[0] == self.shape[1]

    def is_singular(self, *args, **kwargs):
        return self.det == 0

if __name__ == "__main__":
    print("This module is intended to be imported and should not be run directly.")
