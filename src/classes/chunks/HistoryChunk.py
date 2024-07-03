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

class HistoryChunkOptions(typing.TypedDict):
	children : list[Chunk] | None

	lines : list[str]

class HistoryChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(binaryReader : classes.Pure3DBinaryReader.Pure3DBinaryReader) -> dict:
		numberOfLines = binaryReader.readUInt16()

		lines : list[str] = []

		for i in range(numberOfLines):
			lines.append(binaryReader.readPure3DString())

		return {
			"lines": lines,
		}

	def __init__(self, options : HistoryChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["HISTORY"],
				"children": options["children"] if "children" in options else None,
			})

		self.lines : list[str] = options["lines"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writeUInt16(len(self.lines))

		for line in self.lines:
			binaryWriter.writePure3DString(line)