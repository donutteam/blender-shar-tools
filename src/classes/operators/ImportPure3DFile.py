#
# Imports
#

import os

import bpy
import bpy_extras

import classes.chunks.FenceChunk
import classes.chunks.Fence2Chunk
import classes.chunks.HistoryChunk

import classes.File

import libs.fence

#
# Class
#

class ImportPure3DFile(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File..."

	filename_ext = ".p3d"

	# https://docs.blender.org/api/current/bpy.props.html#bpy.props.StringProperty
	filter_glob: bpy.props.StringProperty(default = "*.p3d", options = {"HIDDEN"}, maxlen = 255)

	def execute(self, context):
		#
		# Read Pure3D File
		#

		with open(self.filepath, "rb") as file:
			fileContents = file.read()

		rootChunk = classes.File.File.fromBytes(
			{
				"bytes": fileContents,
			})

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
			if isinstance(chunk, classes.chunks.FenceChunk.FenceChunk):
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, classes.chunks.Fence2Chunk.Fence2Chunk):
						print("Fence", chunkIndex, childChunk.start.__dict__, childChunk.end.__dict__)

						fenceChunkObject = libs.fence.createFence(
							{
								"start": childChunk.start,
								"end": childChunk.end,
								"normal": childChunk.normal,
								"name": f"Fence { chunkIndex }",
							})

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