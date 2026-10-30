package internal

import "log"

type LibraryService struct {
	db *DB
}

func NewLibraryService(db *DB) *LibraryService {
	return &LibraryService{
		db: db,
	}
}

func (g *LibraryService) GetDirs() []ScanDir {
	log.Printf("Getting scanned directories")
	return g.db.GetScanDirs()
}

func (g *LibraryService) GetImages() []GetScanImgsRow {
	log.Printf("Getting scanned images")
	return g.db.GetScanImgs()
}
