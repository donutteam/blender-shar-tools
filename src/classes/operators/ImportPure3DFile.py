#
# Imports
#

from __future__ import annotations

import os

import bpy
import bpy_extras

from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.HistoryChunk import HistoryChunk

from classes.File import File

import libs.fence as FenceLib

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
		# Import Chunks
		#

		for chunkIndex, chunk in enumerate(rootChunk.children):
			if isinstance(chunk, FenceChunk):
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, Fence2Chunk):
						fenceChunkObject = FenceLib.createFence(childChunk.start, childChunk.end, childChunk.normal, f"Fence { chunkIndex }")

						fileCollection.objects.link(fenceChunkObject)
			else:
				print(f"Unsupported chunk type: { hex(chunk.identifier) }")

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