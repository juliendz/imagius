package main

import (
	"imagius/pkg"
	"net/http"
	"os"
	"strconv"
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

	var counter int
	for {
		log.Infof("LOOP %d", counter)
		counter++
		var op pkg.Operation
		err = c.ReadJSON(&op)
		if err != nil {
			log.Error(err)
		}

		switch op.Command {

		case "START_SCAN":
			// pkg.ScanDirs(ws)
			c.WriteJSON(time.Now())
			log.Info("STARTSCAN DONE")
			break

		case "GET_WATCHED":
			log.Info("GET_WATCHED")

			dirs, err := pkg.GetWatchedDirs()
			if err != nil {
				c.WriteJSON(err)
			}

			resOp := pkg.Operation{
				Command: "DATA_WATCHED",
				Payload: dirs,
			}
			c.WriteJSON(resOp)
			break

		case "ADD_WATCHED":
			log.Info("ADD_WATCHED")
			err := pkg.AddWatchedDir(op.Payload.(string))
			if err != nil {
				c.WriteJSON(err)
			}
			dirs, err := pkg.GetWatchedDirs()
			if err != nil {
				c.WriteJSON(err)
			}

			resOp := pkg.Operation{
				Command: "DATA_WATCHED",
				Payload: dirs,
			}
			c.WriteJSON(resOp)
			break

		case "DEL_WATCHED":
			log.Info("DEL_WATCHED")
			removeDirID, _ := strconv.ParseInt(op.Payload.(string), 10, 64)
			err := pkg.DeleteWatchedDir(removeDirID)
			if err != nil {
				c.WriteJSON(err)
			}
			dirs, err := pkg.GetWatchedDirs()
			if err != nil {
				c.WriteJSON(err)
			}

			resOp := pkg.Operation{
				Command: "DATA_WATCHED",
				Payload: dirs,
			}
			c.WriteJSON(resOp)
			break

		default:
			break
		}
	}
}
