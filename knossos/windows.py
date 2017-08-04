## Copyright 2017 Knossos authors, see NOTICE file
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from __future__ import absolute_import, print_function

import os
import sys
import logging
import functools
import json

from . import uhf
uhf(__name__)

from . import center, util, integration, web, repo
from .qt import QtCore, QtWidgets, load_styles
from .ui.hell import Ui_MainWindow as Ui_Hell
from .ui.gogextract import Ui_GogExtractDialog
from .ui.install import Ui_InstallDialog
from .ui.log_viewer import Ui_LogDialog
from .tasks import run_task, GOGExtractTask, InstallTask, WindowsUpdateTask

# Keep references to all open windows to prevent the GC from deleting them.
_open_wins = []
translate = QtCore.QCoreApplication.translate


class QDialog(QtWidgets.QDialog):

    def __init__(self, *args):
        super(QDialog, self).__init__(*args)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class QMainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super(QMainWindow, self).__init__(*args)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def closeEvent(self, e):
        e.accept()

        center.app.quit()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange and integration.current is not None:
            integration.current.annoy_user(False)

        return super(QMainWindow, self).changeEvent(event)


class Window(object):
    win = None
    closed = True
    _is_window = True
    _tpl_cache = None
    _styles = ''
    _qchildren = None

    def __init__(self, window=True):
        super(Window, self).__init__()

        self._is_window = window
        self._tpl_cache = {}
        self._qchildren = []

    def _create_win(self, ui_class, qt_widget=QDialog):
        if not self._is_window:
            qt_widget = QtWidgets.QWidget

        self.win = util.init_ui(ui_class(), qt_widget())

    def open(self):
        global _open_wins

        if not self.closed:
            return

        self.closed = False
        _open_wins.append(self)
        self.win.destroyed.connect(self._del)
        self.win.show()

    def close(self):
        self.win.close()

    def _del(self):
        global _open_wins

        if self.closed:
            return

        self.closed = True

        if self in _open_wins:
            _open_wins.remove(self)

    def label_tpl(self, label, **vars):
        name = label.objectName()
        if name in self._tpl_cache:
            text = self._tpl_cache[name]
        else:
            text = self._tpl_cache[name] = label.text()

        for name, value in vars.items():
            text = text.replace('{' + name + '}', value)

        label.setText(text)

    def load_styles(self, path, append=True):
        data = load_styles(path)

        if append:
            self._styles += data
        else:
            self._styles = data

        self.win.setStyleSheet(self._styles)

    def tr(self, *args):
        return translate(self.__class__.__name__, *args)


class HellWindow(Window):
    _tasks = None
    _mod_filter = 'home'
    _search_text = ''
    _updating_mods = None
    browser_ctrl = None
    progress_win = None

    def __init__(self, window=True):
        super(HellWindow, self).__init__(window)
        self._tasks = {}
        self._updating_mods = {}

        self._create_win(Ui_Hell, QMainWindow)
        self.browser_ctrl = web.BrowserCtrl(self.win.webView)
        self.win.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.win.webView.loadStarted.connect(self.show_indicator)
        self.win.webView.loadFinished.connect(self.check_loaded)

        center.signals.update_avail.connect(self.ask_update)
        center.signals.task_launched.connect(self.watch_task)
        center.signals.repo_updated.connect(self.update_mod_list)

        self.win.setWindowTitle(self.win.windowTitle() + ' ' + center.VERSION)
        self.win.progressInfo.hide()
        self.open()

    def _del(self):
        center.signals.update_avail.disconnect(self.ask_update)
        center.signals.task_launched.disconnect(self.watch_task)

        # Trying to free this object usually leads to memory corruption
        # See http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
        # Since this is the main window and should only be closed whenever the application exits, skipping this
        # won't lead to memory leaks.
        # super(HellWindow, self)._del()

    def finish_init(self):
        # The delay is neccessary to make sure that QtWebkit doesn't swallow the resulting event.
        QtCore.QTimer.singleShot(300, self.check_fso)

    def check_fso(self):
        if 'KN_WELCOME' not in os.environ and center.settings['base_path'] is not None:
            self.update_mod_buttons('home')
        else:
            self.browser_ctrl.bridge.showWelcome.emit()

    def ask_update(self, version):
        # We only have an updater for windows.
        if sys.platform.startswith('win'):
            msg = self.tr('There\'s an update available!\nDo you want to install Knossos %s now?') % str(version)
            buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            result = QtWidgets.QMessageBox.question(center.app.activeWindow(), 'Knossos', msg, buttons)
            if result == QtWidgets.QMessageBox.Yes:
                run_task(WindowsUpdateTask())
        else:
            msg = self.tr('There\'s an update available!\nYou should update to Knossos %s.') % str(version)
            QtWidgets.QMessageBox.information(center.app.activeWindow(), 'Knossos', msg)

    def search_mods(self):
        mods = None

        if self._mod_filter in ('home', 'develop'):
            mods = center.installed.mods
        elif self._mod_filter == 'explore':
            mods = {}
            for mid, mvs in center.mods.mods.items():
                if mid not in center.installed.mods:
                    mods[mid] = mvs
        # elif self._mod_filter == 'updates':
        #     mods = {}
        #     for mid in center.installed.get_updates():
        #         mods[mid] = center.installed.mods[mid]
        else:
            mods = {}

        # Now filter the mods.
        query = self._search_text
        result = []
        for mid, mvs in mods.items():
            if query in mvs[0].title.lower():
                for mod in mvs:
                    item = mod.get()
                    item['progress'] = 0
                    item['progress_info'] = {}

                    try:
                        rmod = center.mods.query(mod)
                    except repo.ModNotFound:
                        rmod = None

                    if rmod and rmod.version > mod.version:
                        item['status'] = 'update'
                    elif mod.mid in self._updating_mods:
                        item['status'] = 'updating'
                        item['progress'] = self._updating_mods[mod.mid]
                    else:
                        item['status'] = 'ready'

                        if self._mod_filter == 'home':
                            for pkg in mod.packages:
                                if pkg.files_checked > 0 and pkg.files_ok < pkg.files_checked:
                                    item['status'] = 'error'
                                    break

                    result.append(item)

        result.sort(key=lambda m: m['title'])
        return result, self._mod_filter

    def update_mod_list(self):
        result, filter_ = self.search_mods()

        if filter_ in ('home', 'explore', 'develop'):
            self.browser_ctrl.bridge.updateModlist.emit(json.dumps(result), filter_)

    def show_settings(self):
        pass

    def show_indicator(self):
        self.win.setCursor(QtCore.Qt.BusyCursor)

    def check_loaded(self, success):
        self.win.unsetCursor()

    def update_mod_buttons(self, clicked=None):
        if center.settings['base_path'] is not None:
            self._mod_filter = clicked
            self.update_mod_list()

    def perform_search(self, term):
        self._search_text = term.lower()
        self.update_mod_list()

    def get_tasks(self):
        return self._tasks

    def watch_task(self, task):
        logging.debug('Task "%s" (%d, %s) started.', task.title, id(task), task.__class__)
        self._tasks[id(task)] = task
        self.browser_ctrl.bridge.taskStarted.emit(id(task), task.title, [m.mid for m in task.mods])

        for m in task.mods:
            self._updating_mods[m.mid] = 0

        task.done.connect(functools.partial(self._forget_task, task))
        task.progress.connect(functools.partial(self._track_progress, task))

        if len(task.mods) == 0:
            if len(self._tasks) == 1:
                self.win.progressInfo.show()
                self.win.progressLabel.setText(task.title)
                self.win.progressBar.setValue(0)

                integration.current.show_progress(0)
            else:
                # TODO: Stop being lazy and calculate the aggregate progress.
                self.win.progressBar.hide()
                self.win.progressLabel.setText(self.tr('Working...'))

    def _track_progress(self, task, pi):
        self.browser_ctrl.bridge.taskProgress.emit(id(task), pi[0] * 100, json.dumps(pi[1]))

        for m in task.mods:
            self._updating_mods[m.mid] = pi[0] * 100

        if len(self._tasks) == 1:
            integration.current.set_progress(pi[0])
            self.win.progressBar.setValue(pi[0] * 100)

    def _forget_task(self, task):
        logging.debug('Task "%s" (%d) finished.', task.title, id(task))
        self.browser_ctrl.bridge.taskFinished.emit(id(task))
        del self._tasks[id(task)]

        for m in task.mods:
            if m.mid in self._updating_mods:
                del self._updating_mods[m.mid]

        if len(self._tasks) == 1:
            task = list(self._tasks.values())[0]
            self.win.progressLabel.setText(task.title)
            self.win.progressBar.setValue(task.get_progress()[0])
            self.win.progressBar.show()
        elif len(self._tasks) == 0:
            self.win.progressInfo.hide()
            integration.current.hide_progress()

    def abort_task(self, task):
        if task in self._tasks:
            self._tasks[task].abort()


class ModInstallWindow(Window):
    _mod = None
    _pkg_checks = None
    _dep_tpl = None

    def __init__(self, mod, sel_pkgs=[]):
        super(ModInstallWindow, self).__init__()

        self._mod = mod
        self._create_win(Ui_InstallDialog)
        self.win.splitter.setStretchFactor(0, 2)
        self.win.splitter.setStretchFactor(1, 1)

        self.label_tpl(self.win.titleLabel, MOD=mod.title)
        self.win.notesField.setPlainText(mod.notes)

        self._pkg_checks = []
        self.show_packages()
        self.update_deps()

        self.win.treeWidget.itemChanged.connect(self.update_selection)

        self.win.accepted.connect(self.install)
        self.win.rejected.connect(self.close)

        self.open()

    def show_packages(self):
        pkgs = self._mod.packages
        try:
            all_pkgs = center.mods.process_pkg_selection(pkgs)
        except repo.ModNotFound as exc:
            logging.exception('Well, I won\'t be installing that...')
            msg = self.tr('I\'m sorry but you won\'t be able to install "%s" because "%s" is missing!') % (
                self._mod.title, exc.mid)
            QtWidgets.QMessageBox.critical(None, 'Knossos', msg)

            self.close()
            return

        needed_pkgs = self._mod.resolve_deps()
        mods = set()

        for pkg in all_pkgs:
            mods.add(pkg.get_mod())

        # Make sure our current mod comes first.
        if self._mod in mods:
            mods.remove(self._mod)

        mods = [self._mod] + list(mods)
        for mod in mods:
            item = QtWidgets.QTreeWidgetItem(self.win.treeWidget, [mod.title, ''])
            item.setExpanded(True)
            item.setData(0, QtCore.Qt.UserRole, mod)
            c = 0

            for pkg in mod.packages:
                fsize = 0
                for f_item in pkg.files.values():
                    fsize += f_item.get('filesize', 0)

                if fsize > 0:
                    fsize = util.format_bytes(fsize)
                else:
                    fsize = '?'

                sub = QtWidgets.QTreeWidgetItem(item, [pkg.name, fsize])
                is_installed = center.installed.is_installed(pkg)

                if is_installed:
                    sub.setText(1, self.tr('Installed'))

                if pkg.status == 'required' or pkg in needed_pkgs or is_installed:
                    sub.setCheckState(0, QtCore.Qt.Checked)
                    sub.setDisabled(True)

                    c += 1
                elif pkg.status == 'recommended':
                    sub.setCheckState(0, QtCore.Qt.Checked)
                    c += 1
                if pkg.status == 'optional':
                    sub.setCheckState(0, QtCore.Qt.Unchecked)

                sub.setData(0, QtCore.Qt.UserRole, pkg)
                sub.setData(0, QtCore.Qt.UserRole + 1, is_installed)
                self._pkg_checks.append(sub)

            if c == len(mod.packages):
                item.setCheckState(0, QtCore.Qt.Checked)
            elif c > 0:
                item.setCheckState(0, QtCore.Qt.PartiallyChecked)
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)

        self.win.treeWidget.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    def update_selection(self, item, col):
        obj = item.data(0, QtCore.Qt.UserRole)
        if isinstance(obj, repo.Mod):
            cs = item.checkState(0)

            for i in range(item.childCount()):
                child = item.child(i)
                if not child.isDisabled():
                    child.setCheckState(0, cs)

        self.update_deps()

    def get_selected_pkgs(self):
        pkgs = []
        for item in self._pkg_checks:
            if item.checkState(0) == QtCore.Qt.Checked:
                pkgs.append(item.data(0, QtCore.Qt.UserRole))

        pkgs = center.mods.process_pkg_selection(pkgs)
        return pkgs

    def update_deps(self):
        pkg_sel = self.get_selected_pkgs()
        dl_size = 0
        for item in self._pkg_checks:
            pkg = item.data(0, QtCore.Qt.UserRole)

            if not item.data(0, QtCore.Qt.UserRole + 1):
                if item.checkState(0) == QtCore.Qt.Checked or pkg in pkg_sel:
                    for f_item in pkg.files.values():
                        dl_size += f_item.get('filesize', 0)

            if item.isDisabled():
                continue

            if pkg in pkg_sel:
                item.setCheckState(0, QtCore.Qt.Checked)

        self.label_tpl(self.win.dlSizeLabel, DL_SIZE=util.format_bytes(dl_size))

    def install(self):
        center.main_win.update_mod_buttons('home')

        run_task(InstallTask(self.get_selected_pkgs(), self._mod))
        self.close()


class LogViewer(Window):

    def __init__(self, path, window=True):
        super(LogViewer, self).__init__(window)

        self._create_win(Ui_LogDialog)
        self.win.pathLabel.setText(path)

        if not os.path.isfile(path):
            QtWidgets.QMessageBox.critical(None, 'Knossos',
                self.tr('Log file %s can\'t be shown because it\'s missing!') % path)
            return

        with open(path, 'r') as stream:
            self.win.content.setPlainText(stream.read())

        self.open()
