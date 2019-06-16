package utils

import (
	"os"
	"time"
	"path/filepath"
)

func IsPathValid(path string) bool{
	if  _, err := os.Stat(path); err == nil{
		return true
	}
	return false
}

func GetModifiedTime(path string) time.Time {
	file, err := os.Stat(path) 
	if err != nil{
		return time.Time{}
	}

	return file.ModTime()
}

func IsSupportedImageFormat(file os.FileInfo) bool {
	if file.Mode().IsRegular(){
		switch filepath.Ext(file.Name()){
		case ".jpg": 
			return true
		case ".jpeg": 
			return true
		case ".png": 
			return true
		default: 
			return false
		}
	}
	return false
}