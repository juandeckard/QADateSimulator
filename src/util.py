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

def sameDayOfnextWeek(today):
	"""
	Soon to be deprecated.
	"""
	today = datetime.datetime.strptime(today,"%d-%m-%Y")
	next_Day = today + datetime.timedelta(days=-today.weekday()+1, weeks=1)
	return next_Day.strftime("%d-%m-%Y")

def startingDate():
	"""
	Input: None
	Output: returns next Tuesday date; todays date if today is Tuesday.
	"""
	if date.today().weekday() == 1:
		return date.today().strftime("%d/%m/%Y")
	else:
		return (date.today() + timedelta(days=date.today().weekday() + 1)).strftime("%d/%m/%Y")

def nextWeeksDate(currentDate):
	"""
	Input: An initial date format %d/%m/%Y
	Output: A date, 7 days after.
	"""
	return (datetime.strptime(currentDate,"%d/%m/%Y") + timedelta(days=7)).strftime("%d/%m/%Y")

def listToTuplaWithElement(listOfElements,Date):
	outputList = []
	nextDate = sameDayOfnextWeek(Date)
	for element in listOfElements:
		outputList += [(element,nextDate)]
	return outputList

def getUsefulData(filename, row_number, sheetname):
	df = readExcel(filename, row_number, sheetname)
	df["QA_Date"] = ""

	QAData = df[['url' ,'address.2','raw_apn','active.1','structure.1', 'rental.1', "QA_Date"]]
	QAData = QAData.rename(columns = {
									  "address.2":"address",
									  "raw_apn":"apn",
									  "active.1": "active",
									  "structure.1": "structure",
									  "rental.1": "rental"
									  })
	return QAData, len(QAData)

def generateWeeklyQA(QAable, urls, addresses, apns, batch_size):
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
	sorted = sortTuples(list(zip(QAable, dates, urls,addresses,apns)),0)
	return list(zip(QAable, dates, [elem[0] for elem in sorted],[elem[1] for elem in sorted],[elem[2] for elem in sorted],[elem[3] for elem in sorted],[elem[4] for elem in sorted]))
	 

def findQAable(QAData):
	QAable = []
	for index, row in QAData.iterrows():
		# We don't want resorts, timeshares, RVs, rooms or inactives
		if not(row.structure == "resort" or row.structure == "timeshare" or row.structure == "hotel" or row.structure == "RV" or row.rental == "room" or row.active == "no"):
			QAable.append(index)
	return QAable
"""
def generateWeeklyQA(QAable):
	batch_size = 5#int(input("Batch size: "))

	QAable_local = QAable.copy()
	index_table  = []
	weekly_QA	= []

	while not len(QAable_local) == 0:
		samples = []
		if len(QAable_local) >= batch_size:
			samples = sample(QAable_local, (batch_size))
		elif len(QAable_local) < batch_size:
			samples = [elem for elem in QAable_local]
		weekly_QA.append(samples)
		for index in samples:
			QAable_local.remove(index)
	return weekly_QA

def generateDateMap(weekly_QA):
	date_map = []

	initial_date = "18-02-2020"#input("Initial date: ")

	for QA in weekly_QA:
		date_map.append(listToTuplaWithElement(QA, initial_date))
		initial_date = sameDayOfnextWeek(initial_date)
	return date_map
"""
def reduceTuples(date_map):
	results = []
	for week in date_map:
		for listing in week:
			results.append(listing)
	return results

def sortTuples(reduced, index):
	return sorted(reduced, key=lambda x: x[index])

def dateFormat(date):
	date = datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%m-%d-%Y")
	return date.replace('-','/',2)

def generateOutputFormat(sort, QAable, originalSize):
	dates = []
	unsorted_list = [elem[0] for elem in sort]
	for originalIndex in range(originalSize):
		if originalIndex in QAable:
			dates.append(dateFormat(sort[unsorted_list.index(originalIndex)][1]))
		else:
			dates.append("")
	return dates

