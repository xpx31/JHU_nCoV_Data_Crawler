"""

Script Description:
Crawl Johns Hopkins University Novel Coronavirus Google Spreadsheet
https://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM

Save the data as in csv format and can return pandas dataframe

DISCLAIMER:
Crawled Data source: John Hopkins University
Original Data sources: WHO, CDC, ECDC, NHC and DXY.

All data crawled from this script, copyright 2020 Johns Hopkins University, all rights reserved.
The information crawled using this crawler is provided to the public strictly for educational and academic research
purposes. Refer to Johns Hopkins University disclaimer for data source concerns.

All scripts within this document are protected by copyright to the creator(s) listed below. This script is provided
strictly for educational and academic research purposes. The creator(s) listed below disclaims any and all
representations and warranties with respect to the scripts.

Created by Pengxiang Xu
Date: Feb/08/2020
Time: 15:29
"""

import pandas as pd
import subprocess
import datetime


class Data_Crawler:
	"""
	Crawl data from JHU 2019 nCoV Google Spreadsheet
	save it as csv under ./Data folder
	return corresponding pandas dataframe by default

	"""
	def __init__(self):
		self.filepath = None

	def crawl(self, url=None, gid=None, df_output=True):
		"""

		:param url: base url of the google spreadsheet
									eg. "https://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM"
		:param gid: the gid page number of the google sheet, see the url of google spread sheet for more detail
		:param df_output: flag indicating output a pandas dataframe for the content crawled
		:return:
		        df_output = True: dataframe for the content crawled
						df_output = False: None for a successful crawl

		"""
		# Determine url address
		url = url if url is not None \
			else "https://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM"
		gid = "" if None else "gid=" + str(gid) + "&"
		url = url + "/export?" + gid + "format=csv"

		# Output path
		today = str(datetime.datetime.today())[:19].replace(" ", "_").replace(":", "_")
		self.filepath = "./Data/data_" + str(today) + ".csv"

		# Run curl command to save data
		bash_com = "curl -o " + self.filepath + " " + url
		print(bash_com)

		try:
			subprocess.Popen(bash_com)
			subprocess.check_output(['bash', '-c', bash_com])
		except subprocess.CalledProcessError:
			print("Error in crawling " + url)
		except ValueError:
			print("bash command not valid, examine url: " + url)

		# Return pandas dataframe
		return pd.read_csv(self.filepath) if df_output else None
