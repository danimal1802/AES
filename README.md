# AES Implementation - ECB Primitive in Python
AES Implementation - ECB primitive in Python using basic libraries - Educational purpose
University of Iowa
Spring 2020
ECE: 5995:002 Spr2020 Contemp Topics in Electrical and Computer Engineering
Cryptography
2 April 2020

Julia Chalaypka – Master’s Computer Engineering
and
Daniel Mitchell – Master’s Computer Engineering

Implementation of the US Government’s Advanced Encryption Standard (AES)

This midterm project implements a subset of the US Government’s Advanced Encryption Standard (AES).  Specifically it implements AES (ECB mode) for the 128, 192, and 256 key sizes.  The code developed in in the Python v2.7 (and later versions) programming language using only the fundamental libraries and modules of Python building the AES primitive. 

Discussion of our implementation:

References used in writing this code:
1.	FIPS 197 – https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
2.	Understanding Cryptography – Christof Paar and Jan Pelzl – ISBN: 978-3-642-04100-6 – Springer Heidelberg Dordrecht London New York
a.	Chapter 4 – The Advanced Encryption Standard (AES)
b.	Chapter 5 – More about Block Ciphers
3.	Paar, Christof. Understanding Cryptography Springer Berlin Heidelberg. Kindle Edition. (for digital images and passages below in this discussion)
4.	Key expansion routine - https://github.com/boppreh/aes/blob/master/aes.py  
5.	Reference code - https://github.com/bozhu/AES-Python/blob/master/aes.py
6.	Website Wikipedia.org
a.	Advanced_Encryption_Standard
b.	Side-Channel_attack
c.	AES_key_schedule
7.	Eclipse IDE – Integrated Development Environment
8.	Github.com as a software development repository 
9.	Raspberry Pi v4 compute platform running Raspian OS (tested under multiple IDE environments)

Brief introduction:
In 2001 – NIST (US National Institute of Standards and Technology) declared  the block cipher Rijndael as the new AES standard (FIPS PUB 197).  
The standard is a block cipher with 128 bit block size, with three key lengths.  The AES cipher and this implementation is based only on a 128 bit block size. 
 
The layers of AES and the functions in this Python implementation are broken into the following main routines called from the main program:

Key Addition Layer –  add_round_key (s,k)  where s is the state and k is the subkey
A 128-bit round key, or subkey, which has been derived from  the main key in the key schedule, is XORed to the state 
Byte Substitution Layer (S-Box) – substitute_bytes(s) for encryption and inv_substitute_bytes(s) for decryption
Each element of the state is nonlinearly transformed using lookup tables with special mathematical properties. This introduces  confusion to the data, i.e., it assures that changes in individual state bits propagate  quickly across the data path. 

In this implementation, the routine uses two variables (s_box for encryption, and inverse_s_box for decryption) defined at the beginning of the python code as a lookup table for substitution

Diffusion Layer – made up of two sub layers as described below 
	Shift Rows – shift_rows(s) for encryption and inv_substitute_bytes(s) for decryption
The routine permutes the data on a byte level as described in the Understanding Cryptography – Christof Paar and Jan Pelzl text.
	Mix Columns – mix_columns(s) for encryption and inv_mix_columns(s) for decryption
The routine is a matrix operation which combines (mixes) blocks of four bytes.
In this implementation, the operation is carried out using two sub-routines
mix_single_column(a) for encryption and inv_mix_columns(s) 
It is here that the major diffusion element of AES takes place

Key Addition Layer – add_round_key(s,k)
The key schedule takes the original input key (of length 128, 192 or 256 bit) and  derives the subkeys. The number of subkeys is equal to the number of rounds plus one, due  to the key needed for key whitening in the first key addition layer.

Array manipulation functions – bytes2matrix(txt) and matrix2bytes(matrix) are used to 
Two additional routines are used in the code for the convenience of matrix manipulations.


A graphical view of the AES-128 10-round process – written here for better understanding and mental imaging of the high-level operations of encryption.  

The internal structure of AES is as shown below.  This is the process that is performed for each of the 10-rounds of AES/128.   In the diagram shown 

•	A(0) to A(15) is the 16-byte input,  depending on the round number – it is either the original plaintext, or the output state of the previous round
•	(S) is the Byte Substitution layer 
•	B(0) to B15 is permuted bytewise in the Shiftrow layer 
•	The Mixcolumn layer produces C(0) to C(16) 
•	Which finishes the round by XORed with the sub-key k(i) which is performed in the Key Addition layer and in this code by routine add_round_key(s,k)
 
Additional notes and comments:
•	Implementation of constants Arrays (S_box and Inverse S_box):  As mentioned in the discussion about code optimization, it is likely that making the S_box and Inverse_S_box constants two dimensional arrays as explained and outlined in the text book, as opposed to a 1-dimensional array as it was implemented here and by other AES code seen on GitHub, would have certainly had an impact in overall execution time.  Specifically, the code and processor cycles needed to do an array lookup on 2 dimensions as opposed to 1 would be one such example.  Although the number of cycles may be very small for one S_box lookup, it would be amplified through the huge number of interations of the encryption rounds (and the number of times the code is called into use in a real-world program using such code).

•	AES (ECB mode) – as this ECB mode is deterministic (predictable output with the same input), the code developed in this project would not be suitable or secure for any real-world application.  It does serve as a building block where different mode implementations could reuse the AES primitive to feature Initialization Vectors, and features of CBC (Cipher Block Chaining and PCBC), CFB (Cipher FeedBack), OFB (Output FeedBack), CTR mode and the XTS mode implemented by NIST in 2010.

•	Side Channel (power-analysis and acoustic) attacks:  We considered some points that might be areas to consider for any future software development of AES and software encryption in general regarding side-channel attacks.  Consideration such as faraday-cage shielding of the processor / computing device, or the implementation of a randomly timed function requiring heavy computations to radio emissions that could thwart a simple side-channel attack of these type.  Wikipedia research indicates these are already a known countermeasures.

•	Relative execution time on various platforms:  The purpose of examining this was out of interest to see how fast the code would run on various devices from small portable to a desktop computer.  The code itself is useless unless put to use for an application or a software program to store or transmit data.  Saying that, we were interested to see device performance such as the Raspberry Pi, the magnitude of the workload and delay of running AES code for practical code implementations. The aes.py/tests.py code ran successfully on a Raspberry-Pi V4 (Python 3.7.3 32-bit) under two different IDE environments (Visual Studio port - https://code.headmelted.com/installers/apt.sh ) and also the “Built-in” IDE with Raspian OS (Thonny).   Additional runs on a Windows desktop and a macOS macbook pro.  

Relative execution time on various platforms RESULTS:  
Processor	Operating System (OS)	IDE and Python version	Time in seconds
Raspberry Pi v4 Quad core Cortex/A72 (ARM v8) 64/bit SoC @ 1.5GHz	Raspian OS	IDE - Visual Studio port
(https://code.headmelted.com/installers/apt.sh)
Interpreter - Python 3.7.3 32-bit	0.278seconds

Raspberry Pi v4 Quad core Cortex/A72 (ARM v8) 64/bit SoC @ 1.5GHz	Raspian OS	IDE – Thonny - 
Interpreter - Python 3.7.3 32-bit	0.038
Intel® Core™ i7/7700K CPU @ 4.20GHy – 32 GBytes Mem	Windows 10
Home Version 1903
Build 18362.720
64bit OS	IDE - Eclipse Version: 2019-12 (4.14.0) - Build id: 20191212-1212
Interpréter – Python 3.8-32	0.009seconds

Intel® Core i7
2.2GHz Quad-Core Intel Core i7 – 16GB Mem 1600 MHz DDR3	macOS Catalina v 10.15.3	IDE – Eclipse Version 2019-12(4.14.0) – Build id: 20191212-1212
Interpreter – Python 3.7 	0.012seconds

•	Code optimization for performance (speed):  This code was written for the purpose of satisfying the class assignment / project requirements.  To carry it forward to a real world implementation, the code would need to be enhanced to map hex/dec values to text/ascii input(open file) or output(write file) on either end of a transmission or data file. Additionally, a method of random number generation for an IV and implementation of various AES modes and key bit sizes would be necessary for practical use.  For the code optimization, the following areas would be considered:  
1.	Use builtin functions and libraries – either software libraries or hardware (as discussed in lecture) – examine the efficiencies of speed of such functions 
2.	Move calculations outside the loop – at a cursory glance focusing on the functions requiring the most number of clock cycle / cpu cycle operations (such as mix column functions)  would be a place we would start any code optimization
3.	Minimize code base – shorten variable names, remove inline comments, etc …
4.	Review data structures – Here lies one of the bigger optimization questions regarding our implementation.  Constants for the S_box and inverse S_box should be a 1-dimentional table as seen in code from others or a 2-dimensional table as described in the textbook.  Certainly matrix operations that are iterative in the code will likely dramatically change both the execution speed and power requirements at the expense of code readability.
5.	Reduce memory footprint
6.	Write the entire code base in machine language such that all possible extraneous operations can be eliminated.  A very extreme but probably the best possible way to maximize efficiency of the code

•	Code optimization for minimizing electrical power consumption: In our opinion, optimization for electrical power consumption for code execution on any device would correlate (but not exclusively) with the optimization for performance. Exploring the tradeoff of power consumption of software library calculations vs hardware (AES enhanced processors) would be interesting to further understand and explore.  This factor would be important to understand when porting the code to a device that had limited power requirements (battery source) or compute platforms where heat dissipation would be a factor. 

How to compile the source code:
The AES implementation is on Github.com at the following link:
•	Replicate the repository from your IDE
•	Run the tests.py file as a unit test
