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

class PositionListChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	positions: list[mathutils.Vector]



class PositionListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		numberOfPositions = binaryReader.readUInt32()
		
		positions = []
		
		for i in range(numberOfPositions):
			positions.append(binaryReader.readPure3DVector3())

		return {
			"positions": positions
		}

	def __init__(self, options : PositionListChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["POSITION_LIST"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.positions = options["positions"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.positions))

		for position in self.positions:
			binaryWriter.writePure3DVector3(position)