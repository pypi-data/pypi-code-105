from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class UiMainClientWindow(object):
    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(813, 637)
        main_window.setStyleSheet(u"background-color: rgb(228, 231, 255);")
        self.action = QAction(main_window)
        self.action.setObjectName(u"action")
        self.menu_exit = QAction(main_window)
        self.menu_exit.setObjectName(u"action_2")
        self.menu_add_contact = QAction(main_window)
        self.menu_add_contact.setObjectName(u"action_3")
        self.menu_del_contact = QAction(main_window)
        self.menu_del_contact.setObjectName(u"action_4")
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.list_contacts = QListView(self.centralwidget)
        self.list_contacts.setObjectName(u"listView")
        self.list_contacts.setGeometry(QRect(640, 20, 131, 471))
        self.list_contacts.setStyleSheet(u"background-color: rgb(228, 231,"
                                         u" 255);")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(640, 0, 121, 16))
        self.btn_add_contact = QPushButton(self.centralwidget)
        self.btn_add_contact.setObjectName(u"pushButton")
        self.btn_add_contact.setGeometry(QRect(640, 500, 131, 26))
        self.btn_remove_contact = QPushButton(self.centralwidget)
        self.btn_remove_contact.setObjectName(u"pushButton_2")
        self.btn_remove_contact.setGeometry(QRect(640, 540, 131, 26))
        self.list_messages = QListView(self.centralwidget)
        self.list_messages.setObjectName(u"listView_2")
        self.list_messages.setGeometry(QRect(30, 20, 581, 211))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 0, 211, 20))
        self.label_new_message = QLabel(self.centralwidget)
        self.label_new_message.setObjectName(u"label_3")
        self.label_new_message.setGeometry(QRect(30, 240, 600, 16))
        self.text_message = QPlainTextEdit(self.centralwidget)
        self.text_message.setObjectName(u"text_message")
        self.text_message.setGeometry(QRect(30, 260, 581, 231))
        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setObjectName(u"pushButton_3")
        self.btn_clear.setGeometry(QRect(30, 540, 121, 26))
        self.btn_send = QPushButton(self.centralwidget)
        self.btn_send.setObjectName(u"pushButton_4")
        self.btn_send.setGeometry(QRect(450, 540, 161, 26))
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 813, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(main_window)
        self.toolBar.setObjectName(u"toolBar")
        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.menu_add_contact)
        self.menu_2.addAction(self.menu_del_contact)

        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

    # setupUi

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow",
                                                             u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow",
                                                       u"\u0412\u044b\u0445\u043e\u0434", None))
        self.menu_exit.setText(QCoreApplication.translate("MainWindow",
                                                          u"\u0412\u044b\u0445\u043e\u0434", None))
        self.menu_add_contact.setText(QCoreApplication.translate("MainWindow",
                                                                 u"\u0414\u043e\u0431\u0430\u0432\u0438"
                                                                 u"\u0442\u044c",
                                                                 None))
        self.menu_del_contact.setText(QCoreApplication.translate("MainWindow",
                                                                 u"\u0423\u0434\u0430\u043b\u0438\0442\u044c", None))
        self.label.setText(QCoreApplication.translate("MainWindow",
                                                      u"\u0421\u043f\u0438\u0441\u043e\u043a "
                                                      u"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043e\u0432:",
                                                      None))
        self.btn_add_contact.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438"
                                                                              u"\u0442\u044c "
                                                                              u"\u043a\u043e\u043d\u0442\u0430\u043a"
                                                                              u"\u0442", None))
        self.btn_remove_contact.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438"
                                                                                 u"\u0442\u044c "
                                                                                 u"\u043a\u043e\u043d\u0442\u0430"
                                                                                 u"\u043a\u0442", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0440\u0438\u044f "
                                                                      u"\u0441\u043e\u043e\u0431\u0449\u0435\u043d"
                                                                      u"\u0438\u0439:", None))
        self.label_new_message.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438"
                                                                                u"\u0442\u0435 "
                                                                                u"\u0441\u043e\u043e\u0431\u0449"
                                                                                u"\u0435\u043d\u0438\u0435:", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442"
                                                                        u"\u044c \u043f\u043e\u043b\u0435", None))
        self.btn_send.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438"
                                                                       u"\u0442\u044c "
                                                                       u"\u0441\u043e\u043e\u0431\u0449\u0435\u043d"
                                                                       u"\u0438\u0435", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043d\u0442\u0430\u043a\u0442"
                                                                      u"\u044b", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
