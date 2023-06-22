from inc_noesis import *

import noesis

import rapi

def registerNoesisTypes():
	handle = noesis.register("XNALara/XPS", ".ascii")
	noesis.setHandlerTypeCheck(handle, xpsCheckType)
	noesis.setHandlerLoadModel(handle, xpsLoadModel)
	return 1
	
def xpsCheckType(data):
	td = NoeBitStream(data)
	return 1

def parseStr(string):
	str = string.split(' ')
	return str[0]
	
def strToInt(str):
	return int(parseStr(str))

def strToFloat(str):
	return float(parseStr(str))

def strToVec(str):
	return str.split(' ')
	
def trim(s):
	if s != '':
		if s[len(s) - 1] == ' ':
			s = s[:len(s)-1]
		if s[0] == ' ':
			s = s[1:]
	return s
	
def readLine(bs):
	ret = bs.readline().split('\r')
	ret = ret[0].split('\n')
	ret[0] = trim(ret[0])
	return ret[0]
	
def loadBones(bs, numBones, bones):
	for i in range(numBones):
		boneIndex = i
		boneName = readLine(bs)
		parentIndex = strToInt(readLine(bs))
		#boneCoordsStr = strToVec(readLine(bs))
		boneStr = readLine(bs).split()
		boneCoords = NoeVec3((float(boneStr[0]) * 100.0, float(boneStr[1]) * 100.0, float(boneStr[2]) * 100.0))
		if len(boneStr)>3:
			quat = []
			quat.append(float(boneStr[3]))
			quat.append(float(boneStr[4]))
			quat.append(float(boneStr[5]))
			quat.append(float(boneStr[6]))
			boneMat = NoeQuat(quat).toMat43().inverse()
		else:
			boneMat = NoeMat43()	
		boneMat[3] = boneCoords
		bone = NoeBone(boneIndex, boneName, boneMat, None, parentIndex)
		bones.append(bone)
		
def loadMeshes(bs, numBones, numberMeshes, meshes, matList):
	for i in range(numberMeshes):
		meshName = parseStr(readLine(bs))
		numUVlayers = strToInt(readLine(bs))
		numTextures = strToInt(readLine(bs))
		for t in range(numTextures):
			texture = parseStr(readLine(bs))
			texName = rapi.getLocalFileName(texture)
			print(meshName + " Texture Used: " + texName)
			layerIndex = strToInt(readLine(bs))

		idxList = []
		posList = []
		normalList = []
		colorList = []
		weightList = []
		uvList = []
		uvList2 = []
		uvList3 = []
		uvList4 = []
		numVertices = strToInt(readLine(bs))
		for v in range(numVertices):
			vertCoordsStr = strToVec(readLine(bs))
			vertCoords = NoeVec3((float(vertCoordsStr[0]) * 100.0, float(vertCoordsStr[1]) * 100.0, float(vertCoordsStr[2]) * 100.0))
			posList.append(vertCoords)

			normCoordsStr = strToVec(readLine(bs))
			normCoords = NoeVec3((float(normCoordsStr[0]), float(normCoordsStr[1]), float(normCoordsStr[2])))	
			normalList.append(normCoords)

			cs = strToVec(readLine(bs))
			rgba = NoeVec4()
			for c in range(0, 4):
				if cs[c] != '0':
					rgba[c] = 255.0 / float(cs[c])
			colorList.append(rgba)

			uv = NoeVec3()
			uv2 = NoeVec3()
			uv3 = NoeVec3()
			uv4 = NoeVec3()
			for u in range(numUVlayers):
				uvStr = strToVec(readLine(bs))
				if u == 0:
					uv[0] = float(uvStr[0])
					uv[1] = float(uvStr[1])
				elif u == 1:
					uv2[0] = float(uvStr[0])
					uv2[1] = float(uvStr[1])
				elif u == 2:
					uv3[0] = float(uvStr[0])
					uv3[1] = float(uvStr[1])
				elif u == 3:
					uv4[0] = float(uvStr[0])
					uv4[1] = float(uvStr[1])
			uvList.append(uv)
			uvList2.append(uv2)
			uvList3.append(uv3)
			uvList4.append(uv4)

			if numBones > 0:
				indices = readLine(bs).split()
				weights = readLine(bs).split()
				bidx = []
				bwgt = []
				for j in range(0, len(weights)):
					bidx.append(int(indices[j]))
					bwgt.append(float(weights[j]))
				weightList.append(NoeVertWeight(bidx, bwgt))

		numFaces = strToInt(readLine(bs))
		for f in range(0, numFaces):
			face = []
			face = strToVec(readLine(bs))
			idxList.append(int(face[0]))
			idxList.append(int(face[2]))
			idxList.append(int(face[1]))

		ignoreTex = "tex"
		mesh = NoeMesh(idxList, posList, meshName, ignoreTex)
		mesh.normals = normalList
		mesh.weights = weightList
		mesh.colors = colorList
		mesh.setUVs(uvList)
		mesh.setUVs(uvList2, 1)
		#mesh.setUVs(uvList3, 2)
		#mesh.setUVs(uvList4, 3)
		meshes.append(mesh)
	return 1

def xpsLoadModel(data, mdlList):
	matList = []
	bs = NoeBitStream(data)
	numBones = strToInt(readLine(bs))
	print('Number of bones: ' + str(numBones))
	bones = []
	loadBones(bs, numBones, bones)

	numberMeshes = strToInt(readLine(bs))
	meshes = []
	if loadMeshes(bs, numBones, numberMeshes, meshes, matList) == 0:
		return 0

	mdl = NoeModel(meshes, bones)
	
	materials = NoeModelMaterials(None, matList)
	mdl.setModelMaterials(materials)

	mdlList.append(mdl)

	return 1