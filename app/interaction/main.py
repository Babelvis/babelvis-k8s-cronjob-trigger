from PyQt6 import QtWidgets, QtGui, QtCore
from generated.main import Ui_MainWindow
from modules.k8s import K8s

class IntUi_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self)
        self.mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainWindow)
        
        self.mainWindow.setFixedSize(self.mainWindow.size())
        self.mainWindow.show()
        
        self.k8s = K8s()
        self.currentNamespace = None

        self.namespacesModel = QtGui.QStandardItemModel()
        self.listViewNamespaces.setModel(self.namespacesModel)
        self.listViewNamespaces.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listViewNamespaces.doubleClicked[QtCore.QModelIndex].connect(self.getCronJobs)
        
        self.cronJobsModel = QtGui.QStandardItemModel()
        self.listViewCronJobs.setModel(self.cronJobsModel)
        self.listViewCronJobs.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # todo background job
        namespaces = self.k8s.getNamespaces()
        for i in namespaces:
            self.namespacesModel.appendRow(QtGui.QStandardItem(i))
            
        self.pushButtonStartJob.clicked.connect(self.startJob)
        
    def getCronJobs(self, index):
        self.currentNamespace = self.namespacesModel.item(index.row()).text()
        cronJobs = self.k8s.getCronJobs(self.currentNamespace)
        for i in cronJobs:
            self.cronJobsModel.appendRow(QtGui.QStandardItem(i))
            
    def startJob(self):
        b = self.listViewCronJobs.currentIndex()
        cronJobName = self.cronJobsModel.item(b.row()).text()
        self.k8s.createJobFromCronJob(self.currentNamespace, cronJobName)
