package main

import (
	"imagius/pkg"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/websocket"
	log "github.com/sirupsen/logrus"
)

var upgrader = websocket.Upgrader{}

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

	http.HandleFunc("/ws", wshandler)

	log.Info("Http server listening on :1323")
	log.Fatal(http.ListenAndServe(":1323", nil))
}

func wshandler(w http.ResponseWriter, r *http.Request) {

	upgrader.CheckOrigin = func(r *http.Request) bool {
		//TODO: check of accpetable origins
		//Ref: https://github.com/gorilla/websocket/issues/367
		return true
	}
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error(err)
		return
	}
	defer c.Close()

	var bytes []byte
	_, bytes, err = c.ReadMessage()
	if err != nil {
		log.Error(err)
	}

	msg := string(bytes)
	switch msg {
	case "STARTSCAN":
		// pkg.ScanDirs(ws)
		c.WriteJSON(time.Now())
		log.Info("STARTSCAN DONE")
		break

	case "GETWATCHED":
		log.Info("GETWATCHED")
		dirs, err := pkg.GetWatchedDirs()
		log.Info(dirs)
		if err != nil {
			c.WriteJSON(err)
		}
		c.WriteJSON(dirs)
		break

	default:
		break
	}
}
