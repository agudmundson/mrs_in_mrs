
__author__  = 'Aaron Gudmundson'
__email__   = 'aarongudmundsonphd@gmail.com'
__date__    = '2023/06/01'


# from fpdf import FPDF
from tkinter import filedialog 														# File Explorer through Tkinter
import tkinter as tk     															# Graphical User Interface
import pandas as pd 																# DataFrames
import numpy as np  																# Arrays
import time as t0 																	# Timer
import subprocess 																	# Running Terminal Commands
import importlib 																	# Verification of Installed Modules
import logging 																		# Log File
import shutil 																		# Copy, Move, "which $program"
import json   																		# Handle JSON files 
import copy  																		# Copying Objects
import glob 																		# Bash-like File Calls
import sys 																			# Interact with System
import re  																			# Regular Expressions 
import os																			# Interact with Operating System


def setup_log(log_name, log_file, level=logging.INFO): 								# Create new global log file
	'''
	- 1. Description:
		- Creates logfile
	
	- 2. Inputs:
		- log_name : (String) Name of the log 
		- log_file : (String) Filename of the log
		- level    : (Func  ) Level to log (default to debug and info)

	- 3. Outputs:
		- logger   : (Logger) Global log object
	'''

	formatter = logging.Formatter('(%(asctime)s) %(message)s'       , 				# Logging format (Time and Message)
								  datefmt = '%m/%d/%Y %I:%M:%S %p') 				# Date/Time Specific Formatting
	
	handler = logging.FileHandler(log_file)         								# Log Handler
	handler.setFormatter(formatter)													# Log Formatting

	logger  = logging.getLogger(log_name) 											# Instantiate Logger
	logger.setLevel(level) 															# Set Log Level
	logger.addHandler(handler) 														# Connect Handler

	return logger 																	# Return Logger Object

def write_log(log, message): 														# Log Writing
	if log != None: 																# Check Log is set to Write
		try:
			long_spc = (' '*36)
			message  = message.replace('\n\t', '\n{}'.format(long_spc)) 			# Add Long Space to Newlines for alignment 
		except Exception as e:
			print('Write Log Error: {}'.format(e))
		log.info(message) 															# Log - 
	# else: 																		# Log Write is set to No
	# 	print('Not writing: {}'.format(message)) 									# Logging is Turned off

class Application(tk.Tk): 															# Create Application Class
	def __init__(self, lwrite=True): 												# Init
		super().__init__() 															# Initialize tk.Tk

		userwidth  = self.winfo_screenwidth() 										# User's Screen Width
		userheight = self.winfo_screenheight() 										# User's Screen Height

		width      = int(userwidth * 0.30) 											# Application Width
		height     = int(userwidth * 0.20) 											# Application Height


		## Main Window Control 														
		# self.geometry('{}x{}'.format(width, height))								# Geometry Width x Height
		self.minsize(width, height) 												# Screen can't be smaller
		self.config(bg='white') 													# Set Background White


		## Required Classes, Functions, etc.													
		# self.mypath  = mypath  													# Updated Path
		self.Table   = Table() 														# MRSinMRS Table Creation
		self.DRead   = DataReaders() 												# Vendor Data Readers
		self.lwrite  = lwrite  														# Write to Log File
		self.exe 	 = bool  														# Executable or CommandLine


		## Window Label
		self.title('Reproducibility Made Easy') 									# Label The Application Window


		## This is the primary Grid Layout Frame
		self.frame  = tk.Frame(self, borderwidth=10)# , width=width, height=height)
		self.frame.grid(row=0, column=0, columnspan=2, rowspan=10, sticky=tk.W+tk.E+tk.N+tk.S)
		self.frame.config(bg='white')
		self.frame.pack(pady=5, padx=5)


		## Primary Label (at Top)
		prim_label      = '  \n'
		prim_label      = 'Reproducibility Made Easy\n'.format(prim_label)
		self.prim_label = tk.Label(self.frame, text='Reproducibility Made Easy')
		self.prim_label.config(font=('Arial', 20, 'bold'), bg='royalblue')
		self.prim_label.grid(row=0, column=0, rowspan=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)


		## Reproducibility Made Easy Description
		desc_label       = ''
		desc_label       = '{}Export a CSV File according to the '.format(desc_label)
		desc_label       = '{}MRSinMRS guidelines using MRS files headers\n'.format(desc_label)
		self.desc_label = tk.Label(self.frame, text=desc_label)
		self.desc_label.config(font=('Arial', 16), bg='royalblue')
		self.desc_label.grid(row=4, column=0, rowspan=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)


		## Reproducibility Made Easy (REMY) Team
		REMY_label       = ''
		REMY_label       = '{}Reproducibility Made Easy Team:\n'.format(REMY_label)
		REMY_label       = '{}Antonia Susnjar, Antonia Kaiser, Gianna Nossa, '.format(REMY_label)
		REMY_label       = '{}Dunja Simicic, and\nAaron Gudmundson\n\n'.format(REMY_label)
		self.REMY_label = tk.Label(self.frame, text=REMY_label)
		self.REMY_label.config(font=('Arial',14), bg='white')
		self.REMY_label.grid(row=5, column=0, rowspan=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
		# self.REMY_label.pack(pady=0)

 
		## MRSinMRS Citation
		cite_names      = ''
		cite_names      = '{}Lin A, Andronesi O, Bogner W, et al.\n'.format(cite_names)
		cite_names      = '{}Minimum Reporting Standards for in vivo Magnetic '.format(cite_names)
		cite_names      = '{}Resonance Spectroscopy (MRSinMRS):\n'.format(cite_names)
		cite_names      = '{}Experts’ consensus recommendations. NMR in Biomedicine. '.format(cite_names)
		cite_names      = '{}2021;34(5). doi:10.1002/nbm.4484\n\n'.format(cite_names)
		self.citation   = tk.Label(self.frame, text=cite_names)
		self.citation.config(font=('Arial', 12), bg='white')
		self.citation.grid(row=6, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
		# self.citation.pack(pady=0)


		## Main Button Box
		self.button_frame      = tk.Frame(self.frame, borderwidth=5)
		self.button_frame.grid(row=7, column=0, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
		self.button_frame.config(bg='white')


		## Determine if running in application or 
		if getattr(sys, 'frozen', False): 													# Determine if Application or CommandLine
			print('Running inside executable...')
			self.cwd = os.path.abspath(os.path.dirname(__file__))
			# self.cwd = os.path.abspath(os.path.dirname(self.mypath))
			self.exe = True 																# Note
		elif __file__: 																		# Command Line
			self.cwd = os.path.dirname(os.path.realpath(__file__)) 							# Command Line - Set Directory
			self.exe = False 																# Note  
		self.cwd = self.cwd.replace('\\', '/') 												# Remove any Windows' backslashes


		## File Import Button
		self.import_button = tk.Button(self.button_frame, text='Import', width=15, height=2, command=self.import_file)
		self.import_button.grid(row=0, column=0)
		self.import_label  = tk.Label(self.button_frame, text=self.cwd)
		self.import_label.config(font=('Arial', 14), bg='white')
		self.import_label.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)


		## File Export Button
		self.export_button = tk.Button(self.button_frame, text='Export', width=15, height=2, command=self.export_file)
		self.export_button.grid(row=1, column=0)
		self.export_label  = tk.Label(self.button_frame, text=self.cwd)
		self.export_label.config(font=('Arial', 14), bg='white')
		self.export_label.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)  


		## Button Commands
		self.command_frame = tk.Frame(self.frame, borderwidth=5)
		self.command_frame.grid(row=9, column=0, columnspan=2)
		self.command_frame.config(bg='white')


		## User Data Selections - Vendor
		self.vendor     = tk.StringVar()
		self.vendor.set('Select Vendor')
		self.vendor_opt = ['Siemens', 'Philips', 'GE', 'Bruker', 'NIfTI']
		self.command_01 = tk.OptionMenu(self.command_frame, self.vendor, *self.vendor_opt, command=self.command_button_01)
		self.command_01.config(height=2, width=30)
		self.command_01.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)


		## User Data Selections - DataType
		self.dtype     = tk.StringVar()
		self.dtype.set('First Select Vendor')
		self.dtype_opt = ['Siemens TWIX (.dat)' ,  											# Siemens Twix  (.dat)
						  'Siemens Dicom (.ima)',  											# Siemens Dicom (.ima)
						  'Siemens RDA (.rda)'  ,  											# Siemens RDA   (.rda)
						  'Philips (.spar)'     ,  											# Philips SPAR  (.sdat or .data/.list)
						  'GE (.7)'             ,  											# GE      Pfile (.7)
						  'Bruker (method)'     ,											# Bruker  method
						  'NIfTI (.json)']  												# NIfTI  JSON
		# 				  'Bruker (2dseq)'      ]  											# Bruker  2dseq (Not active)
		self.command_02 = tk.OptionMenu(self.command_frame, self.dtype, *self.dtype_opt, command=self.command_button_02)
		self.command_02.config(height=2, width=30)
		self.command_02.grid(row=0, column=2, sticky=tk.W+tk.E+tk.N+tk.S)


		## Instantiate Vendor and Dtype
		self.vendor_selection = ''
		self.dtype_selection  = ''


		## Button Commands
		self.run_frame = tk.Frame(self.frame, borderwidth=5)
		self.run_frame.grid(row=10, column=0, columnspan=2, rowspan=1)
		self.run_frame.config(bg='white')


		## Run Script
		self.command_03 = tk.Button(self.run_frame, text='Run', width = 30, command=self.command_button_03)
		self.command_03.config(height=2, width=60)
		self.command_03.grid(row=0, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
		self.update()


	## Import Button Function
	def import_file(self):
		filepath = filedialog.askopenfilename()  											# Open File Explorer
		filepath = filepath.replace('\\', '/') 												# Replace any Windows' backslashes

		filepath = (filepath.replace('.SDAT', '.SPAR') if '.SDAT' in filepath else  		# Must be .spar - User gave .sdat
					filepath.replace('.sdat', '.spar'))
		filepath = (filepath.replace('.DATA', '.SPAR') if '.DATA' in filepath else   		# Must be .spar - User gave .data
					filepath.replace('.data', '.spar'))
		filepath = (filepath.replace('.LIST', '.SPAR') if '.LIST' in filepath else   		# Must be .spar - User gave .list
					filepath.replace('.list', '.spar'))
		filepath = (filepath.replace('.NII' , '.JSON') if '.NII'  in filepath else  		# Must be .json - User gave .nii
					filepath.replace('.nii' , '.json'))

		if os.path.exists(filepath): 														# Ensure Path Exists
			self.import_fpath = copy.deepcopy(filepath) 									# Import Path
			self.export_fpath = os.path.dirname(filepath)
			exp_fpath         = copy.deepcopy(self.export_fpath)

			if len(filepath) > 60:
				self.import_label['text'] = (  filepath[:30 ] + ' ... '  
				 							 + filepath[-30:]        ) 						# Shorten Import Path Display

				self.export_label['text'] = (  exp_fpath[:30 ] + ' ... '  
				 							 + exp_fpath[-30:]        ) 					# Shorten Import Path Display

			else:
				self.export_fpath         = copy.deepcopy(exp_fpath)
				self.import_label['text'] = filepath				 						# Display Import Path
				self.import_label['text'] = filepath				 						# Display Import Path
				# self.export_label['text'] = '{}_MRSinMRS.csv'.format(filepath.split('.')[0])# Display Updated Expport Path

			self.command_03['text'] = 'Run' 												# Update Text
			print('Import file:', filepath) 												# 

	## Export Button Function
	def export_file(self):
		filepath = filedialog.askdirectory() 												# Open File Explorer
		filepath = filepath.replace('\\', '/') 												# Replace any Windows' backslashes

		if os.path.exists(filepath):
			self.export_fpath         = copy.deepcopy(filepath) 							# Export Path
		
			if len(filepath) > 60: 															# Export Path is Long
				self.export_label['text'] = (  filepath[ :30] + '...'  						# 
				 							 + filepath[-30:]        ) 						# Shorten Export Path Display
			else:
				self.export_label['text'] = filepath 										# Display Full Export Path

		print('Export file:', filepath)														# 


	## Vendor Selection Button Function
	def command_button_01(self, selection):
		print('Selected: ', selection) 														# User Selected Vendor  
		
		self.vendor_selection = selection

		if selection.lower() == 'siemens': 													# Siemens
			self.dtype.set('{}: Select Twix (.dat), Dicom (.ima), or RDA (.rda)'.format(selection)) # Twix

		elif selection.lower() == 'philips': 												# Philips
			self.dtype.set('{}: Select (.spar) for .sdat or raw data'.format(selection)) 	# SDAT/SPAR and Data/List

		elif selection.lower() == 'ge': 													# GE
			self.dtype.set('{}: Select Pfile (.7)'.format(selection))						# PFile

		elif selection.lower() == 'bruker': 												# Bruker
			self.dtype.set('{}: Select (method)'.format(selection))							# Method (2dseq?)

		elif selection.lower() == 'nifti': 													# NIfTI
			self.dtype.set('{}: Select (.json)'.format(selection))							# JSON


	## Datatype Selection Button Function
	def command_button_02(self, selection):
		print('Selected: ', selection) 														# User Selected Datatype        

															 								# Vendor Matched to avoid misclicks
		vendor_dtypes = {'siemens': ['Siemens TWIX (.dat)'  , 								# Siemens Twix .dat
									 'Siemens Dicom (.ima)' , 								# Siemens Dicom .ima
									 'Siemens RDA (.rda)'   ], 								# Siemens RDA .rda
						 'philips': ['Philips (.spar)'      ],								# Philips sdat/spar or data/list
						 'ge'     : ['GE (.7)'              ], 								# GE Pfile
						 'bruker' : ['Bruker (method)'      ], 								# Bruker Method File
						 'nifti'  : ['NIfTI (.json)'         ]} 							# NIfTI JSON side car file
		
		vendor_dtypes = vendor_dtypes[self.vendor_selection.lower()] 						# Current Vendor Datatypes
		if selection not in vendor_dtypes: 													# User accidentally selected wrong datatype
			self.command_03['text'] = 'Please Select Appropriate Datatype' 					# Update Text
			return

		self.dtype_selection = selection 													# Datatype Selection
		self.dtype.set(selection) 															# Set the Datatype Text Display

		self.dtype_selection = self.dtype_selection.lower()  								# Lowercase
		self.dtype_selection = self.dtype_selection.split('(')[1] 							# Split off filetype
		self.dtype_selection = self.dtype_selection.split(')')[0] 							# Split off filetype
		self.dtype_selection = self.dtype_selection.replace('/', '_') 						# Remove / if spar/sdat 
		self.dtype_selection = self.dtype_selection.replace('.', '') 						# Remove any period preceding extension


	## Running the Script Button
	def command_button_03(self):

		self.command_03['text'] = 'Running...' 												# Update Text

		## Update Button Selections
		possible_vendors = ['siemens', 'philips', 'ge', 'bruker', 'nifti'] 					# Currently Supported Vendors 
		if self.vendor_selection.lower() not in possible_vendors: 							# User dit not Select Supported Vendors 
			self.command_03['text'] = 'Please select Vendor and Datatype' 					# Update Text
			return

		possible_dtypes  = ['spar', 'dat', 'ima', 'rda', '7', 'method', '2dseq', 'json']	# Currently Supported Datatypes 
		if self.dtype_selection.lower()  not in possible_dtypes:							# User did not Select Supported Datatypes
			self.command_03['text'] = 'Please select Datatype' 								# Update Text
			return


		## Filenames
		if os.path.isdir(self.export_fpath): 												# Determine if Path or .csv
			pname = self.export_fpath 														# Selected Path Name
		else:
			pname = os.path.dirname(self.export_fpath) 										# Selected Path Name

		iname = self.import_fpath[:].split('/')[-1] 										# Get the Filename
		fname = self.import_fpath[:].split('/')[-1] 										# Get the Filename

		oname = '' 																			# This will be the Output file name
		if len(fname.split('.')[0]) == 2: 													# Ensure user doesn't include . in filename
			oname = fname.split('.')[0] 	 												# Remove file extension
		else:  																				# User includes . in filename
			if '.' in fname:			
				fname_ = fname.split('.')[:-1] 												# Remove extension
				for ii in range(len(fname_)): 												# Iterate back through fname pieces
					oname = '{}{}'.format(oname, fname_[ii]) 								# Recombine into oname
			else:
				oname = fname 																# oname will be fname

		## Setup Log File
		if self.lwrite: 																	# Create a Logfile
			log = setup_log(oname, '{}/{}_Log.log'.format(pname, oname)) 					# Log File
		else:
			log = None 																		# User Selected Not to Create Log File


		## Begin Writing Log File 
		write_log(log, ' ') 																# Log - Intentional Empty Line
		write_log(log, '--'*30)  															# Log - Dashed Line to Separate Entries
		write_log(log, 'Reproducibility Made Easy (REMY) is Starting..') 					# Log - Reproducibility Made Easy

		if self.exe == True:
			write_log(log, 'Software Running with Application') 							# Log - Running from Application
			write_log(log, 'Software Directory: {}'.format(self.cwd)) 						# Log - Running from Application
		else:
			write_log(log, 'Software Running from Command Line') 							# Log - Running from the Command Line
			write_log(log, 'Software Directory: {}'.format(self.cwd)) 						# Log - Running from Application

		write_log(log, ' ') 																# Log - Intentional Empty Line
		write_log(log, 'Base Dir : {}'.format(pname))  										# Log - Base Directory
		write_log(log, 'Filename : {}'.format(iname))										# Log - Filename
		write_log(log, 'Out Dir  : {}'.format(pname))										# Log - Export Directory
		write_log(log, 'Out Name : {}.csv'.format(oname))									# Log - Export Filename (without extension)
		write_log(log, 'Vendor   : {}'.format(self.vendor_selection)) 						# Log - Vendor Selected
		write_log(log, 'Datatype : {}\n'.format(self.dtype_selection)) 						# Log - Datatype Selected


		## Data Read using Spec2nii
		write_log(log, 'Data Read: ') 														# Log - Intentional Empty Line
		write_log(log, 'Data Read: Starting Data Read using spec2nii')  					# Log - Failed to Read Data
		if (    (self.exe == False and importlib.util.find_spec('spec2nii') is not None) 	# spec2nii at command line
		     or (self.exe == True)): 														# spec2nii from executable
			write_log(log, 'Data Read: spec2nii is installed'             +					# Log - Successfully Read Data
						   '\n\tNote** The Application version of '  	  +	
						   'Reproducibility Made Easy comes with spec2nii'+
						   ' installed.\n\tThis is intentional to make '  + 
						   'this product usable for anyone\n\tHowever, '  +
						   'this means the downloaded version may become '+
						   'outdated...\n\tWe recommend re-installing '   +
						   'if experiencing problems' 					  )

			try: 																			# Try using spec2nii to Read Data
				import_text  = self.import_fpath
				if self.vendor_selection.lower() == 'siemens': 								# Siemens
					if self.dtype_selection == 'dat': 										# Siemens Data Reader from Twix file
						write_log(log, 'Data Read: Siemens Twix uses pyMapVBVD ')			# Log - pyMapVBVD
						MRSinMRS, log = self.DRead.siemens_twix(import_text, log) 			# Siemens Data Reader from mapVBVD

					if self.dtype_selection == 'ima': 										# Siemens Data Reader from Dicom file
						write_log(log, 'Data Read: Siemens Dicom uses pydicom ')			# Log - pyDicom
						MRSinMRS, log = self.DRead.siemens_ima(import_text, log) 			# Siemens Data Reader from mapVBVD

					if self.dtype_selection == 'rda': 										# Siemens Data Reader from RDA file
						write_log(log, 'Data Read: Siemens RDA directly read with RMY ')	# Log - pyDicom
						MRSinMRS, log = self.DRead.siemens_rda(import_text, log) 			# Siemens Data Reader from mapVBVD

				elif self.vendor_selection.lower() == 'philips': 							# Philips 
					write_log(log, 'Data Read: Philips SPAR uses spec2nii ')				# Log - spec2nii
					MRSinMRS, log = self.DRead.philips_spar(import_text, log)				# Philips .spar Reader from spec2nii
					
				elif self.vendor_selection.lower() == 'ge': 								# GE
					write_log(log, 'Data Read: GE Pfile uses spec2nii ')					# Log - spec2nii
					MRSinMRS, log = self.DRead.ge_7(import_text, log) 						# GE Data Reader from spec2nii

				elif self.vendor_selection.lower() == 'bruker': 							# Bruker
					if self.dtype_selection == 'method': 									# Bruker Data Reader from Method file
						write_log(log, 'Data Read: Bruker Method uses spec2nii ')			# Log - spec2nii
						MRSinMRS, log = self.DRead.bruker_method(import_text, log) 			# Bruker Data Reader from Method file
					
					elif self.dtype_selection == '2dseq':
						write_log(log, 'Data Read: Bruker uses BrukerAPI '    + 			# Log - BrukerAPI
									   'developed by Tomáš Pšorn\n\t'         +				# Log - BrukerAPI Creator
									   'github.com/isi-nmr/brukerapi-python'  )				# Log - BrukerAPI Address
						MRSinMRS, log = self.DRead.bruker_2dseq(import_text, log) 			# Brukler Data Reader from BrukerAPI

				elif self.vendor_selection.lower() == 'nifti': 								# NIfTI
					write_log(log, 'Data Read: NIfTI json side car')						# Log - NIfTI JSON side car
					write_log(log, 'Data Read: NIfTI ** Ensure .json was provided **')		# Log - NIfTI JSON side car check
					write_log(log, ' ') 													# Log - NIfTI JSON Intentional Empty Line
					MRSinMRS, log = self.DRead.nifti_json(import_text, log) 				# NIfTI JSON Reader

				write_log(log, 'Data Read: Completed\n') 									# Log - Successfully Read Data

			except Exception as e: 															# Data Reader Failed
				write_log(log, 'Data Read: Failed ** **')  									# Log - Failed to Read Data
				write_log(log, 'Data Read: Error - {}\n'.format(e))  						# Log - Error

		else:
			d1 = 'aarongudmundsonphd@gmail.com'  											# Aaron Gudmundson, PhD
			d2 = 'antonia.kaiser@epfl.ch'  													# Antonia Kaiser, PhD
			d3 = 'asusnjar@mgh.harvard.edu'  												# Antonia Susjnar, PhD
			write_log(log, 'spec2nii : spec2nii was not found..'          + 				# Log - Successfully Read Data
						   '\n\tNote** The Application version of '  	  +	
						   'Reproducibility Made Easy comes with spec2nii'+
						   ' installed.\n\tHowever, it is not being '     +
						   'located during runtime..\n\tPlease contact '  +
						   'the developers:'             				  +
						   '\n\t\t{}\n\t\t{}\n\t\t{}'.format(d1, d2, d3)  )


		write_log(log, 'Table    :') 																# Log - 
		## Check for Missing MRSinMRS Values that might have different names across versions
		try:
			MRSinMRS = self.Table.table_clean(self.vendor_selection, self.dtype_selection, MRSinMRS)
			write_log(log, 'Table    : table_clean Successful') 							# Log - Failed to Populate Table
		except Exception as e:
			write_log(log, 'Table    : table_clean Failed') 								# Log - Failed to Populate Table
			write_log(log, 'Table    : table_clean Error - {}'.format(e))  					# Log - Error


		## Populate MRS Table
		try:
			self.Table.populate(self.vendor_selection, self.dtype_selection, MRSinMRS)
			write_log(log, 'Table    : populate table Successful') 							# Log - Successfully Populated Table
		except Exception as e:
			write_log(log, 'Table    : populate table Failed') 								# Log - Failed to Populate Table
			write_log(log, 'Table    : populate table Error - {}'.format(e))  				# Log - Error


		## Export Table as .csv
		csvname = '{}/{}_Table.csv'.format(pname, oname) 									# Name of .csv file
		csvcols = ['Header', 'SubHeader', 'MRSinMRS', 'Values'] 							# Columns to Include in Output .csv

		self.Table.MRSinMRS_Table[csvcols].to_csv(csvname) 									# Create .csv
		write_log(log, 'Table    : Created MRSinMRS Table as .csv file\n') 					# Log - Failed to Populate Table


		## Export LaTeX .pdf
		write_log(log, 'LaTeX PDF: ') 														# Log - Intentional Empty Line
		write_log(log, 'LaTeX PDF: Starting LaTeX to PDF') 									# Log - Starting LaTeX
		try:

			LaTeX_dir   = '{}/LaTeX_Extras'.format(pname) 									# LaTeX Extras Directory Name
			os.mkdir(LaTeX_dir) 	 														# Store all the LaTeX Files									

			## LaTeX File
			latex_name  = '{}/{}.tex'.format(LaTeX_dir, oname) 								# LaTeX Filename
			latex_content,errors = self.Table.table_to_latex() 								# Read LaTeX Template
			if len(errors) > 1:
				write_log(log, 'LaTeX PDF: Replaced LaTeX Content w/Errors:') 				# Log - Read LaTeX w/Errors
				write_log(log, errors) 														# Log - Log the Errors
			else:
				write_log(log, 'LaTeX PDF: Replaced LaTeX Content without Errors') 			# Log - Successfully Read LaTeX

			with open(latex_name, 'w') as f: 												# Create Tex File in Subject's Directory
				f.write(latex_content) 														# Write Content to Subject's LaTeX File
			write_log(log, 'LaTeX PDF: Created LaTeX File') 								# Log - Successfully Wrote New LaTeX


			## Control File
			bcf_name        = '{}/MRSinMRS.bcf'.format(self.cwd) 							# LaTeX Control File Template
			with open(bcf_name, 'r') as f: 													# Open LaTeX Control File Template
				bcf_content = f.read() 														# Read LaTeX Control File Template

			bcf_name    = '{}/{}.bcf'.format(LaTeX_dir, oname) 								# LaTeX Control File Filename
			bib_name    = '{}/{}.bib'.format(LaTeX_dir, oname) 								# LaTeX Bibliography Filename
			bcf_content = bcf_content.replace('/MRSinMRS.bib', bib_name) 					# Replace Generic Bilbiography Name
			with open(bcf_name, 'w') as f: 													# Create LaTeX Control File in Subject Directory
				f.write(bcf_content) 														# Write LaTeX Control File in Subject Directory
			write_log(log, 'LaTeX PDF: Created LaTeX Control file') 						# Log - Successfully Created PDF


			## LaTeX Extra Files
			shutil.copy('{}/MRSinMRS.aux'.format(self.cwd),  								# Generic LaTeX Auxilliary File
						'{}/{}.aux'.format(LaTeX_dir, oname)) 								# Subject LaTeX Auxilliary File

			shutil.copy('{}/MRSinMRS.bbl'.format(self.cwd),   								# Generic LaTeX Bibliography-formatted LaTeX
					    '{}/{}.bbl'.format(LaTeX_dir, oname)) 								# Subject LaTeX Bibliography-formatted LaTeX

			shutil.copy('{}/MRSinMRS.bib'.format(self.cwd),   								# Generic LaTeX Bibliography File
						'{}/{}.bib'.format(LaTeX_dir, oname)) 								# Subject LaTeX Bibliography File
			
			shutil.copy('{}/MRSinMRS.blg'.format(self.cwd),   								# Generic LaTeX Bibliography Log File
						'{}/{}.blg'.format(LaTeX_dir, oname)) 								# Subject LaTeX Bibliography Log File

			write_log(log, 'LaTeX PDF: Copied LaTeX Extra Files') 							# Log - Successfully Created PDF


			## Running PDFLaTeX
			if isinstance(shutil.which('pdflatex'), str) == True: 							# Check User has LaTeX Installed
				write_log(log, 'LaTeX PDF: PDFLaTeX is installed') 							# Log - Successfully Created PDF

				script = 'pdflatex -interaction=nonstopmode'
				script = '{} {}.tex > /dev/null 2>&1'.format(script, oname) 				# PDFLaTeX Script to call 
				P = subprocess.run(script, cwd=LaTeX_dir, shell=True) 						# Run PDFLaTeX Script
				write_log(log, 'LaTeX PDF: Created PDF from LaTeX') 						# Log - Successfully Created PDF

				shutil.move('{}/{}.tex'.format(LaTeX_dir, oname), pname) 					# Move LaTeX PDF to Subject Direcctory
				write_log(log, 'LaTeX PDF: Moved Tex to Subject Directory') 				# Log - Successfully Created PDF

				shutil.move('{}/{}.pdf'.format(LaTeX_dir, oname), pname) 					# Move LaTeX PDF to Subject Direcctory
				write_log(log, 'LaTeX PDF: Moved PDF to Subject Directory\n') 				# Log - Successfully Created PDF

			else: 																			# User does not have LaTeX installed
				write_log(log, 'LaTeX PDF: PDFLaTeX is not installed\n' + 					# Log - pdflatex not installed
							   'visit https://www.latex-project.org/get\n') 				# Log - pdflatex download page

		except Exception as e:
			write_log(log, 'LaTeX PDF: Failed Error Below') 								# Log - Failed to Populate Table
			write_log(log, 'LaTeX PDF: Error - {}\n'.format(e))  							# Log - Error


		write_log(log, 'Reproducibility Made Easy has Completed!') 							# Log - Failed to Populate Table
		write_log(log, '--'*30)  															# Log - Dashed Line to Separate Entries
		self.command_03['text'] = 'Completed!' 												# Note Completion


class Table():
	def __init__(self, ):
		
		if getattr(sys, 'frozen', False): 													# Determine if Executable or Command Line
			print('Inside executable')
			# self.cwd = os.path.dirname(sys.executable) 										# Executable
			self.cwd = os.path.abspath(os.path.dirname(__file__))

		elif __file__: 																		#
			self.cwd = os.path.dirname(os.path.realpath(__file__)) 							# Command Line 

		# self.cwd                   = mypath
		self.cwd                   = self.cwd.replace('\\', '/')	 						# Replace any Windows' Backslash
		self.MRSinMRS_Table        = pd.read_csv('{}/MRSinMRS.csv'.format(self.cwd))
		self.latex_file            = '{}/MRSinMRS.tex'.format(self.cwd) 						# Generic LaTeX File

		print('Read in MRSinMRS Table')

	def table_clean(self, vendor, datatype, MRSinMRS): 										# Differences Across Datatype Version
		vendor                 = vendor.lower()

		vendor_string          = 's2nlabel_{}_{}'.format(vendor, datatype).lower() 			# Identify Vendor
		vendor_keys            = list(self.MRSinMRS_Table[vendor_string]) 					# Get Vendor-specific fields
		mrs_keys               = list(MRSinMRS.keys()) 										# Get MRSinMRS Dictionary Items

		known_diffs            = {} 														# Known Differences In Header Field Names
		known_diffs['siemens'] = {'FieldStrength'   : ['lFrequency'           ,				# Siemens Dictionary
													   'Frequency'            ,             # 
													   'SpectrometerFrequency',             # 
                                                       'MRFrequency'          ], 			#
								  'NumberOfAverages': ['Averages',            ], 			# 
								  'TE'              : ['TE_Time',             ], 			# 
								  'DwellTime'       : ['DwellTimeSig',        ], 			# 
								  'tProtocolName'   : ['SequenceFileName',    ], 			# 
								  'Nucleus'         : ['ResonantNucleus',     ],			#
								  'VOIPhaseFOV'     : ['SlabThickness[1]'     ],			#
								  'VOIThickness'    : ['SlabThickness[0]'     ],			#
								  'VOIReadoutFOV'   : ['SlabThickness[2]'     ]} 			# 
		known_diffs['philips'] = {'FieldStrength'   : ['synthesizer_frequency'], 			# Philips Dictionary 
								  'EchoTime'        : ['echo_time',           ], 	 		#
							 	  'RepetitionTime'  : ['repetition_time',     ], 			# 
							 	  'Nucleus'         : ['nucleus'              ]} 			# 
		known_diffs['ge'     ] = {'FieldStrength'   : ['rhr_rh_ps_mps_freq'   ]} 			# GE
		known_diffs['bruker' ] = {} 														# Bruker
		known_diffs['nifti'  ] = {'FieldStrength'   : ['SpectrometerFrequency'],			# NIfTI
								  'Nucleus'         : ['ResonantNucleus'      ]} 			# 

		known_diffs            = known_diffs[vendor] 	 									# Current Vendor	
		known_diffs_keys       = list(known_diffs.keys()) 									# List of all Known Differences

		for ii in range(len(known_diffs_keys)): 											# Iterate over Known Differences
			if (known_diffs_keys[ii] not in mrs_keys) == True: 								# If Key was not found in Data Reading 
				known_diffs_keys_list = known_diffs[known_diffs_keys[ii]] 					# Get the list of potential differences

				for jj in range(len(known_diffs_keys_list)): 								# Iterate over differences
					if (known_diffs_keys_list[jj] in mrs_keys) == True: 					# This Item was found in Data Reading
						MRSinMRS[known_diffs_keys[ii]]= MRSinMRS[known_diffs_keys_list[jj]] # Update with Item Found from Difference

		if 'TE_Time' in list(MRSinMRS.keys()):
			if isinstance(MRSinMRS['TE'], str):
			 	MRSinMRS['TE']  = float(MRSinMRS['TE']) / 1e3 
			else:
			 	MRSinMRS['TE'] /=  1e3 

		if 'FieldStrength' in list(MRSinMRS.keys()):
			if isinstance(MRSinMRS['FieldStrength'], str):
			 	MRSinMRS['FieldStrength'] = MRSinMRS['FieldStrength'].replace(',', '.')
			 	MRSinMRS['FieldStrength']  = float(MRSinMRS['FieldStrength'])

		if vendor.lower() == 'ge': 															# Some GE headers don't seem to contain Nucleus
			larmor = copy.deepcopy(MRSinMRS['rhr_rh_ps_mps_freq']) / 1e7 					# Get the Larmor
 																							# Make a guess on Nucleus based on Larmor
			if larmor > 18 and larmor < 22:
				MRSinMRS['Nucleus'] = '2H'			 										# 2H at 3.0 T
			elif larmor > 30 and larmor < 33:
				MRSinMRS['Nucleus'] = '13C'				 									# 13C at 3.0 T
			elif larmor > 33 and larmor < 35:
				MRSinMRS['Nucleus'] = '23Na'					 							# 23Na at 3.0 T
			elif larmor > 44 and larmor < 47:
				MRSinMRS['Nucleus'] = '2H'					 								# 2H at 7.0 T		
			elif larmor > 49 and larmor < 53:
				MRSinMRS['Nucleus'] = '31P'					 								# 31P at 3.0 T		
			elif larmor > 73 and larmor < 76:
				MRSinMRS['Nucleus'] = '13C'					 								# 13C at 7.0 T	
			elif larmor > 118 and larmor < 122:
				MRSinMRS['Nucleus'] = '31P'					 								# 31P at 7.0 T
			elif larmor > 122.5 and larmor < 130:
				MRSinMRS['Nucleus'] = '1H'					 								# 1H at 3.0 T
			elif larmor > 295 and larmor < 303:
				MRSinMRS['Nucleus'] = '1H'					 								# 1H at 7.0 T

		if 'Nucleus' in list(MRSinMRS.keys()):
			gyro       = {				 													# Gyromagnetic Ratio (MHz/Tesla) or (γ/2π)
						  '1H'  : 42.5760, 													#  1H  Proton
						  '2H'  :  6.5360, 													#  2H  Deuterium
					      '13C' : 10.7084, 													# 13C  Carbon
						  '15N' : -4.3160,													# 15N  Nitrogen
						  '17O' : -5.7720, 													# 17O  Oxygen
						  '23Na': 11.2620, 													# 23Na Sodium
						  '31P' : 17.2350}													# 31P  Phosphorous

			vendor_divs = {'siemens_dat'  : 1e6, 											# Siemens Twix
						   'siemens_ima'  : 1  , 											# Siemens Dicom
						   'siemens_rda'  : 1  , 											# Siemens RDA
						   'philips_spar' : 1e6, 											# Philips Spar
						   'ge_7'         : 1e7, 											# GE Pfile
						   'bruker_method': 1  , 											# Bruker Method
						   'bruker_2dseq' : 1  , 											# Bruker 2dseq
						   'nifti_json'   : 1  ,} 											# NIfTI JSON

			gyro        = gyro[MRSinMRS['Nucleus']] 										# Nucleus Gyromagnetic Ratio
			vendor_divs = vendor_divs['{}_{}'.format(vendor, datatype)] 					# Units
			MRSinMRS['FieldStrength'] = float(MRSinMRS['FieldStrength']) / gyro 			# Field Strenth in T
			MRSinMRS['FieldStrength'] = MRSinMRS['FieldStrength'] / vendor_divs		    	# Field Strenth in T
			MRSinMRS['FieldStrength'] = np.round(MRSinMRS['FieldStrength'], 2) 				# Field Strenth rounded

		return MRSinMRS 																	# Return Clean MRSinMRS Dict

	def populate(self, vendor, datatype, MRSinMRS):  										# Populate our MRSinMRS Table
		vendor_string   = 's2nlabel_{}_{}'.format(vendor, datatype).lower() 				# Identify Vendor

		vendor_keys     = list(self.MRSinMRS_Table[vendor_string]) 							# Get Vendor-specific fields
		mrs_keys        = list(MRSinMRS.keys()) 											# Get MRSinMRS Dictionary Items

		MRSinMRS_values = []   																# Store Values in List
		for ii in range(len(vendor_keys)):			 										# Iterate over Vendor Fields
			if isinstance(vendor_keys[ii], str) == True and vendor_keys[ii] in mrs_keys: 	# If Item in Vendor Fields
				if isinstance(MRSinMRS[vendor_keys[ii]], bytes):
					MRSinMRS[vendor_keys[ii]] = MRSinMRS[vendor_keys[ii]].decode()			
				MRSinMRS_values.append(MRSinMRS[vendor_keys[ii]]) 							# Add Item
			else: 	 																		# Not in Vendor Fields
				MRSinMRS_values.append('') 													# Skip Item

		self.MRSinMRS_Table['Values'] = MRSinMRS_values 									# Add Values to MRSinMRS Table

	def table_to_latex(self,): 																# Convert Table to LaTeX
		
		mrs_fields = list(self.MRSinMRS_Table.Generic) 										# Generic Field Names
		errors     = '' 																	# Instatiate String to Log Errors

		with open(self.latex_file, 'r') as f: 												# Open Generic LaTeX File
			latex_content = f.read() 														# Read Content
			latex_fields  = re.findall(r'\\textbf{(\w+)}', latex_content) 					# Find Fields to Replace

		for ii in range(len(latex_fields)): 												# Iterate over Fields

			try: 																			# Try to Catch Errors
				if latex_fields[ii] in mrs_fields: 											# If Field to Replace is in Table
					df       = copy.deepcopy(self.MRSinMRS_Table) 							# Copy Table
					df       = df[df.Generic == latex_fields[ii]].reset_index(drop=True) 	# Get Copied Table Row
					df_value = str(df.Values[0]) 											# Get Field's Value as String
					df_value = df_value.replace('_', '') 									# Remove any underscores for LaTeX

					if len(df_value) > 1: 													# Empty Strings - Should be > 2 characters
						latex_content = latex_content.replace('\\textbf{{{}}}'.format(      # Replace with Field's Value
																latex_fields[ii]), df_value)						
			
			except Exception as e: 															# Catch Errors
				errors = '{}\nLaTeX Fx : {:3d} {} {}'.format(errors, ii, latex_fields[ii], e)
				print('Error: ', e) 														# Note Error

		return latex_content, errors


class DataReaders():
	def __init__(self,):
		pass

	def siemens_twix(self, fname, log):

		## Siemens Twix
		write_log(log, 'Data Read: Siemens Twix') 											# Log - Twix
		try:
			from mapvbvd import mapVBVD  													# Siemens File Reading with pymapVBVD
			twixObj  = mapVBVD(fname)  														# Get Twix Object

			if isinstance(twixObj, list) == True:
				twixHd   = twixObj[1]['hdr'] 												# Get Twix Header Single Header
				twixPhx  = twixObj[1]['hdr'].Phoenix
			else:
				twixHd   = twixObj['hdr'] 													# Get Twix Header Multiple Headers
				twixPhx  = twixObj['hdr'].Phoenix

		except Exception as e:
			write_log(log, 'Data Read: Siemens Twix - Data Reader Failed') 					# Log - Note Failure
			write_log(log, 'Data Read: Siemens Twix - Error - {}'.format(e)) 				# Log - Note Error Message
			return {}, log 																	# Return Empty Dict and Log File

		## Successfully Read Data - Get Header Information
		write_log(log, 'Data Read: Siemens Twix - Data Reader Successful') 					# Log - Note Success
		MRSinMRS = {} 																		# Create MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'      ]  = 'Siemens'


		## Siemens Twix Object Fields
		dicom_header                    = list(twixHd['Dicom' ].keys())   					# Twix Object Dicom Header
		for ii in range(len(dicom_header)):	 												# Twix Object Dicom Header
			MRSinMRS[dicom_header[ii]]  = twixHd['Dicom' ][dicom_header[ii]]				# Twix Object Dicom Header

		config_header                   = list(twixHd['Config' ].keys())  					# Twix Object Config Header
		for ii in range(len(config_header)):	 											# Twix Object Config Header
			MRSinMRS[config_header[ii]] = twixHd['Config' ][config_header[ii]]				# Twix Object Config Header

		if 'TE_Time' not in list(MRSinMRS.keys()) and 'TE' not in list(MRSinMRS.keys()):
			try:
				MRSinMRS['TE'] = twixPhx(('alTE', '0'))
			except Exception as e:
				write_log(log, 'Data Read: Siemens Twix - Cannot Find TE') 					# Log - Note Lack of TE

		## Calculate Spectral Width - 
		#    Siemens doesn't automatically calculate 
		#    and DwellTime may be named differently across versions.
		headers                         = [] 												# Combine all the Headers
		headers.extend(dicom_header) 														# Dicom Header Fields
		headers.extend(config_header)														# Config Header Fields
		for ii in range(len(headers)): 														# Iterate over Header Fields
			if 'dwelltime' in headers[ii].lower(): 											# Find Dwell Time
				MRSinMRS[headers[ii]]     = str(MRSinMRS[headers[ii]]).replace(',', '.')
				MRSinMRS['SpectralWidth'] =  1 / (float(MRSinMRS[headers[ii]]) * 1e-9) 		# Calulcate Spectral Width


		## Correct Echo/Repetition Time Units
		if 'TE' in list(MRSinMRS.keys()):
			MRSinMRS['TE'              ]  = str(MRSinMRS['TE']).replace(',', '.')
			MRSinMRS['TE'              ]  = float(MRSinMRS['TE'   ]) / 1e3					# Echo Time
		if 'TR' in list(MRSinMRS.keys()):
			MRSinMRS['TR'              ]  = str(MRSinMRS['TR']).replace(',', '.')
			MRSinMRS['TR'              ]  = float(MRSinMRS['TR'   ]) / 1e3  				# Repetition Time

		write_log(log, 'Data Read: Siemens Twix - Returning MRSinMRS Dictionary') 			# Log - Note Success
		return MRSinMRS, log 																# Return MRSinMRS Dictionary

	def siemens_ima(self, fname, log):

		## Siemens Dicom
		write_log(log, 'Data Read: Siemens Dicom') 											# Log - Siemens Dicom
		try:
			from spec2nii.Siemens.dicomfunctions import multi_file_dicom					# Read Siemens Dicom with spec2nii
			imageOut, _  = multi_file_dicom([fname], os.path.dirname(fname), None, False)  	# Get Siemens Dicom Object
			hdr          = imageOut[0].__dict__['_hdr_ext'].__dict__ 						# Siemens Dicom Header
			image        = imageOut[0].__dict__['image'   ].__dict__ 						# Siemens Dicom Image Params

		except Exception as e:
			write_log(log, 'Data Read: Siemens Dicom - Data Reader Failed') 				# Log - Note Failure
			write_log(log, 'Data Read: Siemens Dicom - Error - {}'.format(e)) 				# Log - Note Error Message
			return {}, log 																	# Return Empty Dict and Log File


		## Successfully Read Data - Get Header Information
		write_log(log, 'Data Read: Siemens Dicom - Data Reader Successful') 				# Log - Note Success
		MRSinMRS = {} 																		# Create MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'   ] = 'Siemens'
		MRSinMRS['Model'          ] = hdr['_standard_data'  ]['ManufacturersModelName'] 	# Siemens Model
		MRSinMRS['SoftwareVersion'] = hdr['_standard_data'  ]['SoftwareVersions'      ] 	# Siemens Version
		MRSinMRS['Nucleus'        ] = hdr['ResonantNucleus' ][0                       ] 	# Nucleus
		MRSinMRS['Sequence'       ] = hdr['_standard_data'  ]['ProtocolName'          ] 	# Sequence
		MRSinMRS['ap_size'        ] = image['_Nifti__pixdim'][0                       ] 	# Anterior Posterior
		MRSinMRS['lr_size'        ] = image['_Nifti__pixdim'][1                       ] 	# Left Right
		MRSinMRS['cc_size'        ] = image['_Nifti__pixdim'][2                       ] 	# CranioCaudal
		MRSinMRS['dwelltime'      ] = image['_Nifti__pixdim'][3                       ] 	# DwellTime
		MRSinMRS['TR'             ] = hdr['_standard_data'  ]['RepetitionTime'        ] 	# TR
		MRSinMRS['TE'             ] = hdr['_standard_data'  ]['EchoTime'              ] 	# TE
		MRSinMRS['VectorSize'     ] = image['_Nifti__shape' ][3                       ] 	# Vector Size

		MRSinMRS['FieldStrength'  ] = hdr['SpectrometerFrequency'][0                  ] 	# Field Strength

		MRSinMRS['TR'             ]*= 1e3 													# Units Milliseconds
		MRSinMRS['TE'             ]*= 1e3 													# Units Milliseconds

		try:
			MRSinMRS['TI'         ] = hdr['_standard_data'  ]['InversionTime'         ] 	# TI
			MRSinMRS['TI'         ]*= 1e3 													# Units Milliseconds
		except:
			write_log(log, 'Data Read: Inversion Time Not Included') 						# Log - Inversion time not included


		try:
			write_log(log, 'Data Read: Assuming oversampled by a factor of 2.. doubling SpectralWidth') # Log - Note Spectral Width
			MRSinMRS['SW'] = (1 / (MRSinMRS['dwelltime'] / 2)) 								# Spectral Width
		except:
			write_log(log, 'Data Read: Siemens Dicom - Could not get Spectral Width') 		# Log - Note Success


		write_log(log, 'Data Read: Siemens Dicom - Returning MRSinMRS Dictionary') 			# Log - Note Success
		return MRSinMRS, log 																# Return MRSinMRS Dictionary and Log

	def siemens_rda(self, fname, log):

		## Siemens RDA
		#    This is a modified and simplified version of spec2nii's convert_rda()
		
		write_log(log, 'Data Read: Siemens RDA') 											# Log - Siemens Dicom

		hdr_st   = re.compile(r'>>> Begin of header <<<'  ) 								# Header
		hdr_val  = re.compile(r'^([\d\w\[\],]+): (.*)\r\n') 								# Header
		hdr_end  = re.compile(r'>>> End of header <<<'    ) 								# Header
		MRSinMRS = {} 																		# MRSinMRS Table

		try:
			with open(fname, 'rb') as f: 													# Open Binary
				for ll in f: 																# Iterate over lines
					if hdr_st.search(ll.decode()): 											# Identify Start
						pass
					elif hdr_end.search(ll.decode()): 										# Identify End
						break
					else: 																	# Extract Values
						match = hdr_val.search(ll.decode())
						if len(match.groups()) < 2:
							MRSinMRS[match[1]] = None
						else:
							MRSinMRS[match[1]] = match[2]

		except Exception as e:
			write_log(log, 'Data Read: Siemens RDA - Data Reader Failed') 					# Log - Note Failure
			write_log(log, 'Data Read: Siemens RDA - Error - {}'.format(e)) 				# Log - Note Error Message
			return {}, log 																	# Return Empty Dict and Log File	

		try:
			if 'DwellTime' in list(MRSinMRS.keys()) and 'SpectralWidth' not in list(MRSinMRS.keys()):
				write_log(log, 'Data Read: Assuming oversampled by a factor of 2.. doubling SpectralWidth') # Log - Note Spectral Width
				MRSinMRS['DwellTime'] = MRSinMRS['DwellTime'].replace(',', '.')
				MRSinMRS['SW'] = (1 / ( (float(MRSinMRS['DwellTime']) / 2) / 1e6)) 			# Spectral Width 2x Oversampling
		except:
			write_log(log, 'Data Read: Siemens RDA - Could not get Spectral Width') 		# Log - Note Success

		return MRSinMRS, log 																# Return MRSinMRS Dictionary and Log

	def philips_spar(self, fname, log):

		## Philips SPAR
		write_log(log, 'Data Read: Philips SPAR ') 											# Log - 

		try:
			from spec2nii.Philips.philips import read_spar   								# Read Philips with spec2nii
			spar_params  = read_spar(fname) 												# Read spar (Header file)
			spar_params_ = list(spar_params.keys()) 										# Header Items

		except Exception as e:
			write_log(log, 'Data Read: Philips SPAR - Data Reader Failed') 					# Log - 
			write_log(log, 'Data Read: Philips SPAR - Error - {}'.format(e)) 				# Log - 
			return {}, log 																	# Return Empty Dict and Log File


		## Successfully Read Data - Get Header Information
		write_log(log, 'Data Read: Philips SPAR - Data Reader Successful') 					# Log Note Success
		MRSinMRS     = {} 																	# MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'] = 'Philips' 												# Manufacturer

		for ii in range(len(spar_params_)): 												# Iterate over Header items
			try:
				MRSinMRS[spar_params_[ii]] = spar_params[spar_params_[ii]] 					# Populate MRSinMRS Dictionary
			except Exception as e:
				print('{:3d}| {:<25} =  *** warning ***'.format(ii, spar_params_[ii], ))

		write_log(log, 'Data Read: Philips SPAR - Returning MRSinMRS Dictionary') 			# Log - Note Success
		return MRSinMRS, log 																# Return MRSinMRS Dictionary

	def ge_7(self, fname, log):

		write_log(log, 'Data Read: GE Pfile ') 												# Log - 

		try:
			from spec2nii.GE import ge_read_pfile 											# Read GE with spec2nii
			pfile    = ge_read_pfile.Pfile(fname) 											# Read Pfile
			dumped   = pfile._dump_struct(pfile.hdr) 										# Pfile Header

		except Exception as e:
			write_log(log, 'Data Read: GE Pfile - Data Reader Failed') 						# Log - 
			write_log(log, 'Data Read: GE Pfile - Error - {}'.format(e)) 					# Log - 
			return {}, log 																	# Return Empty Dict and Log File


		## Successfully Read Data - Get Header Information
		write_log(log, 'Data Read: GE Pfile - Data Reader Successful') 						# Log - 
		MRSinMRS = {} 																		# MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'      ] = 'GE' 												# Manufacturer

		cnt      = 0  																		# Iterator
		for info in dumped:             													# Iterate over Header Items
			if (info.label.find("pad") == 0): 												# Skip
				continue

			MRSinMRS[info.label] = info.value 												# Get Header Item
			cnt +=1 																		# Count

		MRSinMRS['rhi_tr'            ] = MRSinMRS['rhi_tr'            ] / 1e3 				# Repetition Time in Milliseconds
		MRSinMRS['rhi_te'            ] = MRSinMRS['rhi_te'            ] / 1e3 				# Echo Time in Milliseconds

		write_log(log, 'Data Read: GE Pfile - Returning MRSinMRS Dictionary') 				# Log - Note Success
		return MRSinMRS, log																# Return MRSinMRS Dictionary

	def bruker_2dseq(self, fname, log):

		write_log(log, 'Data Read: Bruker 2dseq') 											# Log - Note Success

		try:
			from brukerapi.dataset import Dataset  											# BrukerAPI from Tomáš Pšorn
			dataset  = Dataset(fname) 														# Read Bruker 2dseq File
		
		except Exception as e:
			write_log(log, 'Data Read: Bruker 2dseq - Data Reader Failed') 					# Log - 
			write_log(log, 'Data Read: Bruker 2dseq - Error - {}'.format(e)) 				# Log - 
			return {}, log 																	# Return Empty Dict and Log File


		## Successfully Read Data - Get Header Information
		write_log(log, 'Data Read: Bruker 2dseq - Successful') 								# Log - Note Success
		
		MRSinMRS = {} 																		# Create MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'   ] = 'Bruker' 												# Manufacturer is Bruker	
		MRSinMRS['FieldStrength'  ] = dataset.imaging_frequency								# Field Strength - Round to 1 decimal
		MRSinMRS['TR'          	  ] = dataset.TR 											# Repetition Time
		MRSinMRS['TE'          	  ] = dataset.TE 											# Echo Time
		MRSinMRS['Sequence'       ] = dataset.type 											# Echo Time
		MRSinMRS['Averages'       ] = dataset.shape_frames									# Number of Transients
		
		MRSinMRS['SoftwareVersion'] = 'PV {}'.format(dataset.pv_version)					# ParaVision Software Version

		write_log(log, 'Data Read: Bruker 2dseq - Returning MRSinMRS Dictionary') 			# Log - Note Success
		return MRSinMRS, log

	def bruker_method(self, fname, log):

		MRSinMRS = {} 																		# Create MRSinMRS Dictionary to Populate
		MRSinMRS['Manufacturer'   ] = 'Bruker' 												# Manufacturer is Bruker	


		## Read and Parse Method file
		with open(fname, 'r') as f: 														# Open
			method = f.read()		 														# Read
			method = method.split('##') 													# Split by Field


		## Convert Method file to MRSinMRS Dictionary
		for ii in range(len(method)): 														# Iterate
			if len(method[ii]) > 1: 														# If the line is not blank
				method[ii]    = method[ii].replace('\n', '; ') 								# Shorten Everything to 1 line
				method[ii]    = method[ii].split('=') 										# Split by Key and Value

				try:
					MRSinMRS[method[ii][0]] = method[ii][1] 								# Populate MRSinMRS Dictionary
				except Exception as e:
					continue


		mrsinmrs_keys  = list(MRSinMRS.keys())
		for ii in range(len(mrsinmrs_keys)):
			if '$$ @vis' in MRSinMRS[mrsinmrs_keys[ii]]:
				MRSinMRS[mrsinmrs_keys[ii]] = MRSinMRS[mrsinmrs_keys[ii]].split('$$ @vis')[0]
				MRSinMRS[mrsinmrs_keys[ii]] = MRSinMRS[mrsinmrs_keys[ii]].strip()


		field_strength = MRSinMRS['$PVM_FrqRef'].split('; ')[1].split(' ')[0] 				# Bruker Field Strength
		field_strength = float(field_strength) 												# Bruker Field Strength in T

		WS             = MRSinMRS['$PVM_WsMode'      ].replace(';', '') 					# Water Suppression
		Nucleus        = MRSinMRS['$PVM_Nucleus1Enum'].replace(';', '') 					# Nucleus
		
		if '1H' in Nucleus:
			Nucleus = '1H'
		elif '2H' in Nucleus:
			Nucleus = '2H'
		elif '13C' in Nucleus:
			Nucleus = '13C'
		elif '15N' in Nucleus:
			Nucleus = '15N'
		elif '17O' in Nucleus:
			Nucleus = '17O'
		elif '23Na' in Nucleus:
			Nucleus = '23Na'
		elif '31P' in Nucleus:
			Nucleus = '31P'

		Sequence       =       MRSinMRS['$Method'][1:-3] 									# Sequence
		SW             =       MRSinMRS['$PVM_SpecSWH'].split(';')[1].strip() 				# Spectral Width Hertz
		TR             = float(MRSinMRS['$PVM_RepetitionTime'].replace(';', '')) 			# Repetition Time
		TE             = float(MRSinMRS['$PVM_EchoTime'].replace(';', '')) 					# Echo Time

		software       = MRSinMRS['TITLE'].split('ParaVision')[1]
		software       = 'ParaVision {}'.format(software)

		averages       = MRSinMRS['$PVM_NAverages'   ].replace(';', '').strip()				# Number of Blocks
		repetitions    = MRSinMRS['$PVM_NRepetitions'].replace(';', '').strip() 			# Transients per Block
		vectorsize     = MRSinMRS['$PVM_SpecMatrix'  ].split(')')[1] 						# Number of Datapoints
		vox_dims       = MRSinMRS['$PVM_VoxArrSize'].split(')')[1] 							# Voxel Dimensions

		vectorsize     = vectorsize.replace(';', '').strip() 								# 
		vox_dims       = vox_dims.replace(';', '')
		vox_dims       = vox_dims.lstrip().rstrip()
		vox_dims       = vox_dims.split(' ')

		MRSinMRS['FieldStrength'   ] = field_strength										# Field Strength - Round to 1 decimal
		MRSinMRS['SoftwareVersion' ] = software												# Software Version
		MRSinMRS['Nucleus'         ] = Nucleus												# Nucleus
		MRSinMRS['Sequence'        ] = Sequence 											# Sequence
		MRSinMRS['SW'          	   ] = SW													# Spectral Width
		MRSinMRS['TR'          	   ] = TR													# Repetition Time
		MRSinMRS['TE'          	   ] = TE 													# Echo Time

		MRSinMRS['NumberOfAverages'] = int(averages) * int(repetitions) 					# Total Number of Transients
		MRSinMRS['VectorSize'      ] = int(vectorsize) 										# Number of Datapoints
		
		MRSinMRS['ap_size'         ] = float(vox_dims[0]) 									# AP Size
		MRSinMRS['lr_size'         ] = float(vox_dims[1]) 									# LR Size
		MRSinMRS['cc_size'         ] = float(vox_dims[2]) 									# CC Size
		
		MRSinMRS['WaterSuppression'] = WS 													# Water Suppression

		return MRSinMRS, log

	def nifti_json(self, fname, log):

		## NIfTI JSON
		write_log(log, 'Data Read: NIfTI JSON ') 											# Log - 

		try:
			with open(fname, 'r') as json_file: 											# Open NIfTI JSON File
				MRSinMRS = json.load(json_file) 											# Load JSON Data
				write_log(log, 'Data Read: NIfTI JSON - Data Reader Successful') 			# Log Note Success

		except Exception as e:																# Failed Reading NIfTI JSON File
			write_log(log, 'Data Read: NIfTI JSON - Data Reader Failed') 					# Log - Note Failure
			write_log(log, 'Data Read: NIfTI JSON - NOTE** Ensure .json was provided')		# Log - Note Failure
			write_log(log, 'Data Read: NIfTI JSON - Error - {}'.format(e)) 					# Log - Error 

		json_items = list(MRSinMRS.keys())
		if len(json_items) < 1: 															# JSON read failed
			MRSinMRS = {} 																	# Empty MRSinMRS dict
			return MRSinMRS, log															# Return MRSinMRS Dictionary

		for ii  in range(len(json_items)):
			if isinstance(MRSinMRS[json_items[ii]], list):
				MRSinMRS[json_items[ii]] = MRSinMRS[json_items[ii]][0]

		write_log(log, 'Data Read: NIfTI JSON - Returning MRSinMRS Dictionary') 			# Log - Note Success
		return MRSinMRS, log																# Return MRSinMRS Dictionary


if __name__ == '__main__':
	app = Application(lwrite=True)
	app.mainloop()

