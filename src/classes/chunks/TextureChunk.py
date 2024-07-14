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

class TextureChunkOptions(typing.TypedDict):
	children: list[classes.chunks.Chunk.Chunk] | None
	
	name: str

	version: int

	width: int

	height: int

	bitsPerPixel: int

	alphaDepth: int

	numberOfMipMaps: int

	textureType: int

	usage: int

	priority: int



class TextureChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		name = binaryReader.readPure3DString()
		version = binaryReader.readUInt32()
		width = binaryReader.readUInt32()
		height = binaryReader.readUInt32()
		bitsPerPixel = binaryReader.readUInt32()
		alphaDepth = binaryReader.readUInt32()
		numberOfMipMaps = binaryReader.readUInt32()
		textureType = binaryReader.readUInt32()
		usage = binaryReader.readUInt32()
		priority = binaryReader.readUInt32()

		return {
			"name":name,
			"version":version,
			"width": width,
			"height": height,
			"bitsPerPixel": bitsPerPixel,
			"alphaDepth": alphaDepth,
			"numberOfMipMaps": numberOfMipMaps,
			"textureType": textureType,
			"usage": usage,
			"priority": priority,
		}

	def __init__(self, options : TextureChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["TEXTURE"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.name = options["name"]
		self.version = options["version"]
		self.width = options["width"]
		self.height = options["height"]
		self.bitsPerPixel = options["bitsPerPixel"]
		self.alphaDepth = options["alphaDepth"]
		self.numberOfMipMaps = options["numberOfMipMaps"]
		self.textureType = options["textureType"]
		self.usage = options["usage"]
		self.priority = options["priority"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)

		binaryWriter.writeUInt32(self.version)

		binaryWriter.writeUInt32(self.width)
		binaryWriter.writeUInt32(self.height)
		binaryWriter.writeUInt32(self.bitsPerPixel)
		binaryWriter.writeUInt32(self.alphaDepth)
		binaryWriter.writeUInt32(self.numberOfMipMaps)
		binaryWriter.writeUInt32(self.textureType)
		binaryWriter.writeUInt32(self.usage)
		binaryWriter.writeUInt32(self.priority)