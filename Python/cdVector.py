import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeTypeName = 'cdVector'
kPluginNodeTypeId = OpenMaya.MTypeId(0x123e1)


class cdVector(OpenMayaMPx.MPxNode):

    startMat = OpenMaya.MObject()  # World Matrix of our starting obj.
    endMat = OpenMaya.MObject()    # World Matrix of our ending obj.
    mag = OpenMaya.MObject()       # Magnitude of vector.
    normAttr = OpenMaya.MObject()  # Normalize boolean.
    outVec = OpenMaya.MObject()    # Output vector.
    ox = OpenMaya.MObject()        # X value of vector.
    oy = OpenMaya.MObject()        # Y value of vector.
    oz = OpenMaya.MObject()        # Z value of vector.

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):

        if plug == cdVector.mag or\
           plug == cdVector.outVec or\
           plug == cdVector.ox or\
           plug == cdVector.oy or\
           plug == cdVector.oz:

            #Grab out incoming plugs.
            startMat = dataBlock.inputValue(cdVector.startMat).asMatrix()
            endMat = dataBlock.inputValue(cdVector.endMat).asMatrix()
            norm = dataBlock.inputValue(cdVector.normAttr).asBool()

            startVec = OpenMaya.MVector(startMat(3, 0),
                                        startMat(3, 1),
                                        startMat(3, 2))

            endVec = OpenMaya.MVector(endMat(3, 0),
                                      endMat(3, 1),
                                      endMat(3, 2))

            upVec = endVec - startVec

            dist = upVec.length()

            outVecX = dataBlock.outputValue(cdVector.ox)
            outVecY = dataBlock.outputValue(cdVector.oy)
            outVecZ = dataBlock.outputValue(cdVector.oz)
            magVal = dataBlock.outputValue(cdVector.mag)

            if dist > .001:

                if norm:
                    upVec.normalize()
                    outVecX.setFloat(upVec.x)
                    outVecY.setFloat(upVec.y)
                    outVecZ.setFloat(upVec.z)
                    magVal.setFloat(1.0)

                else:
                    outVecX.setFloat(upVec.x)
                    outVecY.setFloat(upVec.y)
                    outVecZ.setFloat(upVec.z)
                    magVal.setFloat(dist)

                dataBlock.setClean(plug)
            else:
                outVecX.setFloat(0.0)
                outVecY.setFloat(0.0)
                outVecZ.setFloat(0.0)


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(cdVector())


def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    cdVector.startMat = mAttr.create("startMatrix",
                                     "startMat",
                                     OpenMaya.MFnMatrixAttribute.kDouble)

    cdVector.addAttribute(cdVector.startMat)

    cdVector.endMat = mAttr.create("endMatrix",
                                   "endMat",
                                   OpenMaya.MFnMatrixAttribute.kDouble)

    cdVector.addAttribute(cdVector.endMat)

    cdVector.mag = nAttr.create("magnitude",
                                "mag",
                                OpenMaya.MFnNumericData.kFloat,
                                0.0)
    cdVector.addAttribute(cdVector.mag)

    cdVector.normAttr = nAttr.create("normalize",
                                     "norm",
                                     OpenMaya.MFnNumericData.kBoolean)

    cdVector.addAttribute(cdVector.normAttr)

    #Output Rotation attribute.
    cdVector.ox = nAttr.create("outVectorX",
                               "ox",
                               OpenMaya.MFnNumericData.kFloat,
                               0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(True)
    nAttr.setReadable(True)

    cdVector.oy = nAttr.create("outVectorY",
                               "oy",
                               OpenMaya.MFnNumericData.kFloat,
                               0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(True)
    nAttr.setReadable(True)

    cdVector.oz = nAttr.create("outVectorZ",
                               "oz",
                               OpenMaya.MFnNumericData.kFloat,
                               0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(True)
    nAttr.setReadable(True)

    cdVector.outVec = nAttr.create("outputVector",
                                   "ov",
                                   cdVector.ox,
                                   cdVector.oy,
                                   cdVector.oz)

    cdVector.addAttribute(cdVector.outVec)

    #Attribute affects.
    cdVector.attributeAffects(cdVector.startMat, cdVector.outVec)
    cdVector.attributeAffects(cdVector.startMat, cdVector.ox)
    cdVector.attributeAffects(cdVector.startMat, cdVector.oy)
    cdVector.attributeAffects(cdVector.startMat, cdVector.oz)
    cdVector.attributeAffects(cdVector.startMat, cdVector.mag)

    cdVector.attributeAffects(cdVector.endMat, cdVector.outVec)
    cdVector.attributeAffects(cdVector.endMat, cdVector.ox)
    cdVector.attributeAffects(cdVector.endMat, cdVector.oy)
    cdVector.attributeAffects(cdVector.endMat, cdVector.oz)
    cdVector.attributeAffects(cdVector.endMat, cdVector.mag)

    cdVector.attributeAffects(cdVector.normAttr, cdVector.outVec)
    cdVector.attributeAffects(cdVector.normAttr, cdVector.ox)
    cdVector.attributeAffects(cdVector.normAttr, cdVector.oy)
    cdVector.attributeAffects(cdVector.normAttr, cdVector.oz)
    cdVector.attributeAffects(cdVector.normAttr, cdVector.mag)


def initializePlugin(mobject):
    '''
    Initializes the plugin.

    Returns: None.
    '''

    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Chris DeVito", "1.0", "Any")
    try:
        mplugin.registerNode(kPluginNodeTypeName,
                             kPluginNodeTypeId,
                             nodeCreator,
                             nodeInitializer,
                             OpenMayaMPx.MPxNode.kDependNode)

        sys.stderr.write("Registered node: %s\n" % kPluginNodeTypeName)
    except:
        sys.stderr.write("Failed to register node: %s\n" % kPluginNodeTypeName)


def uninitializePlugin(mobject):
    '''
    Uninitializes the plugin.

    Returns: None.
    '''

    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeTypeId)
        sys.stderr.write("Deregistered node: %s\n" % kPluginNodeTypeName)
    except:
        sys.stderr.write("Failed to deregister node: %s\n"
                         % kPluginNodeTypeName)
