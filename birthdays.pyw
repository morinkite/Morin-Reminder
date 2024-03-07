from datetime import datetime
from math import fabs
from operator import itemgetter
from os import listdir
from timeIR import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import time
import sys
import re
import getpass
import os
USER_NAME = getpass.getuser()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        app = QApplication(sys.argv)
        mainWidget = QWidget()

        self.appversion = 1.1
        self.listData = list()
        self.sortType = "name"
        self.Program()

        self.MainFontApp = QFont("B Nazanin",14)
        mainWidget.setWindowTitle("BD Remainder")
        mainWidget.setWindowIcon(QIcon('birthday-cake.png'))
        mainWidget.setFixedSize(480,480)

        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)

        self.labelTime = QLabel()
        self.labelTime.setFont(self.MainFontApp)
        layoutSort = QHBoxLayout()
        labelSort = QLabel("مرتب سازی بر اساس:")
        labelSort.setFont(QFont("B Nazanin",12))
        rbtnSort1 = QRadioButton("نام")
        rbtnSort1.setChecked(True)
        rbtnSort1.setFont(QFont("B Nazanin",12))
        rbtnSort1.clicked.connect(self.SortRadio)
        rbtnSort2 = QRadioButton("روزهای باقیمانده")
        rbtnSort2.setChecked(False)
        rbtnSort2.setFont(QFont("B Nazanin",12))
        rbtnSort2.clicked.connect(self.SortRadio)
        rbtnSort3 = QRadioButton("زمان اضافه شدن")
        rbtnSort3.setChecked(False)
        rbtnSort3.setFont(QFont("B Nazanin",12))
        rbtnSort3.clicked.connect(self.SortRadio)

        layoutSort.addWidget(rbtnSort3)
        layoutSort.addWidget(rbtnSort2)
        layoutSort.addWidget(rbtnSort1)
        layoutSort.addWidget(labelSort)
        layoutSort.setAlignment(Qt.AlignmentFlag.AlignRight)

        bottomLayout = QHBoxLayout()
        mainLayout.addWidget(self.labelTime)
        mainLayout.addLayout(layoutSort)
        mainLayout.addLayout(bottomLayout)

        leftLayout = QHBoxLayout()
        rightLayout = QVBoxLayout()
        rightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        bottomLayout.addLayout(leftLayout)
        bottomLayout.addLayout(rightLayout)
        aboutLayout = QHBoxLayout()

        about = QLabel("ساخته شده توسط امید")
        about.setFont(QFont("Dirooz"))
        about.setStyleSheet("color: rgba(0, 0, 0, 0.65);")
        version = QLabel(f"ورژن {self.appversion} - Alpha")
        version.setFont(QFont("Dirooz"))
        version.setStyleSheet("color: rgba(0, 0, 0, 0.65);")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        email = QLabel("Powered by Python")
        email.setFont(QFont("Comic Sans MS"))
        email.setStyleSheet("color: rgba(0, 0, 0, 0.65);")

        mainLayout.addLayout(aboutLayout)
        aboutLayout.addWidget(email)
        aboutLayout.addWidget(version)
        aboutLayout.addWidget(about)
        self.MainTable = QTableWidget()
        self.MainTable.setFixedSize(335,360)
        self.MainTable.setColumnCount(3)
        self.MainTable.setRowCount(self.listData.__len__())
        self.MainTable.setHorizontalHeaderLabels(["Name","Date born","Days left"])
        self.MainTable.setColumnWidth(0,150)
        self.MainTable.setColumnWidth(1,80)
        self.MainTable.setColumnWidth(2,60)

        self.ButtonAddMenu = QPushButton("شخص جدید")
        self.ButtonAddMenu.setFont(self.MainFontApp)
        self.ButtonAddMenu.clicked.connect(self.AddNewOne)

        self.ButtonRemoveMenu = QPushButton("حذف شخص")
        self.ButtonRemoveMenu.setFont(self.MainFontApp)
        self.ButtonRemoveMenu.clicked.connect(self.RemovePerson)

        self.ButtonEditMenu = QPushButton("ویرایش شخص")
        self.ButtonEditMenu.setFont(self.MainFontApp)
        self.ButtonEditMenu.clicked.connect(self.EditPerson)

        self.ButtonClearMenu = QPushButton("پاک کردن \nکامل لیست")
        self.ButtonClearMenu.setFont(self.MainFontApp)
        self.ButtonClearMenu.clicked.connect(self.RemoveAllPersons)

        self.ButtonListImport = QPushButton("وارد کردن لیست")
        self.ButtonListImport.setFont(self.MainFontApp)
        self.ButtonListImport.clicked.connect(self.ImportListField)

        # self.ButtonSetting = QPushButton("تنظیمات")
        # self.ButtonSetting.setFont(self.MainFontApp)
        # self.ButtonSetting.clicked.connect(self.add_to_startup)
        
        ButttonAbout = QPushButton("درباره من")
        ButttonAbout.setFont(self.MainFontApp)
        ButttonAbout.clicked.connect(self.AboutMenu)

        self.ReimportList()
        self.MainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        leftLayout.addWidget(self.MainTable)
        rightLayout.addWidget(self.ButtonAddMenu)
        rightLayout.addWidget(self.ButtonEditMenu)
        rightLayout.addWidget(self.ButtonRemoveMenu)
        rightLayout.addWidget(self.ButtonClearMenu)
        rightLayout.addWidget(self.ButtonListImport)
        # rightLayout.addWidget(self.ButtonSetting)
        rightLayout.addWidget(ButttonAbout)

        mainWidget.show()
        app.exec()

    def SortRadio(self):
        radioSender = self.sender()
        if radioSender.isChecked():
            text = radioSender.text()
            match text:
                case "نام":
                    self.sortType = "name"
                case "زمان اضافه شدن":
                    self.sortType = "default"
                case "روزهای باقیمانده":
                    self.sortType = "remainday"

        self.ReimportList()

    def SplitTime(self,time,index):
        SpilitedTime = time.split("/")
        TimeDay = SpilitedTime[0]
        TimeMonth = SpilitedTime[1]
        TimeYear = SpilitedTime[2]
        match index:
            case 0: #Get day
                return int(TimeDay)
            case 1: #Get month
                return int(TimeMonth)
            case 2: #Get year
                return int(TimeYear)

    def Months(self,index):
        match index:
            case 1:
                return 31
            case 2:
                return 31
            case 3:
                return 31
            case 4:
                return 31
            case 5:
                return 31
            case 6:
                return 31
            case 7:
                return 30
            case 8:
                return 30
            case 9:
                return 30
            case 10:
                return 30
            case 11:
                return 30

    def DayOfYearCalculator(self,day,month):
        dayOfYear = 0
        for m in range(1,month):
            dayOfYear += self.Months(m)
        dayOfYear += day
        return dayOfYear

    def ReimportList(self):
        i = 0
        self.MainTable.setRowCount(self.listData.__len__())
        if not self.sortType == "default":
            newlist = sorted(self.listData,key=itemgetter(self.sortType))
        else:
            newlist = self.listData
        for data in newlist:
            self.MainTable.setItem(i,0,QTableWidgetItem(data["name"]))
            self.MainTable.setItem(i,1,QTableWidgetItem(data["date"]))
            self.MainTable.item(i,1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.MainTable.setItem(i,2,QTableWidgetItem(str(data["remainday"])))
            i+=1
        
        self.Res = self.CloseBirth()
        if not type(self.Res) == int:
            if self.Res["remainday"] == 0:
                self.labelTime.setText(f'تاریخ امروز : {ShowTodayFull()}             نزدیک ترین تولد : امروز!')
            else:
                self.labelTime.setText(f'تاریخ امروز : {ShowTodayFull()}             نزدیک ترین تولد : {self.Res["remainday"]} روز دیگه')
        else:
            self.labelTime.setText(f'تاریخ امروز : {ShowTodayFull()}')

    def CheckList(self):
        if len(self.listData) == 0:
            return 0
        else:
            return 1

    def CloseBirth(self):
        self.CloseBirthDayCalculator()
        if self.CheckList() == 1:
            for l in self.listData:
                if l["remainday"] == self.closestBirth:
                    return l
        else:
            print("List empty")
            return 0

    def AddNewOne(self):
        self.ButtonAddMenu.setEnabled(False)
        self.newWidget = QWidget()
        self.newWidget.setWindowTitle("شخص جدید")
        self.newWidget.setWindowIcon(QIcon('birthday-cake.png'))
        self.newWidget.setWindowFlags(Qt.WindowCloseButtonHint)
        self.newWidget.setWindowFlag(Qt.WindowCloseButtonHint,False)
        self.newWidget.setFixedSize(300,200)
        self.newWidget.show()

        vlayout = QVBoxLayout()
        self.newWidget.setLayout(vlayout)
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        nameLay = QHBoxLayout()

        NameLabel = QLabel("نام شخص:")
        NameLabel.setFont(self.MainFontApp)
        NameLabel2 = QLabel("فقط انگیسی")
        NameLabel2.setFont(self.MainFontApp)
        NameLabel2.setStyleSheet("color: rgba(0, 0, 0, 0.5);")
        self.NewPersonNameInput = QLineEdit()
        self.NewPersonNameInput.setFont(self.MainFontApp)
        DateLabel = QLabel("تاریخ تولد فرد :");
        DateLabel.setFont(self.MainFontApp)
        self.NewPersonDayInput = QLineEdit()
        self.NewPersonDayInput.setMaxLength(2)
        self.NewPersonDayInput.setFont(self.MainFontApp)
        self.NewPersonMonthInput = QLineEdit()
        self.NewPersonMonthInput.setMaxLength(2)
        self.NewPersonMonthInput.setFont(self.MainFontApp)
        self.NewPersonYearInput = QLineEdit()
        self.NewPersonYearInput.setMaxLength(4)
        self.NewPersonYearInput.setFont(self.MainFontApp)
        DayLabel = QLabel("روز :")
        DayLabel.setFont(self.MainFontApp)
        MonthLabel = QLabel("ماه :")
        MonthLabel.setFont(self.MainFontApp)
        YearLabel = QLabel("سال :")
        YearLabel.setFont(self.MainFontApp)
        ButtonAdd = QPushButton("اضافه کردن")
        ButtonAdd.setFont(self.MainFontApp)
        ButtonAdd.clicked.connect(self.CompleteAddWindow)
        ButtonCancel = QPushButton("بازگشت")
        ButtonCancel.setFont(self.MainFontApp)
        ButtonCancel.clicked.connect(self.CloseAddWindow)

        nameLay.addWidget(NameLabel2)
        nameLay.addWidget(NameLabel)
        nameLay.setContentsMargins(140,0,0,0)
        vlayout.addLayout(nameLay)
        vlayout.addWidget(self.NewPersonNameInput)
        vlayout.addWidget(DateLabel)
        vlayout.addLayout(hlayout)
        hlayout.addWidget(self.NewPersonYearInput)
        hlayout.addWidget(YearLabel)
        hlayout.addWidget(self.NewPersonMonthInput)
        hlayout.addWidget(MonthLabel)
        hlayout.addWidget(self.NewPersonDayInput)
        hlayout.addWidget(DayLabel)
        vlayout.addLayout(hlayout2)
        hlayout2.addWidget(ButtonAdd)
        hlayout2.addWidget(ButtonCancel)

    def CloseAddWindow(self):
        self.ButtonAddMenu.setEnabled(True)
        self.newWidget.close()
    
    def CloseEditWindwos(self):
        self.ButtonEditMenu.setEnabled(True)
        self.newWidget2.close()

    def CompleteAddWindow(self):
        day = self.NewPersonDayInput.text()
        month = self.NewPersonMonthInput.text()
        year = self.NewPersonYearInput.text()
        name = self.NewPersonNameInput.text()

        encodedName = self.NewPersonNameInput.text().encode('utf-8').decode('ascii', 'ignore')
        if not len(name) == len(encodedName):
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setWindowTitle("مشکل!")
            msg.setText("نام را انگلیسی وارد کنید")
            returnedValue = msg.exec()
            return

        if name == "" or day =="" or month == "" or year == "":
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setWindowTitle("مشکل!")
            if year == "":
                msg.setText("سال را وارد کنید")
            if month == "":
                msg.setText("ماه را وارد کنید")
            if day == "":
                msg.setText("روز را وارد کنید")
            if name == "":
                msg.setText("نام را وارد کنید")
            returnedValue = msg.exec()
            return
        try:
            int(day)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("روز وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(day) < 1 or int(day) > 32:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("روز وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        try:
            int(month)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("ماه وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(month) < 1 or int(month) > 12:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("ماه وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        try:
            int(year)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("سال وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(year) < 1 or int(year) > int(ShowDateYear()):
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("سال وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        name = name.strip()
        f = open("birthdaysData.txt","a")
        f.write(f"\n{name}:{day}/{month}/{year}")
        f.close()

        self.Program()
        self.ReimportList()
        
    def RemovePerson(self):
        if self.MainTable.rowCount() == 0 or self.MainTable.currentRow() == -1:
            return

        row = self.MainTable.currentRow()
        nameUser = QTableWidgetItem.text(self.MainTable.item(row,0))
        dateUser = QTableWidgetItem.text(self.MainTable.item(row,1))

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"مطمئنید از حذف {nameUser}؟")
        msg.setWindowTitle("!هشدار")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:

            r = open("birthdaysData.txt","r")
            lines = r.readlines()
            r.close()

            w = open("birthdaysData.txt","w")

            for l in lines:
                if l == "\n":
                    continue

                d = l.replace('\n','')

                personData = d.split(":")
                personName = personData[0]
                personTime = personData[1]

                if not d == f"{nameUser}:{dateUser}":
                    w.write(l)
            w.close()
            for p in self.listData:
                if p["name"] == nameUser:
                    self.listData.remove(p)
            self.ReimportList()
        
    def EditPerson(self):
        if self.MainTable.rowCount() == 0 or self.MainTable.currentRow() == -1:
            return

        row = self.MainTable.currentRow()
        self.nameUser2 = QTableWidgetItem.text(self.MainTable.item(row,0))
        self.dateUser2 = QTableWidgetItem.text(self.MainTable.item(row,1))
        splitDate = self.dateUser2.split("/")
        day = splitDate[0]
        month = splitDate[1]
        year = splitDate[2]

        self.ButtonEditMenu.setEnabled(False)
        self.newWidget2 = QWidget()
        self.newWidget2.setWindowTitle(f"ویرایش {self.nameUser2}")
        self.newWidget2.setWindowIcon(QIcon('birthday-cake.png'))
        self.newWidget2.setWindowFlags(Qt.WindowCloseButtonHint)
        self.newWidget2.setWindowFlag(Qt.WindowCloseButtonHint,False)
        self.newWidget2.setFixedSize(300,200)
        self.newWidget2.show()

        vlayout = QVBoxLayout()
        self.newWidget2.setLayout(vlayout)
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()

        NameLabel = QLabel("نام شخص :")
        NameLabel.setFont(self.MainFontApp)
        self.NewPersonNameInput2 = QLineEdit()
        self.NewPersonNameInput2.setFont(self.MainFontApp)
        self.NewPersonNameInput2.setText(self.nameUser2)
        DateLabel = QLabel("تاریخ تولد فرد :");
        DateLabel.setFont(self.MainFontApp)
        self.NewPersonDayInput2 = QLineEdit()
        self.NewPersonDayInput2.setMaxLength(2)
        self.NewPersonDayInput2.setFont(self.MainFontApp)
        self.NewPersonDayInput2.setText(day)
        self.NewPersonMonthInput2 = QLineEdit()
        self.NewPersonMonthInput2.setMaxLength(2)
        self.NewPersonMonthInput2.setFont(self.MainFontApp)
        self.NewPersonMonthInput2.setText(month)
        self.NewPersonYearInput2 = QLineEdit()
        self.NewPersonYearInput2.setMaxLength(4)
        self.NewPersonYearInput2.setFont(self.MainFontApp)
        self.NewPersonYearInput2.setText(year)
        DayLabel = QLabel("روز :")
        DayLabel.setFont(self.MainFontApp)
        MonthLabel = QLabel("ماه :")
        MonthLabel.setFont(self.MainFontApp)
        YearLabel = QLabel("سال :")
        YearLabel.setFont(self.MainFontApp)
        ButtonAdd = QPushButton("ویرایش کردن")
        ButtonAdd.setFont(self.MainFontApp)
        ButtonAdd.clicked.connect(self.CompleteEditWindow)
        ButtonCancel = QPushButton("بازگشت")
        ButtonCancel.setFont(self.MainFontApp)
        ButtonCancel.clicked.connect(self.CloseEditWindwos)

        vlayout.addWidget(NameLabel)
        vlayout.addWidget(self.NewPersonNameInput2)
        vlayout.addWidget(DateLabel)
        vlayout.addLayout(hlayout)
        hlayout.addWidget(self.NewPersonYearInput2)
        hlayout.addWidget(YearLabel)
        hlayout.addWidget(self.NewPersonMonthInput2)
        hlayout.addWidget(MonthLabel)
        hlayout.addWidget(self.NewPersonDayInput2)
        hlayout.addWidget(DayLabel)
        vlayout.addLayout(hlayout2)
        hlayout2.addWidget(ButtonAdd)
        hlayout2.addWidget(ButtonCancel)

    def CompleteEditWindow(self):
        day = self.NewPersonDayInput2.text()
        month = self.NewPersonMonthInput2.text()
        year = self.NewPersonYearInput2.text()
        name = self.NewPersonNameInput2.text()

        encodedName = self.NewPersonNameInput2.text().encode('utf-8').decode('ascii', 'ignore')
        if not len(name) == len(encodedName):
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setWindowTitle("مشکل!")
            msg.setText("نام را انگلیسی وارد کنید")
            returnedValue = msg.exec()
            return

        if name == "" or day =="" or month == "" or year == "":
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setWindowTitle("مشکل!")
            if year == "":
                msg.setText("سال را وارد کنید")
            if month == "":
                msg.setText("ماه را وارد کنید")
            if day == "":
                msg.setText("روز را وارد کنید")
            if name == "":
                msg.setText("نام را وارد کنید")
            returnedValue = msg.exec()
            return
        try:
            int(day)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("روز وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(day) < 1 or int(day) > 32:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("روز وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        try:
            int(month)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("ماه وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(month) < 1 or int(month) > 12:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("ماه وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        try:
            int(year)
        except:
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("سال وارد شده باید عدد باشد")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return
        if int(year) < 1 or int(year) > int(ShowDateYear()):
            msg = QMessageBox()
            msg.setIcon(3)
            msg.setText("سال وارد شده نامجاز است")
            msg.setWindowTitle("مشکل!")
            returnedValue = msg.exec()
            return

        name = name.strip()

        for p in self.listData:
            if p["name"] == self.nameUser2 and p["date"] == self.dateUser2:
                p["name"] = name
                p["date"] = f"{day}/{month}/{year}"
                p["remainday"] = self.RemainCalculatorSimple(day,month)

        w = open("birthdaysData.txt","w")
        for l in self.listData:
            w.write(f'\n{l["name"]}:{l["date"]}')
        w.close()

        self.ReimportList()
        self.CloseEditWindwos()

    def RemoveAllPersons(self):
        if self.MainTable.rowCount() == 0:
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"مطمئنید از حذف تمام لیست؟")
        msg.setWindowTitle("!هشدار")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            w = open("birthdaysData.txt","w").close()
            self.listData.clear()
            self.ReimportList()
        
    def ImportListField(self):
        self.ButtonListImport.setEnabled(False)
        self.newWidget3 = QWidget()
        self.newWidget3.setWindowTitle(f"لیست")
        self.newWidget3.setWindowIcon(QIcon('birthday-cake.png'))
        self.newWidget3.setWindowFlags(Qt.WindowCloseButtonHint)
        self.newWidget3.setWindowFlag(Qt.WindowCloseButtonHint,True)
        self.newWidget3.setFixedSize(300,200)
        self.newWidget3.show()

        vlayout = QVBoxLayout()
        self.newWidget3.setLayout(vlayout)
        vhlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        note = QLabel("فرمت باید به صورت name:day/month/year باشد")
        note.setFont(QFont("Dirooz",10))
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("color: rgba(0,0,0,0.8);")
        self.inputList = QTextEdit()

        ButtonAdd = QPushButton("تایید")
        ButtonAdd.setFont(self.MainFontApp)
        ButtonAdd.clicked.connect(self.CompleteImportWindow)
        ButtonCancel = QPushButton("بازگشت")
        ButtonCancel.setFont(self.MainFontApp)
        ButtonCancel.clicked.connect(self.CloseImportWindwos)

        vlayout.addLayout(vhlayout)
        vlayout.addLayout(hlayout)
        vhlayout.addWidget(note)
        vhlayout.addWidget(self.inputList)
        hlayout.addWidget(ButtonAdd)
        hlayout.addWidget(ButtonCancel)

    def CompleteImportWindow(self):
        text = self.inputList.toPlainText()

        for line in text.splitlines():
            if re.match('[A-Za-z][A-Za-z ]*:[1-2]*[0-9]/[1-6]/1[2-4][0-9][0-9]',line) or re.match('[A-Za-z][A-Za-z ]*:3[0-1]/[1-6]/1[2-4][0-9][0-9]',line) or re.match('[A-Za-z][A-Za-z ]*:[1-2]*[0-9]/[7-9]/1[2-4][0-9][0-9]',line) or re.match('[A-Za-z][A-Za-z ]*:30/[7-9]/1[2-4][0-9][0-9]',line) or re.match('[A-Za-z][A-Za-z ]*:30/1[0-2]/1[2-4][0-9][0-9]',line) or re.match('[A-Za-z][A-Za-z ]*:[0-2]*[0-9]/1[0-2]/1[2-4][0-9][0-9]',line) is not None:
                x = open("birthdaysData.txt","a")
                x.write("\n" + line)
                x.close()
                
        self.Program()
        self.ReimportList()
        self.CloseImportWindwos()

    def CloseImportWindwos(self):
        self.newWidget3.close()
        self.ButtonListImport.setEnabled(True)

    def RemainCalculator(self,d):
        tMonth = int(ShowDateMonth())
        tDay = int(ShowDateDay())
        dayOfYear = self.DayOfYearCalculator(tDay,tMonth)

        personData = d.split(":")
        personName = personData[0]
        personTime = personData[1]

        personMonth = self.SplitTime(personTime,1)
        personDay = self.SplitTime(personTime,0)
        dayOfYearPerosn = self.DayOfYearCalculator(personDay,personMonth)
        personReaming = dayOfYearPerosn - dayOfYear

        if personReaming < 0:
            personReaming += 365

        return personName,personTime,dayOfYearPerosn,personReaming

    def RemainCalculatorSimple(self,day,month):
        tMonth = int(ShowDateMonth())
        tDay = int(ShowDateDay())
        dayOfYear = self.DayOfYearCalculator(tDay,tMonth)

        personDay = int(day)
        personMonth = int(month)
        dayOfYearPerosn = self.DayOfYearCalculator(personDay,personMonth)
        personReaming = dayOfYearPerosn - dayOfYear

        if personReaming < 0:
            personReaming += 365\

        return personReaming

    def CloseBirthDayCalculator(self):
        if len(self.listData) == 0:
            self.closestBirth = 0
            return

        self.closestBirth = 365
        for p in self.listData:
            if p["remainday"] < self.closestBirth:
                self.closestBirth =p["remainday"]

    def Program(self):
        try:
            open("birthdaysData.txt","r")
        except:
            x = open("birthdaysData.txt","x")
        else:
            f = open("birthdaysData.txt","r")
            self.listData.clear()

            for d in f.readlines():
                if not self.string_is_not_blank(d):
                    continue

                d = d.replace('\n','')



                personRes = self.RemainCalculator(d)
                personName = personRes[0]
                personTime = personRes[1]
                dayOfYearPerosn = personRes[2]
                personReaming = personRes[3]

                dataDic = dict(name=personName,date=personTime,dayofyear=dayOfYearPerosn,remainday=personReaming)

                self.listData.insert(0,dataDic)

            f.close()

    def string_is_not_blank(self,s):
        return bool(s and not s.isspace())

    # def add_to_startup(file_path=""):
    #     if file_path == "":
    #         file_path = os.path.dirname(os.path.realpath(__file__))
    #     path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    #     # with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
    #     #     bat_file.write(r'start "" "%s"' % file_path)
    def AboutMenu(self):

        def Back():
            self.AboutWidget.close()

        self.AboutWidget = QWidget()
        self.AboutWidget.setWindowTitle("درباره من")
        self.AboutWidget.setWindowIcon(QIcon('birthday-cake.png'))
        self.AboutWidget.resize(510,200)
        self.AboutWidget.setWindowFlags(Qt.WindowCloseButtonHint)
        self.AboutWidget.setWindowFlag(Qt.WindowCloseButtonHint,True)
        self.AboutWidget.show()

        Layout = QVBoxLayout()
        self.AboutWidget.setLayout(Layout)
        HLayout = QHBoxLayout()

        Text = QLabel(" سلام :) \n اسم من امیدِ و من زیاد تجربه ای تو برنامه نویسی ندارم و اولین اپلیکیشنی هست که منتشرش میکنم. \nاین برنامه رو بخاطره کار خودم ساختم و دوست داشتم همه هم بتونن مثل من از این برنامه بهره ببرن.\n پس به صورت کاملا رایگان آپلودش کردم تا هر کسی که نیاز داشته باشه بتونه بهره ببره. \nراه های ارتباطی زیر هم هست که بتونید با من حرف بزنید و مشکلات رو انتقال بدید تا نسخه های بعدی\nرفعش کنم یا حتی بهم پیشنهاداتون رو بگید که چه چیزایی میتونه برنامه رو بهتر کنه.")
        Text.setFont(QFont("B Nazanin",11))
        TelID = QLabel("Telegram: Morinkite_O")
        TelID.setFont(QFont("Comic Sans MS"))
        Gmail = QLabel("Gmail : omid.vf1383@gmail.com")
        Gmail.setFont(QFont("Comic Sans MS"))

        ButtonBack = QPushButton("بازگشت")
        ButtonBack.setFont(self.MainFontApp)
        ButtonBack.resize(100,100)
        ButtonBack.clicked.connect(Back)

        Layout.addWidget(Text)
        Layout.addLayout(HLayout)
        HLayout.addWidget(TelID)
        HLayout.addWidget(Gmail)
        Layout.addWidget(ButtonBack)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# father new dates
