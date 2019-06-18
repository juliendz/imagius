package image

import (
	"bufio"
	"bytes"
	"encoding/base64"
	"image/jpeg"
	"image/png"
	"imagius/pkg/utils"
	"os"
	"path/filepath"

	"github.com/disintegration/imaging"
	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
	log "github.com/sirupsen/logrus"
)

type ImgManager struct {
	Store ImgStore
}

var ImgMgr *ImgManager

//Not thread safe
func GetImgManager(db *sqlx.DB) *ImgManager {

	if ImgMgr == nil {
		ImgMgr = &ImgManager{ImgStore{db}}
	}
	return ImgMgr
}

func (mgr ImgManager) ProcessImage(file os.FileInfo, parentPath string, dirId string, last_check_ts int64) error {

	abspath := filepath.Join(parentPath, file.Name())

	imgMeta, err := mgr.Store.Get(abspath)
	if err != nil {
		log.Errorf("%v+", err)
		return err
	}

	if imgMeta.ID == 0 {

		log.Info("Generating thumbnail")
		thumbB64, err := mgr.GenerateThumbBase64(abspath)
		if err != nil {
			log.Errorf("%s", err)
			return err
		}

		_, err = mgr.Store.Add(file, dirId, abspath, thumbB64, last_check_ts)
		if err != nil {
			log.Errorf("%v ", err)
			return err
		}

	} else {

		mtime := utils.GetModifiedTime(abspath)
		imgMeta.LastCheck = last_check_ts

		if mtime.Unix() > imgMeta.Mtime {

			//Renegrate the thumb and update it
			thumbB64, err := mgr.GenerateThumbBase64(abspath)
			if err != nil {
				return err
			}
			imgMeta.Thumbnail = thumbB64
			imgMeta.Mtime = mtime.Unix()

			err = mgr.Store.Update(imgMeta)
			if err != nil {
				log.Errorf("%v ", err)
				return err
			}

		} else {

			err = mgr.Store.UpdateLastCheck(imgMeta)
			if err != nil {
				log.Errorf("%v ", err)
				return err
			}
		}

	}

	return nil
}

func (mgr ImgManager) GenerateThumbBase64(abspath string) (string, error) {

	thumbBytes, err := mgr.GenerateThumb(abspath)
	if err != nil {
		return "", errors.Wrap(err, "ImgManager.GenerateThumbBase64")
	}

	encoded := base64.StdEncoding.EncodeToString(thumbBytes)
	return encoded, nil

}

func (mgr ImgManager) GenerateThumb(abspath string) ([]byte, error) {

	img, err := imaging.Open(abspath)
	if err != nil {
		return nil, err
	}

	thumb := imaging.Resize(img, 256, 0, imaging.Lanczos)

	var buffer bytes.Buffer
	bufferWriter := bufio.NewWriter(&buffer)

	ext := filepath.Ext(abspath)
	switch ext {
	case ".jpeg":
	case ".jpg":
		err := jpeg.Encode(bufferWriter, thumb, nil)
		if err != nil {
			return nil, errors.Wrap(err, "ImgManager.GenerateThumb")
		}
		break
	case ".png":
		err := png.Encode(bufferWriter, thumb)
		if err != nil {
			return nil, errors.Wrap(err, "ImgManager.GenerateThumb")
		}
		break
	default:
		return nil, errors.Wrap(err, "ImgManager.GenerateThumb: Unsupported format")
	}

	bufferWriter.Flush()

	return buffer.Bytes(), nil
}
