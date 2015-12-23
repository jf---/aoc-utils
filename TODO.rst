
General
-------
-> pypi (see http://peterdowns.com/posts/first-time-with-pypi.html)
-> CI
-> Coverage

Python 3 tests

tests
-----
doctests?
more tests for *_make.py
operations
geom
more analyze tests (cf. waterline)

examples
--------
add example with handles ...
example using adaptors
operations

examples/geomplate.py
---------------------
- need examples where the tangency to constraining faces is respected
- fix build_curve_network()

brep
----
******** u, v parameters checks against domain
call the BRepCheck methods for every type + test

brep/edge.py
------------
curvature, radius etc ... RuntimeError

_fixme/triangulation.py
-----------------------
Unexpected results :  3 vertexes, 1 edge, 0 triangle from a face ?
