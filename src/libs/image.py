#
# Imports
#

import bpy
import os
import tempfile

from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk

#
# Utility Functions
#

def createImage(chunk: ImageChunk):
    for chunkIndex, childChildChunk in enumerate(chunk.children):
        if isinstance(childChildChunk, ImageDataChunk):
            filename = ""
            with tempfile.NamedTemporaryFile(prefix="image",mode="wb+",delete=False) as f:
                f.write(childChildChunk.imageData)
                filename = f.name
            
            img_src = bpy.data.images.load(filename)
            img = img_src.copy() # Don't make file appear as it's from a file in a temp directory
            img.name = chunk.name
            img.scale(chunk.width,chunk.height) # Make image stay in memory
            bpy.data.images.remove(img_src)
            os.remove(filename)
            return img