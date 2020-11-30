import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from function1 import gui1_2
import app
import psycopg2, urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

qtCreatorFile1 = "function1/gui1_1.ui" # Enter file here.
qtCreatorFile2 = "function1/gui1_result.ui"
qtCreatorFile3 = "function1/tweet.ui"
qtCreatorFile4 = "function1/user.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)
Ui_MainWindow4, QtBaseClass4 = uic.loadUiType(qtCreatorFile4)

location = ''
from_date = ''
to_date = ''
top = ''
hashtag = ''
username = ''

class GetPsql:
    # Connect to databse
    conn = psycopg2.connect(user = "postgres",
                            password = "s",
                            host = "localhost",
                            port = "5432",
                            database = "function1")

    def __init__(self):
        self.cur = self.getdb()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def getdb(self):
        return self.conn.cursor()

    # Query from database
    def get_top_hashtag(self, location, from_date, to_date, limit):
        self.cur.execute('''select ht.hashtag, count(ht.hashtag) as hashtag_count
                            from hashtag as ht, tweet as t
                            where ht.location like '{}' and ht.tweet_id = t.id and t.create_at between '{}' and '{}' 
                            group by ht.hashtag
                            order by hashtag_count desc
                            limit {}'''.format(location, from_date, to_date, limit))
        return self.cur.fetchall()

    def get_tweet(self, from_date, to_date, hashtag):
        self.cur.execute('''select tu.username, t.* 
                            from tweet as t, hashtag as ht, tweeter as tu
                            where t.create_at between '{}' and '{}' 
                            and t.id = ht.tweet_id and ht.hashtag = '{}'
                            and tu.id = t.tweeter_id
                            group by tu.username, t.tweeter_id, t.id'''.format(from_date, to_date, hashtag))
        return self.cur.fetchall()

    def get_user(self, username):
        self.cur.execute('''select *
                            from tweeter as tu
                            where tu.username = '{}' '''.format(username))
        return self.cur.fetchall()

    def plotbar(self, data):
        fig, ax = plt.subplots(figsize = (10, 10))
        y_pos = np.arange(len(data['hashtag']))
        ax.barh(y_pos, data['count'], align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data['hashtag'])
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('count')
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class Compare:
    #plot trending tweet following days
    # 0 : date1 < date2, 1 : date1 > date2
    def compare_dates(self, date1, date2):

        date1_list = date1.split('-')
        date2_list = date2.split('-')
        if int(date1_list[0]) < int(date2_list[0]):
            return 0
        elif int(date1_list[0]) > int(date2_list[0]):
            return 1
        elif int(date1_list[1]) < int(date2_list[1]):
            return 0
        elif int(date1_list[1]) > int(date2_list[1]):
            return 1
        elif int(date1_list[2]) < int(date2_list[2]):
            return 0
        elif int(date1_list[2]) > int(date2_list[2]): 
            return 1
        else:
            return 2

class Funct1_1(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.location_details.clicked.connect(self.switch_to_funct1_2)
        self.filter.clicked.connect(self.get_input)

    def come_back(self):
        pos = self.pos()
        self.main = app.Homepage()
        self.main.move(pos)
        self.main.show()
        self.close()

    def switch_to_funct1_2(self):
        pos = self.pos()
        self.main = gui1_2.Funct1_2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def get_input(self):
        global top, location, from_date, to_date
        # Get data arguments from buttons
        location = self.location.currentText() 
        top = self.top.currentText()
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")
        a = Compare()
        b = a.compare_dates(from_date, to_date)
        if (b == 1):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("From date > to_date")
            msg.exec_()
        else:
            # Show result GUI
            pos = self.pos()
            self.main = Funct1Result()
            self.main.move(pos)
            self.main.show()
            self.close()


class Funct1Result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.chart.clicked.connect(self.show_chart)
        self.tweet_result.clicked.connect(self.view_tweet)
        # Show result from database
        global top, location, from_date, to_date
        a = GetPsql()
        b = a.get_top_hashtag(location, from_date, to_date, top)
        for i in range(0, int(top)):
            self.result.setRowCount(int(top))
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(b[i][1])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(b[i][0]))
            self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(0, int(top)):
            self.hashtag.addItem(b[i][0])

    def come_back(self):
        pos = self.pos()
        self.main = Funct1_1()
        self.main.move(pos)
        self.main.show()
        self.close()

    def show_chart(self):   
        a = GetPsql()
        global top, location, from_date, to_date
        b = a.get_top_hashtag(location, from_date, to_date, top)  
        c = []
        d = []
        dict1 = {}
        for i in b:
            c.append(i[0])
            d.append(i[1])
        dict1['hashtag'] = c
        dict1['count'] = d
        a.plotbar(dict1)

    def view_tweet(self):
        global hashtag
        hashtag = self.hashtag.currentText()
        pos = self.pos()
        self.main = Tweet()
        self.main.move(pos)
        self.main.show()
        self.close()

class Tweet(QtWidgets.QMainWindow, Ui_MainWindow3):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.user_detail.clicked.connect(self.view_user)
        # Show result from database
        global from_date, to_date, hashtag
        a = GetPsql()
        b = a.get_tweet(from_date, to_date, hashtag)
        self.tweet_count.setText(str(len(b)))
        self.hashtag.setText(hashtag)
        for i in range(0, len(b)):
            self.result.setRowCount(len(b))
            self.result.resizeRowsToContents()
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(b[i][0]))
            # self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(b[i][4].day) + "-" + str(b[i][4].month) + "-" + str(b[i][4].year)))
            # self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(str(b[i][5])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(b[i][3]))
        header = self.result.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        c = []
        for i in range(0, len(b)):
            c.append(b[i][0])
        df = pd.DataFrame()
        df['username'] = c
        df = df.drop_duplicates()
        username = df['username'].values
        self.username.addItems(username)

    def come_back(self):
        pos = self.pos()
        self.main = Funct1Result()
        self.main.move(pos)
        self.main.show()
        self.close()

    def view_user(self):
        global username
        username = self.username.currentText()
        pos = self.pos()
        self.main = User()
        self.main.move(pos)
        self.main.show()
        self.close()

class User(QtWidgets.QMainWindow, Ui_MainWindow4):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow4.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        global username
        a = GetPsql()
        b = a.get_user(username)
        avatar_url = "https://amazon.clikpic.com/andreacoltman/images/Facebook_male_profile_web.jpg"
        avatar = QtGui.QImage()
        avatar_data = urllib.request.urlopen(avatar_url).read()
        avatar.loadFromData(avatar_data)
        self.avatar.setPixmap(QtGui.QPixmap(avatar))
        self.name.setText(b[0][1])
        self.name.adjustSize()
        self.username.setText(b[0][2])
        self.address.setText(b[0][3])
        self.tweet.setText(str(b[0][4]))
        self.following.setText(str(b[0][5]))
        self.follower.setText(str(b[0][6]))

    def come_back(self):
        pos = self.pos()
        self.main = Tweet()
        self.main.move(pos)
        self.main.show()
        self.close()