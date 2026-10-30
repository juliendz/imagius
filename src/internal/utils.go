package internal

import (
	"errors"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"time"

	_ "image/gif"
	_ "image/jpeg"
	_ "image/png"

	_ "golang.org/x/image/webp"

	"github.com/disintegration/imaging"
)

func InitDataDir() string {
	baseDir, err := os.UserConfigDir()
	if err != nil {
		log.Fatalf("Failed to get user config directory: %v", err)
	}

	// 2. Append your application's unique folder name
	appDir := filepath.Join(baseDir, APP_NAME)

	// 3. Ensure the folder exists before using it
	if err := os.MkdirAll(appDir, 0755); err != nil {
		log.Fatalf("Failed to create app directory: %v", err)
	}

	return appDir
}

func DirExists(path string) bool {
	info, err := os.Stat(path)
	if err == nil {
		return info.IsDir()
	}
	if errors.Is(err, os.ErrNotExist) {
		return false
	}
	return false
}

func DirModTime(path string) time.Time {
	dirInfo, err := os.Stat(path)
	if err != nil {
		log.Fatalf("Error reading directory metadata: %v", err)
	}

	return dirInfo.ModTime()
}

func GenerateThumb(path string, saveTo string) {
	src, err := imaging.Open(path)
	if err != nil {
		log.Fatalf("failed to open image: %v", err)
	}

	thumbnail := imaging.Thumbnail(src, 256, 256, imaging.Lanczos)

	// ext := filepath.Ext(path)
	log.Printf("Saving thumbnail to: %s", saveTo)
	err = imaging.Save(thumbnail, saveTo)
	if err != nil {
		log.Fatalf("failed to save thumbnail: %v", err)
	}
}

func UintToStr(ID uint) string {
	return strconv.FormatUint(uint64(ID), 10)
}
