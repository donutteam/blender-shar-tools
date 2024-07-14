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

class ImageDataChunkOptions(typing.TypedDict):
	children: list[classes.chunks.Chunk.Chunk] | None
	
	imageData: bytes



class ImageDataChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		imageDataLength = binaryReader.readUInt32()
		imageData = binaryReader.readBytes(imageDataLength)

		return {
			"imageData":imageData
		}

	def __init__(self, options : ImageDataChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["IMAGE_DATA"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.imageData = options["imageData"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt32(len(self.imageData))

		binaryWriter.writeBytes(self.imageData)