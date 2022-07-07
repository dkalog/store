import numpy as np
import os
from os import path
import math
import readCSV
import readJSON
import cv2
import plotPE

_ZEROANGLES = 1E-10

def RTOD(a):
	return (a*(180.0/math.pi))

def vec2quat(rot,qo):


	th=math.sqrt(math.pow(rot[0],2)+math.pow(rot[1],2)+math.pow(rot[2],2))
	if th>_ZEROANGLES:
	    hth=th*0.5
	    s= math.sin(hth)
	    qo[0]=math.cos(hth)
	    s=s/th
	    qo[1]=rot[0]*s
	    qo[2]=rot[1]*s
	    qo[3]=rot[2]*s
	    
	else:
		qo[0]=1.0
		qo[1]=qo[2]=qo[3]=0.0
	
	return qo

def quat2rotmat(q, R):
	w,x,y,z = q[0],q[1],q[2],q[3]
	s=2.0/(w*w + x*x + y*y + z*z)

	xs,ys,zs = x*s,y*s,z*s
	wx,wy,wz = w*xs,w*ys,w*zs
	xx,xy,xz = x*xs,x*ys,x*zs
	yy,yz,zz=y*ys,y*zs,z*zs

	R[0]=1.0 - yy - zz
	R[1]=xy - wz
	R[2]=xz + wy

	R[3]=xy + wz
	R[4]=1.0 - xx - zz
	R[5]=yz - wx

	R[6]=xz - wy
	R[7]=yz + wx
	R[8]=1.0 - xx - yy

	return R

def _clamp(a, b, x):
	return max(min(x,b),a)

def motionError(r,rg,t,tg):
	q=np.zeros(4)
	qg=np.zeros(4)
	q=vec2quat(r, q)
	qg=vec2quat(rg, qg)
	
	a=tg[0]-t[0]
	b=tg[1]-t[1]
	c=tg[2]-t[2]
	terr=math.sqrt(a*a + b*b + c*c)
	
	Rg=np.zeros(9)
	R=np.zeros(9)
	
	Rg=quat2rotmat(qg, Rg)
	R=quat2rotmat(q, R)
	
	a=Rg[0]*R[0] + Rg[3]*R[3] + Rg[6]*R[6]
	b=Rg[1]*R[1] + Rg[4]*R[4] + Rg[7]*R[7]
	c=Rg[2]*R[2] + Rg[5]*R[5] + Rg[8]*R[8]
	trc=a+b+c
	
	a=0.5*(trc-1.0)

	"""
	Rg=Rg.reshape((3,3))
	R=R.reshape((3,3))
	r, _ = cv2.Rodrigues(R.dot(np.transpose(Rg)))

	rot_error = np.linalg.norm(r)	
	print(f"ROTATION ERROR = {RTOD(rot_error)}")
	"""
	print(f" a = {a}")
	aerr=math.acos(_clamp(-1.0, 1.0, a))


	return terr,aerr

def motionRelError(rest, rtrue,test,ttrue):
  
  qest=np.zeros(4)
  qtrue=np.zeros(4)	

  qest=vec2quat(rest, qest)
  qtrue=vec2quat(rtrue, qtrue)

  denom=(qtrue[0]*qtrue[0] + qtrue[1]*qtrue[1] + qtrue[2]*qtrue[2] + qtrue[3]*qtrue[3])

  aerr1=math.sqrt((
      (qtrue[0] - qest[0])*(qtrue[0] - qest[0]) +
      (qtrue[1] - qest[1])*(qtrue[1] - qest[1]) +
      (qtrue[2] - qest[2])*(qtrue[2] - qest[2]) +
      (qtrue[3] - qest[3])*(qtrue[3] - qest[3]) ) / denom)

  # take care of possibly erroneous sign 
  aerr2=math.sqrt((
      (qtrue[0] + qest[0])*(qtrue[0] + qest[0]) +
      (qtrue[1] + qest[1])*(qtrue[1] + qest[1]) +
      (qtrue[2] + qest[2])*(qtrue[2] + qest[2]) +
      (qtrue[3] + qest[3])*(qtrue[3] + qest[3]) ) / denom)

  if aerr1<=aerr2:
  	aerr=aerr1
  else:
  	aerr=aerr2
  
  terr=math.sqrt((
      (ttrue[0] - test[0])*(ttrue[0] - test[0]) +
      (ttrue[1] - test[1])*(ttrue[1] - test[1]) +
      (ttrue[2] - test[2])*(ttrue[2] - test[2])) /
      (ttrue[0]*ttrue[0] + ttrue[1]*ttrue[1] + ttrue[2]*ttrue[2]) )

  return terr,aerr
def main():
	
	rot=np.array([-0.7687228589660535,-0.6395656483477845 ,-0.004576850066902893, -0.20235592657698573, 0.24999667658115354, -0.9468652177990003, 0.6067266642255197, -0.7269507845458706, -0.32159805933170227])
	trans=np.array([-14.359012647477527, 38.59186488570627, 17961.490988514553])
	rotg=np.array([-0.766044, -0.642788, 0.000000, -0.198632, 0.236721, -0.951056, 0.611327, -0.728552, -0.309017])
	transg=np.array([-0.000977, 0.000000, 18000.000000])
	
	#get absolute path of script
	abs_path = os.path.dirname(os.path.realpath(__file__))
	print("Absolute directory of python file : ",abs_path)

	R,T,imID,time,infile = readCSV.csvRead('PROGRESSIVEX_carObj1-test2.csv') # read file with estimated poses
	Rg,Tg,imIDgt = readJSON.readJson('scene_gt2.json')# read ground truth poses from json

	#sort the entries
	srimID = imID.argsort()
	R = R[srimID[::1]]
	T=T[srimID[::1]]
	imID = imID[srimID[::1]]

	terrAR = []
	terrREAR = []
	print(len(imID))
	for id in range(0,len(imID)):


			#print(f"Ground truth rotation is \n{Rg[0]}\n and estimated is \n{R[0]}")
			#print(f"Ground truth translation is \n{Tg[0]}\n and estimated is \n{T[0]}")
	
	
			terrME,aerrME = motionError(R[id],Rg[id],T[id],Tg[id])
			#terrAR=np.vstack([terrAR,[int(imID[id]),terrME,RTOD(aerrME)]])
			terrAR.append([int(imID[id]),terrME,RTOD(aerrME)])
			#print("translational error %g, angular %g\n", terrME, RTOD(aerrME))



			terrRE,aerrRE = motionRelError(R[id],Rg[id],T[id],Tg[id])
			terrREAR.append([int(imID[id]),terrRE,RTOD(aerrRE)])
			#print("relative translational error %g, angular %g\n", terrRE, aerrRE)
	terrREAR=np.array(terrREAR)
	terrAR=np.array(terrAR)
	print(terrREAR[0:1])
	print(terrAR[290])
	print(f"Max angular error : {np.max(terrAR[0:len(imID),2])}")
	np.set_printoptions(suppress=True)
	
	outfile_path = os.path.join(abs_path,"results_csv")
	if(path.exists(outfile_path)==False):
		os.mkdir(outfile_path)
	outfilename = infile.split(".")[0]+'_res.csv'
	np.savetxt(os.path.join(outfile_path,outfilename),np.concatenate((terrAR,terrREAR[:,1:]),axis=1),header='im_id,Tar_error,Rar_error,Tre_error,Rre_error',delimiter=',',fmt='%f')



	#plot histogramm of angular error
	#print(terrAR[0:len(imID),2])
	plotPE.histogram(abs_path,len(imID),50,terrAR[0:len(imID),2],title=infile.split(".")[0]+"_histogram",typE="angular")
	plotPE.scatterplot(abs_path,terrAR[0:len(imID),2],imID,color='r',title=infile.split(".")[0]+"_scatterplot",typE="angular")

	plotPE.histogram(abs_path,len(imID),50,terrAR[0:len(imID),1],title=infile.split(".")[0]+"_histogram",typE="translation")
	plotPE.scatterplot(abs_path,terrAR[0:len(imID),1],imID,color='r',title=infile.split(".")[0]+"_scatterplot",typE="translation")

	plotPE.histogram(abs_path,len(imID),50,terrREAR[0:len(imID),2],title=infile.split(".")[0]+"_histogram",typE="Relative angular")
	plotPE.scatterplot(abs_path,terrREAR[0:len(imID),2],imID,color='r',title=infile.split(".")[0]+"_scatterplot",typE="Relative angular")

	plotPE.histogram(abs_path,len(imID),50,terrREAR[0:len(imID),1],title=infile.split(".")[0]+"_histogram",typE="Relative translation")
	plotPE.scatterplot(abs_path,terrREAR[0:len(imID),1],imID,color='r',title=infile.split(".")[0]+"_scatterplot",typE="Relative translation")
if __name__ == "__main__":
	main()
