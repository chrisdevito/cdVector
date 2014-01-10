#ifndef CDVECTOR_H
#define CDVECTOR_H

#include <maya/MPxNode.h>
#include <maya/MGlobal.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <iostream>

class cdVector : public MPxNode
{
public:
						cdVector();
	virtual				~cdVector(); 
	static  void*		creator();

	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );
	static  MStatus		initialize();

	static MTypeId	id;

    static MObject  startMat;  //World Matrix of our starting obj.
    static MObject  endMat;    //World Matrix of our ending obj.
    static MObject  mag;       //Magnitude of vector.
    static MObject  normAttr;       //Magnitude of vector.
    static MObject  outVec;    //Output Vector.
    static MObject  ox;        //X value of vector.
    static MObject  oy;        //Y value of vector.
    static MObject  oz;        //Z value of vector.

};

#endif