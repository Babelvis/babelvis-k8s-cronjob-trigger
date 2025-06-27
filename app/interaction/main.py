from PyQt6 import QtWidgets, QtGui, QtCore
from generated.main import Ui_MainWindow
from modules.k8s import K8s
import time

class ThreadResultListFunction(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    def __init__(self, listReturnFunction):
        self.listReturnFunction = listReturnFunction
        super().__init__()

    def run(self):
        result = self.listReturnFunction()
        self.signal.emit(result)

class ThreadCheckJob(QtCore.QThread):
    signal = QtCore.pyqtSignal(tuple)
    def __init__(self, k8s: K8s, namespace: str, jobName: str):
        self.k8s = k8s
        self.namespace = namespace
        self.jobName = jobName
        super().__init__()

    def run(self):
        while True:
            status = self.k8s.currentStatusJob(self.namespace, self.jobName)
            self.signal.emit((self.jobName, status))
            if status in ("Complete", "Failed"):
                # We are done!
                break
            time.sleep(5)

class IntUi_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self)
        self.mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainWindow)
        
        self.mainWindow.setFixedSize(self.mainWindow.size())
        self.mainWindow.show()

        self.currentNamespace = None

        self.namespacesModel = QtGui.QStandardItemModel()
        self.listViewNamespaces.setModel(self.namespacesModel)
        self.listViewNamespaces.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listViewNamespaces.doubleClicked[QtCore.QModelIndex].connect(self.getCronJobs)

        self.cronJobsModel = QtGui.QStandardItemModel()
        self.listViewCronJobs.setModel(self.cronJobsModel)
        self.listViewCronJobs.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.jobsModel = QtGui.QStandardItemModel(0,2)
        self.jobsModel.setHorizontalHeaderLabels(['Job', 'Status'])
        self.tableViewJobs.setModel(self.jobsModel)
        self.tableViewJobs.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableViewJobs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.tableViewJobs.setColumnWidth(0, 500)
        self.tableViewJobs.setColumnWidth(1, 160)

        self.pushButtonStartJob.clicked.connect(self.startJob)
        self.StatusJobs = {}
        self.threads = []

        self.k8s = K8s()
        self.getNamespaces()

    def getNamespaces(self):
        getNamespacesThread = ThreadResultListFunction(self.k8s.getNamespaces)
        # connect trigger when thread is done
        getNamespacesThread.signal.connect(self.putNamespacesOnScreen)
        # start Thread
        getNamespacesThread.start()
        # put thread in current active class (keep it alive!)
        self.threads.append(getNamespacesThread)

    def putNamespacesOnScreen(self, namespaces: list):
        for i in namespaces:
            self.namespacesModel.appendRow(QtGui.QStandardItem(i))

    def getCronJobs(self, index):
        self.listViewNamespaces.setDisabled(True)
        self.cronJobsModel.clear()
        self.currentNamespace = self.namespacesModel.item(index.row()).text()
        getCronJobsThread = ThreadResultListFunction(lambda: self.k8s.getCronJobs(self.currentNamespace))
        getCronJobsThread.signal.connect(self.putCronJobsOnScreen)
        getCronJobsThread.start()
        self.threads.append(getCronJobsThread)
        self.listViewNamespaces.setDisabled(False)

    def putCronJobsOnScreen(self, cronJobs: list):
        for i in cronJobs:
            self.cronJobsModel.appendRow(QtGui.QStandardItem(i))

    def updateStatusJob(self, jobStatus: tuple):
        jobName = jobStatus[0]
        status = jobStatus[1]
        if jobName in self.StatusJobs:
            statusItem = self.StatusJobs.get(jobName)
            statusItem.setText(status)
        else:
            self.StatusJobs[jobName] = QtGui.QStandardItem(status)
            self.jobsModel.appendRow([QtGui.QStandardItem(jobName), self.StatusJobs[jobName]])

    def startJob(self):
        currentRow = self.listViewCronJobs.currentIndex().row()
        if currentRow > 0:
            self.pushButtonStartJob.setEnabled(False)
            cronJobName = self.cronJobsModel.item(currentRow).text()
            jobName = self.k8s.createJobFromCronJob(self.currentNamespace, cronJobName)
            statusJob = ThreadCheckJob(self.k8s, self.currentNamespace, jobName)
            statusJob.signal.connect(self.updateStatusJob)
            statusJob.start()
            self.threads.append(statusJob)
            self.pushButtonStartJob.setEnabled(True)
