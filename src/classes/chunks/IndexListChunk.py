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

class IndexListChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	indices: list[int]



class IndexListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		numberOfIndices = binaryReader.readUInt32()
		
		indices = []
		
		for i in range(numberOfIndices):
			indices.append(binaryReader.readUInt32())
		
		return {
			"indices": indices
		}

	def __init__(self, options : IndexListChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["INDEX_LIST"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.indices = options["indices"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.indices))

		for index in self.indices:
			binaryWriter.writeUInt32(index)