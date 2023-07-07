using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius.Models
{
    public class Thumb
    {
        public string Path { get; set; } = string.Empty;
        public int Order { get; set; } = 0;

        public Thumb(string path, int order)
        {
            Path = path;
            Order = order;
        }
    }
}
