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
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.MeshChunk import MeshChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.PathChunk import PathChunk

from classes.File import File

import libs.fence as FenceLib
import libs.mesh as MeshLib
import libs.image as ImageLib
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

	option_import_fences: bpy.props.BoolProperty(name = "Import Fences", description = "Import Fence chunks from the Pure3D File(s)", default = True)
	option_import_paths: bpy.props.BoolProperty(name = "Import Paths", description = "Import Path chunks from the Pure3D File(s)", default = True)

	def draw(self, context):
		self.layout.prop(self, "option_import_fences")

		self.layout.prop(self, "option_import_paths")

	files: bpy.props.CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={"HIDDEN","SKIP_SAVE"}
	)

	directory: bpy.props.StringProperty(subtype="DIR_PATH")

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
	
			if result["numberOfTextureChunks"] > 0:
				messageLines.append(f"\t- Number of Textures: { result['numberOfTextureChunks'] }")

			if result["numberOfShaderChunks"] > 0:
				messageLines.append(f"\t- Number of Shaders: { result['numberOfShaderChunks'] }")

			if result["numberOfMeshChunks"] > 0:
				messageLines.append(f"\t- Number of Meshes: { result['numberOfMeshChunks'] }")

			if result["numberOfUnsupportedChunks"] > 0:
				messageLines.append(f"\t- Number of Unsupported Chunks: { result['numberOfUnsupportedChunks'] }")

		MessageLib.alert("\n".join(messageLines))

		print("\n".join(messageLines))

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

		meshCollection = bpy.data.collections.new("Meshes")

		#
		# Import Chunks
		#

		numberOfFenceChunks = 0

		numberOfPathChunks = 0

		numberOfTextureChunks = 0

		numberOfShaderChunks = 0

		numberOfMeshChunks = 0 # TODO: Don't use meshes directly, but use the container formats

		numberOfUnsupportedChunks = 0

		# Import these first so that shaders, etc. can find the images
		for chunkIndex, chunk in enumerate(rootChunk.children):
			if isinstance(chunk, TextureChunk):
				is_already_used = False
				for i in bpy.data.images:
					if i.name == chunk.name:
						is_already_used = True
				if is_already_used:
					continue
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, ImageChunk):
						ImageLib.createImage(childChunk,chunk)
						numberOfTextureChunks += 1

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
			
			elif isinstance(chunk, TextureChunk):
				pass # Imported above
				
			elif isinstance(chunk, ShaderChunk):
				if chunk.name in bpy.data.materials:
					continue
				material = bpy.data.materials.new(chunk.name)
				material.use_nodes = True
				bsdf = material.node_tree.nodes["Principled BSDF"]

				material.shaderProperties.pddiShader = chunk.pddiShaderName

				if chunk.hasTranslucency:
					material.blend_method = "HASHED"
					material.shadow_method = "HASHED"

				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, ShaderTextureParameterChunk):
						if childChunk.parameter == "TEX":
							if childChunk.value not in bpy.data.images:
								print("Image",childChunk.value,"not found to apply on a material")
								continue

							image = bpy.data.images[childChunk.value]

							texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
							texture_image.image = image
							
							material.node_tree.links.new(bsdf.inputs["Base Color"],texture_image.outputs["Color"])
							material.node_tree.links.new(bsdf.inputs["Alpha"],texture_image.outputs["Alpha"]) # Always connect alpha nodes, transparency only visible when blend method is set to "Alpha Hashed"
					
					elif isinstance(childChunk, ShaderColourParameterChunk):
						# hacky way to do it
						color_argb = (childChunk.colour.red / 255,childChunk.colour.green / 255,childChunk.colour.blue / 255,childChunk.colour.alpha / 255)
						color_rgb = (childChunk.colour.red / 255,childChunk.colour.green / 255,childChunk.colour.blue / 255)
						if childChunk.parameter == "DIFF":
							bsdf.inputs[0].default_value = color_argb # Diffusive Color
							material.shaderProperties.diffuseColor = color_rgb # Specular
						elif childChunk.parameter == "SPEC":
							material.shaderProperties.specularColor = color_rgb # Specular
						elif childChunk.parameter == "AMBI":
							material.shaderProperties.ambientColor = color_rgb # Ambient
						elif childChunk.parameter == "EMIS":
							bsdf.inputs[26].default_value = color_argb # Emission Color
							bsdf.inputs[27].default_value = 1 # Emission Strength
						else:
							pass
					
					elif isinstance(childChunk, ShaderIntegerParameterChunk):
						if childChunk.parameter == "2SID":
							material.shaderProperties.twoSided = childChunk.value
							material.use_backface_culling = not childChunk.value
						elif childChunk.parameter == "LIT":
							material.shaderProperties.lighting = childChunk.value == 1
						elif childChunk.parameter == "ATST":
							material.shaderProperties.alphaTest = childChunk.value == 1
						elif childChunk.parameter == "BLMD":
							material.shaderProperties.blendMode = ("none","alpha","additive","subtractive")[childChunk.value]
						elif childChunk.parameter == "FIMD":
							material.shaderProperties.filterMode = ("nearestNeighbour","linear","nearestNeighbourMipNN","linearMipNN","linearMipL")[childChunk.value]
						elif childChunk.parameter == "UVMD":
							material.shaderProperties.uvMode = ("tile","clamp")[childChunk.value]
						elif childChunk.parameter == "SHMD":
							material.shaderProperties.shadeMode = ("flat","gouraud")[childChunk.value]
						elif childChunk.parameter == "ACMP":
							material.shaderProperties.alphaCompare = ("none","always","less","lessEqual","greater","greaterEqual","equal","notEqual")[childChunk.value]
						elif childChunk.parameter == "MMIN":
							material.shaderProperties.mipmapMin = str(pow(2,3+childChunk.value))
						elif childChunk.parameter == "MMAX":
							material.shaderProperties.mipmapMax = str(pow(2,3+childChunk.value))
						else:
							pass
					
					elif isinstance(childChunk, ShaderFloatParameterChunk):
						if childChunk.parameter == "SHIN":
							material.shaderProperties.shininess = childChunk.value
						elif childChunk.parameter == "ACTH":
							material.shaderProperties.alphaCompareThreshold = childChunk.value
						else:
							pass
			
				numberOfShaderChunks += 1
			

			elif isinstance(chunk, MeshChunk):
				obj = MeshLib.createMesh(chunk)
				meshCollection.objects.link(obj)
				numberOfMeshChunks += 1

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
		
		if numberOfMeshChunks > 0:
			fileCollection.children.link(meshCollection)
		else:
			bpy.data.collections.remove(meshCollection)

		#
		# Return
		#

		return {
			"fileName": fileName,
			"numberOfFenceChunks": numberOfFenceChunks,
			"numberOfPathChunks": numberOfPathChunks,
			"numberOfTextureChunks": numberOfTextureChunks,
			"numberOfShaderChunks": numberOfShaderChunks,
			"numberOfMeshChunks": numberOfMeshChunks,
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