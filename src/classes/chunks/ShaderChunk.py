#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

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
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		name = binaryReader.readPure3DString()

		version = binaryReader.readUInt32()

		pddiShaderName = binaryReader.readPure3DString()

		hasTranslucency = binaryReader.readUInt32()

		vertexNeeds = binaryReader.readUInt32()

		vertexMask = binaryReader.readUInt32()

		return {
			"name":name,
			"version":version,
			"pddiShaderName":pddiShaderName,
			"hasTranslucency":hasTranslucency,
			"vertexNeeds":vertexNeeds,
			"vertexMask":vertexMask,
		}

	def __init__(self, options : ShaderChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["SHADER"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.name = options["name"]
		self.version = options["version"]
		self.pddiShaderName = options["pddiShaderName"]
		self.hasTranslucency = options["hasTranslucency"]
		self.vertexNeeds = options["vertexNeeds"]
		self.vertexMask = options["vertexMask"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)
		binaryWriter.writeUInt32(self.version)
		binaryWriter.writePure3DString(self.pddiShaderName)
		binaryWriter.writeUInt32(self.hasTranslucency)
		binaryWriter.writeUInt32(self.vertexNeeds)
		binaryWriter.writeUInt32(self.vertexMask)
		binaryWriter.writeUInt32(len(self.children))