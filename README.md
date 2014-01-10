cdVector
========
cdVector is a simple MPxNode plugin that calculates a vector between two matrix inputs.

I've done two versions of the plugin. One version in C++ and one in Python.

Compiling:
------------

It's currently only compiled for Linux, but I've provided the source code and CMakeList to make your own.

To compile in CMake from command line:

cmake -G "Compiler you want" .. -D MAYA_VERSION:string=Your maya version "Path to the src folder"

Example:
	cmake -G "Unix Makefiles" .. -D MAYA_VERSION:string=2012 ../src

Use:
------------
Attributes:

startMatrix : World Matrix of our starting obj.
endMatrix : World Matrix of our ending obj.
mag : Magnitude of vector.
normAttr : Normalizes the outVector.
outVec : Output Vector.
ox : X value of vector.
oy : Y value of vector.
oz : Z value of vector.

Just plug two world matrices into the node and it'll spit out a vector and a magnitude. If you want the vector normalized, just check that attribute.

Good Luck!