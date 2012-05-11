
import numpy
from bugs import bugs_db


class Identify(object):

    """
    Scene generator.

    **Example:**

    .. code-block:: python

       gen = Identify(bugnames = "tetrist/tetrisl/tetrisj", seed = 932, w = 10, h = 10)
       # gen.nout = 1
       # gen.nclasses = [3]
       for ((x, y), bug), target in gen:
           # target = [0] -> tetrist
           # target = [1] -> tetrisl
           # target = [2] -> tetrisj
           # 0 <= x < w, 0 <= y < h, bug is a Bug object
           # the bug's name corresponds to the target
           ...

    Each scene contains one bug chosen from the list of ``bugnames``.
    ``bugnames`` must be a list of bug names separated by "/", and the
    bugs described by these names must be found in
    ``bugland.bugs_db``.  The bug's location is picked randomly in the
    scene.

    The target is a vector containing one integer representing the id
    of the bug in the scene. The id is the position of the bug's name
    in the slash-separated bugnames.

    ``w`` and ``h`` are the width and the height of the scene,
    respectively.
    """
    def __init__(self, bugnames, seed, w, h):

        self.bugnames = map(str.upper, bugnames.split('/'))
        self.bugs = map(bugs_db.__getitem__, bugnames)

        self.out_format = 'array'
        self.out_dtype = 'uint8'
        self.nout = 1
        self.nclasses = [len(bugs)]

        self.w = w
        self.h = h

    def __iter__(self):
        bugs = self.bugs
        R = numpy.random.RandomState(self.seed)
        ri = R.random_integers
        while True:
            index = ri(0, len(bugs) - 1)
            bug = bugs[index]
            yield [[(ri(0, self.w - bug.w),
                     ri(0, self.h - bug.h)), bug]], numpy.array([index], dtype = self.out_dtype)


class TwoGroups(object):
    """
    Scene generator.

    **Example:**

    .. code-block:: python

       gen = TwoGroups(bugnames = "tetrist/tetrisl/tetrisj", seed = 666, w = 10, h = 10,
                       n1 = 1, n2 = 2, rot = False, task = 1)
       # task = 1 means that:
       #  gen.nout = 1
       #  gen.nclasses = [3]
       for scene, target in gen:
           # target = [0] -> tetrist
           # target = [1] -> tetrisl
           # target = [2] -> tetrisj
           # scene_n = (x_n, y_n), bug_n
           # 0 <= x_n < w, 0 <= y_n < h, bug_n is a Bug object
           # first n1 bugs correspond to the target
           # others correspond to one of the two other possible bugs
           # NOTE: This is for **task 1**. targets work differently for tasks 2 and 3
           ...

    **Defaults:** ``n1 = 1, n2 = 2, rot = False, task = 1``

    Each scene contains ``n1`` bugs of one type and ``n2`` bugs from
    another type, both chosen randomly from a list of bugs defined by
    ``bugnames``. ``bugnames`` must be a list of bug names separated
    by "/", and the bugs described by these names must be found in
    ``bugland.bugs_db``. ``n1`` must be different from ``n2``. If
    ``rot`` is True, the bugs may be randomly rotated.
    If ``scale`` is True, the bugs can be randomly scaled.
    The target depends on the value of the task parameter:

    ``task = 1`` -> The target is a vector containing one integer
    representing the id of the bug of which there are ``n1`` of in the
    scene. The id is the position of the bug's name in the
    slash-separated bugnames. *This is the default*.

    ``task = 2`` -> Same as task 1, but the id is the one of the bug
    of which there are ``n2`` of.

    ``task = 3`` -> The target is a vector containing two integers,
    respectively the id of the shape there are ``n1`` occurrences of
    and the id of the shape there are ``n2`` occurrences of.

    The object's ``nout`` field contains the length of the target
    vector and the object's ``nclasses`` field contains a vector of
    length ``nout`` where each element is the number of possible bugs.

    The ``seed`` controls the random number generation, so different
    seeds lead to different scenes.

    ``w`` and ``h`` are the width and the height of the scene,
    respectively.
    """

    def __init__(self, bugnames, seed, w, h, n1 = 1, n2 = 2, rot = False, scale = False, task = 1):
        if n1 == n2:
            raise ValueError('n1 must be different from n2', n1, n2)

        self.bugnames = map(str.upper, bugnames.split('/'))
        bugs = map(bugs_db.__getitem__, self.bugnames)
        if len(bugs) < 2:
            raise ValueError("There must be at least two possible bugs.")
        self.bugs = [bug.margin(1) for bug in bugs]

        self.seed = seed
        self.n1 = n1
        self.n2 = n2
        self.rot = rot
        self.scale = scale
        self.task = task

        self.out_format = 'array'
        self.out_dtype = 'uint8'
        if task == 1 or task == 2:
            self.nout = 1
            self.nclasses = [len(self.bugs)]
        elif task == 3:
            self.nout = 2
            self.nclasses = [len(self.bugs)] * 2
        else:
            raise ValueError("task must be 1, 2 or 3")

        self.w = w
        self.h = h

    def __iter__(self):

        R = numpy.random.RandomState(self.seed)
        ri = R.random_integers

        while True:
            index1 = ri(0, len(self.bugs)-1)
            index2 = ri(0, len(self.bugs)-1)
            while index1 == index2:
                index2 = ri(0, len(self.bugs)-1)

            bugs1 = [self.bugs[index1]] * self.n1
            bugs2 = [self.bugs[index2]] * self.n2

            if self.rot:
                bugs1 = [bug.rotate(ri(0, 3) * 90) for bug in bugs1]
                bugs2 = [bug.rotate(ri(0, 3) * 90) for bug in bugs2]
            if self.scale:
                bugs1 = [bug.scale(ri(1, 2)) for bug in bugs1]
                bugs2 = [bug.scale(ri(1, 2)) for bug in bugs2]
            descr = []
            for bug in bugs1 + bugs2:
                descr.append(((ri(0, self.w - bug.w), ri(0, self.h - bug.h)), bug))

            if self.task == 1:
                yield descr, numpy.array([index1], dtype = self.out_dtype)
            elif self.task == 2:
                yield descr, numpy.array([index2], dtype = self.out_dtype)
            else:
                yield descr, numpy.array([index1, index2], dtype = self.out_dtype)

