#
# Imports
#

from __future__ import annotations

import typing

from classes.chunks.Chunk import Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class PositionListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		numberOfPositions = binaryReader.readUInt32()
		
		positions = []
		
		for i in range(numberOfPositions):
			positions.append(binaryReader.readPure3DVector3())

		return [positions]

	def __init__(self, identifier: chunkIdentifiers.POSITION_LIST, children : list[Chunk] | None = None, positions: list[mathutils.Vector] = []) -> None:
		super().__init__(identifier,children)
	
		self.positions = positions
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.positions))

		for position in self.positions:
			binaryWriter.writePure3DVector3(position)