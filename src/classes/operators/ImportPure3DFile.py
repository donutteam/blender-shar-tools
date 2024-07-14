#
# Imports
#

import os
import tempfile

import bpy
import bpy_extras

import classes.chunks.Chunk
import classes.chunks.FenceChunk
import classes.chunks.Fence2Chunk
import classes.chunks.HistoryChunk
import classes.chunks.ImageChunk
import classes.chunks.ImageDataChunk
import classes.chunks.IndexListChunk
import classes.chunks.MeshChunk

import classes.File

import classes.chunks.OldPrimitiveGroupChunk
import classes.chunks.PositionListChunk
import classes.chunks.ShaderChunk
import classes.chunks.ShaderTextureParameterChunk
import classes.chunks.TextureChunk
import libs.fence
import libs.mesh

#
# Class
#

class ImportPure3DFile(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File..."
	bl_description = "Import a Pure3D file (limited support)"

	filename_ext = ".p3d"

	# https://docs.blender.org/api/current/bpy.props.html#bpy.props.StringProperty
	filter_glob: bpy.props.StringProperty(default = "*.p3d", options = {"HIDDEN"}, maxlen = 255)

	files: bpy.props.CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={"HIDDEN","SKIP_SAVE"}
	)

	directory: bpy.props.StringProperty(subtype="DIR_PATH")

	def execute(self, context):
		for file in self.files:
			filepath = os.path.join(self.directory,file.name)
			self.read_file(filepath)
		
		#
		# Return
		#

		return {"FINISHED"}
	
	def read_file(self,filepath):
		#
		# Read Pure3D File
		#

		print("Reading Pure3D file " + filepath)

		with open(filepath, "rb") as file:
			fileContents = file.read()

		rootChunk = classes.File.File.fromBytes(
			{
				"bytes": fileContents,
			})

		#
		# Create File Collection
		#

		fileName = os.path.basename(filepath)

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
			
			elif isinstance(chunk, classes.chunks.TextureChunk.TextureChunk):
				is_already_used = False
				for i in bpy.data.images:
					if i.name == chunk.name:
						is_already_used = True
				if is_already_used:
					continue
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, classes.chunks.ImageChunk.ImageChunk):
						for childChildChunkIndex, childChildChunk in enumerate(childChunk.children):
							if isinstance(childChildChunk, classes.chunks.ImageDataChunk.ImageDataChunk):
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
				
			elif isinstance(chunk, classes.chunks.ShaderChunk.ShaderChunk):
				if chunk.name in bpy.data.materials:
					continue
				material = bpy.data.materials.new(chunk.name)
				material.use_nodes = True
				bsdf = material.node_tree.nodes["Principled BSDF"]

				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, classes.chunks.ShaderTextureParameterChunk.ShaderTextureParameterChunk):
						if childChunk.parameter == "TEX":
							if childChunk.value not in bpy.data.images:
								continue

							image = bpy.data.images[childChunk.value]

							texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
							texture_image.image = image

							material.node_tree.links.new(bsdf.inputs["Base Color"],texture_image.outputs["Color"])


			elif isinstance(chunk, classes.chunks.MeshChunk.MeshChunk):
				obj = libs.mesh.createMesh(chunk)
				fileCollection.objects.link(obj)
			
			else:
				print(f"Unsupported chunk type: { hex(chunk.identifier) }")


def menu_item(self, context):
	self.layout.operator(ImportPure3DFile.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ImportPure3DFile)
	
	bpy.types.TOPBAR_MT_file_import.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ImportPure3DFile)

	bpy.types.TOPBAR_MT_file_import.remove(menu_item)