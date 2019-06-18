package image

import (
	"fmt"
	"imagius/pkg/image"
	"os"
	"path/filepath"
	"testing"
)

func Test_GenerateThumbBase64(t *testing.T) {

	mgr := image.GetImgManager(nil)

	b64, err := mgr.GenerateThumbBase64(filepath.FromSlash("C:/Users/Julien/Downloads/test/a.jpg"))
	fmt.Println(b64)
	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}
}

func Test_GenerateThumb(t *testing.T) {

	mgr := image.GetImgManager(nil)

	bytes, err := mgr.GenerateThumb(filepath.FromSlash("C:/Users/Julien/Downloads/test/b.png"))

	ofile, err := os.Create(filepath.FromSlash("C:/Users/Julien/Downloads/test/thumb.png"))
	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}

	defer ofile.Close()

	_, err = ofile.Write(bytes)

	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}
}
