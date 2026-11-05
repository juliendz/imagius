package main

import (
	"julien/imagius-go/internal"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/wailsapp/wails/v3/pkg/application"
)

func GinMiddleware(ginEngine *gin.Engine) application.Middleware {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

			log.Printf("Request URL: %s\n", r.URL.Path)
			// Let Wails handle the `/wails` route
			if strings.HasPrefix(r.URL.Path, "/wails") {
				log.Printf("Handling Wails URL: %s\n", r.URL.Path)
				next.ServeHTTP(w, r)
				return
			}

			if strings.HasPrefix(r.URL.Path, "/thumbs") || strings.HasPrefix(r.URL.Path, "/img") {
				ginEngine.ServeHTTP(w, r)
				return
			}

			application.AssetFileServerFS(assets).ServeHTTP(w, r)

		})
	}
}

func NewGinEngine(thumbDir string, db *internal.DB) *gin.Engine {
	// Create a new Gin router

	ginEngine := gin.New() // Using New() instead of Default() to add custom middleware

	// Add middlewares
	ginEngine.Use(gin.Recovery())

	log.Printf("Serving thumbnails from: %s\n", thumbDir)
	ginEngine.Static("/thumbs", thumbDir)

	// Define your merged filesystem
	// mergedStaticFS := &MultiDirFS{
	// 	Dirs: []string{
	// 		"/home/julien/Downloads/imagius-test",
	// 	},
	// }

	// ginEngine.StaticFS("/img", mergedStaticFS)

	// ginEngine.GET("/", func(c *gin.Context) {
	// 	// Serve your main page
	// })

	// Route for serving images by ID for the slideshow view
	ginEngine.GET("/img", func(c *gin.Context) {
		ID, _ := strconv.Atoi(c.Query("id"))
		img := db.GetScanImgByID(ID)
		c.File(img.AbsPath)
	})

	return ginEngine
}

// MultiDirFS implements http.FileSystem to search multiple directories
type MultiDirFS struct {
	Dirs []string
}

// Open tries to find the file in each directory sequentially
func (m *MultiDirFS) Open(name string) (http.File, error) {
	for _, dir := range m.Dirs {
		fullPath := filepath.Join(dir, name)

		// Check if file exists before trying to open it
		if _, err := os.Stat(fullPath); err == nil {
			// Use http.Dir to open the file properly
			return http.Dir(dir).Open(name)
		}
	}
	return nil, os.ErrNotExist
}
