"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtCore import QItemSelectionModel, QItemSelection, QSize, QPointF
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PyQt5.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QListView
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsGridLayout, QScroller
from .meta_files import MetaFilesManager
from .ui.ui_mainwindow import Ui_MainWindow
from .foldermanager_window import FolderManagerWindow
from .settings_window import SettingsWindow
from .slideshow_window import SlideshowWindow
from .properties_widget import PropertiesWidget
from .qgraphics_thumb_item import QGraphicsThumbnailItem
from .thumbs_listview import ThumbsListView

from .types import Thumb_Caption_Type
from .watcher import Watcher
from .log import LOGGER
import settings
from settings import SettingType


class MainWindow(QMainWindow, Ui_MainWindow):

    _batch_count = 50

    _TV_FOLDERS_ITEM_MAP = {}

    # signals
    _dir_load_start = pyqtSignal(object)
    _dir_watcher_start = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.actiongrp_thumbs_size = QtWidgets.QActionGroup(self)
        self.actiongrp_thumbs_size.addAction(self.action_small_thumbs)
        self.actiongrp_thumbs_size.addAction(self.action_normal_thumbs)

        self.actiongrp_thumbs_caption = QtWidgets.QActionGroup(self)
        self.actiongrp_thumbs_caption.addAction(self.action_caption_none)
        self.actiongrp_thumbs_caption.addAction(self.action_caption_filename)
        self.action_caption_none.setChecked(True)

        # threads
        self._dir_watcher_thread = QThread()

        # helpers
        self._meta_files_mgr = MetaFilesManager()
        self._watch = Watcher()

        self.listView_thumbs = ThumbsListView(self.frame_thumbs)
        self.vlayout_frame_thumbs.addWidget(self.listView_thumbs)

        # connections
        self._setup_connections()

        self._setup_scan_dir_list_model()

        # Properties widget
        self.vlayout_properties = QtWidgets.QVBoxLayout(self.toolbox_metadata_properties)
        self.vlayout_properties.setContentsMargins(0, 0, 0, 0)
        self.vlayout_properties.setSpacing(0)
        self.properties_widget = PropertiesWidget(self.toolbox_metadata_properties)
        self.vlayout_properties.addWidget(self.properties_widget)

        self.statusBar().showMessage("Ready")

        # settings
        self.hslider_thumb_size.setValue(settings.get(SettingType.UI_THUMBS_SIZE, 128, 'int'))

        if settings.get(SettingType.UI_METADATA_SHOW_PROPS, False, 'bool'):
            self.toolBox_metadata.setCurrentIndex(0)
            self.toolbutton_properties.setChecked(True)
            self.toolbutton_tags.setChecked(False)
            self.action_properties.setChecked(True)
            self.action_tags.setChecked(False)
            self.frame_metadata.show()
        elif settings.get(SettingType.UI_METADATA_SHOW_TAGS, False, 'bool'):
            self.toolBox_metadata.setCurrentIndex(1)
            self.toolbutton_properties.setChecked(False)
            self.toolbutton_tags.setChecked(True)
            self.action_properties.setChecked(False)
            self.action_tags.setChecked(True)
            self.frame_metadata.show()
        else:
            self.frame_metadata.hide()

    def resizeEvent(self, event):
        if event.spontaneous():
            # Begin loading the currently selected dir
            folders_index = self._dirs_list_model.indexFromItem(self._TV_FOLDERS_ITEM_MAP[0])
            if self._dirs_list_model.rowCount(folders_index) > 0:
                self._dirs_list_selection_model.select(
                    self._dirs_list_model.index(0, 0).child(0, 0),
                    QItemSelectionModel.Select | QItemSelectionModel.Rows
                )
                selected = self.treeView_scandirs.selectedIndexes()
                sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
                if sd_id > 0:
                    self._load_dir_images(sd_id)
            # Start the dir watcher thread
            self.init_watch_thread()

    def _setup_connections(self):
        # Menu
        # File
        self.action_add_folder.triggered.connect(self.action_folder_manager_clicked)
        self.action_file_locate.triggered.connect(self.handle_action_file_locate_triggered)
        self.action_exit.triggered.connect(self.action_exit_clicked)
        # View
        self.action_small_thumbs.triggered.connect(self.handle_action_small_thumbs_triggered)
        self.action_normal_thumbs.triggered.connect(self.handle_action_normal_thumbs_triggered)
        self.action_properties.triggered.connect(self.action_properties_clicked)
        self.action_tags.triggered.connect(self.action_tags_clicked)
        self.action_slideshow.triggered.connect(self.start_slideshow)
        self.action_caption_none.triggered.connect(self.handle_action_thumbnail_caption_none_triggered)
        self.action_caption_filename.triggered.connect(self.handle_action_thumbnail_caption_filename_triggered)
        # Folder
        self.action_folder_slideshow.triggered.connect(self.start_slideshow)
        self.action_folder_locate.triggered.connect(self.handle_action_folder_locate_triggered)
        # Picture
        self.action_picture_properties.triggered.connect(self.show_image_properties)
        # Tools
        self.action_settings.triggered.connect(self.handle_action_settings_triggered)
        self.action_folder_manager.triggered.connect(self.action_folder_manager_clicked)

        # Btns
        self.btn_slideshow.clicked.connect(self.start_slideshow)
        self.hslider_thumb_size.valueChanged.connect(self.on_hslider_thumb_size_value_changed)

        # Watcher
        self._dir_watcher_start.connect(self._watch.watch_all)
        self._watch.new_img_found.connect(self.on_new_img_found)
        self._watch.watch_all_done.connect(self.on_watch_all_done)
        self._watch.dir_added_or_updated.connect(self.on_dir_added_or_updated)
        self._watch.dir_empty_or_deleted.connect(self.on_dir_empty_deleted)

        # Tree View
        self.treeView_scandirs.clicked.connect(self.on_scan_dir_treeView_clicked)

        # Thumbs view
        self.listView_thumbs.clicked.connect(self.on_thumb_clicked)
        self.listView_thumbs.empty_area_clicked.connect(self.on_thumb_listview_empty_area_clicked)

        self.buttonGroup_metadata.buttonClicked.connect(self.on_buttongroup_metadata_clicked)

    def init_watch_thread(self):
        self._watch.moveToThread(self._dir_watcher_thread)
        self._dir_watcher_thread.start()
        LOGGER.info('Watcher thread started.')
        self._dir_watcher_start.emit()

    def _setup_scan_dir_list_model(self):
        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        self._dirs_list_model = QStandardItemModel()
        self._dirs_list_selection_model = QItemSelectionModel(self._dirs_list_model)
        self._thumbs_view_model = QStandardItemModel()
        self._thumbs_selection_model = QItemSelectionModel(self._thumbs_view_model)

        self._dirs_list_model.setColumnCount(1)
        # self._dirs_list_model.setRowCount(len(scan_dirs))

        self._root_tree_item = self._dirs_list_model.invisibleRootItem()
        # FOLDERS item
        folder_item = QStandardItem("Folders")
        folder_item_font = QFont()
        folder_item_font.setBold(True)
        folder_item.setFont(folder_item_font)
        folder_item.setSizeHint(QSize(folder_item.sizeHint().width(), 24))
        self._root_tree_item.appendRow(folder_item)
        self._TV_FOLDERS_ITEM_MAP[0] = folder_item

        self.treeView_scandirs.setModel(self._dirs_list_model)
        self.treeView_scandirs.setSelectionModel(self._dirs_list_selection_model)
        self.treeView_scandirs.expandAll()

        self.listView_thumbs.setModel(self._thumbs_view_model)
        self.listView_thumbs.setSelectionModel(self._thumbs_selection_model)

        if scan_dirs:
            for idx, dir in enumerate(scan_dirs):
                item_title = "%s(%s)" % (dir['name'], dir['img_count'])
                item = QStandardItem(item_title)
                item.setData(dir['id'], QtCore.Qt.UserRole + 1)
                item.setSizeHint(QSize(item.sizeHint().width(), 24))
                item.setIcon(QIcon(':/images/icon_folder'))
                folder_item.appendRow(item)
                self._TV_FOLDERS_ITEM_MAP[dir['id']] = item

    def handle_action_file_locate_triggered(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
            self._meta_files_mgr.connect()
            dr_img = self._meta_files_mgr.get_image_from_id(curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
            self._meta_files_mgr.disconnect()
            explorer_process = QtCore.QProcess()
            explorer_process.setProgram('explorer.exe')
            explorer_process.setArguments(['/select,%s' % QtCore.QDir.toNativeSeparators(dr_img['abspath'])])
            explorer_process.startDetached()

    def handle_action_folder_locate_triggered(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids:
            self._meta_files_mgr.connect()
            dr_sd = self._meta_files_mgr.get_scan_dir(curr_sel_ids['sd_id'])
            self._meta_files_mgr.disconnect()
            explorer_process = QtCore.QProcess()
            explorer_process.setProgram('explorer.exe')
            explorer_process.setArguments(['/select,%s' % QtCore.QDir.toNativeSeparators(dr_sd['abspath'])])
            explorer_process.startDetached()
    
    def handle_action_small_thumbs_triggered(self):
        if self.action_small_thumbs.isChecked():
            self.hslider_thumb_size.triggerAction(self.hslider_thumb_size.SliderToMinimum)

    def handle_action_normal_thumbs_triggered(self):
        if self.action_normal_thumbs.isChecked():
            slider_value = self.hslider_thumb_size.value()
            if slider_value < 128:
                self.hslider_thumb_size.triggerAction(self.hslider_thumb_size.SliderPageStepAdd)
            elif slider_value > 128 and slider_value <= 192:
                self.hslider_thumb_size.triggerAction(self.hslider_thumb_size.SliderPageStepSub)
            elif slider_value > 192 and slider_value <= 256:
                self.hslider_thumb_size.triggerAction(self.hslider_thumb_size.SliderPageStepSub)
                self.hslider_thumb_size.triggerAction(self.hslider_thumb_size.SliderPageStepSub)

    def handle_action_thumbnail_caption_none_triggered(self):
        if self.action_caption_none.isChecked():
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids:
                self._load_dir_images(curr_sel_ids['sd_id'])

    def handle_action_thumbnail_caption_filename_triggered(self):
        if self.action_caption_filename.isChecked():
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids:
                self._load_dir_images(curr_sel_ids['sd_id'], Thumb_Caption_Type.FileName)
 
    def action_folder_manager_clicked(self):
        self.folder_mgr_window = FolderManagerWindow(self)
        self.folder_mgr_window.setModal(True)
        self.folder_mgr_window.show()

    def action_properties_clicked(self):
        if self.action_properties.isChecked():
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
                img_props = self._meta_files_mgr.get_img_properties(curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
                self.properties_widget.setup_properties(img_props)

            self.toolBox_metadata.setCurrentIndex(0)
            self.frame_metadata.show()
            self.toolbutton_properties.setChecked(True)
            self.toolbutton_tags.setChecked(False)
            self.action_tags.setChecked(False)
            settings.save(SettingType.UI_METADATA_SHOW_PROPS, True)
            settings.save(SettingType.UI_METADATA_SHOW_TAGS, False)
        else:
            self.frame_metadata.hide()
            self.toolbutton_properties.setChecked(False)
            settings.save(SettingType.UI_METADATA_SHOW_PROPS, False)
            settings.save(SettingType.UI_METADATA_SHOW_TAGS, False)

    def action_tags_clicked(self):
        if self.action_tags.isChecked():
            self.toolBox_metadata.setCurrentIndex(1)
            self.frame_metadata.show()
            self.toolbutton_tags.setChecked(True)
            self.toolbutton_properties.setChecked(False)
            self.action_properties.setChecked(False)
            settings.save(SettingType.UI_METADATA_SHOW_PROPS, False)
            settings.save(SettingType.UI_METADATA_SHOW_TAGS, True)
        else:
            self.frame_metadata.hide()
            self.toolbutton_tags.setChecked(False)
            settings.save(SettingType.UI_METADATA_SHOW_PROPS, False)
            settings.save(SettingType.UI_METADATA_SHOW_TAGS, False)

    def show_image_properties(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
            img_props = self._meta_files_mgr.get_img_properties(curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
            self.properties_widget.setup_properties(img_props)

        self.toolBox_metadata.setCurrentIndex(0)
        self.frame_metadata.show()
        self.toolbutton_properties.setChecked(True)
        self.toolbutton_tags.setChecked(False)
        self.action_properties.setChecked(True)
        self.action_tags.setChecked(False)
    
    def handle_action_settings_triggered(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.setModal(True)
        self.settings_window.show()

    def on_buttongroup_metadata_clicked(self, button):
        if button.objectName() == 'toolbutton_tags':
            self.action_tags.trigger()
        elif button.objectName() == 'toolbutton_properties':
            self.action_properties.trigger()

    def on_hslider_thumb_size_value_changed(self, value):
        if self.hslider_thumb_size.value() == 64:
            self.action_small_thumbs.setChecked(True)
        elif self.hslider_thumb_size.value() == 128:
            self.action_normal_thumbs.setChecked(True)
        else:
            self.action_small_thumbs.setChecked(False)
            self.action_normal_thumbs.setChecked(False)

        self.listView_thumbs.setIconSize(QSize(value, value))
        self.listView_thumbs.setGridSize(QSize(value + 20, value + 20))

        settings.save(SettingType.UI_THUMBS_SIZE, value)

    def _load_dir_images(self, sd_id, thumb_caption_type=Thumb_Caption_Type.NoCaption):
        self._clear_thumbs()

        dir_info = self._meta_files_mgr.get_scan_dir(sd_id)
        self.lbl_dir_name.setText(dir_info['name'])

        images = self._meta_files_mgr.get_scan_dir_images(sd_id)

        for img in images:
            img['thumb'] = QImage.fromData(img['thumb'])
            item = QStandardItem()

            if thumb_caption_type == Thumb_Caption_Type.FileName:
                item.setText(img['name'])

            item.setData(img['id'], QtCore.Qt.UserRole + 1)
            item.setData(img['serial'], QtCore.Qt.UserRole + 2)
            item.setIcon(QIcon(QPixmap.fromImage(img['thumb'])))
            self._thumbs_view_model.appendRow(item)

        QScroller.grabGesture(self.listView_thumbs.viewport(),
                              QScroller.LeftMouseButtonGesture)

    def _clear_thumbs(self):
        self._thumbs_view_model.clear()

    def _tv_add_scan_dir(self, dir_info, highlight=False):
        item_title = "%s(%s)" % (dir_info['name'], dir_info['img_count'])
        item = QStandardItem(item_title)
        item.setData(dir_info['id'], QtCore.Qt.UserRole + 1)
        item.setSizeHint(QSize(item.sizeHint().width(), 24))
        item.setIcon(QIcon(':/images/icon_folder'))
        if highlight:
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(bold_font)
        folder_item = self._TV_FOLDERS_ITEM_MAP[0]
        folder_item.appendRow(item)
        self._TV_FOLDERS_ITEM_MAP[dir_info['id']] = item

    @pyqtSlot()
    def start_slideshow(self):
        selected = self.treeView_scandirs.selectedIndexes()
        sd_id = selected[0].data(QtCore.Qt.UserRole + 1)

        img_serial = 1
        thumb_selected = self.listView_thumbs.selectedIndexes()
        if len(thumb_selected) > 0:
            img_serial = thumb_selected[0].data(QtCore.Qt.UserRole + 2)

        if sd_id > 0:
            self._slideshow = SlideshowWindow(sd_id, img_serial)
            self._slideshow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
            self._slideshow.showFullScreen()

    @pyqtSlot(QModelIndex)
    def on_thumb_clicked(self, mindex):
        selected = self.treeView_scandirs.selectedIndexes()
        sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
        si_id = mindex.data(QtCore.Qt.UserRole + 1)
        img_props = self._meta_files_mgr.get_img_properties(si_id, sd_id)
        self.lbl_selection_summary.setText(self.get_thumb_selection_summary(img_props))

        if self.action_properties.isChecked():
            self.properties_widget.setup_properties(img_props)

    @pyqtSlot()
    def on_thumb_listview_empty_area_clicked(self):
        selected_thumb = self.listView_thumbs.selectedIndexes()
        if len(selected_thumb) == 0:
            selected = self.treeView_scandirs.selectedIndexes()
            sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
            props = self._meta_files_mgr.get_dir_properties(sd_id)
            self.lbl_selection_summary.setText(self.get_dir_selection_summary(props))

    def get_dir_selection_summary(self, props):
        img_count = props['img_count']
        modified = props['modified'].toString('dd MMMM yyyy')
        size = props['size']
        return "%s pictures        %s        %s on disk" % (img_count, modified, size)

    def get_thumb_selection_summary(self, props):
        filename = props['filename']
        modified = props['DateTime'] if 'DateTime' in props else ''
        dimensions = props['dimensions']
        filesize = props['filesize']
        return "%s        %s        %s        %s" % (filename, modified, dimensions, filesize)

    @pyqtSlot(QModelIndex)
    def on_scan_dir_treeView_clicked(self, index):
        sd_id = index.data(QtCore.Qt.UserRole + 1)
        props = self._meta_files_mgr.get_dir_properties(sd_id)
        self.lbl_selection_summary.setText(self.get_dir_selection_summary(props))
        # Categories tree nodes will not contain 'data'
        if sd_id:
            self._load_dir_images(sd_id)

    @pyqtSlot(object)
    def on_new_img_found(self, img_info):
        self.statusBar().showMessage("Found new image: %s - %s" %
                                     (img_info['dir'],
                                      img_info['filename']))

    @pyqtSlot(object)
    def on_dir_added_or_updated(self, dir_info):
        if dir_info['id'] in self._TV_FOLDERS_ITEM_MAP:
            item = self._TV_FOLDERS_ITEM_MAP[dir_info['id']]
            item_title = "%s(%s)" % (dir_info['name'], dir_info['img_count'])
            item.setText(item_title)
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(bold_font)
        else:
            self._tv_add_scan_dir(dir_info, True)

    @pyqtSlot(object)
    def on_dir_empty_deleted(self, dir_info):
        if dir_info['id'] in self._TV_FOLDERS_ITEM_MAP:
            item = self._TV_FOLDERS_ITEM_MAP[dir_info['id']]
            item_index = self._dirs_list_model.indexFromItem(item)
            parent_index = self._dirs_list_model.indexFromItem(self._TV_FOLDERS_ITEM_MAP[0])
            self._dirs_list_model.removeRow(item_index.row(), parent_index)
            self._TV_FOLDERS_ITEM_MAP.pop(dir_info['id'])

    @pyqtSlot()
    def on_watch_all_done(self):
        self.statusBar().clearMessage()

    def get_current_selection_ids(self):
        selected_ids = {}
        selected = self.treeView_scandirs.selectedIndexes()
        selected_ids['sd_id'] = selected[0].data(QtCore.Qt.UserRole + 1)
        selected_thumb = self.listView_thumbs.selectedIndexes()
        if len(selected_thumb) > 0:
            selected_ids['si_id'] = selected_thumb[0].data(QtCore.Qt.UserRole + 1)
        return selected_ids

    def action_exit_clicked(self):
        self.close()

    def closeEvent(self, event):
        settings.persist_to_disk()
