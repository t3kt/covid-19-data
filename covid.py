import datetime

def PrepareCountyTable(dat, inDat):
	dat.clear()
	dat.appendCol(['countyid'] + inDat.col('GEOID')[1:])
	dat.appendCol(['name'] + inDat.col('NAME')[1:])
	dat.appendCol(['tx'] + inDat.col('X')[1:])
	dat.appendCol(['ty'] + inDat.col('Y')[1:])

def PrepareDateTable(dat):
	dat.appendCol(['dateoffset'])
	firstDay = datetime.date.fromisoformat(dat[1, 'date'].val)
	for i in range(1, dat.numRows):
		day = datetime.date.fromisoformat(dat[i, 'date'].val)
		offset = day - firstDay
		dat[i, 'dateoffset'] = offset.days

def BuildTimeLinesPrimitiveTable(dat, reportsTable):
	dat.clear()
	countyPoints = {}
	for i in range(1, reportsTable.numRows):
		countyId = reportsTable[i, 'countyid'].val
		if countyId in countyPoints:
			countyPoints[countyId] += ' ' + str(i - 1)
		else:
			countyPoints[countyId] = str(i - 1)
	dat.appendRows([
		[points, '0']
		for points in countyPoints.values()
	])

def BuildValueTimelineByCounty(
		dat,
		countyTable,
		reportTable,
		dateTable,
		statName):
	dat.clear()
	dat.appendRow(['countyid'] + dateTable.col('date')[1:])
	dat.appendRows([[countyId] for countyId in countyTable.col('countyid')[1:]])
	for i in range(1, reportTable.numRows):
		countyId = reportTable[i, 'countyid'].val
		date = reportTable[i, 'date'].val
		outCell = dat[countyId, date]
		if outCell is None:
			raise Exception(f'unable to find cell for countyId: {countyId!r} date: {date!r}')
		val = reportTable[i, statName]
		outCell.val = val
