using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius {

   public enum MetaNodeType { Directory, Image }
   public enum SortMode { CreationTime, RecentChanges, Name, Size }

    public static class Constants {

        public const string AppName = "Imagius";
        public const string DbName = "meta";

        public const string ThumbnailDirectory = ".imagius";
        public const int ThumbnailHeight = 256;
    }
}

