import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QAction, QHeaderView, QLineEdit, QLabel,
							 QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QDialog)
from PyQt5.QtGui import QPainter, QStandardItemModel, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries

class About(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("About MyWallet")
		self.resize(200,200)

class DataEntryForm(QWidget):
	def __init__(self):
		super().__init__()
		self.items = 0

		self._data = {}

		# left side
		self.table = QTableWidget()
		self.table.setColumnCount(2)
		self.table.setHorizontalHeaderLabels(('Item', 'Price'))
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.layoutRight = QVBoxLayout()

		# chart widget
		self.chartView = QChartView()
		self.chartView.setRenderHint(QPainter.Antialiasing) 
		
		self.lineEditDescription = QLineEdit()
		self.lineEditPrice = QLineEdit()
		self.lineEditName = QLineEdit()
		self.buttonAdd = QPushButton('Add to Table')
		self.buttonClear = QPushButton('Clear Everything')
		self.butotnPlot = QPushButton('Create Chart')
		self.button_csv = QPushButton('Save as .csv File')

		self.buttonAdd.setEnabled(False)

		self.copyright = QLabel("© Copyright Simple Apps 2020")
		self.copyright.setAlignment(Qt.AlignRight)

		self.layoutRight.setSpacing(10)
		self.layoutRight.addWidget(QLabel('Item Name Here'))
		self.layoutRight.addWidget(self.lineEditDescription)
		self.layoutRight.addWidget(QLabel('Price Here (Please only use numbers \nEx: 1000 or 1000.00)'))
		self.layoutRight.addWidget(self.lineEditPrice)
		self.layoutRight.addWidget(QLabel('Name you .csv file'))
		self.layoutRight.addWidget(self.lineEditName)
		self.layoutRight.addWidget(self.buttonAdd)
		self.layoutRight.addWidget(self.butotnPlot)
		self.layoutRight.addWidget(self.chartView)
		self.layoutRight.addWidget(self.buttonClear)
		self.layoutRight.addWidget(self.button_csv)
		self.layoutRight.addWidget(self.copyright)

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.table, 40)
		self.layout.addLayout(self.layoutRight, 60)

		self.setLayout(self.layout)

		self.buttonClear.clicked.connect(self.clear_table)
		self.butotnPlot.clicked.connect(self.graph_chart)
		self.buttonAdd.clicked.connect(self.add_item)
		self.button_csv.clicked.connect(self.export_to_csv)

		self.lineEditDescription.textChanged[str].connect(self.check_disable)
		self.lineEditPrice.textChanged[str].connect(self.check_disable)

		self.put_in_table()

	def put_in_table(self, data=None):
		data = self._data if not data else data

		for desc, price in data.items():
			descItem = QTableWidgetItem(desc)
			priceItem = QTableWidgetItem('${0:.2f}'.format(price))
			priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

			self.table.insertRow(self.items)
			self.table.setItem(self.items, 0, descItem)
			self.table.setItem(self.items, 1, priceItem)
			self.items += 1

	def add_item(self):
		desc = self.lineEditDescription.text()
		price = self.lineEditPrice.text()
		print(self._data.keys)

		try: 
			descItem = QTableWidgetItem(desc)
			priceItem = QTableWidgetItem('${0:.2f}'.format(float(price)))
			priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

			self.table.insertRow(self.items)
			self.table.setItem(self.items, 0, descItem)
			self.table.setItem(self.items, 1, priceItem)
			self.items += 1

			self.lineEditDescription.setText('')
			self.lineEditPrice.setText('')
		except ValueError:
			pass
	
	def check_disable(self):
		if self.lineEditDescription.text() and self.lineEditPrice.text():
			self.buttonAdd.setEnabled(True)
		else:
			self.buttonAdd.setEnabled(False)

	def clear_table(self):
		self.table.setRowCount(0)
		self.items = 0

		chart = QChart()
		self.chartView.setChart(chart)

	def graph_chart(self):
		series = QPieSeries()

		for i in range(self.table.rowCount()):
			text = self.table.item(i, 0).text()
			val = float(self.table.item(i, 1).text().replace('$', ''))
			series.append(text, val)
		chart = QChart()
		chart.addSeries(series)
		chart.legend().setAlignment(Qt.AlignTop)
		self.chartView.setChart(chart)

	def export_to_csv(self):
		a = self.lineEditName.text()
		try:
			with open(a + '.csv', 'w', newline='') as file:
				writer = csv.writer(file)
				writer.writerow((w.table.horizontalHeaderItem(0).text(), w.table.horizontalHeaderItem(1).text()))
				for rowNumber in range(w.table.rowCount()):
					writer.writerow([w.table.item(rowNumber, 0).text(), w.table.item(rowNumber, 1).text()])			
			file.close()
		except Exception as e:
			print(e)

class MainWindow(QMainWindow):
	def __init__(self, w):
		super().__init__()
		self.setWindowTitle('My Wallet')
		self.setWindowIcon(QIcon(r"expenses.png"))
		self.resize(1200, 700)

		self.setCentralWidget(w)

	def Open_About(self):
		mydialog= QDialog
		mydialog.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	w = DataEntryForm()

	demo = MainWindow(w)
	demo.show()

	sys.exit(app.exec_())
