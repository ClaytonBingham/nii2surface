#!/usr/bin/env python3
import nibabel as nib
import numpy as np
import subprocess as sp
import os

class nii2surface():
	'''
	nii2surface takes a nifti brain image stack, identifies a particular target voxel value (perhaps a label from an atlas) and creates a surface from the labeled voxels using Poisson Surface Reconstruction. If you use this class in your own work, kindly cite: "Bingham C.S., Parent M., McIntyre, C.C. Histology-Driven Model of the Macaque Hyperdirect Pathway. In Review."
	
	Dependencies: Python3, nibabel, and PoissonRecon (available at: https://github.com/mkazhdan/PoissonRecon)
	
	Usage: This can be used as a standalone script by editing the Main() section below, or by importing nii2surface and scripting as follows:
	
	`if __name__ == "__main__":
	`		surfacemaker = nii2surface(os.getcwd()+'/macaque_volume_conductor/Macaque_subject2_segmentation/sub-02_T1w_skullstripped.nii.gz',resolution=0.5,target_label=None)
	`		os.chdir(os.getcwd()+'/PoissonRecon/Bin/Linux')
	`		print('running PoissonRecon')
	`		sp.call('./PoissonRecon --in pointsnormals.txt --out brain.ply --depth 7',shell=True)
	
	nii2surface() takes the following arguments:
	fname - name of the nifti file you would like to create a surface from
	resolution - 1d voxel size (e.g. 0.5mm)
	target_label - voxel value corresponding to the particular volume you wish to create a surface from. 
	The default value is None, in this case, the script will attempt to create a surface from the entire image stack for all values greater than 1 (presumed to be a reasonable background threshold)
	
	'''
	def __init__(self,fname,resolution=0.5,target_label=None):
		self.resolution = resolution
		self.target_label=target_label
		img = nib.load(os.getcwd()+'/macaque_volume_conductor/Macaque_subject2_segmentation/sub-02_T1w_skullstripped.nii.gz')
		data = img.get_fdata()
		
		if self.target_label is not None:
			data = np.where(data!=self.target_label,0,data)

		#remove background and threshold
		data = np.where(data==1,0,data) 
		print('got data...calculating normals')
		normals = self.calculate_voxel_normals(data)
		print('starting to write points/normals')
		self.write_points_normals(os.getcwd()+'/PoissonRecon/Bin/Linux/',normals,resolution=self.resolution)
	
	def locate_voxels_by_value(self,data,value=None):
		'''
		locate voxels in numpy array with a particular value
		
		'''
		if value==None:		
			coords = []
			X,Y,Z = data.shape
			for x in range(X):
				for y in range(Y):
					for z in range(Z):
						if data[x][y][z] > 0:
							coords.append([x,y,z])

		else:
			coords = []
			X,Y,Z = data.shape
			for x in range(X):
				for y in range(Y):
					for z in range(Z):
						if data[x][y][z] == value:
							coords.append([x,y,z])
		
		return(coords)

	def get_surrounding_voxels(self,voxel,data):
		vox_ = dict()
		for x in range(-1,2):
			for y in range(-1,2):
				for z in range(-1,2):
					try:
						vox_[(x,y,z)] = data[voxel[0]+x][voxel[1]+y][voxel[2]+z]
					except:
						continue
		
		del(vox_[(0,0,0)])
		return(vox_)
		
	def weigh_neighbors(self,neighbors):
		summed = 0
		for key in neighbors.keys():
			summed+=neighbors[key]
		
		weights = dict()
		if summed == 0:
			for key in neighbors.keys():
				weights[key] = 0
		else:
			for key in neighbors.keys():
				weights[key] = neighbors[key]/summed
		
		return(weights)

	def calculate_normal_from_weights(self,weights):
		normal = np.array([0,0,0])
		for key in weights.keys():
			normal=normal+np.array(key)*weights[key]
		
		return(normal)


	def calculate_voxel_normals(self,data):
		shapex,shapey,shapez = data.shape
		shapenorm = 3
		normals = np.zeros((shapex,shapey,shapez,shapenorm))
		maxx,maxy,maxz = data.shape
		for x in range(maxx):
			for y in range(maxy):
				for z in range(maxz):
					neighbors = self.get_surrounding_voxels([x,y,z],data)
					weights = self.weigh_neighbors(neighbors)
					normals[x][y][z] = self.calculate_normal_from_weights(weights)
		
		return(normals)

	def write_points_normals(self,outputdir,normals,resolution):
		with open(outputdir+'pointsnormals.txt','wb') as f:
			X,Y,Z,n = normals.shape
			for x in range(X):
				for y in range(Y):
					for z in range(Z):
						point = str(resolution*(x-X/2.0))+' '+str(resolution*(y-Y/2.0))+' '+str(resolution*(z-Z/2.0))+' '+str(normals[x][y][z][0])+' '+str(normals[x][y][z][1])+' '+str(normals[x][y][z][2])+'\n'
						f.write(point.encode('ascii'))


if __name__ == "__main__":
	surfacemaker = nii2surface(os.getcwd()+'/macaque_volume_conductor/Macaque_subject2_segmentation/sub-02_T1w_skullstripped.nii.gz',resolution=0.5,target_label=None)
	os.chdir(os.getcwd()+'/PoissonRecon/Bin/Linux')
	print('running PoissonRecon')
	sp.call('./PoissonRecon --in pointsnormals.txt --out brain.ply --depth 7',shell=True)



