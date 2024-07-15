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

from classes.File import File

import libs.fence as FenceLib
import libs.mesh as MeshLib
import libs.image as ImageLib

#
# Class
#

class ImportPure3DFile(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File..."
	bl_description = "Import a Pure3D file (limited support)"
	bl_options = {"REGISTER", "UNDO"}

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

		rootChunk = File.fromBytes(fileContents)

		#
		# Create File Collection
		#

		fileName = os.path.basename(filepath)

		fileCollection = bpy.data.collections.new(fileName)

		bpy.context.scene.collection.children.link(fileCollection)

		#
		# Import Chunks
		#

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

		for chunkIndex, chunk in enumerate(rootChunk.children):
			if isinstance(chunk, FenceChunk):
				for childChunkIndex, childChunk in enumerate(chunk.children):
					if isinstance(childChunk, Fence2Chunk):
						fenceChunkObject = FenceLib.createFence(childChunk.start, childChunk.end, childChunk.normal, f"Fence { chunkIndex }")

						fileCollection.objects.link(fenceChunkObject)
			
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
			
			

			elif isinstance(chunk, MeshChunk):
				obj = MeshLib.createMesh(chunk)
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