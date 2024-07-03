#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryWriter

#
# Class
#

class RootChunkOptions(typing.TypedDict):
	identifier : int

	children : list[Chunk]

	isNewFile : bool

class RootChunk(classes.chunks.Chunk.Chunk):
	def __init__(self, options : RootChunkOptions) -> None:
		super().__init__(options)

		self.isNewFile : bool = options["isNewFile"]