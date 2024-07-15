#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter
from classes.Vector3 import Vector3

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class Fence2Chunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		start = binaryReader.readPure3DVector3()

		end = binaryReader.readPure3DVector3()

		normal = binaryReader.readPure3DVector3()

		return [ start, end, normal ]

	def __init__(self, identifier : int = chunkIdentifiers.FENCE_2, children : list[Chunk] | None = None, start : Vector3 = Vector3(0, 0, 0), end : Vector3 = Vector3(0, 0, 0), normal : Vector3 = Vector3(0, 0, 0)) -> None:
		super().__init__(chunkIdentifiers.FENCE_2, children)

		self.start : Vector3 = start

		self.end : Vector3 = end

		self.normal : Vector3 = normal

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DVector3(self.start)

		binaryWriter.writePure3DVector3(self.end)

		binaryWriter.writePure3DVector3(self.normal)