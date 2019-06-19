package dir

import (
	"fmt"
	"imagius/pkg/dir"
	"imagius/pkg/utils"
	"os"
	"testing"
)

func Test_GetWatched(t *testing.T) {

	db, err := utils.OpenDB()
	if err != nil {
		panic(err)
	}
	defer db.Close()

	dirMgr := dir.GetDirManager(db)

	dirs, err := dirMgr.Store.GetWatched()
	fmt.Fprintf(os.Stdout, "%v+", dirs)

	if err != nil {
		t.Errorf("Test failed: %+v", err)
	}
}
