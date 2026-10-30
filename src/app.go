package main

import (
	"context"

	"julien/imagius-go/internal"

	"github.com/wailsapp/wails/v3/pkg/application"
)

type AppService struct {
	dataDir string
	db      *internal.DB
}

func NewAppService(dataDir string, db *internal.DB) *AppService {
	return &AppService{
		dataDir: dataDir,
		db:      db,
	}
}

func (c *AppService) ServiceStartup(ctx context.Context, options application.ServiceOptions) error {

	scanner := internal.NewScanner(c.dataDir)
	scanner.ScanDirs(c.db)

	return nil
}
