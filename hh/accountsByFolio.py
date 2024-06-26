# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Mar  6 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.adv
import re

from connectToDb import connectToDB

conn = connectToDB()

###########################################################################
## Class MyFrame1
###########################################################################

class folioAccountsPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		self.selectedFolio = 'Cash'
		
		wx.Panel.__init__ ( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		
		bSizerMain = wx.BoxSizer( wx.VERTICAL )
		
		bSizerDate = wx.BoxSizer( wx.HORIZONTAL )
		bSizerGrid = wx.BoxSizer( wx.HORIZONTAL )
		
		########### Combo Box Start
		self.folios = self.fetchFolios()
		
		self.m_folioCombo = wx.ComboBox(self, size=wx.DefaultSize, choices= list(self.folios.keys()) )

		########### Combo Box End
		bSizerDate.Add (self.m_folioCombo, 1, wx.ALL|wx.EXPAND, 5 )

		
		########### Date Picker Start
		self.m_startDate = wx.adv.DatePickerCtrl(self, size=(60,-1),dt=wx.DateTime.Now(), style = wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
		self.m_endDate = wx.adv.DatePickerCtrl(self, size=(60,-1),dt=wx.DateTime.Now(), style = wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
		########### Date Picker End
		
		bSizerDate.Add (self.m_startDate, 1, wx.ALL|wx.EXPAND, 5 )
		bSizerDate.Add (self.m_endDate, 1, wx.ALL|wx.EXPAND, 5 )
		
		########### Cart Grid Start
		self.m_journalGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_journalGrid.CreateGrid( 500, 10 )
		self.m_journalGrid.EnableEditing( False )
		self.m_journalGrid.EnableGridLines( True )
		self.m_journalGrid.EnableDragGridSize( False )
		self.m_journalGrid.SetMargins( 0, 0 )
		self.m_journalGrid.SetRowLabelSize( 1 )
		#self.m_journalGrid.AutoSizeColLabelSize( True )
		
		'''
		self.m_journalGrid.SetColSize( 0, 20 )
		self.m_journalGrid.SetColSize( 1, 40 )
		self.m_journalGrid.SetColSize( 2, 60 )
		self.m_journalGrid.SetColSize( 3, 80 )
		self.m_journalGrid.SetColSize( 4, 90 )
		self.m_journalGrid.SetColSize( 5, 110 )
		self.m_journalGrid.SetColSize( 6, 130 )
		self.m_journalGrid.SetColSize( 7, 150 )
		self.m_journalGrid.SetColSize( 8, 170 )
		'''
		
		self.m_journalGrid.SetColSize( 0, 30 )
		self.m_journalGrid.SetColSize( 1, 60 )
		self.m_journalGrid.SetColSize( 2, 90 )
		self.m_journalGrid.SetColSize( 3, 120 )
		self.m_journalGrid.SetColSize( 4, 150 )
		self.m_journalGrid.SetColSize( 5, 180 )
		self.m_journalGrid.SetColSize( 6, 210 )
		self.m_journalGrid.SetColSize( 7, 240 )
		self.m_journalGrid.SetColSize( 8, 270 )
		self.m_journalGrid.SetColSize( 9, 300 )
		
		self.m_journalGrid.SetColLabelValue( 0, u"ID" )
		self.m_journalGrid.SetColLabelValue( 1, u"Date" )
		self.m_journalGrid.SetColLabelValue( 2, u"Time" )
		self.m_journalGrid.SetColLabelValue( 3, u"Head of A/C" )
		self.m_journalGrid.SetColLabelValue( 4, u"Folio Number" )
		self.m_journalGrid.SetColLabelValue( 5, u"Transaction ID" )
		self.m_journalGrid.SetColLabelValue( 6, u"Cheque Number" )
		self.m_journalGrid.SetColLabelValue( 7, u"Debit" )
		self.m_journalGrid.SetColLabelValue( 8, u"Credit" )
		self.m_journalGrid.SetColLabelValue( 9, u"Balance" )
		
		self.m_journalGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		self.m_journalGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		self.populateTable()
		########### Cart Grid End
		
		bSizerGrid.Add (self.m_journalGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizerMain.Add( bSizerDate, 1, wx.ALL|wx.EXPAND, 5 )
		bSizerMain.Add( bSizerGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizerMain )
		self.Layout()
		bSizerMain.Fit( self )
		
		self.m_startDate.Bind(wx.adv.EVT_DATE_CHANGED, self.dateChangeHandler)
		self.m_endDate.Bind(wx.adv.EVT_DATE_CHANGED, self.dateChangeHandler)
		self.m_folioCombo.Bind(wx.EVT_COMBOBOX, self.folioChangeHandler)
		
	def folioChangeHandler (self, event):
		self.selectedFolio = self.m_folioCombo.GetValue()
		self.reloadJournal()
	
	def dateChangeHandler (self, event):
		self.reloadJournal()
	
	def reloadJournal (self):
		self.m_journalGrid.DeleteRows(numRows=self.m_journalGrid.GetNumberRows())
		self.m_journalGrid.InsertRows(numRows=500)
		
		self.populateTable()
	
	def transformHOAtoName (self, desc):
		x = re.search ("(?<=Customer)[0-9]*", desc)
		if x is not None:
			q = 'SELECT name FROM customer WHERE id = %s' % (x.group(0))
			c = conn.cursor()
			c.execute(q)
			cust = c.fetchone()
			return cust['name'] + " A/C Recievable"

		x = re.search ("(?<=Supplier)[0-9]*", desc)
		if x is not None:
			q = 'SELECT name FROM supplier WHERE id = %s' % (x.group(0))
			c = conn.cursor()
			c.execute(q)
			cust = c.fetchone()
			return cust['name'] + " A/C Payable"
		return None
	
	def fetchFolios (self):
		qry = 'SELECT id, description FROM headOfAccounts'
		curs = conn.cursor()
		curs.execute(qry)
		r = curs.fetchall()
		
		folios = {}
		for x in r:
			z = self.transformHOAtoName(x['description'])
			if z is not None:
				folios.update({z : x['id']})
			else:
				folios.update({x['description'] : x['id']})
		return folios
	
	def populateTable (self):
		#print(type(self.m_startDate.GetValue()))
		#print(type(self.m_endDate.GetValue().Format("%F")))
		if (self.selectedFolio[:8] == "Customer" and self.selectedFolio[-1:] == "R"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio[:8] == "Supplier" and self.selectedFolio[-1:] == "P"):
			computation = "SUM(Credit) - SUM(Debit)"
		elif (self.selectedFolio == "Purchase"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio == "Sale"):
			computation = "SUM(Credit) - SUM(Debit)"
		elif (self.selectedFolio == "Cash"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio == "Bank"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio == "SalesDiscount"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio == "PurchaseDiscount"):
			computation = "SUM(Credit) - SUM(Debit)"
		elif (self.selectedFolio == "SalesReturn"):
			computation = "SUM(Debit) - SUM(Credit)"
		elif (self.selectedFolio == "PurchaseReturn"):
			computation = "SUM(Credit) - SUM(Debit)"
		else:
			computation = "SUM(Credit) - SUM(Debit)"
		
		st = self.m_startDate.GetValue().Format("%F") + " 00:00:00"
		et = self.m_endDate.GetValue().Format("%F") + " 23:59:59"
		qry = '''SELECT 
				gl.id, gl.dateTime, hoa.description, gl.headOfAc, gl.transactionType, gl.chequeNo, gl.Debit, 					gl.Credit, ( SELECT %s FROM generalLedger WHERE id <= gl.id and headOfAc = "%s" AND dateTime BETWEEN "%s" AND "%s" ) AS Balance 
			FROM generalLedger gl, headOfAccounts hoa 
			WHERE gl.headOfAc = hoa.id AND gl.dateTime BETWEEN "%s" AND "%s" AND hoa.id = "%s" LIMIT 500''' % ( computation, self.folios[self.selectedFolio], st, et, st, et, self.folios[self.selectedFolio] )
		
		con = connectToDB()
		curs = con.cursor()
		curs.execute(qry)
		
		row = 0
		while (1):
			r = curs.fetchone()
			if (r is not None):
				x = re.search ("(?<=Customer)[0-9]*", r['description'])
				if x is not None:
					q = 'SELECT name FROM customer WHERE id = %s' % (x.group(0))
					c = con.cursor()
					c.execute(q)
					cust = c.fetchone()
					r['description'] = cust['name'] + " A/C Recievable"
				
				x = re.search ("(?<=Supplier)[0-9]*", r['description'])
				if x is not None:
					q = 'SELECT name FROM supplier WHERE id = %s' % (x.group(0))
					c = con.cursor()
					c.execute(q)
					cust = c.fetchone()
					r['description'] = cust['name'] + " A/C Payable"
				
				self.m_journalGrid.SetCellValue(row, 0, str(r['id']))
				self.m_journalGrid.SetCellValue(row, 1, str(r['dateTime'])[:11])
				self.m_journalGrid.SetCellValue(row, 2, str(r['dateTime'])[11:])
				
				if (r['Credit'] > 0):
					self.m_journalGrid.SetCellValue(row, 3, "        "+r['description'])
					self.m_journalGrid.SetCellValue(row, 8, str(r['Credit']))
				else:
					self.m_journalGrid.SetCellValue(row, 3, r['description'])
					self.m_journalGrid.SetCellValue(row, 7, str(r['Debit']))
				self.m_journalGrid.SetCellValue(row, 4, str(r['headOfAc']))
				self.m_journalGrid.SetCellValue(row, 5, r['transactionType'])
				if (r['chequeNo'] is not None):
					self.m_journalGrid.SetCellValue(row, 6, r['chequeNo'])
				#self.m_journalGrid.SetCellValue(row, 7, str(r['Debit']))
				#self.m_journalGrid.SetCellValue(row, 8, str(r['Credit']))
				self.m_journalGrid.SetCellValue(row, 9, str(r['Balance']))
				
				row = row+1
			else:
				break
