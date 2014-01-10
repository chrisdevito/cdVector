#include "cdVector.h"

MTypeId cdVector::id(0x123e1);

MObject cdVector::startMat;   //World Matrix of our starting obj.
MObject cdVector::endMat;     //World Matrix of our ending obj.
MObject cdVector::mag;        //Magnitude of vector.
MObject cdVector::normAttr;   //Normalize boolean.
MObject cdVector::outVec;     //Output Vector.
MObject cdVector::ox;         //X value of vector.
MObject cdVector::oy;         //Y value of vector.
MObject cdVector::oz;         //Z value of vector.

cdVector::cdVector() 
{
}

cdVector::~cdVector() 
{
}

void* cdVector::creator()
{ 
    return new cdVector(); 
}


MStatus cdVector::compute(const MPlug& plug, MDataBlock& data)
{

    if((plug == mag)||(plug == outVec)||(plug == ox)||(plug == oy)||(plug == oz))
    {

        MStatus status;

        MMatrix startMatrix = data.inputValue( startMat, &status ).asMatrix();
        CHECK_MSTATUS_AND_RETURN_IT( status );

        MMatrix endMatrix = data.inputValue( endMat, &status ).asMatrix();
        CHECK_MSTATUS_AND_RETURN_IT( status );

        bool norm = data.inputValue( normAttr, &status ).asBool();
        CHECK_MSTATUS_AND_RETURN_IT( status );

        MVector startVec(startMatrix[3][0], startMatrix[3][1], startMatrix[3][2]);
        MVector endVec(endMatrix[3][0], endMatrix[3][1], endMatrix[3][2]);

        MVector upVec = endVec - startVec;
        float dist = upVec.length();

        //Set the outgoing plugs.
        MDataHandle outVecX = data.outputValue(ox);
        MDataHandle outVecY = data.outputValue(oy);
        MDataHandle outVecZ = data.outputValue(oz);
        MDataHandle magVal = data.outputValue(mag);

        if (dist > 0.001f )
        {

            if (norm == true)
            {
                upVec.normalize();
                outVecX.setFloat(upVec.x);
                outVecY.setFloat(upVec.y);
                outVecZ.setFloat(upVec.z);
                magVal.setFloat(1.0f);
            }

            else
            {
                outVecX.setFloat(upVec.x);
                outVecY.setFloat(upVec.y);
                outVecZ.setFloat(upVec.z);
                magVal.setFloat(dist);
            }

        }

        else
        {
            outVecX.setFloat(0.0f);
            outVecY.setFloat(0.0f);
            outVecZ.setFloat(0.0f);
        }

        data.setClean(plug);

    }

    else
    {
        return MS::kUnknownParameter;
    }

    return MS::kSuccess;

}

MStatus cdVector::initialize()
{
    MStatus status;

    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;

    startMat = mAttr.create("startMatrix", "startMat", MFnMatrixAttribute::kDouble);
    addAttribute(startMat);

    endMat = mAttr.create("endMatrix", "endMat", MFnMatrixAttribute::kDouble);
    addAttribute(endMat);

    mag = nAttr.create("endPoint", "ePoint", MFnNumericData::kFloat);
    addAttribute(mag);

    normAttr = nAttr.create("normalize", "norm", MFnNumericData::kBoolean);
    addAttribute(normAttr);

    ox = nAttr.create("outVectorX", "ox", MFnNumericData::kFloat, 0.0);
    nAttr.setWritable(false);
    nAttr.setStorable(true);
    nAttr.setReadable(true);

    oy = nAttr.create("outVectorY", "oy", MFnNumericData::kFloat, 0.0);
    nAttr.setWritable(false);
    nAttr.setStorable(true);
    nAttr.setReadable(true);

    oz = nAttr.create("outVectorZ", "oz", MFnNumericData::kFloat, 0.0);
    nAttr.setWritable(false);
    nAttr.setStorable(true);
    nAttr.setReadable(true);

    outVec = nAttr.create("outputVector", "ov", ox, oy, oz);
    addAttribute(outVec);

    //Attribute affects.
    attributeAffects(startMat, outVec);
    attributeAffects(startMat, ox);
    attributeAffects(startMat, oy);
    attributeAffects(startMat, oz);
    attributeAffects(startMat, mag);

    attributeAffects(endMat, outVec);
    attributeAffects(endMat, ox);
    attributeAffects(endMat, oy);
    attributeAffects(endMat, oz);
    attributeAffects(endMat, mag);

    attributeAffects(normAttr, outVec);
    attributeAffects(normAttr, ox);
    attributeAffects(normAttr, oy);
    attributeAffects(normAttr, oz);
    attributeAffects(normAttr, mag);

    return MS::kSuccess;

}