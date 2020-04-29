import c4d
import collections
import os
import sys

from c4d.modules import mograph as mo

# constants

PLUGIN_ID = 1054961

MoGraphClonerObject = 1018544
MoGraphVoronoiFractureObject = 1036557

COMMAND_CURRENT_STATE_TO_OBJECT = 12233

COMMAND_CLEAR_CONSOLE = 13957

class MoGraphBakerCommandData( c4d.plugins.CommandData ):

    def Do( self, obj, doc ):

        print( "Doing " + obj.GetName() + " (MoGraph Cloner)" )

        doc.StartUndo()

        c4d.CallCommand( COMMAND_CURRENT_STATE_TO_OBJECT )

        newObj = obj.GetNext()

        if newObj is None: raise Exception( "COMMAND_CURRENT_STATE_TO_OBJECT: Could not find the object derived from: " + obj.GetName() )
        
        newObj.SetEditorMode( c4d.MODE_UNDEF )
        newObj.SetRenderMode( c4d.MODE_UNDEF )

        obj.SetEditorMode( c4d.MODE_OFF )
        obj.SetRenderMode( c4d.MODE_OFF )

        endFrame = doc.GetMaxTime()

        frameIncrement = c4d.BaseTime( 1, doc.GetFps() ) 

        currentFrame = doc.GetMinTime()

        children = newObj.GetChildren()

        while currentFrame <= endFrame:
            
            doc.SetTime( currentFrame )

            success = doc.ExecutePasses( None, True, True, True, c4d.BUILDFLAGS_NONE )

            data = mo.GeGetMoData( obj )

            cloneCount = data.GetCount()

            clonesMatrixArray = data.GetArray( c4d.MODATA_MATRIX )
            # clonesSizeArray = data.GetArray( c4d.MODATA_SIZE )

            for index, child in enumerate( children, start = 0 ):

                child.SetMl( clonesMatrixArray[ index ] )

                doc.RecordKey( child, [ c4d.ID_BASEOBJECT_REL_POSITION ], currentFrame )
                doc.RecordKey( child, [ c4d.ID_BASEOBJECT_REL_ROTATION ], currentFrame )
                doc.RecordKey( child, [ c4d.ID_BASEOBJECT_REL_SCALE ], currentFrame )

            currentFrame = currentFrame + frameIncrement

        obj.SetDeformMode( False )

        doc.SetSelection( newObj, c4d.SELECTION_NEW )

        doc.AddUndo( c4d.UNDOTYPE_NEW, newObj )

        doc.EndUndo()

    def Execute( self, doc ):

        c4d.CallCommand( COMMAND_CLEAR_CONSOLE )

        usersCurrentFrame = doc.GetTime()

        acceptable = [ MoGraphClonerObject, MoGraphVoronoiFractureObject ]

        selected = doc.GetActiveObjects( c4d.GETACTIVEOBJECTFLAGS_NONE )

        for obj in selected:

            if obj.GetType() in acceptable:
        
                try:

                    self.Do( obj, doc )

                except Exception as exc:

                    print( exc )

            else:

                print( "Only works with MoGraph Cloners and Voronoi Fractures. Skipping: " + obj.GetName() )

        doc.SetTime( usersCurrentFrame )

        c4d.EventAdd()

        return True

if __name__ == "__main__":
    
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "icon.png")

    bmp = c4d.bitmaps.BaseBitmap()

    if bmp is None:
        raise MemoryError( "Failed to create a BaseBitmap." )

    if bmp.InitWith(fn)[0] != c4d.IMAGERESULT_OK:
        raise MemoryError( "Failed to initialize the BaseBitmap." )

    c4d.plugins.RegisterCommandPlugin( id = PLUGIN_ID, 
                                       str = "MoGraph Baker", 
                                       help = "Makes a baked copy of MoGraph that can be exported in FBXs etc", 
                                       info = 0, 
                                       dat = MoGraphBakerCommandData(), 
                                       icon = bmp )
