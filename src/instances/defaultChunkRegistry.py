#
# Imports
#

import classes.chunks.Chunk
import classes.chunks.Fence2Chunk
import classes.chunks.FenceChunk
import classes.chunks.HistoryChunk

import classes.ChunkRegistry

#
# Default Chunk Registry
#

defaultChunkRegistry = classes.ChunkRegistry.ChunkRegistry()

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["HISTORY"], classes.chunks.HistoryChunk.HistoryChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["FENCE"], classes.chunks.FenceChunk.FenceChunk)

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["FENCE_2"], classes.chunks.Fence2Chunk.Fence2Chunk)