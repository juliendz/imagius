package pkg

import (
	"imagius/pkg/dir"
	"imagius/pkg/utils"
	"path/filepath"
	"time"

	"golang.org/x/net/websocket"

	log "github.com/sirupsen/logrus"
)

func ScanDirs(ws *websocket.Conn) error {

	log.Info("Beginning scanning of dirs")

	lastCheckTs := time.Now().Unix()
	// websocket.Message.Send(ws, strconv.FormatInt(lastCheckTs, 10))

	//Get the list of all folders to scan
	FoldersToScan := []string{filepath.FromSlash("C:/Users/Julien/Downloads/test")}

	db, err := utils.OpenDB()
	if err != nil {
		panic(err)
	}
	defer db.Close()

	dirMgr := dir.GetDirManager(db)

	//Begin the scan
	for _, dir := range FoldersToScan {
		dirMgr.Scan(dir, lastCheckTs)
	}

	//Prune the img_dir table
	_, err = dirMgr.Store.Prune(lastCheckTs)
	if err != nil {
		log.Errorf("%v+", err)
		panic(err)
	}

	log.Info("End of scanning of dirs")

	return nil
}
