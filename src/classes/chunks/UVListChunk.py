#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import mathutils

#
# Class
#

class UVListChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	channel: int

	uvs: list[mathutils.Vector]



class UVListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		numberOfUVs = binaryReader.readUInt32()

		channel = binaryReader.readUInt32()
		
		uvs = []
		
		for i in range(numberOfUVs):
			uvs.append(binaryReader.readPure3DVector2())

		return {
			"channel":channel,
			"uvs": uvs
		}

	def __init__(self, options : UVListChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["UV_LIST"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.channel = options["channel"]
		self.uvs = options["uvs"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.uvs))

		binaryWriter.writeUInt32(self.channel)

		for uv in self.uvs:
			binaryWriter.writePure3DVector2(uv)