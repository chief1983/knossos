# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Fri Feb 21 04:26:27 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(458, 548)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.build = QtGui.QComboBox(Dialog)
        self.build.setObjectName("build")
        self.verticalLayout.addWidget(self.build)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.resolutionLabel = QtGui.QLabel(Dialog)
        self.resolutionLabel.setObjectName("resolutionLabel")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.resolutionLabel)
        self.vid_res = QtGui.QComboBox(Dialog)
        self.vid_res.setObjectName("vid_res")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.vid_res)
        self.depthLabel = QtGui.QLabel(Dialog)
        self.depthLabel.setObjectName("depthLabel")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.depthLabel)
        self.vid_depth = QtGui.QComboBox(Dialog)
        self.vid_depth.setObjectName("vid_depth")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.vid_depth)
        self.horizontalLayout_2.addLayout(self.formLayout_4)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.textureFilterLabel = QtGui.QLabel(Dialog)
        self.textureFilterLabel.setObjectName("textureFilterLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.textureFilterLabel)
        self.vid_texfilter = QtGui.QComboBox(Dialog)
        self.vid_texfilter.setObjectName("vid_texfilter")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.vid_texfilter)
        self.antialiasingLabel = QtGui.QLabel(Dialog)
        self.antialiasingLabel.setObjectName("antialiasingLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.antialiasingLabel)
        self.vid_aa = QtGui.QComboBox(Dialog)
        self.vid_aa.setObjectName("vid_aa")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.vid_aa)
        self.anisotropicFilterLabel = QtGui.QLabel(Dialog)
        self.anisotropicFilterLabel.setObjectName("anisotropicFilterLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.anisotropicFilterLabel)
        self.vid_af = QtGui.QComboBox(Dialog)
        self.vid_af.setObjectName("vid_af")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.vid_af)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_3 = QtGui.QFrame(Dialog)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_3 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.playbackDeviceLabel = QtGui.QLabel(Dialog)
        self.playbackDeviceLabel.setObjectName("playbackDeviceLabel")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.playbackDeviceLabel)
        self.snd_playback = QtGui.QComboBox(Dialog)
        self.snd_playback.setObjectName("snd_playback")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.snd_playback)
        self.captureDeviceLabel = QtGui.QLabel(Dialog)
        self.captureDeviceLabel.setObjectName("captureDeviceLabel")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.captureDeviceLabel)
        self.snd_capture = QtGui.QComboBox(Dialog)
        self.snd_capture.setObjectName("snd_capture")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.snd_capture)
        self.sampleRateLabel = QtGui.QLabel(Dialog)
        self.sampleRateLabel.setObjectName("sampleRateLabel")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.sampleRateLabel)
        self.snd_samplerate = QtGui.QLineEdit(Dialog)
        self.snd_samplerate.setObjectName("snd_samplerate")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.snd_samplerate)
        self.snd_efx = QtGui.QCheckBox(Dialog)
        self.snd_efx.setObjectName("snd_efx")
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.snd_efx)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.line_4 = QtGui.QFrame(Dialog)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.label_4 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.controller = QtGui.QComboBox(Dialog)
        self.controller.setObjectName("controller")
        self.verticalLayout.addWidget(self.controller)
        self.line_5 = QtGui.QFrame(Dialog)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.label_5 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runButton = QtGui.QPushButton(Dialog)
        self.runButton.setDefault(True)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "FreeSpace build", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Video", None, QtGui.QApplication.UnicodeUTF8))
        self.resolutionLabel.setText(QtGui.QApplication.translate("Dialog", "Resolution :", None, QtGui.QApplication.UnicodeUTF8))
        self.depthLabel.setText(QtGui.QApplication.translate("Dialog", "Color depth :", None, QtGui.QApplication.UnicodeUTF8))
        self.textureFilterLabel.setText(QtGui.QApplication.translate("Dialog", "Texture filter :", None, QtGui.QApplication.UnicodeUTF8))
        self.antialiasingLabel.setText(QtGui.QApplication.translate("Dialog", "Antialiasing :", None, QtGui.QApplication.UnicodeUTF8))
        self.anisotropicFilterLabel.setText(QtGui.QApplication.translate("Dialog", "Anisotropic filtering  :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.playbackDeviceLabel.setText(QtGui.QApplication.translate("Dialog", "Playback device :", None, QtGui.QApplication.UnicodeUTF8))
        self.captureDeviceLabel.setText(QtGui.QApplication.translate("Dialog", "Capture device :", None, QtGui.QApplication.UnicodeUTF8))
        self.sampleRateLabel.setText(QtGui.QApplication.translate("Dialog", "Sample rate :", None, QtGui.QApplication.UnicodeUTF8))
        self.snd_efx.setText(QtGui.QApplication.translate("Dialog", "Enable EFX", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Controller", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Advanced settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Command line flags for Mod name", None, QtGui.QApplication.UnicodeUTF8))
        self.runButton.setText(QtGui.QApplication.translate("Dialog", "Launch", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

