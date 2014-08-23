#-
# ==========================================================================
# Copyright (C) 1995 - 2006 Autodesk, Inc. and/or its licensors.  All 
# rights reserved.
#
# The coded instructions, statements, computer programs, and/or related 
# material (collectively the "Data") in these files contain unpublished 
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its 
# licensors, which is protected by U.S. and Canadian federal copyright 
# law and by international treaties.
#
# The Data is provided for use exclusively by You. You have the right 
# to use, modify, and incorporate this Data into other products for 
# purposes authorized by the Autodesk software license agreement, 
# without fee.
#
# The copyright notices in the Software and this entire statement, 
# including the above license grant, this restriction and the 
# following disclaimer, must be included in all copies of the 
# Software, in whole or in part, and all derivative works of 
# the Software, unless such copies or derivative works are solely 
# in the form of machine-executable object code generated by a 
# source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. 
# AUTODESK DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED 
# WARRANTIES INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF 
# NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR 
# PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE, OR 
# TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS LICENSORS 
# BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL, 
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK 
# AND/OR ITS LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY 
# OR PROBABILITY OF SUCH DAMAGES.
#
# ==========================================================================
#+

#
# Autodesk Script File
# MODIFY THIS AT YOUR OWN RISK
#
# Creation Date:   27 September 2006
#
# swissArmyManip.py
# 
# This plug-in is an example of a user-defined manipulator,
# which is comprised of a variety of the base manipulators:
# - MFnCircleSweepManip
# - MFnDirectionManip
# - MFnDiscManip
# - MFnDistanceManip
# - MFnFreePointTriadManip
# - MFnStateManip
# - MFnToggleManip
# - MFnRotateManip
# - MFnScaleManip
#
# To use this plug-in:
# 
#	import maya.cmds as cmds
#	cmds.createNode("spSwissArmyLocator")
#
#   click on the showManipTool
# 

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math,sys

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

kSwissArmyLocatorName = "spSwissArmyLocator"
kSwissArmyLocatorId = OpenMaya.MTypeId(0x87006)
kSwissArmyLocatorManipName = "spSwissArmyLocatorManip"
kSwissArmyLocatorManipId = OpenMaya.MTypeId(0x87007)

delta1 = 0.01
delta2 = 0.02
delta3 = 0.03
delta4 = 0.04

# Locator Data
centre = [	[  0.10, 0.0,  0.10 ],
			[  0.10, 0.0, -0.10 ],
			[ -0.10, 0.0, -0.10 ],
			[ -0.10, 0.0,  0.10 ], 
			[  0.10, 0.0,  0.10 ] ] 
state1 = [	[  1.00, 0.0,  1.00 ],
			[  1.00, 0.0,  0.50 ],
			[  0.50, 0.0,  0.50 ],
			[  0.50, 0.0,  1.00 ], 
			[  1.00, 0.0,  1.00 ] ] 
state2 = [	[  1.00, 0.0, -1.00 ],
			[  1.00, 0.0, -0.50 ],
			[  0.50, 0.0, -0.50 ],
			[  0.50, 0.0, -1.00 ], 
			[  1.00, 0.0, -1.00 ] ] 
state3 = [	[ -1.00, 0.0, -1.00 ],
			[ -1.00, 0.0, -0.50 ],
			[ -0.50, 0.0, -0.50 ],
			[ -0.50, 0.0, -1.00 ], 
			[ -1.00, 0.0, -1.00 ] ] 
state4 = [	[ -1.00, 0.0,  1.00 ],
			[ -1.00, 0.0,  0.50 ],
			[ -0.50, 0.0,  0.50 ],
			[ -0.50, 0.0,  1.00 ], 
			[ -1.00, 0.0,  1.00 ] ] 
arrow1 = [	[  0.00, 0.0,  1.00 ],
			[  0.10, 0.0,  0.20 ],
			[ -0.10, 0.0,  0.20 ],
			[  0.00, 0.0,  1.00 ] ] 
arrow2 = [	[  1.00, 0.0,  0.00 ],
			[  0.20, 0.0,  0.10 ],
			[  0.20, 0.0, -0.10 ],
			[  1.00, 0.0,  0.00 ] ] 
arrow3 = [	[  0.00, 0.0, -1.00 ],
			[  0.10, 0.0, -0.20 ],
			[ -0.10, 0.0, -0.20 ],
			[  0.00, 0.0, -1.00 ] ] 
arrow4 = [	[ -1.00, 0.0,  0.00 ],
			[ -0.20, 0.0,  0.10 ],
			[ -0.20, 0.0, -0.10 ],
			[ -1.00, 0.0,  0.00 ] ] 
perimeter=[	[  1.10, 0.0,  1.10 ],
			[  1.10, 0.0, -1.10 ],
			[ -1.10, 0.0, -1.10 ],
			[ -1.10, 0.0,  1.10 ], 
			[  1.10, 0.0,  1.10 ] ] 

kCentreCount = 5
kState1Count = 5
kState2Count = 5
kState3Count = 5
kState4Count = 5
kArrow1Count = 4
kArrow2Count = 4
kArrow3Count = 4
kArrow4Count = 4
kPerimeterCount = 5


########################################################################
########################################################################

class swissArmyLocatorManip(OpenMayaMPx.MPxManipContainer):
		
		self.fCircleSweepManip = OpenMaya.MDagPath()
		self.fDirectionManip = OpenMaya.MDagPath()
		self.fDiscManip = OpenMaya.MDagPath()
		self.fDistanceManip = OpenMaya.MDagPath()
		self.fFreePointTriadManip = OpenMaya.MDagPath()
		self.fStateManip = OpenMaya.MDagPath()
		self.fToggleManip = OpenMaya.MDagPath()
		self.fRotateManip = OpenMaya.MDagPath()
		self.fScaleManip = OpenMaya.MDagPath()
		self.fNodePath = OpenMaya.MDagPath()


	def createChildren(self):
		# FreePointTriadManip
		self.fFreePointTriadManip = self.addFreePointTriadManip("freePointTriadManip", "point")
		freePointTriadManipFn = OpenMayaUI.MFnFreePointTriadManip(self.fFreePointTriadManip)

		# DirectionManip
		self.fDirectionManip = self.addDirectionManip("directionManip", "direction")
		directionManipFn = OpenMayaUI.MFnDirectionManip(self.fDirectionManip)

		# ToggleManip
		self.fToggleManip = self.addToggleManip("toggleManip", "toggle")
		toggleManipFn = OpenMayaUI.MFnToggleManip(self.fToggleManip)

		# StateManip
		self.fStateManip = self.addStateManip("stateManip", "state")
		stateManipFn = OpenMayaUI.MFnStateManip(self.fStateManip)

		# DiscManip
		self.fDiscManip = self.addDiscManip("discManip", "angle")
		discManipFn = OpenMayaUI.MFnDiscManip(self.fDiscManip)

		# CircleSweepManip
		self.fCircleSweepManip = self.addCircleSweepManip("circleSweepManip", "angle")
		circleSweepManipFn = OpenMayaUI.MFnCircleSweepManip(self.fCircleSweepManip)
		circleSweepManipFn.setCenterPoint(OpenMaya.MPoint(0, 0, 0))
		circleSweepManipFn.setNormal(OpenMaya.MVector(0, 1, 0))
		circleSweepManipFn.setRadius(2.0)
		circleSweepManipFn.setDrawAsArc(True)

		# DistanceManip
		self.fDistanceManip = self.addDistanceManip("distanceManip", "distance")
		distanceManipFn = OpenMayaUI.MFnDistanceManip(self.fDistanceManip)
		distanceManipFn.setStartPoint(OpenMaya.MPoint(0, 0, 0))
		distanceManipFn.setDirection(OpenMaya.MVector(0, 1, 0))

		# RotateManip
		self.fRotateManip = self.addRotateManip("RotateManip", "rotation")
		rotateManipFn = OpenMayaUI.MFnRotateManip(self.fRotateManip)

		# ScaleManip
		self.fScaleManip = self.addScaleManip("scaleManip", "scale")
		scaleManipFn = OpenMayaUI.MFnScaleManip(self.fScaleManip)


	def connectToDependNode(self, node):
		# Get the DAG path
		dagNodeFn = OpenMaya.MFnDagNode(node)
		dagNodeFn.getPath(self.fNodePath)
		parentNode = dagNodeFn.parent(0)
		parentNodeFn = OpenMaya.MFnDagNode(parentNode)

		# Connect the plugs
		nodeFn = OpenMaya.MFnDependencyNode()
		nodeFn.setObject(node)   

		# FreePointTriadManip
		freePointTriadManipFn = OpenMayaUI.MFnFreePointTriadManip(self.fFreePointTriadManip)
		try:
			translationPlug = parentNodeFn.findPlug("t")
			freePointTriadManipFn.connectToPointPlug(translationPlug)
		except:
			pass

		# DirectionManip
		directionManipFn = OpenMayaUI.MFnDirectionManip()
		directionManipFn.setObject(self.fDirectionManip)
		try:
			directionPlug = nodeFn.findPlug("arrow2Direction")
			directionManipFn.connectToDirectionPlug(directionPlug)
			startPointIndex = directionManipFn.startPointIndex()
			self.addPlugToManipConversion(startPointIndex)
		except:
			pass

		# DistanceManip
		distanceManipFn = OpenMayaUI.MFnDistanceManip()
		distanceManipFn.setObject(self.fDistanceManip)
		try:
			sizePlug = nodeFn.findPlug("size")
			distanceManipFn.connectToDistancePlug(sizePlug)
			startPointIndex = distanceManipFn.startPointIndex()
			self.addPlugToManipConversion(startPointIndex)
		except:
			pass

		# CircleSweepManip
		circleSweepManipFn = OpenMayaUI.MFnCircleSweepManip(self.fCircleSweepManip)
		try:
			arrow1AnglePlug = nodeFn.findPlug("arrow1Angle")
			circleSweepManipFn.connectToAnglePlug(arrow1AnglePlug)
			centerIndex = circleSweepManipFn.centerIndex()
			self.addPlugToManipConversion(centerIndex)
		except:
			pass

		# DiscManip
		discManipFn = OpenMayaUI.MFnDiscManip(self.fDiscManip)
		try:
			arrow3AnglePlug = nodeFn.findPlug("arrow3Angle")
			discManipFn.connectToAnglePlug(arrow3AnglePlug)
			centerIndex = discManipFn.centerIndex()
			self.addPlugToManipConversion(centerIndex)
		except:
			pass

		# StateManip
		stateManipFn = OpenMayaUI.MFnStateManip(self.fStateManip)
		try:
			statePlug = nodeFn.findPlug("state")
			stateManipFn.connectToStatePlug(statePlug)
			positionIndex = stateManipFn.positionIndex()
			self.addPlugToManipConversion(positionIndex)
		except:
			pass

		# ToggleManip
		toggleManipFn = OpenMayaUI.MFnToggleManip(self.fToggleManip)
		try:
			togglePlug = nodeFn.findPlug("toggle")
			toggleManipFn.connectToTogglePlug(togglePlug)
			startPointIndex = toggleManipFn.startPointIndex()
			self.addPlugToManipConversion(startPointIndex)
		except:
			pass

		# Determine the transform node for the locator
		transformPath = OpenMaya.MDagPath(self.fNodePath)
		transformPath.pop()

		transformNode = OpenMaya.MFnTransform(transformPath)

		# RotateManip
		rotateManipFn = OpenMayaUI.MFnRotateManip(self.fRotateManip)
		try:
			rotatePlug = transformNode.findPlug("rotate")
			rotateManipFn.connectToRotationPlug(rotatePlug)
			rotateManipFn.displayWithNode(node)
		except:
			pass

		# ScaleManip
		scaleManipFn = OpenMayaUI.MFnScaleManip(self.fScaleManip)
		try:
			scalePlug = transformNode.findPlug("scale")
			scaleManipFn.connectToScalePlug(scalePlug)
			scaleManipFn.displayWithNode(node)
		except:
			pass

		self.finishAddingManips()
		OpenMayaMPx.MPxManipContainer.connectToDependNode(self, node)


	def draw(self, view, path, style, status):
		OpenMayaMPx.MPxManipContainer.draw(self, view, path, style, status)
		view.beginGL()
		textPos = OpenMaya.MPoint(self.nodeTranslation())
		view.drawText("Swiss Army Manipulator", textPos, OpenMayaUI.M3dView.kLeft)
		view.endGL()


	def plugToManipConversion(self, theIndex):
		numData = OpenMaya.MFnNumericData()
		numDataObj = numData.create(OpenMaya.MFnNumericData.k3Float)
		vec = self.nodeTranslation()
		numData.setData3Float(vec.x, vec.y, vec.z)
		manipData = OpenMayaUI.MManipData(numDataObj)
		return manipData

	
	def nodeTranslation(self):
		dagFn = OpenMaya.MFnDagNode(self.fNodePath)
		path = OpenMaya.MDagPath()
		dagFn.getPath(path)
		path.pop()  # pop from the shape to the transform
		transformFn = OpenMaya.MFnTransform(path)
		return transformFn.getTranslation(OpenMaya.MSpace.kWorld)


########################################################################
########################################################################

class swissArmyLocator(OpenMayaMPx.MPxLocatorNode):
	aSize = OpenMaya.MObject()         # The size of the locator
	aPoint = OpenMaya.MObject()
	aPointX = OpenMaya.MObject()
	aPointY = OpenMaya.MObject()
	aPointZ = OpenMaya.MObject()
	aArrow1Angle = OpenMaya.MObject()
	aArrow2Direction = OpenMaya.MObject()
	aArrow2DirectionX = OpenMaya.MObject()
	aArrow2DirectionY = OpenMaya.MObject()
	aArrow2DirectionZ = OpenMaya.MObject()
	aArrow3Angle = OpenMaya.MObject()
	aArrow4Distance = OpenMaya.MObject()
	aState = OpenMaya.MObject()
	aToggle = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)


	def compute(self, plug, data):
		return OpenMaya.kUnknownParameter


	def draw(self, view, path, style, status):

		# Get the size
		thisNode = self.thisMObject()

		plug = OpenMaya.MPlug(thisNode, swissArmyLocator.aSize)
		sizeVal = plug.asMDistance()

		arrow1AnglePlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aArrow1Angle)
		arrow1Angle = arrow1AnglePlug.asMAngle()
		angle1 = -arrow1Angle.asRadians() - 3.1415927/2.0

		arrow3AnglePlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aArrow3Angle)
		arrow3Angle = arrow3AnglePlug.asMAngle()
		angle3 = arrow3Angle.asRadians()

		statePlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aState)
		state = statePlug.asInt()

		togglePlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aToggle)
		toggle = togglePlug.asBool()

		directionXPlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aArrow2DirectionX)
		directionYPlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aArrow2DirectionY)
		directionZPlug = OpenMaya.MPlug(thisNode, swissArmyLocator.aArrow2DirectionZ)
		dirX = directionXPlug.asDouble()
		dirY = directionYPlug.asDouble()
		dirZ = directionZPlug.asDouble()

		angle2 = math.atan2(dirZ, dirX)
		angle2 += 3.1415927

		multiplier = sizeVal.asCentimeters()

		view.beginGL() 

		if ((style == OpenMayaUI.M3dView.kFlatShaded) or
				(style == OpenMayaUI.M3dView.kGouraudShaded)):
			# Push the color settings
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)

			if (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor(13, OpenMayaUI.M3dView.kActiveColors)
			else:
				view.setDrawColor(13, OpenMayaUI.M3dView.kDormantColors)

			if (toggle):
				if (status == OpenMayaUI.M3dView.kActive):
					view.setDrawColor(15, OpenMayaUI.M3dView.kActiveColors)
				else:
					view.setDrawColor(15, OpenMayaUI.M3dView.kDormantColors)
				glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
				last = kCentreCount - 1
				for i in range(last):
					glFT.glVertex3f(centre[i][0] * multiplier,
							   centre[i][1] * multiplier,
							   centre[i][2] * multiplier)
				glFT.glEnd()

			if (state == 0):
				if (status == OpenMayaUI.M3dView.kActive):
					view.setDrawColor(19, OpenMayaUI.M3dView.kActiveColors)
				else:
					view.setDrawColor(19, OpenMayaUI.M3dView.kDormantColors)
				glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
				last = kState1Count - 1
				for i in range(last):
					glFT.glVertex3f(state1[i][0] * multiplier,
									state1[i][1] * multiplier,
									state1[i][2] * multiplier)
				glFT.glEnd()

			if (state == 1):
				if (status == OpenMayaUI.M3dView.kActive):
					view.setDrawColor(21, OpenMayaUI.M3dView.kActiveColors)
				else:
					view.setDrawColor(21, OpenMayaUI.M3dView.kDormantColors)
				glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
				last = kState2Count - 1
				for i in range(last):
					glFT.glVertex3f(state2[i][0] * multiplier,
									state2[i][1] * multiplier,
									state2[i][2] * multiplier)
				glFT.glEnd()

			if (state == 2):
				if (status == OpenMayaUI.M3dView.kActive):
					view.setDrawColor(18, OpenMayaUI.M3dView.kActiveColors)
				else:
					view.setDrawColor(18, OpenMayaUI.M3dView.kDormantColors)
					glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
					last = kState3Count - 1
					for i in range(last):
						glFT.glVertex3f(state3[i][0] * multiplier,
										state3[i][1] * multiplier,
										state3[i][2] * multiplier)
					glFT.glEnd()

			if (state == 3):
				if (status == OpenMayaUI.M3dView.kActive):
					view.setDrawColor(17, OpenMayaUI.M3dView.kActiveColors)
				else:
					view.setDrawColor(17, OpenMayaUI.M3dView.kDormantColors)
				glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
				last = kState4Count - 1
				for i in range(last):
					glFT.glVertex3f(state4[i][0] * multiplier,
									state4[i][1] * multiplier,
									state4[i][2] * multiplier)
				glFT.glEnd()

			if (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor(12, OpenMayaUI.M3dView.kActiveColors)
			else:
				view.setDrawColor(12, OpenMayaUI.M3dView.kDormantColors)
			glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
			last = kArrow1Count - 1
			for i in range(last):
				glFT.glVertex3f((-arrow1[i][0] * multiplier * math.cos(angle1) - arrow1[i][2] * multiplier * math.sin(angle1)),
								(arrow1[i][1] * multiplier + delta1),
								(arrow1[i][2] * multiplier * math.cos(angle1) - arrow1[i][0] * multiplier * math.sin(angle1)))
			glFT.glEnd()

			if (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor(16, OpenMayaUI.M3dView.kActiveColors)
			else:
				view.setDrawColor(16, OpenMayaUI.M3dView.kDormantColors)
			glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
			last = kArrow2Count - 1
			for i in range(last):
				glFT.glVertex3f((-arrow2[i][0] * multiplier * math.cos(angle2) - arrow2[i][2] * multiplier * math.sin(angle2)),
								(arrow2[i][1] * multiplier + delta2),
								(arrow2[i][2] * multiplier * math.cos(angle2) - arrow2[i][0] * multiplier * math.sin(angle2)))
			glFT.glEnd()

			if (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor(13, OpenMayaUI.M3dView.kActiveColors)
			else:
				view.setDrawColor(13, OpenMayaUI.M3dView.kDormantColors)
			glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
			last = kArrow3Count - 1
			for i in range(last):
				glFT.glVertex3f((-arrow3[i][0] * multiplier * math.cos(angle3) - arrow3[i][2] * multiplier * math.sin(angle3)),
								(arrow3[i][1] * multiplier + delta3),
								(arrow3[i][2] * multiplier * math.cos(angle3) - arrow3[i][0] * multiplier * math.sin(angle3)))
			glFT.glEnd()

			if (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor(5, OpenMayaUI.M3dView.kActiveColors)
			else:
				view.setDrawColor(5, OpenMayaUI.M3dView.kDormantColors)
			glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
			last = kArrow4Count - 1
			for i in range(last):
				glFT.glVertex3f((arrow4[i][0] * multiplier),
								(arrow4[i][1] * multiplier + delta4),
								(arrow4[i][2] * multiplier))
			glFT.glEnd()

			glFT.glPopAttrib()

		# Draw the outline of the locator
		glFT.glBegin(OpenMayaRender.MGL_LINES)

		if toggle:
			last = kCentreCount - 1
			for i in range(last): 
				glFT.glVertex3f(centre[i][0] * multiplier, 
								centre[i][1] * multiplier, 
								centre[i][2] * multiplier)
				glFT.glVertex3f(centre[i+1][0] * multiplier, 
								centre[i+1][1] * multiplier, 
								centre[i+1][2] * multiplier)

		if (state == 0):
			last = kState1Count - 1
			for i in range(last): 
				glFT.glVertex3f(state1[i][0] * multiplier, 
								state1[i][1] * multiplier, 
								state1[i][2] * multiplier)
				glFT.glVertex3f(state1[i+1][0] * multiplier, 
								state1[i+1][1] * multiplier, 
								state1[i+1][2] * multiplier)

		if (state == 1):
			last = kState2Count - 1
			for i in range(last): 
				glFT.glVertex3f(state2[i][0] * multiplier, 
								state2[i][1] * multiplier, 
								state2[i][2] * multiplier)
				glFT.glVertex3f(state2[i+1][0] * multiplier, 
								state2[i+1][1] * multiplier, 
								state2[i+1][2] * multiplier)

		if (state == 2):
			last = kState3Count - 1
			for i in range(last): 
				glFT.glVertex3f(state3[i][0] * multiplier, 
								state3[i][1] * multiplier, 
								state3[i][2] * multiplier)
				glFT.glVertex3f(state3[i+1][0] * multiplier, 
								state3[i+1][1] * multiplier, 
								state3[i+1][2] * multiplier)

		if (state == 3):
			last = kState4Count - 1
			for i in range(last): 
				glFT.glVertex3f(state4[i][0] * multiplier, 
								state4[i][1] * multiplier, 
								state4[i][2] * multiplier)
				glFT.glVertex3f(state4[i+1][0] * multiplier, 
								state4[i+1][1] * multiplier, 
								state4[i+1][2] * multiplier)

		last = kArrow1Count - 1
		for i in range(last): 
			glFT.glVertex3f((-arrow1[i][0] * multiplier * math.cos(angle1) - arrow1[i][2] * multiplier * math.sin(angle1)),
							(arrow1[i][1] * multiplier + delta1),
							(arrow1[i][2] * multiplier * math.cos(angle1) - arrow1[i][0] * multiplier * math.sin(angle1)))
			glFT.glVertex3f((-arrow1[i+1][0] * multiplier * math.cos(angle1) - arrow1[i+1][2] * multiplier * math.sin(angle1)),
							(arrow1[i+1][1] * multiplier + delta1),
							(arrow1[i+1][2] * multiplier * math.cos(angle1) - arrow1[i+1][0] * multiplier * math.sin(angle1)))

		last = kArrow2Count - 1
		for i in range(last): 
			glFT.glVertex3f((-arrow2[i][0] * multiplier * math.cos(angle2) - arrow2[i][2] * multiplier * math.sin(angle2)),
							(arrow2[i][1] * multiplier + delta2),
							(arrow2[i][2] * multiplier * math.cos(angle2) - arrow2[i][0] * multiplier * math.sin(angle2)))
			glFT.glVertex3f((-arrow2[i+1][0] * multiplier * math.cos(angle2) - arrow2[i+1][2] * multiplier * math.sin(angle2)),
							(arrow2[i+1][1] * multiplier + delta2),
							(arrow2[i+1][2] * multiplier * math.cos(angle2) - arrow2[i+1][0] * multiplier * math.sin(angle2)))

		last = kArrow3Count - 1
		for i in range(last): 
			glFT.glVertex3f((-arrow3[i][0] * multiplier * math.cos(angle3) - arrow3[i][2] * multiplier * math.sin(angle3)),
							(arrow3[i][1] * multiplier + delta3),
							(arrow3[i][2] * multiplier * math.cos(angle3) - arrow3[i][0] * multiplier * math.sin(angle3)))
			glFT.glVertex3f((-arrow3[i+1][0] * multiplier * math.cos(angle3) - arrow3[i+1][2] * multiplier * math.sin(angle3)),
							(arrow3[i+1][1] * multiplier + delta3),
							(arrow3[i+1][2] * multiplier * math.cos(angle3) - arrow3[i+1][0] * multiplier * math.sin(angle3)))

		last = kArrow4Count - 1
		for i in range(last): 
			glFT.glVertex3f((arrow4[i][0] * multiplier),
							(arrow4[i][1] * multiplier + delta4),
							(arrow4[i][2] * multiplier))
			glFT.glVertex3f((arrow4[i+1][0] * multiplier),
							(arrow4[i+1][1] * multiplier + delta4),
							(arrow4[i+1][2] * multiplier))

		last = kPerimeterCount - 1
		for i in range(last): 
			glFT.glVertex3f(perimeter[i][0] * multiplier,
							perimeter[i][1] * multiplier,
							perimeter[i][2] * multiplier)
			glFT.glVertex3f(perimeter[i+1][0] * multiplier,
							perimeter[i+1][1] * multiplier,
							perimeter[i+1][2] * multiplier)

		glFT.glEnd()

		view.endGL()


	def isBounded(self):
		return True


	def boundingBox(self):
		thisNode = self.thisMObject()
		plug = OpenMaya.MPlug(thisNode, swissArmyLocator.aSize)
		sizeVal = plug.asMDistance()

		multiplier = sizeVal.asCentimeters()

		corner1 = OpenMaya.MPoint(-1.1, 0.0, -1.1)
		corner2 = OpenMaya.MPoint(1.1, 0.0, 1.1)

		corner1 = corner1 * multiplier
		corner2 = corner2 * multiplier

		return OpenMaya.MBoundingBox(corner1, corner2)



########################################################################
########################################################################


def locatorCreator():
	return swissArmyLocator()


def locatorInit():
	unitFn = OpenMaya.MFnUnitAttribute()
	numericFn = OpenMaya.MFnNumericAttribute()

	# aSize
	swissArmyLocator.aSize = unitFn.create("size", "sz", OpenMaya.MFnUnitAttribute.kDistance, 10.0)
	unitFn.setStorable(True)
	unitFn.setWritable(True)

	# aPoint
	swissArmyLocator.aPointX = numericFn.create("pointX", "ptx", OpenMaya.MFnNumericData.kDouble, 0.0)
	swissArmyLocator.aPointY = numericFn.create("pointY", "pty", OpenMaya.MFnNumericData.kDouble, 0.0)
	swissArmyLocator.aPointZ = numericFn.create("pointZ", "ptz", OpenMaya.MFnNumericData.kDouble, 0.0)
	swissArmyLocator.aPoint = numericFn.create("point", "pt", swissArmyLocator.aPointX, swissArmyLocator.aPointY, swissArmyLocator.aPointZ)

	# aArrow1Angle
	swissArmyLocator.aArrow1Angle = unitFn.create("arrow1Angle", "a1a", OpenMaya.MFnUnitAttribute.kAngle, 0.0)

	# aArrow2Direction
	swissArmyLocator.aArrow2DirectionX = numericFn.create("arrow2DirectionX", "a2x", OpenMaya.MFnNumericData.kDouble, 1.0)
	swissArmyLocator.aArrow2DirectionY = numericFn.create("arrow2DirectionY", "a2y", OpenMaya.MFnNumericData.kDouble, 0.0)
	swissArmyLocator.aArrow2DirectionZ = numericFn.create("arrow2DirectionZ", "a2z", OpenMaya.MFnNumericData.kDouble, 0.0)
	swissArmyLocator.aArrow2Direction = numericFn.create("arrow2Direction", "dir", swissArmyLocator.aArrow2DirectionX, swissArmyLocator.aArrow2DirectionY, swissArmyLocator.aArrow2DirectionZ)

	# aArrow3Angle
	swissArmyLocator.aArrow3Angle = unitFn.create("arrow3Angle", "a3a", OpenMaya.MFnUnitAttribute.kAngle, 0.0)
	# aArrow4Distance
	swissArmyLocator.aArrow4Distance = unitFn.create("arrow2Distance", "dis", OpenMaya.MFnUnitAttribute.kDistance, 0.0)

	# aState
	swissArmyLocator.aState = numericFn.create("state", "s", OpenMaya.MFnNumericData.kLong, 0)

	# aToggle
	swissArmyLocator.aToggle = numericFn.create("toggle", "t", OpenMaya.MFnNumericData.kBoolean, False)

	swissArmyLocator.addAttribute(swissArmyLocator.aPoint)
	swissArmyLocator.addAttribute(swissArmyLocator.aArrow1Angle)
	swissArmyLocator.addAttribute(swissArmyLocator.aArrow2Direction)
	swissArmyLocator.addAttribute(swissArmyLocator.aArrow3Angle)
	swissArmyLocator.addAttribute(swissArmyLocator.aArrow4Distance)
	swissArmyLocator.addAttribute(swissArmyLocator.aState)
	swissArmyLocator.addAttribute(swissArmyLocator.aToggle)
	swissArmyLocator.addAttribute(swissArmyLocator.aSize)

	OpenMayaMPx.MPxManipContainer.addToManipConnectTable(kSwissArmyLocatorId)


def locatorManipCreator():
     return swissArmyLocatorManip()


def locatorManipInit():
    OpenMayaMPx.MPxManipContainer.initialize()


# initialize the script plug-in
	try:
								locatorCreator,
								locatorInit,
								OpenMayaMPx.MPxNode.kLocatorNode)
	try:
								locatorManipCreator, 
								locatorManipInit,
								OpenMayaMPx.MPxNode.kManipContainer)

# uninitialize the script plug-in
	try:
	try: