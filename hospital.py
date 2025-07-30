import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextEdit,QPushButton,QTableWidget,QTableWidgetItem
from PyQt5 import uic
import pyodbc

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('Hospital.ui', self)
        self.load_patients()

        # Define Widgets
        # labels
        self.manage_label = self.findChild(QLabel, 'manage_label')
        self.label_name = self.findChild(QLabel, 'label_name')
        self.label_code = self.findChild(QLabel, 'label_code')
        self.label_age = self.findChild(QLabel, 'label_age')
        self.label_address = self.findChild(QLabel, 'label_address')
        self.label_dname = self.findChild(QLabel, 'label_dname')
        self.label_blood = self.findChild(QLabel, 'label_blood')
        self.label_phone = self.findChild(QLabel, 'label_phone')
        self.label_date = self.findChild(QLabel, 'label_date')
        self.label_gender = self.findChild(QLabel, 'label_gender')
        self.label_disease = self.findChild(QLabel, 'label_disease')
        # combo_box and push Button
        self.comboBox_gender = self.findChild(QComboBox, 'comboBox_gender')
        self.comboBox_blood = self.findChild(QComboBox, 'comboBox_blood')
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton_edit = self.findChild(QPushButton, 'pushButton_edit')
        self.tableWidget = self.findChild(QTableWidget, 'tableWidget')

        # text Edits
        self.textEdit_disease = self.findChild(QTextEdit, 'textEdit_disease')
        self.textEdit_code = self.findChild(QTextEdit, 'textEdit_code')
        self.textEdit_date = self.findChild(QTextEdit, 'textEdit_date')
        self.textEdit_dname = self.findChild(QTextEdit, 'textEdit_dname')
        self.textEdit_name = self.findChild(QTextEdit, 'textEdit_name')
        self.textEdit_age = self.findChild(QTextEdit, 'textEdit_age')
        self.textEdit_phone = self.findChild(QTextEdit, 'textEdit_phone')
        self.textEdit_address = self.findChild(QTextEdit, 'textEdit_address')
        # Add item to comboBox
        self.comboBox_blood.addItems(["+A", "-A","+B","-B","+AB","-AB","+O","-O"])
        self.comboBox_gender.addItems(["مرد","زن"])

        # connect to pushbutton
        self.pushButton.clicked.connect(self.register_patients)
        self.pushButton_edit.clicked.connect(self.edit_patients)

        self.show()

    def connect_to_db(self):
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=localhost;'
                              'DATABASE=HospitalDB;'
                              'Trusted_Connection=yes;'
                              )
        return conn

    def load_patients(self):
        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dbo.Patients")
            results = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(results[0]))
            self.tableWidget.setHorizontalHeaderLabels([
                "شناسه", "نام بیمار", "سن", "آدرس", "تلفن",
                "جنسیت", "گروه خونی", "تاریخ مراجعه", "بیماری", "نام دکتر"
            ])

            for row_idx, row_data in enumerate(results):
                self.tableWidget.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            cursor.close()
            conn.close()
        except Exception as e:
            print("خطا در بارگذاری اطلاعات:", e)

    def edit_patients(self):
        self.load_patients()
        code = self.textEdit_code.toPlainText()
        self.manage_label.setText("شناسه بیمار را وارد کنید")

        if not code:
            print("لطفا شناسه بیمار را وارد کنید")
            return
        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dbo.Patients WHERE[شناسه] = ?",code)
            result = cursor.fetchone()
            if result[0] == 0:
                print("بیماری با این کد پیدا نشد")
                return
            name = self.textEdit_name.toPlainText()
            code = self.textEdit_code.toPlainText()
            age = self.textEdit_age.toPlainText()
            address = self.textEdit_address.toPlainText()
            dname = self.textEdit_dname.toPlainText()
            date = self.textEdit_date.toPlainText()
            phone = self.textEdit_phone.toPlainText()
            disease = self.textEdit_disease.toPlainText()
            blood = self.comboBox_blood.currentText()
            gender = self.comboBox_gender.currentText()

            try:
                conn = self.connect_to_db()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE dbo.Patients
                    SET 
                        [نام بیمار] = ?,
                        [سن] = ?,
                        [آدرس] = ?,
                        [تلفن] = ?,
                        [جنسیت] = ?,
                        [گروه خونی] = ?,
                        [تاریخ مراجعه] = ?,
                        [بیماری] = ?,
                        [نام دکتر] = ?
                    WHERE [شناسه] = ?
                """, name, age, address, phone, gender, blood, date, disease, dname, code)

                conn.commit()
                cursor.close()
                conn.close()
                print("اطلاعات با موفقیت ذخیره شد")
            except Exception as e:
                print("خطا در ثبت اطلاعات", e)
        finally:
            cursor.close()
            conn.close()
            self.load_patients()
    def register_patients(self):
        self.load_patients()
        name = self.textEdit_name.toPlainText()
        code = self.textEdit_code.toPlainText()
        age = self.textEdit_age.toPlainText()
        address = self.textEdit_address.toPlainText()
        dname = self.textEdit_dname.toPlainText()
        date = self.textEdit_date.toPlainText()
        phone = self.textEdit_phone.toPlainText()
        disease = self.textEdit_disease.toPlainText()
        blood = self.comboBox_blood.currentText()
        gender = self.comboBox_gender.currentText()

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO dbo.Patients
                ([شناسه], [نام بیمار], [سن], [آدرس], [تلفن],
                 [جنسیت], [گروه خونی], [تاریخ مراجعه], [بیماری], [نام دکتر])
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, code, name, age, address, phone, gender, blood, date, disease, dname)

            conn.commit()
            cursor.close()
            conn.close()
            print("اطلاعات با موفقیت ذخیره شد")
        except Exception as e:
            print("خطا در ثبت اطلاعات", e)



os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"F:\aferdos\پایتون\GUI\venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
app = QApplication(sys.argv)
window = UI()
app.exec_()
