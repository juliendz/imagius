using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Imagius.Models;

namespace Imagius.ViewModels {
    public class MainWindowViewModel : ViewModelBase {
        public List<Thumb> Thumbs { get; set; }

        public MainWindowViewModel() {
        }

        public async Task<List<Thumb>> GetThumbsAsync() {
            var t = await Task<List<Thumb>>.Factory.StartNew(() => {
                var index = 0;
                var thumbs = new List<Thumb>();
                foreach (var file in Directory.EnumerateFiles("D:\\Media\\vcpc\\pc\\lingere-new")) {
                    if (file.EndsWith(".jpg")) {
                        var img = new Thumb(file, index);
                        thumbs.Add(img);
                        index++;

                        if (index == 24) {
                            break;
                        }
                    }
                }
                return thumbs;
            });
            return t;
        }
    }
}