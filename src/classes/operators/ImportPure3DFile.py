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
import libs.message as MessageLib
import libs.path as PathLib

#
# Class
#

class ImportPure3DFile(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File(s)..."
	bl_description = "Import Pure3D File(s) from The Simpsons Hit & Run."
	bl_options = {"REGISTER", "UNDO"}

	filename_ext = ".p3d"

	directory: bpy.props.StringProperty(subtype = "DIR_PATH", options = {"HIDDEN"})
	filter_glob: bpy.props.StringProperty(default = "*.p3d", options = {"HIDDEN"}, maxlen = 255)
	files: bpy.props.CollectionProperty(type = bpy.types.OperatorFileListElement, options = {"HIDDEN", "SKIP_SAVE"})

	option_import_fences: bpy.props.BoolProperty(name = "Import Fences", description = "Import Fence chunks from the Pure3D File(s).", default = True)
	option_import_paths: bpy.props.BoolProperty(name = "Import Paths", description = "Import Path chunks from the Pure3D File(s).", default = True)

	def draw(self, context):
		self.layout.prop(self, "option_import_fences")

		self.layout.prop(self, "option_import_paths")

	def execute(self, context):
		print(self.files)

		results : list[dict] = []

		for file in self.files:
			filePath = os.path.join(self.directory, file.name)

			print(f"Importing Pure3D File: { filePath }")

			results.append(self.importFile(filePath))

		messageLines : list[str] = []

		messageLines.append(f"Imported { len(results) } Pure3D File(s):")

		for result in results:
			messageLines.append(f"- { result['fileName'] }:")

			if result["numberOfFenceChunks"] > 0:
				messageLines.append(f"\t- Number of Fences: { result['numberOfFenceChunks'] }")

			if result["numberOfPathChunks"] > 0:
				messageLines.append(f"\t- Number of Paths: { result['numberOfPathChunks'] }")

			if result["numberOfUnsupportedChunks"] > 0:
				messageLines.append(f"\t- Number of Unsupported Chunks: { result['numberOfUnsupportedChunks'] }")

		MessageLib.alert("\n".join(messageLines))

		return {"FINISHED"}

	def importFile(self, filePath) -> dict:
		#
		# Read Pure3D File
		#

		with open(filePath, "rb") as file:
			fileContents = file.read()

		rootChunk = File.fromBytes(fileContents)

		#
		# Create File Collection
		#

		fileName = os.path.basename(filePath)

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

		numberOfFenceChunks = 0

		numberOfPathChunks = 0

		numberOfUnsupportedChunks = 0

		for chunkIndex, chunk in enumerate(rootChunk.children):
			if isinstance(chunk, FenceChunk):
				if self.option_import_fences:
					for childChunkIndex, childChunk in enumerate(chunk.children):
						if isinstance(childChunk, Fence2Chunk):
							fenceChunkObject = FenceLib.createFence(childChunk.start, childChunk.end, childChunk.normal, f"Fence { chunkIndex }")

							fenceCollection.objects.link(fenceChunkObject)

							numberOfFenceChunks += 1

			elif isinstance(chunk, PathChunk):
				if self.option_import_paths:
					pathChunkObject = PathLib.createPath(chunk.points, f"Path { chunkIndex }")

					pathCollection.objects.link(pathChunkObject)

					numberOfPathChunks += 1

			else:
				print(f"Unsupported chunk type: { hex(chunk.identifier) }")

				numberOfUnsupportedChunks += 1

		#
		# Add Sub Collections to File Collection OR Remove Empty Sub Collections
		#

		if numberOfFenceChunks > 0:
			fileCollection.children.link(fenceCollection)
		else:
			bpy.data.collections.remove(fenceCollection)

		if numberOfPathChunks > 0:
			fileCollection.children.link(pathCollection)
		else:
			bpy.data.collections.remove(pathCollection)

		#
		# Return
		#

		return {
			"fileName": fileName,
			"numberOfFenceChunks": numberOfFenceChunks,
			"numberOfPathChunks": numberOfPathChunks,
			"numberOfUnsupportedChunks": numberOfUnsupportedChunks,
		}

def menu_item(self, context):
	self.layout.operator(ImportPure3DFile.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ImportPure3DFile)
	
	bpy.types.TOPBAR_MT_file_import.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ImportPure3DFile)

	bpy.types.TOPBAR_MT_file_import.remove(menu_item)