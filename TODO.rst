
General
-------
-> pypi (see http://peterdowns.com/posts/first-time-with-pypi.html)
-> CI
-> Coverage

README.rst -> better presentation of pip install

Python 3 tests


tests
-----
doctests?
more tests for *_make.py
operations

examples
--------
add example with handles ...
example using adaptors
operations

examples/geomplate.py
---------------------
- need examples where the tangency to constraining faces is respected
- fix build_curve_network()

display
-------
Store default backend in a python file and use this instead of hardcoding wx all over the place
This is similar to the tolerance.py file

_fixme/triangulation.py
-----------------------
Unexpected results :  3 vertexes, 1 edge, 0 triangle from a face ?


brep
----
u, v parameters checks against domain
call the BRepCheck methods for every type + test

brep/edge.py
------------
curvature, radius etc ... RuntimeError
