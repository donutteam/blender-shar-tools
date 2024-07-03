#
# Imports
#

import classes.chunks.Chunk
import classes.chunks.HistoryChunk

import classes.ChunkRegistry

#
# Default Chunk Registry
#

defaultChunkRegistry = classes.ChunkRegistry.ChunkRegistry()

defaultChunkRegistry.register(classes.chunks.Chunk.IDENTIFIERS["HISTORY"], classes.chunks.HistoryChunk.HistoryChunk)