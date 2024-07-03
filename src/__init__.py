#
# Blender Add-on Metadata
#

bl_info = {
	"name": "The Simpsons Hit & Run Tools",
	"description": "A collection of tools to help mod The Simpsons Hit & Run.",
	"author": "Donut Team",
	"version": (1, 0, 0),
	"blender": (4, 1, 1),
	"location": "TODO",
	"doc_url": "https://donutteam.com", # TODO: Actual documentation URL
	"tracker_url": "https://github.com/donutteam/blender-shar-tools/issues",
	"category": "Import-Export",
}

#
# Add Add-on Directory to Path (HACK: Blender is shit ass software)
#

import os
import sys

sys.path.append(os.path.dirname(__file__))

#
# Imports
#

import bpy

import classes.operators.ImportPure3DFile
import classes.operators.MoveObjectX

#
# Initialisation
#

def register():
	print("Registered The Simpsons Hit & Run Tools.")

	classes.operators.ImportPure3DFile.register()
	classes.operators.MoveObjectX.register()

def unregister():
	print("Unregistered The Simpsons Hit & Run Tools.")

	classes.operators.ImportPure3DFile.unregister()
	classes.operators.MoveObjectX.unregister()