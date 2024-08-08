#
# Imports
#

import bpy
import os
import tempfile

from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk

#
# Utility Functions
#

def createImage(chunk: ImageChunk, textureChunk: TextureChunk | None = None):
    for chunkIndex, childChildChunk in enumerate(chunk.children):
        if isinstance(childChildChunk, ImageDataChunk):
            filename = ""
            with tempfile.NamedTemporaryFile(prefix="image",mode="wb+",delete=False) as f:
                f.write(childChildChunk.imageData)
                filename = f.name
            
            img_src = bpy.data.images.load(filename)

            img = bpy.data.images.new(textureChunk.name if textureChunk else chunk.name, chunk.width, chunk.height,alpha=True)

            new_pixels = []
            for i in img_src.pixels:
                new_pixels.append(i)

            img.pixels = new_pixels

            img.use_fake_user = True

            bpy.data.images.remove(img_src)

            os.remove(filename)

            img.update()

            return img