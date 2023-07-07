using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Enumeration;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using Imagius.Utils;
using static System.Net.Mime.MediaTypeNames;

namespace Imagius.Services {

    public class MetaDataWatcher {

        public MetaDataService service { get; set; }
        private static readonly NLog.Logger logger = NLog.LogManager.GetCurrentClassLogger();

        private long integrityTimestamp;
        private string[] imgExtFilter;

        public MetaDataWatcher() {
            imgExtFilter = new string[] { "*.jpg", "*.jpeg" };

            service = new MetaDataService();
        }

        public void Watch() {
            var startTime = Time.UnixTimeNow();
            integrityTimestamp = startTime;

            logger.Info("Watch all started");

            service.dbmgr.Open();

            this.ScanDirs();

            var elapsed = Time.UnixTimeNow() - startTime;
            var suffix = "seconds";
            if(elapsed > 60) {
                elapsed /= 60;
                suffix = "minutes";
            }
            logger.Info("Watch all completed in {0} {1}", elapsed, suffix);

            service.dbmgr.Close();
        }

        private void ScanDirs() {
            //var watchedFoldersDt = service.GetWatchedDirectories();
            var watchedDirs = new List<Dictionary<string, object?>>();
            watchedDirs.Add(new Dictionary<string, object?>() {
                        { "id", 0L },
                        { "abspath", "D:\\imagius-test" },
                        { "name", "imagius-test" },
            });

            service.dbmgr.BeginTransaction();

            foreach(var watchedDir in watchedDirs) {
                this.ScanDir((long)watchedDir["id"], (string)watchedDir["abspath"], (string)watchedDir["name"]);
            }

            service.dbmgr.CommitTransaction();

            logger.Info("Folder scan completed");

        }

        private void ScanDir(long parentId, string absPath, string dirName) {

            bool isNewOrModified = false;
            if (!Filesystem.IsDirectory(absPath)) {
                return;
            }
            long mtime = Time.DateTimeToUnixTimestamp(File.GetLastWriteTime(absPath));
            long dirId = 0;
            var dirInfo = service.GetMetaNode(MetaNodeType.Directory, absPath);
            if (dirInfo.Count == 0) {
                dirId = service.AddMetaDir(parentId, absPath, dirName, integrityTimestamp);
                dirInfo = service.GetMetaNode(MetaNodeType.Directory, absPath);
                isNewOrModified = true;
            } else {
                dirId = (long)dirInfo["id"];
                service.UpdateMetaDirIntegrityCheck(dirId, integrityTimestamp);
                if((dirInfo["mtime"] == null) || (mtime > (long)dirInfo["mtime"])) {
                    logger.Info("Dir{0}:{1} has changed since last scan.", dirId, (string)dirInfo["abspath"]);
                    isNewOrModified = true;
                }
            }

            IEnumerable<string> metaNodes;
            if (isNewOrModified) {
                var metaNodesFiles = Directory.EnumerateFiles(absPath, "*", SearchOption.TopDirectoryOnly)
                    .Where(fileName => imgExtFilter.Any(ext => FileSystemName.MatchesSimpleExpression(ext, fileName))).ToList();
                var metaNodesDirs = Directory.EnumerateDirectories(absPath, "*", SearchOption.TopDirectoryOnly).ToList();
                metaNodesFiles.AddRange(metaNodesDirs);
                metaNodes = metaNodesFiles;
            } else {
                metaNodes = Directory.EnumerateDirectories(absPath, "*", SearchOption.TopDirectoryOnly);
            }

            var hasNewImage = false;
            var metaImgOrder = service.GetMetaImageNextOrder(dirId);
            foreach(var metaNodePath in metaNodes) {

                if(Filesystem.IsDirectory(metaNodePath)) {

                    if(new DirectoryInfo(metaNodePath).Name == ".imagius") {
                        continue;
                    }

                    logger.Info("Direcory found: {0}", metaNodePath);
                    ScanDir(dirId, metaNodePath, Path.GetDirectoryName(metaNodePath));

                } else {

                    var imgInfo = service.GetMetaNode(MetaNodeType.Image, metaNodePath);
                    if(imgInfo.Count > 0) {
                        logger.Info("Found image: {0}", metaNodePath);
                        var lastMTime = Time.DateTimeToUnixTimestamp(File.GetLastWriteTime(metaNodePath)); 
                        if(lastMTime > (long)imgInfo["mtime"]) {
                            service.UpdateMetaImage((long)imgInfo["id"], metaNodePath, lastMTime, integrityTimestamp);
                        } else {
                            service.UpdateMetaImage((long)imgInfo["id"], integrityTimestamp);
                        }

                    //new image to add
                    } else {
                        logger.Info("Found new image: {0}", metaNodePath);
                        service.AddMetaImage(dirId, metaNodePath, Path.GetFileName(metaNodePath), integrityTimestamp, metaImgOrder);
                        hasNewImage = true;
                        metaImgOrder++;
                    }

                }
            }


            if (isNewOrModified) {
                var imgDelCount = service.DeleteStaleMetaImages(dirId, integrityTimestamp);
                var imgCount = service.GetMetaNodeChildCount(dirId);
                service.UpdateMetaDirImgCount(dirId, imgCount);
                if(hasNewImage || imgDelCount > 0) {
                    //TODO: Emit notify
                } 

                if(imgCount > 0) {
                    service.UpdateMetaDirMtime(dirId, mtime);
                } else {
                    service.DeleteMetaDir(dirId);
                }
            }
        }

    }
}
