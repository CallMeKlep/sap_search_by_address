import pyodbc
import sys
from PySide2.QtWidgets import (QLabel, QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.title = 'SAP Search By Address'
        # Create widgets
        self.street_number = QLineEdit("Enter Street Number")
        self.street_name = QLineEdit("Enter Street Name")
        self.button = QPushButton("Search")
        self.result_table = QTableWidget()
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.street_number)
        layout.addWidget(self.street_name)
        layout.addWidget(self.button)
        layout.addWidget(self.result_table)
        # Set dialog layout
        self.setLayout(layout)
        self.setWindowTitle(self.title)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.address_search)

    def address_search(self):
        # Store input from form as string variables
        street_number_input = str(self.street_number.text())
        street_name_input = str(self.street_name.text())
        
        # Add column labels to result_table
        col_labels = ['BP Number', 'BP Name', 'City', 'State']
        self.result_table.setHorizontalHeaderLabels(col_labels)

        # Connect to SAP and run query w number and name input
        sap_cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=CASTLE2;"
                        "Database=PQSYS_Prod;"
                        "Trusted_Connection=yes;")
        cursor = sap_cnxn.cursor()
        query = "SELECT DISTINCT BpNumber, BpName, City, State FROM dbo.k_ContactSummary WHERE Street LIKE '" + street_number_input + "%' AND Street LIKE '%" + street_name_input + "%';"

        # Set row count to zero
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(4)

        # Add data from to table? 
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        self.result_table.resizeColumnsToContents()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.resize(500, 500)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())