package internal

import (
	"context"
	"database/sql"
	"log"
	"path/filepath"
	"time"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Dir struct {
	gorm.Model
	AbsPath  string
	Name     string
	ImgCount int64
}

type ScanDir struct {
	gorm.Model
	ParentId     uint
	AbsPath      string
	Name         string
	ImgCount     int64
	LastScanTime time.Time
	ModifiedTime time.Time
}

type ScanImg struct {
	gorm.Model
	ParentID     uint
	Parent       ScanDir `gorm:"constraint:OnDelete: CASCADE;"`
	AbsPath      string
	Name         string
	ThumbPath    string
	SerialNo     int64
	LastScanTime time.Time
}

type Setting struct {
	gorm.Model
	Key   string
	Value string
}

type DB struct {
	db   *gorm.DB
	ctxt context.Context
}

func NewDB(ctxt context.Context) *DB {
	return &DB{
		ctxt: ctxt,
	}
}

func (d *DB) BeginTx() {
	d.db = d.db.Begin()
}
func (d *DB) CommitTx() {
	d.db.Commit()
}

func (d *DB) RollbackTx() {
	d.db.Rollback()
}

func (d *DB) InitDB(dataDir string) (err error) {
	dbPath := filepath.Join(dataDir, APP_NAME+".db")
	log.Printf("Opening database: %s\n", dbPath)
	d.db, err = gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to open database : %v", err)
		return err
	}

	d.db.AutoMigrate(&Dir{}, &ScanDir{}, &ScanImg{}, &Setting{})
	log.Printf("Database initialized successfully")
	return nil
}

func (d *DB) GetWatchedDirs() []Dir {
	dirs, err := gorm.G[Dir](d.db).Find(d.ctxt)
	if err != nil {
		log.Printf("Failed to get watched dirs: %v", err)
	}
	return dirs
}

func (d *DB) GetScanDir(absPath string) (ScanDir, error) {
	dir, err := gorm.G[ScanDir](d.db).Where("abs_path = ?", absPath).First(d.ctxt)
	return dir, err
}

func (d *DB) GetScanDirs() []ScanDir {
	dirs, err := gorm.G[ScanDir](d.db).Order("modified_time DESC").Find(d.ctxt)
	if err != nil {
		log.Printf("Failed to get scan dirs: %v", err)
	}
	return dirs
}

func (d *DB) GetScanImg(absPath string) (ScanImg, error) {
	img, err := gorm.G[ScanImg](d.db).Where("abs_path = ?", absPath).First(d.ctxt)
	return img, err
}

type GetScanImgsRow struct {
	ID         uint
	ParentID   uint
	Name       string
	SerialNo   int64
	ThumbPath  string
	ParentName string
}

func (d *DB) GetScanImgs() []GetScanImgsRow {
	var imgs []GetScanImgsRow
	err := d.db.Model(&ScanImg{}).Select("scan_imgs.id, scan_imgs.parent_id, scan_imgs.name, scan_imgs.serial_no, scan_imgs.thumb_path, dir.name as parent_name").
		Joins("left join scan_dirs as dir on scan_imgs.parent_id = dir.id").
		Order("dir.modified_time desc, scan_imgs.name").
		Scan(&imgs)
	if err != nil {
		// log.Printf("Failed to get scan images: %v", err)
	}
	return imgs
}

func (d *DB) InsertDir(parentID uint, absPath string, name string, scanTime time.Time, mtime time.Time) (ScanDir, error) {
	sd := ScanDir{}
	sd.ParentId = parentID
	sd.AbsPath = absPath
	sd.Name = name
	sd.LastScanTime = scanTime
	sd.ModifiedTime = mtime
	err := gorm.G[ScanDir](d.db).Create(d.ctxt, &sd)
	return sd, err
}

func (d *DB) InsertImg(parentID uint, absPath string, name string, scanTime time.Time, serialNo int64, thumbPath string) (ScanImg, error) {
	si := ScanImg{}
	si.ParentID = parentID
	si.AbsPath = absPath
	si.Name = name
	si.LastScanTime = scanTime
	si.SerialNo = serialNo
	si.ThumbPath = thumbPath
	err := gorm.G[ScanImg](d.db).Create(d.ctxt, &si)
	return si, err
}

func (d *DB) UpdateDirScanTime(ID uint, scanTime time.Time) error {
	//UpdatedAt is automatically updated by gorm
	_, err := gorm.G[ScanDir](d.db).Where("id = ?", ID).Update(d.ctxt, "last_scan_time", scanTime)
	return err
}

func (d *DB) UpdateDirModifiedTime(ID uint, mtime time.Time) error {
	_, err := gorm.G[ScanDir](d.db).Where("id = ?", ID).Update(d.ctxt, "modified_time", mtime)
	return err
}

func (d *DB) UpdateImgThumb(ID uint, thumbPath string, scanTime time.Time) error {
	//UpdatedAt is automatically updated by gorm
	_, err := gorm.G[ScanImg](d.db).Where("id = ?", ID).Updates(d.ctxt, ScanImg{ThumbPath: thumbPath, LastScanTime: scanTime})
	return err
}

func (d *DB) UpdateImgScanTime(ID uint, scanTime time.Time) error {
	//UpdatedAt is automatically updated by gorm
	_, err := gorm.G[ScanImg](d.db).Where("id = ?", ID).Update(d.ctxt, "last_scan_time", scanTime)
	return err
}

func (d *DB) GetNextImgSerial(parentID uint) int64 {
	var maxSerial sql.NullInt64
	gorm.G[ScanImg](d.db).Where("parent_id = ?", parentID).Select("MAX(serial_no)").Scan(d.ctxt, &maxSerial)
	if maxSerial.Valid {
		return maxSerial.Int64 + 1
	}
	return 1
}

func (d *DB) PruneScanImg(parentID uint, scanTime time.Time) int {
	delCount, err := gorm.G[ScanImg](d.db).Where("parent_id = ? AND last_scan_time < ?", parentID, scanTime).Delete(d.ctxt)
	if err != nil {
		log.Printf("Failed to prune ScanImg for ParentID %d: %v", parentID, err)
	}
	return delCount
}

func (d *DB) GetScanDirImgCount(ID uint) int64 {
	count, _ := gorm.G[ScanImg](d.db).Where("parent_id = ?", ID).Count(d.ctxt, "id")
	return count
}

func (d *DB) UpdateScanDirImgCount(ID uint, count int64) {
	gorm.G[ScanDir](d.db).Where("id = ?", ID).Update(d.ctxt, "img_count", count)
}

func (d *DB) DeleteScanDir(ID uint) error {
	_, err := gorm.G[ScanDir](d.db).Where("id = ?", ID).Delete(d.ctxt)
	return err
}

func (d *DB) GetSoftDeletedScanImg() []*ScanImg {
	var softDeleted []*ScanImg
	d.db.Unscoped().Where("deleted_at IS NOT NULL").Find(&softDeleted)
	return softDeleted
}

func (d *DB) DeleteSoftDeletedScanImg() {
	d.db.Unscoped().Where("deleted_at IS NOT NULL").Delete(&ScanImg{})
}
