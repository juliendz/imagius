package utils

import(
	"github.com/rs/xid"
)

func GenerateGUID() string{
	guid := xid.New()
	return guid.String()
}