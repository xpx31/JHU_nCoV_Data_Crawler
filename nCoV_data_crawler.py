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
import time
import os


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
		gid_ = "" if gid is None else "gid=" + str(gid) + "&"
		url = "{0}/export?{1}format=csv".format(url, gid_)
		print(url)

		# Output path
		today = str(datetime.datetime.today())[:19].replace(" ", "_").replace(":", "_")
		self.filepath = "./Data/data_{0}.csv".format(today)

		# Run curl command to save data
		bash_com = "curl -o {0} {1}".format(self.filepath, url)
		print(bash_com)

		try:
			p = subprocess.Popen(bash_com)
			subprocess.check_output(['bash', '-c', bash_com])
			p.wait()
		except subprocess.CalledProcessError:
			print("Error in crawling " + url)
		except ValueError:
			print("bash command not valid, examine url: " + url)

		# Return pandas dataframe
		return pd.read_csv(self.filepath) if df_output else None

	def cont_crawl(self, url=None, sleep=7200):
		"""
		continuous crawling from the JHU Google Spreadsheet
		delete any duplicated csv files saved

		:param url: base url of the google spreadsheet
									eg. "https://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM"
		:param sleep: sleep time between each crawl, 2 hours by default
		:return: None
		"""

		while True:
			filepath_old = self.filepath
			df_new = self.crawl(url)

			if filepath_old is None:
				pass
			else:
				df_old = pd.read_csv(filepath_old)
				if df_new.equals(df_old):
					os.remove(self.filepath)
					self.filepath = filepath_old

			time.sleep(sleep)


dc = Data_Crawler()
dc.cont_crawl()
