import cv2
import numpy as np
from matplotlib import pyplot as plt


def printParenthesis(str, n): 
	if(n > 0): 
		_printParenthesis(str, 0,  
						  n, 0, 0); 
	return; 
  
def _printParenthesis(str, pos, n,  
					  open, close): 
	# print(pos)
	if(close == n): 
		for i in str: 
			print(i, end = ""); 
		print(); 
		return; 
	else: 
		if(open > close): 
			# str[pos] = '}';
			newStr = str + "}" 
			_printParenthesis(newStr, pos + 1, n,  
							  open, close + 1); 
		if(open < n): 
			newStr = str + "{"; 
			_printParenthesis(newStr, pos + 1, n,  
							  open + 1, close); 
  

def sorted_search(elements,target):
	if not elements or len(elements)<= 0:
		return -1
	left = 0 
	right = len(elements) - 1
	while left < right:
		print("left is ",left)
		middle = (left + right + 1)//2

		if elements[middle] > target:
			right = middle -1
		else:
			left = middle + 1
	if elements[right] == target:
		return right
	return -1

def count_palindromes(S):
	len_s = len(S)
	pal_list = []
	for i in range(len(S)):
		char = S[i]
		pal_list.append([char,i,i])
	for i in range(len(S)-1):
		if S[i] == S[i+1]:
			pal_list.append([S[i]+S[i+1],i,i+1])
	new_pal_list = []
	for pal in pal_list:
		new_pal_list.append(pal)
	while(len(new_pal_list)>0):
		# print("wow")
		# print(pal)
		# print(len(new_pal_list))
		pal = new_pal_list[0]
		new_pal_list= new_pal_list[1:]
		i = pal[1]
		j = pal[2]
		if i > 0 and j < len(S)-1:
			if S[i-1] == S[j+1]:
				print("wtf")
				pal_list.append([S[i-1:j+2],i-1,j+1])
				new_pal_list.append([S[i-1:j+2],i-1,j+1])
	print(pal_list)
	return len(pal_list)

def edge():
	img = cv2.imread('Assets/sung.jpg',0)
	edges = cv2.Canny(img,50,200)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
	plt.show()
def checkValidString(s):
		lo = hi = 0
		for c in s:
			# print("lo,hi = ",lo,hi)
			if c == "(":
				lo += 1 
			else:
				lo -= 1
			if c != ")":
				hi += 1
			else:
				hi -= 1
			if hi < 0:
				break
			print("c,lo,hi = ",c,lo,hi)
			lo = max(lo,0)
			print("c,lo,hi = ",c,lo,hi)
			print("\n")

		return lo == 0


def main():
	n = 3; 
	str = [""] * 2 * n; 
	# printParenthesis("", n); 
	elem = [1,3,5,7]
	target = 5
	# print(sorted_search(elem,target))
	# print(count_palindromes("hellolle"))
	print(checkValidString("(**)))"))







if __name__ == '__main__':
	main()