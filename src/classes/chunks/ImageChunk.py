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

class ImageChunkOptions(typing.TypedDict):
	children: list[classes.chunks.Chunk.Chunk] | None
	
	name: str

	version: int

	width: int

	height: int

	bitsPerPixel: int

	palettized: int

	hasAlpha: int

	format: int



class ImageChunk(classes.chunks.Chunk.Chunk):
	formats = {
		"RAW": 0,
		"PNG": 1,
		"TGA": 2,
		"BMP": 3,
		"IPU": 4,
		"DXT": 5,
		"DXT1": 6,
		"DXT2": 7,
		"DXT3": 8,
		"DXT4": 9,
		"DXT5": 10,
		"PS24BIT": 11,
		"PS28BIT": 12,
		"PS216BIT": 13,
		"PS232BIT": 14,
		"GC4BIT": 15,
		"GC8BIT": 16,
		"GC16BIT": 17,
		"GC32BIT": 18,
		"GCDXT1": 19,
		"OTHER": 20,
		"INVALID": 21,
		"PSP4BIT": 22,
	}
	
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		name = binaryReader.readPure3DString()
		version = binaryReader.readUInt32()
		width = binaryReader.readUInt32()
		height = binaryReader.readUInt32()
		bitsPerPixel = binaryReader.readUInt32()
		palettized = binaryReader.readUInt32()
		hasAlpha = binaryReader.readUInt32()
		format = binaryReader.readUInt32()

		return {
			"name":name,
			"version":version,
			"width": width,
			"height": height,
			"bitsPerPixel": bitsPerPixel,
			"palettized": palettized,
			"hasAlpha": hasAlpha,
			"format": format,
		}

	def __init__(self, options : ImageChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["IMAGE"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.name = options["name"]
		self.version = options["version"]
		self.width = options["width"]
		self.height = options["height"]
		self.bitsPerPixel = options["bitsPerPixel"]
		self.palettized = options["palettized"]
		self.hasAlpha = options["hasAlpha"]
		self.format = options["format"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)

		binaryWriter.writeUInt32(self.version)

		binaryWriter.writeUInt32(self.width)
		binaryWriter.writeUInt32(self.height)
		binaryWriter.writeUInt32(self.bitsPerPixel)
		binaryWriter.writeUInt32(self.palettized)
		binaryWriter.writeUInt32(self.hasAlpha)
		binaryWriter.writeUInt32(self.format)