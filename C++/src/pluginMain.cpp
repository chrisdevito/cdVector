#include "cdVector.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "Christopher DeVito", "1.0", "Any" );

    status = fnPlugin.registerNode( "cdVector",
                                     cdVector::id,
                                     cdVector::creator,
                                     cdVector::initialize );

    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );

    status = fnPlugin.deregisterNode( cdVector::id );

    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}