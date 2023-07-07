using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius.Utils {
    public class Format {
        public static string FormatSize(int sizeBytes, string suffix="B") {
            foreach(var unit in new string[] { "", "Ki", "Mi" }) {
                if (Math.Abs(sizeBytes) < 1024.0) {
                    return string.Format("{0} {1}{2}", sizeBytes.ToString("000"), unit, suffix);
                }
                sizeBytes /= 1024;
            }
            return string.Format("{0} {1}{2}", sizeBytes, "Gi", suffix);
        }
    }
}
