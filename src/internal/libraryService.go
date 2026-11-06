package internal

import (
	"context"
	"log"

	"github.com/wailsapp/wails/v3/pkg/application"
)

type LibraryService struct {
	app *application.App
	db  *DB
}

func NewLibraryService(db *DB) *LibraryService {
	return &LibraryService{
		db: db,
	}
}

func (s *LibraryService) ServiceStartup(ctx context.Context, options application.ServiceOptions) error {
	s.app = application.Get()
	return nil
}

func (s *LibraryService) ServiceShutdown() {}

type DirListItem struct {
	ID             uint
	Name           string
	ThumbViewIndex int
}

type ThumbRow struct {
	Key      int
	ID       uint
	Type     string
	ParentID uint
	Name     string
	Thumbs   []*ThumbRowItem
}

type ThumbRowItem struct {
	Key       int
	ID        uint
	ParentID  uint
	Name      string
	SerialNo  int64
	ThumbPath string
}

type Library struct {
	Dirs   []*DirListItem
	Thumbs []*ThumbRow
}

func (g *LibraryService) GetLibrary() *Library {

	log.Printf("Getting library")
	imgs := g.db.GetScanImgs()

	dirs := []*DirListItem{}
	rows := []*ThumbRow{}
	key := 1
	var currThumbow *ThumbRow
	for index, img := range imgs {
		if index == 0 || (img.ParentID != imgs[index-1].ParentID) {

			//Create a new directory list item for the current scan directory
			log.Printf("Creating scanned directory")
			dirListItem := DirListItem{
				ID:   img.ParentID,
				Name: img.ParentName,
			}

			log.Printf("Creating new header row for parent ID %d", img.ParentID)
			//Header row
			headerRow := ThumbRow{
				Key:      key,
				ID:       img.ParentID,
				Type:     "header-row",
				Name:     img.ParentName,
				ParentID: 0,
			}
			rows = append(rows, &headerRow)
			key++

			//Assign the index of the header row added above as the thumb view index for the current directory list item
			dirListItem.ThumbViewIndex = len(rows) - 1
			dirs = append(dirs, &dirListItem)

			//Thumb Row after the current header
			currThumbow = &ThumbRow{
				Key:      key,
				Type:     "thumb-row",
				ParentID: img.ParentID,
				Thumbs:   []*ThumbRowItem{},
			}
			rows = append(rows, currThumbow)
			key++
		}

		//Append the current image to the current thumb row
		currThumbow.Thumbs = append(currThumbow.Thumbs, &ThumbRowItem{
			Key:       key,
			ID:        img.ID,
			ParentID:  img.ParentID,
			Name:      img.Name,
			SerialNo:  img.SerialNo,
			ThumbPath: img.ThumbPath,
		})
		key++
		log.Printf("Appended image %d to thumb row, current thumb count: %d", img.ID, len(currThumbow.Thumbs))

		//If the column limit is reached, create a new thumb row for the same parent ID
		// if (len(currThumbow.Thumbs) == colCount) && (index+1 < len(imgs)) && (img.ParentID == imgs[index+1].ParentID) {
		// 	log.Printf("Column limit reached, creating new thumb row")
		// 	currThumbow = &ThumbRow{
		// 		Key:      key,
		// 		ID:       img.ParentID,
		// 		Type:     "thumb-row",
		// 		Name:     img.ParentName,
		// 		ParentID: img.ParentID,
		// 		Thumbs:   []*ThumbRowItem{},
		// 	}
		// 	key++
		// 	rows = append(rows, currThumbow)
		// 	key++
		// }

	}

	for i := range rows {
		log.Printf("Row %d: Type=%s, ID=%d, Thumbs=%d", i, rows[i].Type, rows[i].ID, len(rows[i].Thumbs))
	}

	Library := &Library{
		Dirs:   dirs,
		Thumbs: rows,
	}
	return Library
}

func (g *LibraryService) GetImage(id int) ScanImg {
	return g.db.GetScanImgByID(id)
}

func (g *LibraryService) GetSlideShowImages(dirID int, sortBy string) []SlideshowImg {
	return g.db.GetScanImgsforSlideshow(dirID, sortBy)
}
