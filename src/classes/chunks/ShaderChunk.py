#
# Imports
#

from __future__ import annotations

import typing

from classes.chunks.Chunk import Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ShaderChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	name: str

	version: int

	pddiShaderName: str

	hasTranslucency: int

	vertexNeeds: int

	vertexMask: int



class ShaderChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		name = binaryReader.readPure3DString()

		version = binaryReader.readUInt32()

		pddiShaderName = binaryReader.readPure3DString()

		hasTranslucency = binaryReader.readUInt32()

		vertexNeeds = binaryReader.readUInt32()

		vertexMask = binaryReader.readUInt32()

		return [name,version,pddiShaderName,hasTranslucency,vertexNeeds,vertexMask]

	def __init__(self, identifier: chunkIdentifiers.SHADER, children : list[Chunk] | None = None, name: str = "", version: int = 0, pddiShaderName: str = "", hasTranslucency: int = 0, vertexNeeds: int = 0, vertexMask: int = 0) -> None:
		super().__init__(identifier,children)
	
		self.name = name
		self.version = version
		self.pddiShaderName = pddiShaderName
		self.hasTranslucency = hasTranslucency
		self.vertexNeeds = vertexNeeds
		self.vertexMask = vertexMask
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)
		binaryWriter.writeUInt32(self.version)
		binaryWriter.writePure3DString(self.pddiShaderName)
		binaryWriter.writeUInt32(self.hasTranslucency)
		binaryWriter.writeUInt32(self.vertexNeeds)
		binaryWriter.writeUInt32(self.vertexMask)
		binaryWriter.writeUInt32(len(self.children))