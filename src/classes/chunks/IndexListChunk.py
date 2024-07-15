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

class IndexListChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		numberOfIndices = binaryReader.readUInt32()
		
		indices = []
		
		for i in range(numberOfIndices):
			indices.append(binaryReader.readUInt32())
		
		return [indices]

	def __init__(self, identifier: int = chunkIdentifiers.INDEX_LIST, children: list[Chunk] = [], indices: list[int] = []) -> None:
		super().__init__(chunkIdentifiers.INDEX_LIST, children)
	
		self.indices = indices
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.indices))

		for index in self.indices:
			binaryWriter.writeUInt32(index)