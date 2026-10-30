package internal

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"gorm.io/gorm"
)

type Scanner struct {
	scanTime      time.Time
	filterExt     map[string]bool
	thumbCacheDir string
}

func NewScanner(appDataDir string) *Scanner {
	thumbsDir := filepath.Join(appDataDir, "thumbs")
	if !DirExists(thumbsDir) {
		os.Mkdir(thumbsDir, 0755)
	}
	return &Scanner{
		scanTime: time.Now(),
		filterExt: map[string]bool{
			".jpg":  true,
			".jpeg": true,
			".png":  true,
		},
		thumbCacheDir: thumbsDir,
	}
}

func (s *Scanner) ScanDirs(db *DB) {

	watchedDirs := db.GetWatchedDirs()
	watchedDirs = []Dir{
		Dir{Model: gorm.Model{ID: 0}, AbsPath: "/home/julien/Downloads/imagius-test/", Name: "imagius-test"},
	}

	db.BeginTx()
	for _, dir := range watchedDirs {
		s.ScanDir(db, dir.ID, dir.AbsPath, dir.Name)
	}
	db.CommitTx()
}

func (s *Scanner) ScanDir(db *DB, parentId uint, absPath string, dirName string) {
	isNewOrModified := false
	if !DirExists(absPath) {
		return
	}

	mtime := DirModTime(absPath)
	scanDir, _ := db.GetScanDir(absPath)
	if scanDir.ID <= 0 {
		scanDir, _ = db.InsertDir(parentId, absPath, dirName, s.scanTime)
		isNewOrModified = true

	} else {
		db.UpdateDirScanTime(scanDir.ID, s.scanTime)
		if scanDir.UpdatedAt.IsZero() || mtime.After(scanDir.UpdatedAt) {
			log.Printf("Folder(%d):(%s) has changed since last scan.", scanDir.ID, scanDir.AbsPath)
			isNewOrModified = true
		}
	}

	thumbDirPath := filepath.Join(s.thumbCacheDir, UintToStr(scanDir.ID))
	if !DirExists(thumbDirPath) {
		os.Mkdir(thumbDirPath, 0755)
	}

	entries, err := os.ReadDir(absPath)
	if err != nil {
		panic(err)
	}

	hasNewImages := false
	imgSerial := db.GetNextImgSerial(scanDir.ID)
	for _, entry := range entries {
		if entry.IsDir() {
			//directory

			fullPath := filepath.Join(absPath, entry.Name())
			log.Printf("Found directory:(%s)", fullPath)
			s.ScanDir(db, scanDir.ID, fullPath, entry.Name())

		} else {
			//image

			ext := filepath.Ext(entry.Name())
			if !s.filterExt[ext] {
				continue
			}

			entryInfo, _ := entry.Info()
			fullPath := filepath.Join(absPath, entry.Name())
			scanImage, _ := db.GetScanImg(fullPath)
			if scanImage.ID > 0 {
				//image exists

				imgMtime := entryInfo.ModTime()
				thumbPath := filepath.Join(thumbDirPath, filepath.Base(scanImage.AbsPath))
				log.Printf("Found existing Image:(%s), thumb:(%s)", fullPath, thumbPath)
				if imgMtime.After(scanImage.UpdatedAt) {
					GenerateThumb(scanImage.AbsPath, thumbPath)
					db.UpdateImgThumb(scanImage.ID, thumbPath, s.scanTime)

				} else {

					if _, err := os.Stat(thumbPath); os.IsNotExist(err) {
						GenerateThumb(scanImage.AbsPath, thumbPath)
					}
					db.UpdateImgScanTime(scanImage.ID, s.scanTime)
				}

			} else {
				//new image to add
				log.Printf("Found new Image:(%s)", fullPath)
				thumbPath := filepath.Join(thumbDirPath, filepath.Base(fullPath))
				newImage, _ := db.InsertImg(scanDir.ID, fullPath, entry.Name(), s.scanTime, imgSerial, thumbPath)
				log.Print("thumbpath:", thumbPath, " Abspath:", newImage.AbsPath)
				GenerateThumb(newImage.AbsPath, thumbPath)
				imgSerial++
				hasNewImages = true
			}
		}
	}

	//Partial commit
	db.db.SavePoint(fmt.Sprintf("svpt%d", scanDir.ID))

	if isNewOrModified {
		imgDelCount := db.PruneScanImg(scanDir.ID, s.scanTime)

		imgCount := db.GetScanDirImgCount(scanDir.ID)
		log.Printf("Pruned %d old ScanImg for ParentID %d, remaining images: %d", imgDelCount, scanDir.ID, imgCount)
		db.UpdateScanDirImgCount(scanDir.ID, imgCount)
		if hasNewImages || imgDelCount > 0 {
			//TODO: Send event for new or modified images
		}
		if imgCount > 0 {
			db.UpdateDirModifiedTime(scanDir.ID, mtime)
		} else {
			db.DeleteScanDir(scanDir.ID)
			//TODO: Send event for deleted directory
		}
	}

	//Delete any cached thumbnails for soft deleted images
	prunedImgs := db.GetSoftDeletedScanImg()
	for _, img := range prunedImgs {
		log.Printf("Deleting cached thumb: %s", img.ThumbPath)
		os.Remove(img.ThumbPath)
	}
	//Remove the soft deleted entry for the image
	db.DeleteSoftDeletedScanImg()

}
