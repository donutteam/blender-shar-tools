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

class FenceChunkOptions(typing.TypedDict):
	children : list[Chunk] | None

class FenceChunk(classes.chunks.Chunk.Chunk):
	def __init__(self, options : FenceChunkOptions) -> None:
		super().__init__(
			{
				"identifier": classes.chunks.Chunk.IDENTIFIERS["FENCE"],
				"children": options["children"] if "children" in options else None,
			})