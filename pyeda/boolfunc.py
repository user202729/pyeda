"""
Boolean Functions

Interface Classes:
    Variable
    Function
        Constant
            Zero
            One
    VectorFunction

Boolean Identities
+---------------------------------+--------------+
| (x')' = x                       | Involution   |
+---------------------------------+--------------+
| x + x = x                       | Idempotent   |
| x * x = x                       |              |
+---------------------------------+--------------+
| x + 0 = x                       | Identity     |
| x * 1 = x                       |              |
+---------------------------------+--------------+
| x + 1 = 1                       | Domination   |
| x * 0 = 0                       |              |
+---------------------------------+--------------+
| x + y = y + x                   | Commutative  |
| x * y = y * x                   |              |
+---------------------------------+--------------+
| x + (y + z) = (x + y) + z       | Associative  |
| x * (y * z) = (x * y) * z       |              |
+---------------------------------+--------------+
| x + (y * z) = (x + y) * (x + z) | Distributive |
| x * (y + z) = (x * y) + (x * z) |              |
+---------------------------------+--------------+
| (x + y)' = x' * y'              | De Morgan    |
| (x * y)' = x' + y'              |              |
+---------------------------------+--------------+
| x + (x * y) = x                 | Absorption   |
| x * (x + y) = x                 |              |
+---------------------------------+--------------+
| x + x' = 1                      | Complement   |
| x * x' = 0                      |              |
+---------------------------------+--------------+
"""

__copyright__ = "Copyright (c) 2012, Chris Drake"

from .common import bit_on


class Variable:
    """
    A Boolean variable is a numerical quantity that may assume any value in the
    set B = {0, 1}.

    This implementation includes an optional "index", a nonnegative integer
    that is convenient for bit vectors.
    """
    def __init__(self, name, index=None):
        self._name = name
        self._index = index

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Return the string representation.

        >>> str(Variable('a'))
        'a'
        >>> str(Variable('v', 42))
        'v[42]'
        """
        if self._index is None:
            return self._name
        else:
            return "{0._name}[{0._index}]".format(self)

    def __lt__(self, other):
        """Return rich "less than" result, for ordering.

        >>> a, b = map(Variable, 'ab')
        >>> a < b, b < a
        (True, False)

        >>> c1, c2, c10 = Variable('c', 1), Variable('c', 2), Variable('c', 10)
        >>> c1 < c2, c1 < c10, c2 < c10
        (True, True, True)
        """
        if self.name == other.name:
            return self.index < other.index
        else:
            return self.name < other.name

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index


class Function:
    """
    Abstract base class that defines an interface for a scalar Boolean function
    of N variables.
    """
    @property
    def support(self):
        """Return the support set of a function.

        Let f(x1, x2, ..., xn) be a Boolean function of N variables. The set
        {x1, x2, ..., xn} is called the *support* of the function.
        """
        raise NotImplementedError()

    @property
    def degree(self):
        """Return the degree of a function.

        A function from B^N => B is called a Boolean function of *degree* N.
        """
        return len(self.support)

    # Overloaded operators
    def __neg__(self):
        return self.op_not()

    def __add__(self, other):
        return self.op_or(other)

    def __radd__(self, other):
        return self.op_or(other)

    def __mul__(self, other):
        return self.op_and(other)

    def __rmul__(self, other):
        return self.op_and(other)

    def __rshift__(self, other):
        """Return a >> b, equivalent to a -> b."""
        return self.op_le(other)

    def __rrshift__(self, other):
        return self.op_ge(other)

    # Operators
    def op_not(self):
        """Return symbolic complement of a Boolean function.

        +---+----+
        | f | -f |
        +---+----+
        | 0 |  1 |
        | 1 |  0 |
        +---+----+

        Also known as: NOT
        """
        raise NotImplementedError()

    def op_or(self, *args):
        """Return symbolic disjunction of functions.

        +---+---+-------+
        | f | g | f + g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   1   |
        | 1 | 0 |   1   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: sum, OR
        """
        raise NotImplementedError()

    def op_nor(self, *args):
        """Return symbolic NOR (NOT AND) of functions."""
        raise NotImplementedError()

    def op_and(self, *args):
        """Return symbolic conjunction of functions.

        +---+---+-------+
        | f | g | f * g |
        +---+---+-------+
        | 0 | 0 |   0   |
        | 0 | 1 |   0   |
        | 1 | 0 |   0   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: product, AND
        """
        raise NotImplementedError()

    def op_nand(self, *args):
        """Return symbolic NAND (NOT AND) of functions."""
        raise NotImplementedError()

    def op_xor(self, *args):
        """Return symbolic XOR of functions.

        +---+---+--------+
        | f | g | f != g |
        +---+---+--------+
        | 0 | 0 |    0   |
        | 0 | 1 |    1   |
        | 1 | 0 |    1   |
        | 1 | 1 |    0   |
        +---+---+--------+

        Also known as: odd parity
        """
        raise NotImplementedError()

    def op_xnor(self, *args):
        """Return symbolic XNOR of functions.

        +---+---+-------+
        | f | g | f = g |
        +---+---+-------+
        | 0 | 0 |   1   |
        | 0 | 1 |   0   |
        | 1 | 0 |   0   |
        | 1 | 1 |   1   |
        +---+---+-------+

        Also known as: even parity
        """
        raise NotImplementedError()

    def op_le(self, *args):
        """Return symbolic "less than or equal to" of functions.

        +---+---+--------+
        | f | g | f <= g |
        +---+---+--------+
        | 0 | 0 |    1   |
        | 0 | 1 |    1   |
        | 1 | 0 |    0   |
        | 1 | 1 |    1   |
        +---+---+--------+

        Also known as: implies (f -> g)
        """
        raise NotImplementedError()

    def op_ge(self, *args):
        """Return symbolic "greater than or equal to" of functions.

        +---+---+--------+
        | f | g | f >= g |
        +---+---+--------+
        | 0 | 0 |    1   |
        | 0 | 1 |    0   |
        | 1 | 0 |    1   |
        | 1 | 1 |    1   |
        +---+---+--------+

        Also known as: reverse implies (g -> f)
        """
        raise NotImplementedError()

    def restrict(self, mapping):
        """
        Return the Boolean function that results after restricting a subset of
        its input variables to {0, 1}.

        g = f | xi=b
        """
        raise NotImplementedError()

    def vrestrict(self, mapping):
        """Expand all vectors before applying 'restrict'."""
        return self.restrict(_expand_vectors(mapping))

    def compose(self, mapping):
        """
        Return the Boolean function that results after substituting a subset of
        its input variables for other Boolean functions.

        g = f1 | xi=f2
        """
        raise NotImplementedError()

    def satisfy_one(self):
        """
        If this function is satisfiable, return a satisfying input point.
        Otherwise, return None.
        """
        raise NotImplementedError()

    def satisfy_all(self):
        """Return the list of all satisfying input points."""
        raise NotImplementedError()

    def satisfy_count(self):
        """Return the cardinality of the set of all satisfying input points."""
        raise NotImplementedError()

    def iter_cofactors(self, vs=None):
        """Iterate through the cofactors of N variables."""
        if vs is None:
            vs = list()
        for n in range(2 ** len(vs)):
            yield self.restrict({v: bit_on(n, i) for i, v in enumerate(vs)})

    def cofactors(self, vs=None):
        """Return a tuple of cofactors of N variables.

        The *cofactor* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi is f[xi] = f(x1, x2, ..., 1, ..., xn)

        The *cofactor* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi' is f[xi'] = f(x1, x2, ..., 0, ..., xn)
        """
        return tuple(cf for cf in self.iter_cofactors(vs))

    def is_neg_unate(self, vs=None):
        """Return whether a function is negative unate.

        A function f(x1, x2, ..., xi, ..., xn) is negative unate in variable
        xi if f[xi'] >= f[xi].
        """
        raise NotImplementedError()

    def is_pos_unate(self, vs=None):
        """Return whether a function is positive unate.

        A function f(x1, x2, ..., xi, ..., xn) is positive unate in variable
        xi if f[xi] >= f[xi'].
        """
        raise NotImplementedError()

    def is_binate(self, vs=None):
        """Return whether a function is binate.

        A function f(x1, x2, ..., xi, ..., xn) is binate in variable xi if it
        is neither negative nor positive unate in xi.
        """
        return not (self.is_neg_unate(vs) or self.is_pos_unate(vs))

    def smoothing(self, vs=None):
        """Return the smoothing of a function.

        The *smoothing* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi is S[xi](f) = f[xi] + f[xi']
        """
        raise NotImplementedError()

    def consensus(self, vs=None):
        """Return the consensus of a function.

        The *consensus* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi is C[xi](f) = f[xi] * f[xi']
        """
        raise NotImplementedError()

    def derivative(self, vs=None):
        """Return the derivative of a function.

        The *derivate* of f(x1, x2, ..., xi, ..., xn) with respect to
        variable xi is df/dxi = f[xi] (xor) f[xi']
        """
        raise NotImplementedError()


class VectorFunction:
    """
    Abstract base class that defines an interface for a vector Boolean function.
    """
    UNSIGNED, TWOS_COMPLEMENT = range(2)

    def __init__(self, *fs, **kwargs):
        self.fs = list(fs)
        self._start = kwargs.get("start", 0)
        self._bnr = kwargs.get("bnr", self.UNSIGNED)

    def __int__(self):
        return self.to_int()

    def __iter__(self):
        return iter(self.fs)

    def __len__(self):
        return len(self.fs)

    @property
    def start(self):
        """Return the start index."""
        return self._start

    def _get_bnr(self):
        """Get the binary number representation."""
        return self._bnr

    def _set_bnr(self, value):
        """Set the binary number representation."""
        self._bnr = value

    bnr = property(fget=_get_bnr, fset=_set_bnr)

    # Operators
    def uor(self):
        """Return the unary OR reduction."""
        raise NotImplementedError()

    def uand(self):
        """Return the unary AND reduction."""
        raise NotImplementedError()

    def uxor(self):
        """Return the unary XOR reduction."""
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __xor__(self, other):
        raise NotImplementedError()

    def restrict(self, mapping):
        """
        Return the vector that results from applying the 'restrict' method to
        all functions.
        """
        cpy = self[:]
        for i, _ in enumerate(cpy.fs):
            cpy[i] = cpy[i].restrict(mapping)
        return cpy

    def vrestrict(self, mapping):
        """Expand all vectors before applying 'restrict'."""
        return self.restrict(_expand_vectors(mapping))

    def to_uint(self):
        """Convert vector to an unsigned integer, if possible."""
        num = 0
        for i, f in enumerate(self.fs):
            if type(f) is int:
                if f:
                    num += 2 ** i
            else:
                raise ValueError("cannot convert to uint")
        return num

    def to_int(self):
        """Convert vector to an integer, if possible."""
        num = self.to_uint()
        if self._bnr == self.TWOS_COMPLEMENT and self.fs[-1]:
            return -2 ** self.__len__() + num
        else:
            return num

    def ext(self, num):
        """Extend this vector by N bits.

        If this vector uses two's complement representation, sign extend;
        otherwise, zero extend.
        """
        if self.bnr == self.TWOS_COMPLEMENT:
            bit = self.fs[-1]
        else:
            bit = 0
        for _ in range(num):
            self.append(bit)

    def getifz(self, i):
        """Get item from zero-based index."""
        return self.__getitem__(i + self.start)

    def __getitem__(self, sl):
        if isinstance(sl, int):
            return self.fs[self._norm_idx(sl)]
        else:
            cls = self.__class__
            norm_sl = self._norm_slice(sl)
            return cls(*self.fs.__getitem__(norm_sl),
                       start=(norm_sl.start + self._start), bnr=self._bnr)

    def __setitem__(self, sl, f):
        if isinstance(sl, int):
            self.fs.__setitem__(sl, f)
        else:
            norm = self._norm_slice(sl)
            self.fs.__setitem__(norm, f)

    def _norm_idx(self, i):
        """Return an index normalized to vector start index."""
        if i >= 0:
            if i < self._start:
                raise IndexError("list index out of range")
            else:
                idx = i - self._start
        else:
            idx = i + self._start
        return idx

    @property
    def _sl(self):
        """Return a slice object that represents the vector's index range."""
        return slice(self._start, len(self.fs) + self._start)

    def _norm_slice(self, sl):
        """Return a slice normalized to vector start index."""
        limits = dict()
        for k in ("start", "stop"):
            idx = getattr(sl, k)
            if idx is not None:
                limits[k] = (idx if idx >= 0 else self._sl.stop + idx)
            else:
                limits[k] = getattr(self._sl, k)
        if limits["start"] < self._sl.start or limits["stop"] > self._sl.stop:
            raise IndexError("list index out of range")
        elif limits["start"] >= limits["stop"]:
            raise IndexError("zero-sized slice")
        return slice(limits["start"] - self._start,
                     limits["stop"] - self._start)

    def append(self, f):
        """Append a function to the end of this vector."""
        self.fs.append(f)


def _expand_vectors(mapping):
    """Expand all vectors in a substitution dict."""
    temp = { k: v for k, v in mapping.items() if
             isinstance(k, VectorFunction) }
    mapping = {k: v for k, v in mapping.items() if k not in temp}
    while temp:
        key, val = temp.popitem()
        if isinstance(key, VectorFunction):
            assert len(key) == len(val)
            for i, f in enumerate(val):
                mapping[key.getifz(i)] = f
        else:
            mapping[key] = val
    return mapping
