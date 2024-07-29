#
# Imports
#

from __future__ import annotations

import os
import tempfile

import bpy
import bpy_extras
import mathutils

import utils

import re

from classes.chunks.RootChunk import RootChunk
from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.HistoryChunk import HistoryChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.MeshChunk import MeshChunk
from classes.chunks.PathChunk import PathChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.StaticEntityChunk import StaticEntityChunk

from classes.properties.ShaderProperties import ShaderProperties

from classes.File import File

import libs.fence as FenceLib
import libs.image as ImageLib
import libs.mesh as MeshLib
import libs.message as MessageLib
import libs.path as PathLib

#
# Class
#

def collectionItems(self: ExportPure3DFileOperator = None, context: bpy.types.Context = None):
	items = []

	index = 0
	for collection in bpy.data.collections:
		if collection.name.endswith(".p3d"):
			items.append((collection.name,collection.name,"","",index))
			index += 1

	return items

class ExportPure3DFileOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
	bl_idname = "operators.export_pure3d_file"
	bl_label = "Export Pure3D File."
	bl_description = "Export a Pure3D file from The Simpsons Hit & Run."
	bl_options = {"REGISTER", "UNDO"}

	filename_ext = ".p3d"
	
	collection: bpy.props.EnumProperty(
		name="File Collection",
		description="The collection should contain all things to export and end with \".p3d\"",
		items=collectionItems,
		default=0
		# TODO: Automatically update filename when collection changes
	)
	
	def draw(self, context):
		layout = self.layout

		layout.use_property_decorate = False
		layout.use_property_split = True

		layout.prop(self, "collection")

		if len(collectionItems()) > 0 and os.path.basename(self.filepath) != self.collection:
			layout.label(text="Warning: Filename doesn't match collection name")

	def execute(self, context):
		print("Exporting to " + self.filepath)

		if len(collectionItems()) > 0:
			collection = bpy.data.collections[self.collection]
		else:
			collection = bpy.context.scene.collection
		
		exportedPure3DFile = ExportedPure3DFile(self,self.filepath,collection)

		exportedPure3DFile.export()

		return {"FINISHED"}

class ExportedPure3DFile():
	def __init__(self, exportPure3DFileOperator: ExportPure3DFileOperator, filePath: str, collection: bpy.types.Collection):
		self.exportPure3DFileOperator = exportPure3DFileOperator

		self.filePath = filePath
		
		self.fileName = os.path.basename(filePath)

		self.collection = collection

		self.textureChunks = []
		self.shaderChunks = []
		self.chunks = []
		
		self.imagesAlreadyExported = []
		self.materialsAlreadyExported = []

	def exportTexture(self, image: bpy.types.Image):
		if image.name in self.imagesAlreadyExported:
			return
		self.imagesAlreadyExported.append(image.name)

		width, height = image.size

		temppath = tempfile.mktemp(prefix="tempbstimage")
		image.save(filepath=temppath)

		with open(temppath,"rb") as f:
			data = f.read()

		self.textureChunks.append(TextureChunk(
			children = [
				ImageChunk(
					children = [
						ImageDataChunk(
							imageData = data
						)
					],
					name = image.name,
					version = 14000,
					width = width,
					height = height,
					bitsPerPixel = 8,
					palettized = 1,
					hasAlpha = 1,
					format = ImageChunk.formats["PNG"],
				)
			],
			version = 14000,
			name = image.name,
			width = width,
			height = height,
			alphaDepth = 8,
			bitsPerPixel = 8,
			textureType = 1,
			usage = 0,
			priority = 0,
			numberOfMipMaps = 1
		))

	def exportShader(self, mat: bpy.types.Material):
		if mat.name in self.materialsAlreadyExported:
			return
		self.materialsAlreadyExported.append(mat.name)

		shaderProperties: ShaderProperties = mat.shaderProperties

		params = []

		if mat.use_nodes and mat.node_tree != None and "Principled BSDF" in mat.node_tree.nodes and "Image Texture" in mat.node_tree.nodes:
			imageTexture = mat.node_tree.nodes["Image Texture"]

			self.exportTexture(imageTexture.image)

			params.append(ShaderTextureParameterChunk(parameter="TEX",value=imageTexture.image.name))

		self.shaderChunks.append(ShaderChunk(
			children = params,
			name = mat.name,
			version = 0,
			pddiShaderName = shaderProperties.pddiShader,
			hasTranslucency = mat.blend_method == "HASHED",
		))
		

	def export(self):
		for childCollection in self.collection.children:
			collectionBasename = utils.get_basename(childCollection.name)
	
			if collectionBasename == "Fences":
				for fence in childCollection.all_objects:
					if not fence.isFence:
						continue

					fenceCurve: bpy.types.Curve = fence.data

					fenceCurveSpline = fenceCurve.splines[0]

					start = fenceCurveSpline.points[0].co.xzy
					end = fenceCurveSpline.points[1].co.xzy

					calculatedNormal = (end - start).cross(mathutils.Vector((0, 1, 0))).normalized()

					calculatedNormal.y = 0

					if fence.fenceProperties.isFlipped:
						calculatedNormal = -calculatedNormal

					self.chunks.append(FenceChunk(children=[
						Fence2Chunk(
							start=start,
							end=end,
							normal=calculatedNormal
						)
					]))
			elif collectionBasename == "Static Entities":
				for obj in childCollection.all_objects:
					mesh = obj.data
					for mat in mesh.materials:
						self.exportShader(mat)
					chunk = MeshLib.meshToChunk(mesh)
					self.chunks.append(StaticEntityChunk(
						version = 0,
						hasAlpha = 0,
						name = obj.name,
						children = [
							chunk
						]
					))


		chunks = []
		chunks.extend(self.textureChunks)
		chunks.extend(self.shaderChunks)
		chunks.extend(self.chunks)
		b = File.toBytes(chunks) # don't do it directly in the with context to not make a file when an error occurs
		with open(self.filePath,"wb+") as f:
			f.write(b)
	
def menu_item(self, context):
	self.layout.operator(ExportPure3DFileOperator.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ExportPure3DFileOperator)
	
	bpy.types.TOPBAR_MT_file_export.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ExportPure3DFileOperator)

	bpy.types.TOPBAR_MT_file_export.remove(menu_item)
