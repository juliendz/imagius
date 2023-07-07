using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius.Services {
    public class Settings {
        public Settings() { }

        public static string GetDbPath() {
            var userAppDataDir = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            var appDataDir = Path.Combine(userAppDataDir, Constants.AppName);
            if (!Directory.Exists(appDataDir)){
                Directory.CreateDirectory(appDataDir);
            }
            return Path.Combine(appDataDir, Constants.DbName);
        }

        public static void InitDatabase(string dbPath) {
            DbMgr.InitDatabase(dbPath);
        }
    }
}
