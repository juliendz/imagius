using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Imagius.Services;
using Imagius.ViewModels;
using Imagius.Views;
using NLog;
using System.IO;

namespace Imagius {
    public partial class App : Application {
        public override void Initialize() {
            AvaloniaXamlLoader.Load(this);
        }

        public override void OnFrameworkInitializationCompleted() {
            if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop) {

                //Configure logging
                var config = new NLog.Config.LoggingConfiguration();
                var logfile = new NLog.Targets.FileTarget("logfile") { FileName = "C:\\Users\\Julien\\AppData\\Local\\Imagius\\notesalot.log" };
                config.AddRule(LogLevel.Debug, LogLevel.Fatal, logfile);
                NLog.LogManager.Configuration = config;

                //Init db
                var dbPath = Settings.GetDbPath();
                if (!File.Exists(dbPath)) {
                    Settings.InitDatabase(dbPath);
                }

                desktop.MainWindow = new MainWindow();
            }

            base.OnFrameworkInitializationCompleted();
        }
    }
}