from pandas import read_excel
import datetime
from random import sample
from datetime import date, timedelta, datetime


def readExcel(fileName, titleRow, sheetName):
	"""
	Inputs: File name with no file termination
			Example: If you have doc.txt, just write doc.

			Row where the title rows are at.
			Example: If the table headers are at row 2 and some space at row 1, input 2.

			Sheet name you are trying to read. 

	Output: A dataframe with the table.
	"""
	try:
		excelFileName = "./io/input/" + fileName + ".xlsx"

		data = read_excel(excelFileName, header=(int(titleRow) - 1), sheet_name=sheetName)#, usecols=['provider_url', 'active'])
		return data
	except Exception as ex:
		print(ex)
		input()

def startingDate():
	"""
	Input: None
	Output: returns next Tuesday date; todays date if today is Tuesday.
	"""
	if date.today().weekday() == 1:
		return date.today().strftime("%m/%d/%Y")
	else:
		return (date.today() + timedelta(days=date.today().weekday() + 1)).strftime("%m/%d/%Y")

def nextWeeksDate(currentDate):
	"""
	Input: An initial date format %d/%m/%Y
	Output: A date, 7 days after.
	"""
	return (datetime.strptime(currentDate,"%m/%d/%Y") + timedelta(days=7)).strftime("%m/%d/%Y")

def getUsefulData(filename, row_number, sheetname):
	df = readExcel(filename, row_number, sheetname)
	df["QA_Date"] = ""

	QAData = df[['url','address.2','raw_apn','active.1','residential.1','structure.1', 'rental.1', "comments"]]
	QAData = QAData.rename(columns = {
									  "address.2":"address",
									  "raw_apn":"apn",
									  "active.1": "active",
									  "residential.1":"residential",
									  "structure.1": "structure",
									  "rental.1": "rental"
									  })
	return QAData

def generateWeeklyQA(QAable, header_row, batch_size):
	# First, we sample the whole QAable array in order to have randomness.
	QAable = sample(QAable,len(QAable))

	# Now we make a new array with the dates. We initialize the date too.
	date = startingDate()
	dates = []
	while len(dates) < len(QAable):
		for index in range(5):
			dates.append(date)
		date = nextWeeksDate(date)
	# At this point we are not sure if the size match, so lets cut some at the end.
	while len(dates) != len(QAable):
		dates.pop()

	# Last thing is to make an array of arrays using this two bad boys.
	return list(zip(dates, [elem[0] + header_row + 1 for elem in QAable], [elem[1] for elem in QAable], [elem[2] for elem in QAable], [elem[3] for elem in QAable], [elem[4] for elem in QAable], [elem[5] for elem in QAable], [elem[6] for elem in QAable], [elem[7] for elem in QAable]))
	 

def findQAable(QAData):
	""" findQAable( DataFrame data ) : list """
	QAable = []
	for index, row in QAData.iterrows():
		# We don't want resorts, timeshares, RVs, rooms or inactives
		if not(type(row.url) != str or type(row.address) != str or row.structure == "resort" or row.structure == "timeshare" or row.structure == "hotel" or row.structure == "RV" or row.rental == "room" or row.active == "no"):
			QAable.append((index, '=HYPERLINK(' + row.url + ')', row.address, str(row.apn).replace('-',''), row.residential, row.structure, row.rental, row.comments))
	return QAable

def reduceTuples(date_map):
	""" reducedTuples( list tuples ) : list """
	results = []
	for week in date_map:
		for listing in week:
			results.append(listing)
	return results

def sortTuples(reduced, index):
	""" sortTuples( list reduced, int index ) : list """
	return sorted(reduced, key=lambda x: x[index])