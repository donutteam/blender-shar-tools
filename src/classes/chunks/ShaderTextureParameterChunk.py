#
# Imports
#

from __future__ import annotations

import typing

import classes.Vector2
import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

#
# Class
#

class ShaderTextureParameterChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	parameter: str

	value: str



class ShaderTextureParameterChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		parameter = binaryReader.readPure3DFourCharacterCode()
		value = binaryReader.readPure3DString()

		return {
			"parameter":parameter,
			"value":value,
		}

	def __init__(self, options : ShaderTextureParameterChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["SHADER_TEXTURE_PARAMETER"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.parameter = options["parameter"]
		self.value = options["value"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DFourCharacterCode(self.parameter)
		binaryWriter.writePure3DString(self.value)