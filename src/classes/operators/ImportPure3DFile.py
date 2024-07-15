#
# Imports
#

from __future__ import annotations

import os

import bpy
import bpy_extras

from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.PathChunk import PathChunk

from classes.File import File

import libs.fence as FenceLib
import libs.path as PathLib

#
# Class
#

class ImportPure3DFile(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File..."
	bl_options = {"REGISTER", "UNDO"}

	filename_ext = ".p3d"

	# https://docs.blender.org/api/current/bpy.props.html#bpy.props.StringProperty
	filter_glob: bpy.props.StringProperty(default = "*.p3d", options = {"HIDDEN"}, maxlen = 255)

	def execute(self, context):
		#
		# Read Pure3D File
		#

		with open(self.filepath, "rb") as file:
			fileContents = file.read()

		rootChunk = File.fromBytes(fileContents)

		#
		# Create File Collection
		#

		fileName = os.path.basename(self.filepath)

		fileCollection = bpy.data.collections.new(fileName)

		bpy.context.scene.collection.children.link(fileCollection)

		#
		# Create Sub Collections
		#

		fenceCollection = bpy.data.collections.new("Fences")

		pathCollection = bpy.data.collections.new("Paths")

		#
		# Import Chunks
		#

		for chunkIndex, chunk in enumerate(rootChunk.children):
			if isinstance(chunk, FenceChunk):
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, Fence2Chunk):
						fenceChunkObject = FenceLib.createFence(childChunk.start, childChunk.end, childChunk.normal, f"Fence { chunkIndex }")

						fenceCollection.objects.link(fenceChunkObject)

			elif isinstance(chunk, PathChunk):
				pathChunkObject = PathLib.createPath(chunk.points, f"Path { chunkIndex }")

				pathCollection.objects.link(pathChunkObject)

			else:
				print(f"Unsupported chunk type: { hex(chunk.identifier) }")

		#
		# Add Sub Collections to File Collection OR Remove Empty Sub Collections
		#

		if len(fenceCollection.objects) > 0:
			fileCollection.children.link(fenceCollection)
		else:
			bpy.data.collections.remove(fenceCollection)

		if len(pathCollection.objects) > 0:
			fileCollection.children.link(pathCollection)
		else:
			bpy.data.collections.remove(pathCollection)

		#
		# Return
		#

		return {"FINISHED"}

def menu_item(self, context):
	self.layout.operator(ImportPure3DFile.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ImportPure3DFile)
	
	bpy.types.TOPBAR_MT_file_import.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ImportPure3DFile)

	bpy.types.TOPBAR_MT_file_import.remove(menu_item)