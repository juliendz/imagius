package utils
import (
	"os"
	"runtime"
	"path/filepath"
	_ "github.com/mattn/go-sqlite3"
    "github.com/jmoiron/sqlx"
)

func OpenDB() (*sqlx.DB, error) {
	var dbPath string

	if runtime.GOOS == "windows" {
		userHomePath := os.Getenv("HOMEDRIVE") + os.Getenv("HOMEPATH")
		dbPath = userHomePath + filepath.FromSlash("/AppData/Local/Imagius/app.db")

	} else if runtime.GOOS == "linux" {
		//TODO:
		//userHomePath := os.Getenv("XDG_CONFIG_HOME")
	}

	db, err := sqlx.Open("sqlite3", dbPath)
	return db, err
}