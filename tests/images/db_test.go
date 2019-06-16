package images

import (
	"imagius/pkg/images"
	"testing"
	"path/filepath"
	"fmt"
	"os"
)

func Test_images_db_GetDir(t *testing.T) {

	dirMeta, err := images.GetDirDB(filepath.FromSlash("D:/Files/Dropbox/Pictures/Rose Bysrne"))
	fmt.Fprintln(os.Stdout, dirMeta)
	fmt.Fprintln(os.Stdout, err)

	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}
	if dirMeta.Name != "Rose Byrne" {
		t.Errorf("Error %s", err)
	}
}

func Test_AddDirDB(t *testing.T) {

	dirId, err := images.AddDirDB(filepath.FromSlash("D:/Files/Dropbox/Pictures/Furniture"))
	fmt.Fprintln(os.Stdout, err)
	fmt.Fprintln(os.Stdout, dirId)

	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}
}