package main

import (
	"imagius/pkg"
	"os"

	log "github.com/sirupsen/logrus"
)

func init() {

	log.SetFormatter(&log.TextFormatter{})
	log.SetOutput(os.Stdout)
	logLevel := "DEBUG"
	switch logLevel {
	case "DEBUG":
		log.SetLevel(log.DebugLevel)
	case "WARN":
		log.SetLevel(log.WarnLevel)
	}

}

func main() {

	// e := echo.new()

	// e.use(middleware.logger())
	// e.use(middleware.recover())

	// e.logger.fatal(e.start(":1323"))
	log.Info("Beginning scanning of dirs")
	pkg.ScanDirs()
	log.Info("End of scanning of dirs")

}
