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

class MeshChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		name = binaryReader.readPure3DString()

		version = binaryReader.readUInt32()

		return [name, version]

	def __init__(self, identifier: chunkIdentifiers.MESH, children : list[Chunk] | None = None, name: str = "", version: int = 0) -> None:
		super().__init__(chunkIdentifiers.MESH,children)
	
		self.name = name

		self.version = version
	
	def getNumberOfOldPrimitiveGroups(self) -> int:
		numberOfOldPrimitiveGroups = 0
		for child in self.children:
			if child.identifier == chunkIdentifiers.OLD_PRIMITIVE_GROUP:
				numberOfOldPrimitiveGroups += 1
		return numberOfOldPrimitiveGroups

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)

		binaryWriter.writeUInt32(self.version)

		binaryWriter.writeUInt32(self.getNumberOfOldPrimitiveGroups())