using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading.Tasks;


namespace Imagius.Utils {
    public class Filesystem {
        public static long GetDirectorySize(string abspath) {
            var rootPath = abspath;
            long totalSize = 0;
            List<string> files = new List<string>(Directory.EnumerateFiles(rootPath));
            foreach(var file in files) {
                totalSize += new FileInfo(file).Length;
            }
            return totalSize;
        }

        public static bool IsDirectory(string absPath) {
            FileAttributes attr = File.GetAttributes(absPath);
            if (attr.HasFlag(FileAttributes.Directory))
                return true;
            return false;
        }
    }
}
