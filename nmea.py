class nmea():
	def __init__(self, debug=0):
		self._sentence = ''
		self.time = '00:00:00'
		self.date = '01/01/2000'
		self.latitude = 0
		self.longitude = 0
		self.satcount = 0
		self._debug = debug
		
	def dprint(self,mess):
		if self._debug:
			print(mess)
			
	def checksum(self):
		""" takes a sentence in the format 
			"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
			returns True / False
		"""
		# drop the '*47'
		t = self._sentence[:len(self._sentence)-3]
		a = 0
		# xor each character value
		for b in t:
			a ^= ord(b)
			
		# strip away the sentence to leave the '47'
		csum = self._sentence[len(self._sentence)-2:]
		# format the xor result into a hex string
		# return true if it's '47'
		return int(csum,16) == a
			
	def parse(self, b):
		# for all the characters collected
		for c in b:
			
			if chr(c) =='$':							# if '$' then it's the start of a sentence
				self._sentence = ""						# clear out the old sentence
			elif c == 0x0d:								# carriage return means completed sentence
				if 'GPRMC' in self._sentence:			# GPRMS - recommended minimum data for gps
					self.dprint(self._sentence)			# in debig - print the sentence
					self.format()						# grab the data from the sentence
				elif 'GPGSA' in self._sentence:			# GPRMS - recommended minimum data for gps
					self.dprint(self._sentence)			# in debug - print the sentence
					self.format()						# grab the data from the sentence
				else:
					self.dprint(self._sentence[:5])		# for other types just print the identifying letters
			else:
				self._sentence += chr(c)				# otherwise, just collect the character

	def degmin_to_decdeg(self, d):
		degs = int(d/100)
		mins = d % 100
		degs += mins/60
		return degs
		
	def format(self):
		if not self.checksum():
			self.dprint('BAD CHECKSUM')
			return
			
		data = self._sentence.split(',')
		
		if data[0] == 'GPRMC':
			# parse GPRMC
			
			# time of day (UTC)
			try:
				t = data[1]		# e.g. '073053'
				
				hh = t[:2]		# hours valid?
				if int(hh) < 0 or int(hh) > 23:
					return
				
				mm = t[2:4]		# minutes valid?
				if int(mm) < 0 or int(mm) > 59:
					return
					
				ss = t[4:6]		# seconds valid?
				if int(ss) < 0 or int(ss) > 59:
					return
				
				# format time string e.g.  '07:30:53'
				self.time = '{}:{}:{}'.format(hh, mm, ss)
			except Exception as e:
				dprint(e, 'time error', d)
				return
			
			try:
				d = data[9]		# e.g. 070817
				
				# format date string e.g. 07/08/2017
				self.date = '{}/{}/20{}'.format(d[:2], d[2:4], d[4:6])
			except Exception as e:
				dprint(e, 'date error', d)
			
			# test to see if position status is valid
			if data[2] != 'A':
				self.dprint('INVALID')
				return
				
			try:
				d = data[3]
				if d != '':
					d = self.degmin_to_decdeg(float(d))
					if data[4] == 'S':
						d = -1*d		
					self.latitude = d
			except Exception as e:
				dprint(e, 'latitude error', d)
			
			try:
				d = data[5]
				if d != '':
					d = self.degmin_to_decdeg(float(d))
					if data[6] == 'W':
						d = -1*d		
					self.longitude = d
			except Exception as e:
				dprint(e, 'longitude error', d)
				
		elif data[0] == 'GPGSA':
			# parse GPGSA
			if data[1] != 'A':
				self.dprint('INVALID')
				return
				
			satellites = 0
			for s in data[3:15]:
				# self.dprint(s)
				if s != '':
					satellites += 1
			self.satcount = satellites
			# self.dprint('satcount {}'.format(satellites))
				
		else:
			return


				
