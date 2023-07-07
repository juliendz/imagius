using Avalonia.Controls;
using Avalonia.Media.Imaging;
using Imagius.Models;
using Imagius.Services;
using Imagius.ViewModels;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace Imagius.Views {
    public partial class MainWindow : Window {
        public MainWindow() {
            InitializeComponent();

            this.Opened += MainWindow_Opened;
        }

        private async void MainWindow_Opened(object? sender, System.EventArgs e) {
            var vm = new MainWindowViewModel();
            //vm.Thumbs = await vm.GetThumbsAsync();
            DataContext = vm;

            var metaWatcher = new MetaDataWatcher();
            metaWatcher.Watch();

        }


    }
}