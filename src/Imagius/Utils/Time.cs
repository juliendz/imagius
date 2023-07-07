using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius.Utils {
    public static class Time {
        public static long DateTimeToUnixTimestamp(DateTime dt) {
            DateTimeOffset dto = new DateTimeOffset(dt.ToUniversalTime());
            return dto.ToUnixTimeSeconds();
        }

        public static long UnixTimeNow() {
            DateTimeOffset dto = new DateTimeOffset(DateTime.UtcNow);
            return dto.ToUnixTimeSeconds();
        }
    }
}
