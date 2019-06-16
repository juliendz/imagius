package utils

import (
	"imagius/pkg/utils"
	"testing"
	"path/filepath"
	"fmt"
	"os"
)

func Test_GetModifiedTime(t *testing.T) {

	mtime := utils.GetModifiedTime(filepath.FromSlash("D:/Files/Dropbox/Pictures/Rose Byrne"))
	fmt.Fprintln(os.Stdout, mtime)
	if mtime.IsZero() {
		t.Errorf("Test failed: %+v", mtime)
	}
}