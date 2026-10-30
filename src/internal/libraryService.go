package internal

type LibraryService struct {
	db *DB
}

func NewLibraryService(db *DB) *LibraryService {
	return &LibraryService{
		db: db,
	}
}

func (g *LibraryService) GetDirs() []ScanDir {
	return g.db.GetScanDirs()
}
