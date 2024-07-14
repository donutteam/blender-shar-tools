#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk
import classes.chunks.UnknownChunk

#
# Class
#

class ChunkRegistryOptions(typing.TypedDict):
	chunkRegistry : ChunkRegistry | None

class ChunkRegistry:
	def __init__(self, options : ChunkRegistryOptions = {}) -> None:
		self.chunkClasses = {} 
		
		if "chunkRegistry" in options and options["chunkRegistry"] is not None:
			self.chunkClasses = options["chunkRegistry"].chunkClasses

	def getClass(self, chunkIdentifier : int) -> classes.chunks.Chunk:
		if chunkIdentifier in self.chunkClasses:
			return self.chunkClasses[chunkIdentifier]
		else:
			return classes.chunks.UnknownChunk.UnknownChunk

	def register(self, chunkIdentifier : int, chunkClass : classes.chunks.Chunk) -> None:
		print("Register",chunkClass.__name__,hex(chunkIdentifier))
		self.chunkClasses[chunkIdentifier] = chunkClass