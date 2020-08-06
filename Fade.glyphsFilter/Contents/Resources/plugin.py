# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSMutableArray

class Fade(FilterWithDialog):

	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	fadeTextField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Fade',
			'de': 'Verschwinden',
			'fr': 'Disparaître',
			'es': 'Desaparecer',
			'pt': 'Desaparecer',
			'jp': '消える',
			'ko': '사라지다',
			'zh': '消失',
			})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Apply',
			'de': 'Anwenden',
			'fr': 'Appliquer',
			'es': 'Aplicar',
			'pt': 'Aplique',
			'jp': '申し込む',
			'ko': '대다',
			'zh': '应用',
			})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		# Set default value
		Glyphs.registerDefault('com.mekkablue.Fade.coordinates', "y<200")
		
		# Set value of text field
		self.fadeTextField.setStringValue_(
			self.cleanSyntax(Glyphs.defaults['com.mekkablue.Fade.coordinates'])
			)
		
		# Set focus to text field
		self.fadeTextField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setFadeText_( self, sender ):
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.Fade.coordinates'] = sender.stringValue()
		# Trigger redraw
		self.update()
	
	@objc.python_method
	def cleanSyntax(self, coordinateCode):
		return "".join( coordinateCode.split() )
	
	@objc.python_method
	def rectPath(self, minX, minY, maxX, maxY):
		# define nodes:
		nodes = (
			GSNode(NSPoint(minX, minY)),
			GSNode(NSPoint(maxX, minY)),
			GSNode(NSPoint(maxX, maxY)),
			GSNode(NSPoint(minX, maxY)),
		)
		# build rectangle path:
		rect = GSPath()
		# add nodes to path:
		for node in nodes:
			rect.nodes.append(node)
		# close path
		rect.closed = True
		return rect

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if "coordinates" in customParameters:
			coordinates = customParameters['coordinates']
		
		# Called through UI, use stored value
		else:
			coordinates = Glyphs.defaults['com.mekkablue.Fade.coordinates']
		
		pathOperator = NSClassFromString("GSPathOperator")
		
		for coordinateCode in coordinates.split(","):
			# remove all whitespace:
			coordinateCode = self.cleanSyntax(coordinateCode)
			
			# check if syntax valid:
			if coordinateCode and coordinateCode[0] in "xy" and coordinateCode[1] in "<>":
				# bounding rect coordinates:
				minX, minY = layer.bounds.origin
				maxX, maxY = minX + layer.bounds.size.width, minY + layer.bounds.size.height

				# pad rectangle coordinates:
				minX -= 1
				minY -= 1
				maxX += 1
				maxY += 1
				
				# cut value
				cut = float(coordinateCode[2:])
				
				# cut rectangle value:
				if coordinateCode[0]=="x":
					if coordinateCode[1]==">":
						minX = cut
					elif coordinateCode[1]=="<":
						maxX = cut
				elif coordinateCode[0]=="y":
					if coordinateCode[1]==">":
						minY = cut
					elif coordinateCode[1]=="<":
						maxY = cut
				
				# calculate GSPath subtracting:
				subtractRect = self.rectPath(minX, minY, maxX, maxY)
				subtractPaths = NSMutableArray.alloc().initWithObject_(subtractRect)
				layerPaths = NSMutableArray.alloc().init() # should work with simply ...layer.shapes
				for p in layer.copyDecomposedLayer().shapes:
					layerPaths.addObject_(p)
				if pathOperator.subtractPaths_from_error_(subtractPaths, layerPaths, None):
					layer.shapes = layerPaths

	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; coordinates:%s" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.Fade.coordinates'],
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
