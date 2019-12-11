"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Signal, Slot, QSize, QThread, QModelIndex
from PySide2.QtCore import QItemSelectionModel, QItemSelection, QSize, QPointF
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PySide2.QtGui import QPixmap, QImage, QColor, QIcon
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide2.QtWidgets import QGridLayout, QLabel, QWidget, QPushButton
from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QListView
from PySide2.QtWidgets import QGraphicsDropShadowEffect, QGraphicsGridLayout, QScroller
from imagius.meta_files import MetaFilesManager
from imagius.ui.ui_mainwindow import Ui_MainWindow
from imagius.foldermanager_window import FolderManagerWindow
from imagius.settings_window import SettingsWindow
from imagius.slideshow_window import SlideshowWindow
from imagius.properties_widget import PropertiesWidget
# from qgraphics_thumb_item import QGraphicsThumbnailItem
from imagius.thumbs_listview import ThumbsListView

from imagius.imagius_types import Thumb_Caption_Type
from imagius.watcher import Watcher
from imagius.loader import ImageLoader
from imagius.log import LOGGER
from imagius.update_manager import UpdateManager
from imagius import settings
from imagius.settings import SettingType
from imagius.constants import ScrollDirection


class MainWindow(QMainWindow, Ui_MainWindow):

    _TV_FOLDERS_ITEM_MAP = {}

    # signals
    _dir_load_start = Signal(object)
    _dir_watcher_start = Signal()

    _loader_load_scandir = Signal(int, int, int, object)

    _is_watcher_running = False
    _update_mgr = None

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
        self._img_loader_thread = QThread()

        # helpers
        self._meta_files_mgr = MetaFilesManager()
        self._meta_files_mgr.connect()
        self._watch = Watcher()
        self._img_loader = ImageLoader()

        self.listView_thumbs = ThumbsListView(self.frame_thumbs)
        self.listView_thumbs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.vlayout_frame_thumbs.addWidget(self.listView_thumbs)

        # connections
        self._setup_connections()

        # Populates the folder list
        self._setup_scan_dir_list_model()

        # Properties widget
        self.vlayout_properties = QtWidgets.QVBoxLayout(
            self.toolbox_metadata_properties)
        self.vlayout_properties.setContentsMargins(0, 0, 0, 0)
        self.vlayout_properties.setSpacing(0)
        self.properties_widget = PropertiesWidget(
            self.toolbox_metadata_properties)
        self.vlayout_properties.addWidget(self.properties_widget)

        self.statusBar().showMessage("Ready")

        # settings
        self.hslider_thumb_size.setValue(settings.get(
            SettingType.UI_THUMBS_SIZE, 128, 'int'))

        thumb_caption_type = settings.get(
            SettingType.UI_THUMBS_CAPTION_DISPLAY_MODE, Thumb_Caption_Type.NoCaption.name)
        if thumb_caption_type == Thumb_Caption_Type.FileName.name:
            self.action_caption_filename.setChecked(True)

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

        # Set event filters
        self.btn_slideshow.installEventFilter(self)

        self._curr_img_serial = 1

    def resizeEvent(self, event):
        if event.spontaneous():
            # Begin loading the currently selected dir
            self._make_default_dir_list_selection()
            cur_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in cur_sel_ids:
                self._load_dir_images(cur_sel_ids['sd_id'])
            # Start the dir watcher thread
            self.init_watch_thread()
            # Start the loader thread
            self.init_loader_thread()

    def closeEvent(self, event):
        LOGGER.debug('Shutting down gracefully....')
        self._meta_files_mgr.disconnect()
        settings.persist_to_disk()

        self._dir_watcher_thread.quit()
        self._dir_watcher_thread.wait()

        self._img_loader_thread.quit()
        self._img_loader_thread.wait()

    def _make_default_dir_list_selection(self):
        folders_index = self._dirs_list_model.indexFromItem(
            self._TV_FOLDERS_ITEM_MAP[0])
        if self._dirs_list_model.rowCount(folders_index) > 0:
            self._dirs_list_selection_model.select(
                self._dirs_list_model.index(0, 0).child(0, 0),
                QItemSelectionModel.Select | QItemSelectionModel.Rows
            )

    def _setup_connections(self):
        # Menu
        # File
        self.action_add_folder.triggered.connect(
            self.action_folder_manager_clicked)
        self.action_rescan.triggered.connect(self._run_watcher)
        self.action_file_locate.triggered.connect(
            self.handle_action_file_locate_triggered)
        self.action_exit.triggered.connect(self.action_exit_clicked)
        # View
        self.action_small_thumbs.triggered.connect(
            self.handle_action_small_thumbs_triggered)
        self.action_normal_thumbs.triggered.connect(
            self.handle_action_normal_thumbs_triggered)
        self.action_properties.triggered.connect(
            self.action_properties_clicked)
        self.action_tags.triggered.connect(self.action_tags_clicked)
        self.action_slideshow.triggered.connect(self.start_slideshow)
        self.action_caption_none.triggered.connect(
            self.handle_action_thumbnail_caption_none_triggered)
        self.action_caption_filename.triggered.connect(
            self.handle_action_thumbnail_caption_filename_triggered)
        # Folder
        self.action_folder_slideshow.triggered.connect(self.start_slideshow)
        self.action_folder_locate.triggered.connect(
            self.handle_action_folder_locate_triggered)
        # Picture
        self.action_picture_properties.triggered.connect(
            self.show_image_properties)
        # Tools
        self.action_settings.triggered.connect(
            self.handle_action_settings_triggered)
        self.action_folder_manager.triggered.connect(
            self.action_folder_manager_clicked)
        # Help
        self.action_check_updates.triggered.connect(
            self._handle_check_for_updates_clicked)

        # Btns
        self.btn_slideshow.clicked.connect(self.start_slideshow)
        self.hslider_thumb_size.valueChanged.connect(
            self.on_hslider_thumb_size_value_changed)

        # Watcher
        self._dir_watcher_start.connect(self._watch.watch_all)
        self._watch.new_img_found.connect(self.on_new_img_found)
        self._watch.watch_all_done.connect(self.on_watch_all_done)
        self._watch.dir_added_or_updated.connect(self.on_dir_added_or_updated)
        self._watch.dir_empty_or_deleted.connect(self.on_dir_empty_deleted)
        self._watch.watch_empty_or_deleted_done.connect(
            self.on_watch_dir_empty_deleted_done)

        # Loader
        self._loader_load_scandir.connect(self._img_loader.load_scandir)
        # self._loader_load_scanimg.connect(self._img_loader.load_scanimg)
        self._img_loader.load_scan_dir_info_success.connect(
            self._handle_load_scan_dir_info_success)
        # self._img_loader.load_images_success.connect(
            # self._handle_load_images_sucess)
        self._img_loader.load_images_success.connect(
            self.listView_thumbs.render_thumbs)

        # Tree View
        self.treeView_scandirs.clicked.connect(
            self.on_scan_dir_treeView_clicked)

        # Thumbs view
        self.listView_thumbs.clicked.connect(self.on_thumb_clicked)
        self.listView_thumbs.empty_area_clicked.connect(
            self.on_thumb_listview_empty_area_clicked)
        self.listView_thumbs.load_dir_images_for_scroll_up.connect(
            self.on_load_dir_images_for_scroll_up)
        self.listView_thumbs.load_dir_images_for_scroll_down.connect(
            self.on_load_dir_images_for_scroll_down)

        self.buttonGroup_metadata.buttonClicked.connect(
            self.on_buttongroup_metadata_clicked)

        self.txtbox_search.textEdited.connect(self.handle_search)

    def init_watch_thread(self):
        self._watch.moveToThread(self._dir_watcher_thread)
        self._dir_watcher_thread.start()
        self._run_watcher()
        LOGGER.debug('Watcher thread started.')

    def init_loader_thread(self):
        self._img_loader.moveToThread(self._img_loader_thread)
        self._img_loader_thread.start()
        LOGGER.debug('Loader thread started.')

    def _run_watcher(self):
        self._is_watcher_running = True
        self.action_rescan.setEnabled(False)
        self._dir_watcher_start.emit()

    def _populate_dirs_tree_view(self, parent_key, folders):
        parent_item = self._TV_FOLDERS_ITEM_MAP[parent_key]
        if folders:
            for idx, dir in enumerate(folders):
                item_title = "%s(%s)" % (dir['name'], dir['img_count'])
                item = QStandardItem(item_title)
                item.setData(dir['id'], QtCore.Qt.UserRole + 1)
                item.setSizeHint(QSize(item.sizeHint().width(), 24))
                item.setIcon(QIcon(':/images/icon_folder'))
                parent_item.appendRow(item)
                if parent_key == 0:
                    self._TV_FOLDERS_ITEM_MAP[dir['id']] = item
        self.treeView_scandirs.expandAll()

    def _setup_scan_dir_list_model(self):
        self._dirs_list_model = QStandardItemModel()
        self._dirs_list_selection_model = QItemSelectionModel(
            self._dirs_list_model)
        self._thumbs_view_model = QStandardItemModel()
        self._thumbs_selection_model = QItemSelectionModel(
            self._thumbs_view_model)

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
        self.treeView_scandirs.setSelectionModel(
            self._dirs_list_selection_model)
        # self.treeView_scandirs.setRootIsDecorated(False)

        self.listView_thumbs.setModel(self._thumbs_view_model)
        self.listView_thumbs.setSelectionModel(self._thumbs_selection_model)

        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        self._populate_dirs_tree_view(0, scan_dirs)

    def _repopulate_scan_dir_list_model(self):
        self._clear_folders_tree_view()
        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        self._populate_dirs_tree_view(0, scan_dirs)

    def _populate_search_tree_view(self, results):
        if 'search' not in self._TV_FOLDERS_ITEM_MAP:
            self._root_tree_item = self._dirs_list_model.invisibleRootItem()
            # FOLDERS item
            search_item = QStandardItem("Search")
            search_item_font = QFont()
            search_item_font.setBold(True)
            search_item.setFont(search_item_font)
            search_item.setSizeHint(QSize(search_item.sizeHint().width(), 24))
            self._root_tree_item.insertRow(0, search_item)
            self._TV_FOLDERS_ITEM_MAP['search'] = search_item
        self._populate_dirs_tree_view('search', results)

    def eventFilter(self, widget, event):
        if widget.objectName() == 'btn_slideshow':
            if event.type() == QtCore.QEvent.Enter:
                self.label_thumbs_toolbar_tooltip.setText(
                    "Play Fullscreen Slideshow")
            elif event.type() == QtCore.QEvent.Leave:
                self.label_thumbs_toolbar_tooltip.setText("")
        return QtWidgets.QWidget.eventFilter(self, widget, event)

    def handle_search(self, search_term):
        self._clear_search()
        if search_term != '':
            searches = self._meta_files_mgr.search_scan_dirs(search_term)
            self._populate_search_tree_view(searches)
        else:
            self._remove_search_tree_view()

    def handle_action_file_locate_triggered(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
            dr_img = self._meta_files_mgr.get_image_from_id(
                curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
            explorer_process = QtCore.QProcess()
            explorer_process.setProgram('explorer.exe')
            explorer_process.setArguments(
                ['/select,%s' % QtCore.QDir.toNativeSeparators(dr_img['abspath'])])
            explorer_process.startDetached()

    def handle_action_folder_locate_triggered(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids:
            dr_sd = self._meta_files_mgr.get_scan_dir(curr_sel_ids['sd_id'])
            explorer_process = QtCore.QProcess()
            explorer_process.setProgram('explorer.exe')
            explorer_process.setArguments(
                ['/select,%s' % QtCore.QDir.toNativeSeparators(dr_sd['abspath'])])
            explorer_process.startDetached()

    def handle_action_small_thumbs_triggered(self):
        if self.action_small_thumbs.isChecked():
            self.hslider_thumb_size.triggerAction(
                self.hslider_thumb_size.SliderToMinimum)

    def handle_action_normal_thumbs_triggered(self):
        if self.action_normal_thumbs.isChecked():
            slider_value = self.hslider_thumb_size.value()
            if slider_value < 128:
                self.hslider_thumb_size.triggerAction(
                    self.hslider_thumb_size.SliderPageStepAdd)
            elif slider_value > 128 and slider_value <= 192:
                self.hslider_thumb_size.triggerAction(
                    self.hslider_thumb_size.SliderPageStepSub)
            elif slider_value > 192 and slider_value <= 256:
                self.hslider_thumb_size.triggerAction(
                    self.hslider_thumb_size.SliderPageStepSub)
                self.hslider_thumb_size.triggerAction(
                    self.hslider_thumb_size.SliderPageStepSub)

    def handle_action_thumbnail_caption_none_triggered(self):
        if self.action_caption_none.isChecked():
            settings.save(SettingType.UI_THUMBS_CAPTION_DISPLAY_MODE,
                          Thumb_Caption_Type.NoCaption.name)
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids:
                self._load_dir_images(curr_sel_ids['sd_id'])

    def handle_action_thumbnail_caption_filename_triggered(self):
        if self.action_caption_filename.isChecked():
            settings.save(SettingType.UI_THUMBS_CAPTION_DISPLAY_MODE,
                          Thumb_Caption_Type.FileName.name)
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids:
                self._load_dir_images(curr_sel_ids['sd_id'])

    def action_folder_manager_clicked(self):
        self.folder_mgr_window = FolderManagerWindow(self)
        self.folder_mgr_window.accepted.connect(
            self._on_folder_manager_window_accepted)
        self.folder_mgr_window.setModal(True)
        self.folder_mgr_window.show()

    def _on_folder_manager_window_accepted(self):
        self._repopulate_scan_dir_list_model()
        self._run_watcher()

    def action_properties_clicked(self):
        if self.action_properties.isChecked():
            curr_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
                img_props = self._meta_files_mgr.get_img_properties(
                    curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
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
            # Forces the list view to re-render after the metadata window is hidden
            self._thumbs_view_model.layoutChanged.emit()

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
            # Forces the list view to re-render after the metadata window is hidden
            self._thumbs_view_model.layoutChanged.emit()

    def show_image_properties(self):
        curr_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in curr_sel_ids and 'si_id' in curr_sel_ids:
            img_props = self._meta_files_mgr.get_img_properties(
                curr_sel_ids['si_id'], curr_sel_ids['sd_id'])
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

    def _handle_check_for_updates_clicked(self):
        if not self._update_mgr:
            self._update_mgr = UpdateManager()
        self._update_mgr.get_updates()

    def _load_dir_images(self, sd_id):
        self._clear_thumbs()
        load_count = self.listView_thumbs.get_visible_thumb_count(
            self.hslider_thumb_size.value() + 20)
        print("load count %d" % load_count)
        self._loader_load_scandir.emit(
            sd_id, 0, load_count, ScrollDirection.Down)
        QScroller.grabGesture(self.listView_thumbs.viewport(),
                              QScroller.LeftMouseButtonGesture)

    def _load_dir_images_for_scroll_up(self, sd_id, serial, count):
        # self._clear_thumbs()
        load_count = self.listView_thumbs.get_visible_thumb_count(
            self.hslider_thumb_size.value() + 20)
        self._loader_load_scandir.emit(
            sd_id, serial, count, ScrollDirection.Up)
        QScroller.grabGesture(self.listView_thumbs.viewport(),
                              QScroller.LeftMouseButtonGesture)

    def _load_dir_images_for_scroll_down(self, sd_id, serial, count):
        # self._clear_thumbs()
        load_count = self.listView_thumbs.get_visible_thumb_count(
            self.hslider_thumb_size.value() + 20)
        self._loader_load_scandir.emit(
            sd_id, serial, count, ScrollDirection.Down)
        QScroller.grabGesture(self.listView_thumbs.viewport(),
                              QScroller.LeftMouseButtonGesture)

    @Slot(int, int)
    def on_load_dir_images_for_scroll_up(self, serial, count):
        cur_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in cur_sel_ids:
            self._load_dir_images_for_scroll_up(
                cur_sel_ids['sd_id'], serial, count)

    @Slot(int, int)
    def on_load_dir_images_for_scroll_down(self, serial, count):
        cur_sel_ids = self.get_current_selection_ids()
        if 'sd_id' in cur_sel_ids:
            self._load_dir_images_for_scroll_down(
                cur_sel_ids['sd_id'], serial, count)

    def _handle_load_scan_dir_info_success(self, dir_info):
        self.lbl_dir_name.setText(dir_info['name'])

    @Slot(object, int)
    def _handle_load_images_sucess(self, images, scrollDirection):
        img_count = len(images)
        print('Recevied %s images' % img_count)
        LOGGER.debug('Recevied %s images' % img_count)
        for img in images:
            img['thumb'] = QImage.fromData(img['thumb'])
            item = QStandardItem()

            thumb_caption_type = settings.get(
                SettingType.UI_THUMBS_CAPTION_DISPLAY_MODE, Thumb_Caption_Type.NoCaption.name)
            if thumb_caption_type == Thumb_Caption_Type.FileName.name:
                item.setText(img['name'])

            item.setData(img['id'], QtCore.Qt.UserRole + 1)
            item.setData(img['serial'], QtCore.Qt.UserRole + 2)
            item.setIcon(QIcon(QPixmap.fromImage(img['thumb'])))
            item.setText(str(img['serial']))

            if scrollDirection == ScrollDirection.Up:
                self._thumbs_view_model.insertRow(0, item)
            if scrollDirection == ScrollDirection.Down:
                self._thumbs_view_model.appendRow(item)

    def _clear_thumbs(self):
        self._thumbs_view_model.clear()
        self.lbl_dir_name.setText('')

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

    @Slot()
    def start_slideshow(self):
        selected = self.treeView_scandirs.selectedIndexes()
        sd_id = selected[0].data(QtCore.Qt.UserRole + 1)

        img_serial = 1
        thumb_selected = self.listView_thumbs.selectedIndexes()
        if len(thumb_selected) > 0:
            img_serial = thumb_selected[0].data(QtCore.Qt.UserRole + 2)

        if sd_id > 0:
            self._slideshow = SlideshowWindow(sd_id, img_serial)
            self._slideshow.setWindowFlags(
                QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
            self._slideshow.showFullScreen()

    @Slot(QModelIndex)
    def on_thumb_clicked(self, mindex):
        selected = self.treeView_scandirs.selectedIndexes()
        sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
        si_id = mindex.data(QtCore.Qt.UserRole + 1)
        img_props = self._meta_files_mgr.get_img_properties(si_id, sd_id)
        self.lbl_selection_summary.setText(
            self.get_thumb_selection_summary(img_props))

        if self.action_properties.isChecked():
            self.properties_widget.setup_properties(img_props)

    @Slot()
    def on_thumb_listview_empty_area_clicked(self):
        selected_thumb = self.listView_thumbs.selectedIndexes()
        if len(selected_thumb) == 0:
            selected = self.treeView_scandirs.selectedIndexes()
            sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
            if sd_id:
                props = self._meta_files_mgr.get_dir_properties(sd_id)
                self.lbl_selection_summary.setText(
                    self.get_dir_selection_summary(props))

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

    @Slot(QModelIndex)
    def on_scan_dir_treeView_clicked(self, index):
        sd_id = index.data(QtCore.Qt.UserRole + 1)
        # Categories tree nodes will not contain 'data'
        if sd_id:
            item = self._TV_FOLDERS_ITEM_MAP[sd_id]
            bold_font = QFont()
            bold_font.setBold(False)
            item.setFont(bold_font)
            props = self._meta_files_mgr.get_dir_properties(sd_id)
            self.lbl_selection_summary.setText(
                self.get_dir_selection_summary(props))
            self._load_dir_images(sd_id)

    @Slot(object)
    def on_new_img_found(self, img_info):
        self.statusBar().showMessage("Found new image: %s - %s" %
                                     (img_info['dir'],
                                      img_info['filename']))

    @Slot(object)
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

    @Slot(object)
    def on_dir_empty_deleted(self, dir_info):
        if dir_info['id'] in self._TV_FOLDERS_ITEM_MAP:
            item = self._TV_FOLDERS_ITEM_MAP[dir_info['id']]
            item_index = self._dirs_list_model.indexFromItem(item)
            parent_index = self._dirs_list_model.indexFromItem(
                self._TV_FOLDERS_ITEM_MAP[0])
            self._dirs_list_model.removeRow(item_index.row(), parent_index)
            self._TV_FOLDERS_ITEM_MAP.pop(dir_info['id'])

    @Slot()
    def on_watch_dir_empty_deleted_done(self):
        # Here we make sure a folder is always selected if one more folders
        # ever get deleted by the watcher thread. If no folders exits, just
        # display an empty thumbs list
        cur_sel_ids = self.get_current_selection_ids()
        print(cur_sel_ids)
        if 'sd_id' not in cur_sel_ids:
            self._make_default_dir_list_selection()
            cur_sel_ids = self.get_current_selection_ids()
            if 'sd_id' in cur_sel_ids:
                self._load_dir_images(cur_sel_ids['sd_id'])
            else:
                self._clear_thumbs()

    @Slot(object, object)
    def on_watch_all_done(self, elapsed, suffix):
        self.statusBar().clearMessage()
        self._is_watcher_running = False
        self.action_rescan.setEnabled(True)
        self.statusBar().showMessage("Folder scan completed in %.2f %s" % (elapsed, suffix))

    def get_current_selection_ids(self):
        selected_ids = {}
        selected = self.treeView_scandirs.selectedIndexes()
        if len(selected) <= 0:
            return selected_ids
        selected_ids['sd_id'] = selected[0].data(QtCore.Qt.UserRole + 1)
        selected_thumb = self.listView_thumbs.selectedIndexes()
        if len(selected_thumb) <= 0:
            return selected_ids
        selected_ids['si_id'] = selected_thumb[0].data(QtCore.Qt.UserRole + 1)
        return selected_ids

    def action_exit_clicked(self):
        self.close()

    def _clear_search(self):
        if 'search' in self._TV_FOLDERS_ITEM_MAP:
            search_item = self._TV_FOLDERS_ITEM_MAP['search']
            search_item.removeRows(0, search_item.rowCount())

    def _clear_folders_tree_view(self):
        folder_item = self._TV_FOLDERS_ITEM_MAP[0]
        self._TV_FOLDERS_ITEM_MAP.clear()
        self._TV_FOLDERS_ITEM_MAP[0] = folder_item
        folder_item.removeRows(0, folder_item.rowCount())

    def _remove_search_tree_view(self):
        if 'search' in self._TV_FOLDERS_ITEM_MAP:
            root_tree_item = self._dirs_list_model.invisibleRootItem()
            root_tree_item.removeRow(0)
            self._TV_FOLDERS_ITEM_MAP.pop('search')

    def is_watcher_running(self):
        return self._is_watcher_running
