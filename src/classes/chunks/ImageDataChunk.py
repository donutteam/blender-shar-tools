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

class ImageDataChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		imageDataLength = binaryReader.readUInt32()
		imageData = binaryReader.readBytes(imageDataLength)

		return [imageData]

	def __init__(self, identifier: int = chunkIdentifiers.IMAGE_DATA, children: list[Chunk] = [], imageData: bytes = bytes()) -> None:
		super().__init__(chunkIdentifiers.IMAGE_DATA,children)
	
		self.imageData = imageData

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.imageData))

		binaryWriter.writeBytes(self.imageData)