package main

import (
	"log"
	"net/http"
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

			if strings.HasPrefix(r.URL.Path, "/thumbs") {
				ginEngine.ServeHTTP(w, r)
				return
			}

			application.AssetFileServerFS(assets).ServeHTTP(w, r)

		})
	}
}

func NewGinEngine(thumbDir string) *gin.Engine {
	// Create a new Gin router

	ginEngine := gin.New() // Using New() instead of Default() to add custom middleware

	// Add middlewares
	ginEngine.Use(gin.Recovery())

	log.Printf("Serving thumbnails from: %s\n", thumbDir)
	ginEngine.Static("/thumbs", thumbDir)

	// ginEngine.GET("/", func(c *gin.Context) {
	// 	// Serve your main page
	// })

	// Define routes
	// ginEngine.GET("/", func(c *gin.Context) {
	// 	path := c.Query("p")
	// 	imageData, err := os.ReadFile(path)
	// 	if err != nil {
	// 		c.String(http.StatusNotFound, "Image not found")
	// 		return
	// 	}
	// 	ext := filepath.Ext(path)

	// 	// Set the appropriate Content-Type (e.g., image/jpeg, image/png)
	// 	contentType := "image/jpeg"
	// 	switch ext {
	// 	case ".jpg":
	// 		contentType = "image/jpeg"
	// 	case ".jpeg":
	// 		contentType = "image/jpeg"
	// 	case ".png":
	// 		contentType = "image/png"
	// 	case ".gif":
	// 		contentType = "image/gif"
	// 	}
	// 	c.Data(http.StatusOK, contentType, imageData)
	// 	// Serve your main page
	// })

	return ginEngine
}
