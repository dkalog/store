import os, sys
import numpy as np
import re


def csvRead(filename):

	#initialize arrays for data
	R = np.empty([1,9])

	#print(R)
   
	T = np.empty([1,3])

	time=np.array([])
	imID = np.array([])

	#filename = 'estimated-poses.csv'
	line_count=0
	with open(filename, 'r') as file:
		next(file)
		for line in file:
			splited = re.split(',| ',line)
			#print(splited[1])
			
			imID= np.append(imID,splited[1]).astype(int)
			#print(splited[16])
			time = np.append(time,splited[16]).astype(float)
			#R.shape(1,len(splited))
			R=np.vstack([R,np.array(splited[4:13]).astype(float)])
			#print(R[0])
			T=np.vstack([T,np.array(splited[13:16])]).astype(float)
			#print(T)
			line_count+=1
			
		#print(imID)
		#print(time)

		#print(T)
		R=np.delete(R,0,0)
		T=np.delete(T,0,0)
		print(f"Proccessed images {line_count}")

	return R,T,imID,time,filename



"""
def main():
	R,T,imID,time = csvRead('estimated-poses.csv')

	print(R)
	print(T)
	print(imID)
	print(time)
"""