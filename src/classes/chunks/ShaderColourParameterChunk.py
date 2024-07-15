#
# Imports
#

from __future__ import annotations

import typing

import classes.Colour
import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

#
# Class
#

class ShaderColourParameterChunkOptions(typing.TypedDict):
	children : list[classes.chunks.Chunk.Chunk] | None
	
	parameter: str

	colour: classes.Colour.Colour



class ShaderColourParameterChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(options["data"], options["isLittleEndian"])

		parameter = binaryReader.readPure3DFourCharacterCode()
		colour = binaryReader.readPure3DColour()

		return {
			"parameter":parameter,
			"colour":colour,
		}

	def __init__(self, options : ShaderColourParameterChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["SHADER_COLOUR_PARAMETER"],
				"children": options["children"] if "children" in options else None,
			})
	
		self.parameter = options["parameter"]
		self.colour = options["colour"]
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DFourCharacterCode(self.parameter)
		binaryWriter.writePure3DColour(self.colour)