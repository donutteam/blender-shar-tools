#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter
import classes.Vector3

#
# Class
#

class Fence2ChunkOptions(typing.TypedDict):
	children : list[Chunk] | None

	lines : list[str]

	start : classes.Vector3.Vector3

	end : classes.Vector3.Vector3

	normal : classes.Vector3.Vector3

class Fence2Chunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def readData(binaryReader : classes.Pure3DBinaryReader.Pure3DBinaryReader) -> dict:
		start = binaryReader.readPure3DVector3()

		end = binaryReader.readPure3DVector3()

		normal = binaryReader.readPure3DVector3()

		return {
			"start": start,
			"end": end,
			"normal": normal,
		}

	def __init__(self, options : Fence2ChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["FENCE_2"],
				"children": options["children"] if "children" in options else None,
			})

		self.start : classes.Vector3.Vector3 = options["start"]

		self.end : classes.Vector3.Vector3 = options["end"]

		self.normal : classes.Vector3.Vector3 = options["normal"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt16(len(self.lines))

		for line in self.lines:
			binaryWriter.writePure3DString(line)