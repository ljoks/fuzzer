# fuzzer
Cybersecurity Fuzz Testing Implementation

The target program `jpgbmp` converts jpg images to bmp files. Our goal is to use a mutation based fuzzing technique to uncover 7 bugs in the program.

For details of implementation and results, see `PA2 Report.pdf`

## Instructions to Run
Make sure `jpgbmp` is executable
```
$chmod u+x  jpgbmp
```

Test the jpgbmp executable
```
./jpgbmp cross.jpg cross.bmp
```

Run the fuzzer
```
python fuzzer.py
```
Any mutation jpgs that trigger bugs will be saved in a folder that is named by the
current timestamp.
