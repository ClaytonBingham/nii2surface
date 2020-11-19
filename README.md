nii2surface takes a nifti brain image stack, identifies a particular target voxel value (perhaps a label from an atlas) and creates a surface from the labeled voxels using Poisson Surface Reconstruction. If you use this class in your own work, kindly cite: "Bingham C.S., Parent M., McIntyre, C.C. Histology-Driven Model of the Macaque Hyperdirect Pathway. In Review."

![Example Brain Surface](https://github.com/bingsome/nii2surface/blob/master/docs/gif.gif)

	Dependencies: Python3, nibabel, and PoissonRecon (available at: https://github.com/mkazhdan/PoissonRecon)
	
	Usage: This can be used as a standalone script by editing the Main() section below, or by importing nii2surface and scripting as follows:
	
	```
	if __name__ == "__main__":
			surfacemaker = nii2surface(os.getcwd()+'/macaque_volume_conductor/Macaque_subject2_segmentation/sub-02_T1w_skullstripped.nii.gz',resolution=0.5,target_label=None)
			os.chdir(os.getcwd()+'/PoissonRecon/Bin/Linux')
			print('running PoissonRecon')
			sp.call('./PoissonRecon --in pointsnormals.txt --out brain.ply --depth 7',shell=True)
	```
	
	nii2surface() takes the following arguments:
	fname - name of the nifti file you would like to create a surface from
	resolution - 1d voxel size (e.g. 0.5mm)
	target_label - voxel value corresponding to the particular volume you wish to create a surface from. 
	The default value is None, in this case, the script will attempt to create a surface from the entire image stack for all values greater than 1 (presumed to be a reasonable background threshold)
