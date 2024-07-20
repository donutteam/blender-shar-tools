#
# Imports
#

from __future__ import annotations

import os

import bpy
import bpy_extras

from classes.chunks.RootChunk import RootChunk
from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.HistoryChunk import HistoryChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.MeshChunk import MeshChunk
from classes.chunks.PathChunk import PathChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.StaticEntityChunk import StaticEntityChunk

from classes.File import File

import libs.fence as FenceLib
import libs.image as ImageLib
import libs.mesh as MeshLib
import libs.message as MessageLib
import libs.path as PathLib

#
# Class
#

def collectionItems(self: ExportPure3DFileOperator, context: bpy.types.Context):
	items = []

	for collectionIndex, collection in enumerate(bpy.data.collections):
		if collection.name.endswith(".p3d"):
			items.append((collection.name,collection.name,"",collectionIndex))

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
		# TODO: Automatically update filename when collection changes
	)
	
	def execute(self, context):
		chunks = []

		chunks.append(HistoryChunk(lines=["Hello","World"]))

		b = File.toBytes(chunks) # don't do it directly in the with context to not make a file when an error occurs
		with open(self.filepath,"wb+") as f:
			f.write(b)

		return {"FINISHED"}

def menu_item(self, context):
	self.layout.operator(ExportPure3DFileOperator.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ExportPure3DFileOperator)
	
	bpy.types.TOPBAR_MT_file_export.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ExportPure3DFileOperator)

	bpy.types.TOPBAR_MT_file_export.remove(menu_item)
