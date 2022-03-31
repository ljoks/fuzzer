from mutate import magic, rand
from random import randint
from subprocess import Popen, PIPE, STDOUT
from time import strftime, localtime
import os

# directory to save mutated image files
directory = strftime("%Y-%m-%d_%H_%M_%S", localtime())

# read bytes from cross.jpg and return them as an array
def get_bytes():

	f = open("cross.jpg", "rb").read()
	return bytearray(f)

# save the mutated image in case it triggers a bug
def save_mutated(mutated_image, fname):
	print(fname)
	f = open(fname, "wb")
	f.write(mutated_image)
	f.close()

# run the jpgbmp program using a provided input and output file
def run(input, output):
	process = Popen(["./jpgbmp", input, output],
															stdout=PIPE,
															stderr=STDOUT)
	stdout, stderr = process.communicate()
	# return the output from the cmd line
#	print(stdout) 
	return stdout

# analyze the output of the cmd line to determine if the 
# mutated image produced a bug.
def analyze(program_output, input_file, output_file, bugs_triggered, bug_num,):
	# decode the output	
	program_output = program_output.decode("utf-8")
	
	# if the mutated image produced a bug:
	if 'You triggered Bug' in program_output:
		# get the bug number from the cmd line output
		bug = int(program_output.split(" ")[3][1])
		# increment the number of times that bug was triggered
		bugs_triggered[bug-1] += 1

		# rename the input file to append the bug triggered
		#print("File " + input_file + " triggered bug #" + bug + ". Saving...")
		print("File {} triggered bug #{}. Saving...".format(input_file, bug))
		#os.rename(input_file, input_file.split(".")[0] + "-" + bug + ".jpg")
		os.rename(input_file, "{}-{}.jpg".format(input_file.split(".")[0], bug))
		
		# see if that bug was already found
		if bug not in bug_num:
			bug_num.append(bug)
	
	# mutated image did not produce a bug. delete file
	else: 
		os.remove(input_file)
		if os.path.exists(output_file):
			os.remove(output_file)

# 8 possible bugs
bugs_triggered = [0,0,0,0,0,0,0,0]
bug_num = []

#create directory to save mutated image files
os.mkdir(directory)

# make 10 thousand mutations
for i in range(10000):
	# read the image file
	image = get_bytes()
	# mutate the image
	mutated_image = rand(image) if i%2 == 0 else  magic(image)
	# save the mutated image in case it triggers a bug
	input_file = os.path.join(directory, "test{}.jpg".format(i))
	save_mutated(mutated_image, input_file)

	# run jpgbmp on the mutated image
	output_file = os.path.join(directory, "test{}.bmp".format(i))
	program_output = run(input_file, output_file)

	# analyze the output to see if it triggered a bug
	analyze(program_output, input_file, output_file, bugs_triggered, bug_num,)

	# in case we trigger all 8 bugs early, stop the program
	if len(bug_num) >= 8:
		print("All 8 bugs triggered. stopping early")
		break	

print("---------------Results---------------")
print("Of {} files mutated, {} triggered bugs.".format(i+1, sum(bugs_triggered)))

for i in range(8):
	print("Bug {}: {} times".format(i+1, bugs_triggered[i]))
