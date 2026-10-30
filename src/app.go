package main

import (
	"context"
	"log"

	"julien/imagius-go/internal"

	"github.com/wailsapp/wails/v3/pkg/application"
)

type AppService struct{}

func (c *AppService) ServiceStartup(ctx context.Context, options application.ServiceOptions) error {
	dataDir := internal.InitDataDir()
	log.Printf("App Data Dir: %s\n", dataDir)

	db := internal.NewDB(ctx)
	db.InitDB(dataDir)

	scanner := internal.NewScanner(dataDir)
	scanner.ScanDirs(db)

	return nil
}
