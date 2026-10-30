package internal

import (
	"context"
	"testing"
)

func TestScanDirs(t *testing.T) {
	ctx := context.Background()
	db := NewDB(ctx)

	appDataDir := InitDataDir()
	db.InitDB(appDataDir)

	scanner := NewScanner(appDataDir)
	scanner.ScanDirs(db)

}
