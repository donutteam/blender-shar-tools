#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class PositionListChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		numberOfPositions = binaryReader.readUInt32()
		
		positions = []
		
		for i in range(numberOfPositions):
			positions.append(binaryReader.readPure3DVector3())

		return [ positions ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.POSITION_LIST, 
		children : list[Chunk] = [], 
		positions: list[mathutils.Vector] = []
	) -> None:
		super().__init__(identifier,children)
	
		self.positions = positions
		

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.positions))

		for position in self.positions:
			binaryWriter.writePure3DVector3(position)