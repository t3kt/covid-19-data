import datetime

def PrepareCountyTable(dat, inDat):
	dat.clear()
	dat.appendCol(['countyid'] + inDat.col('GEOID')[1:])
	dat.appendCol(['name'] + inDat.col('NAME')[1:])
	dat.appendCol(['tx'] + inDat.col('X')[1:])
	dat.appendCol(['ty'] + inDat.col('Y')[1:])


def PrepareCountyStatsTable(dat, inDat, countyTable, dateTable):
	dat.copy(inDat)
	dat.appendCols([
		['tx'],
		['ty'],
		['dateoffset'],
	])
	for i in range(1, dat.numRows):
		countyId = dat[i, 'fips']
		dat[i, 'tx'] = countyTable[countyId, 'tx']
		dat[i, 'ty'] = countyTable[countyId, 'ty']
		dat[i, 'dateoffset'] = dateTable[dat[i, 'date'], 'dateoffset']


def PrepareDateTable(dat):
	dat.appendCol(['dateoffset'])
	firstDay = datetime.date.fromisoformat(dat[1, 'date'].val)
	for i in range(1, dat.numRows):
		day = datetime.date.fromisoformat(dat[i, 'date'].val)
		offset = day - firstDay
		dat[i, 'dateoffset'] = offset.days

def BuildTimeLinesPrimitiveTable(dat, statsTable):
	dat.clear()
	countyPoints = {}
	for i in range(1, statsTable.numRows):
		countyId = statsTable[i, 'countyid'].val
		if countyId in countyPoints:
			countyPoints[countyId] += ' ' + str(i - 1)
		else:
			countyPoints[countyId] = str(i - 1)
	dat.appendRows([
		[points, '0']
		for points in countyPoints.values()
	])

