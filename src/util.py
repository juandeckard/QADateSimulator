from pandas import read_excel
import datetime
from random import sample

def readExcel(fileName, titleRow, sheetName):
    try:
        excelFileName = "./io/input/" + fileName + ".xlsx"

        data = read_excel(excelFileName, header=(int(titleRow) - 1), sheet_name=sheetName)#, usecols=['provider_url', 'active'])
        
        return data
    except Exception as ex:
        print(ex)
        input()

def sameDayOfnextWeek(today):
    today = datetime.datetime.strptime(today,"%d-%m-%Y")
    next_Day = today + datetime.timedelta(days=-today.weekday()+1, weeks=1)
    return next_Day.strftime("%d-%m-%Y")

def listToTuplaWithElement(listOfElements,Date):
    outputList = []
    nextDate = sameDayOfnextWeek(Date)
    for element in listOfElements:
         outputList += [(element,nextDate)]
    return outputList

def getUsefulData(filename, row_number, sheetname):
	df = readExcel(filename, row_number, sheetname)
	df["QA_Date"] = ""

	QAData = df[['active.1','structure.1', 'rental.1', "QA_Date"]]
	QAData = QAData.rename(columns = {"active.1": "active",
    	                              "structure.1": "structure",
        	                          "rental.1": "rental"})
	return QAData, len(QAData)

def findQAable(QAData):
	QAable = []
	for index, row in QAData.iterrows():
	    # We don't want resorts, timeshares, RVs, rooms or inactives
	    if not(row.structure == "resort" or row.structure == "timeshare" or row.structure == "RV" or row.rental == "room" or row.active == "no"):
	        QAable.append(index)
	return QAable

def generateWeeklyQA(QAable):
	batch_size = 5#int(input("Batch size: "))

	QAable_local = QAable.copy()
	index_table  = []
	weekly_QA    = []

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

def reduceTuples(date_map):
	results = []
	for week in date_map:
	    for listing in week:
	        results.append(listing)
	return results

def sortTuples(reduced):
	return sorted(reduced, key=lambda x: x[0])

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

