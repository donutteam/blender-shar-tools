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

class MeshChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	name: str

	version: int
	
	data : bytes | None



class MeshChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		name = binaryReader.readPure3DString()

		version = binaryReader.readUInt32()

		return {
			"name":name,
			"version":version,
			"data": options["data"],
		}

	def __init__(self, options : MeshChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["MESH"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.name: str = options["name"]

		self.version: int = options["version"]

		self.data : bytes = options["data"]
	
	def getNumberOfOldPrimitiveGroups(self) -> int:
		numberOfOldPrimitiveGroups = 0
		for child in self.children:
			if child.identifier == classes.chunks.Chunk.IDENTIFIERS["OLD_PRIMITIVE_GROUP"]:
				numberOfOldPrimitiveGroups += 1
		return numberOfOldPrimitiveGroups

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)

		binaryWriter.writeUInt32(self.version)

		binaryWriter.writeUInt32(self.getNumberOfOldPrimitiveGroups())