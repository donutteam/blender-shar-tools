#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.HistoryChunk import HistoryChunk

from classes.ChunkRegistry import ChunkRegistry

import data.chunkIdentifiers as chunkIdentifiers

#
# Default Chunk Registry
#

defaultChunkRegistry = ChunkRegistry()

defaultChunkRegistry.register(chunkIdentifiers.HISTORY, HistoryChunk)

defaultChunkRegistry.register(chunkIdentifiers.FENCE, FenceChunk)

defaultChunkRegistry.register(chunkIdentifiers.FENCE_2, Fence2Chunk)