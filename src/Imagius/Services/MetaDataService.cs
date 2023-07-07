using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Threading.Tasks.Sources;
using System.IO;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Formats.Jpeg;
using Imagius.Utils;
using SixLabors.ImageSharp.Metadata.Profiles.Exif;
using Avalonia.Markup.Parsers.Nodes;

namespace Imagius.Services {
    public class MetaDataService {

        public DbMgr dbmgr { get; set; }
        private Settings settings;

        public MetaDataService() {
            settings = new Settings();
            dbmgr = new DbMgr(Settings.GetDbPath());
        }

        public DataTable GetWatchedDirectories() {
            var query = "SELECT * FROM scan_dirs;";
            dbmgr.Open();
            var dt = dbmgr.Select(query);
            dbmgr.Close();
            return dt;
        }

        public async Task<DataTable> GetMetaDirAsync(SortMode sortMode, bool reverseSort=false) {
            var predicate = string.Empty;
            if (sortMode == SortMode.Name) {
                if (reverseSort) {
                    predicate = "ORDER BY name DESC";
                }
            } else {
                predicate = "ORDER BY name ASC";
            }

            var query = "SELECT * FROM meta_nodes WHERE type_id = 1 ;" + predicate;
            await dbmgr.OpenAsync();
            var dt =await dbmgr.SelectAsync(query);
            await dbmgr.CloseAsync();
            return dt;
        }

        public async Task<DataTable> SearchMetaDirAsync(string searchTerm) {
            var query = "SELECT * FROM meta_nodes WHERE type_id = 1 AND name LIKE $name;";
            await dbmgr.OpenAsync();

            var param = new SqliteParameter[] {
                new SqliteParameter("$name", searchTerm)
            };
            var dt =await dbmgr.SelectAsync(query, param);
            await dbmgr.CloseAsync();
            return dt;
        }

        public async Task<DataTable> GetMetaDirAsync(long id) {
            var query = "SELECT * FROM meta_nodes WHERE type_id = 1 AND id = $id;";
            await dbmgr.OpenAsync();

            var param = new SqliteParameter[] {
                new SqliteParameter("$id", id)
            };
            var dt =await dbmgr.SelectAsync(query, param);
            await dbmgr.CloseAsync();
            return dt;
        }

        public async Task<DataTable> GetMetaDirAsync(string absPath) {
            var query = "SELECT * FROM meta_nodes WHERE type_id = 1 AND abspath = $abspath;";
            await dbmgr.OpenAsync();

            var param = new SqliteParameter[] {
                new SqliteParameter("$abspath", absPath)
            };
            var dt =await dbmgr.SelectAsync(query, param);
            await dbmgr.CloseAsync();
            return dt;
        }

        public long AddMetaDir(long parent_id, string absPath, string name, long integrityCheck) {
            var query = "INSERT INTO meta_nodes (parent_id, type_id, abspath, name, integrity_check) VALUES ($parent_id, 1, $abspath, $name, $intcheck)";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", parent_id),
                new SqliteParameter("$abspath", absPath),
                new SqliteParameter("$name", name),
                new SqliteParameter("$intcheck", integrityCheck),
            };
            var id = dbmgr.Insert(query, param);
            return id;
        }

        public long DeleteMetaDir(long id) {
            var query = "DELETE FROM meta_nodes WHERE id = $id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$id", id)
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public long UpdateMetaDirIntegrityCheck(long id, long integrityCheck) {
            var query = "UPDATE meta_nodes SET integrity_check = $intcheck WHERE id = $id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$intcheck", integrityCheck),
                new SqliteParameter("$id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public long UpdateMetaDirMtime(long id, long mtime) {
            var query = "UPDATE meta_nodes SET mtime = $mtime WHERE id = $id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$mtime", mtime),
                new SqliteParameter("$id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public long UpdateMetaDirImgCount(long id, long count) {
            var query = "UPDATE meta_nodes SET child_count = $count WHERE id = $id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$count", count),
                new SqliteParameter("$id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        private string GenerateThumbnail(string absPath, int thumbHeight) {
            var parentdir = Directory.GetParent(absPath);
            var thumbDir = string.Format("{0}/{1}", parentdir.FullName, Constants.ThumbnailDirectory);
            var thumbName = Path.GetFileNameWithoutExtension(absPath);
            var thumbPath = string.Format("{0}/{1}.jpg", thumbDir, thumbName);
            if (!Directory.Exists(thumbDir)){
                Directory.CreateDirectory(thumbDir);
            }
            using (Image img = Image.Load(absPath)) {
                img.Mutate(x => x.Resize(0, thumbHeight, KnownResamplers.Lanczos3));
                img.Save(thumbPath, new JpegEncoder());
            }
            return thumbPath;
        }

        public long AddMetaImage(long parent_id, string absPath, string name, long integrityCheck, long order) {

            var thumbPath = GenerateThumbnail(absPath, Constants.ThumbnailHeight);
            var mtime = Time.DateTimeToUnixTimestamp(File.GetLastWriteTime(thumbPath));

            var query = @"INSERT INTO meta_nodes (parent_id, type_id, abspath, thumb_abspath, name, mtime, integrity_check, 'order') 
                          VALUES ($parent_id, 2, $abspath, $thumb_abspath, $name, $mtime, $intcheck, $order)";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", parent_id),
                new SqliteParameter("$abspath", absPath),
                new SqliteParameter("$thumb_abspath", thumbPath),
                new SqliteParameter("$name", name),
                new SqliteParameter("$mtime", mtime),
                new SqliteParameter("$intcheck", integrityCheck),
                new SqliteParameter("$order", order),
            };
            return dbmgr.Insert(query, param);
        }

        public long UpdateMetaImage(long id, long integrityCheck) {

            var query = @"UPDATE meta_nodes SET integrity_check = $intcheck WHERE id = $id AND type_id = 2";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$intcheck", integrityCheck),
                new SqliteParameter("$id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public long UpdateMetaImage(long id, string absPath, long mtime, long integrityCheck) {

            var thumbPath = GenerateThumbnail(absPath, Constants.ThumbnailHeight);

            var query = @"UPDATE meta_nodes SET thumb_abspath=$thumb_abspath, mtime=$mtime, integrity_check=$intcheck WHERE id=$id AND type_id=2";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$thumb_abspath", thumbPath),
                new SqliteParameter("$mtime", mtime),
                new SqliteParameter("$intcheck", integrityCheck),
                new SqliteParameter("$id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public Dictionary<string, object?> GetMetaNode(MetaNodeType nodeType, string abspath) {
            var query = string.Empty;
            switch(nodeType) {
                case MetaNodeType.Directory:
                    query = "SELECT * FROM meta_nodes WHERE type_id=1 AND abspath=$abspath";
                    break;
                case MetaNodeType.Image:
                    query = "SELECT * FROM meta_nodes WHERE type_id=2 AND abspath=$abspath";
                    break;
            }
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$abspath", abspath),
            };
            var dt = dbmgr.Select(query, param);
            return DbTable.ToDictionarySingle(dt);
        }

        public DataTable GetMetaNode(MetaNodeType nodeType, long id) {
            var query = string.Empty;
            switch(nodeType) {
                case MetaNodeType.Directory:
                    query = "SELECT * FROM meta_nodes WHERE type_id=1 AND id=$id";
                    break;
                case MetaNodeType.Image:
                    query = "SELECT * FROM meta_nodes WHERE type_id=2 AND id=$id";
                    break;
            }
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$id", id),
            };
            return dbmgr.Select(query, param);
        }

        public DataTable GetMetaImage(long parentId, long order) {
            var query = "SELECT * FROM meta_nodes WHERE type_id=2 AND parent_id=$parent_id AND order=$order";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", parentId),
                new SqliteParameter("$order", order),
            };
            return dbmgr.Select(query, param);
        }

        public DataTable GetMetaImages(long parentId, bool idsOnly) {
            var query = string.Empty;
            if (idsOnly) {
                query = "SELECT id FROM meta_nodes WHERE type_id=2 AND parent_id=$parent_id";

            } else {
                query = "SELECT * FROM meta_nodes WHERE type_id=2 AND parent_id=$parent_id";
            }
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", parentId),
            };
            return dbmgr.Select(query, param);
        }

        public DataTable GetStaleMetaNodes(long integrity_check) {
            var query = "SELECT abspath FROM meta_nodes WHERE (type_id=1 OR type_id=2) AND integrity_check < $int_check";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$int_check", integrity_check),
            };
            return dbmgr.Select(query, param);
        }

        public long DeleteStaleMetaImages(long integrityCheck) {

            var query = @"DELETE FROM meta_nodes WHERE integrity_check < $int_check AND type_id=2";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$int_check", integrityCheck),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public long DeleteStaleMetaImages(long parent_id, long integrityCheck) {

            var query = @"DELETE FROM meta_nodes WHERE integrity_check < $int_check AND type_id=2 AND parent_id=$parent_id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$int_check", integrityCheck),
                new SqliteParameter("$parent_id", parent_id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public DataTable GetOrphanedMetaDirs(long integrity_check) {
            var query = "SELECT * FROM meta_nodes WHERE type_id=1 AND integrity_check < $int_check";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$int_check", integrity_check),
            };
            return dbmgr.Select(query, param);
        }

        public long DeleteStaleMetaDirs(long id) {
            var query = @"DELETE FROM meta_nodes WHERE type_id=1 AND id=$id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$id", id),
            };
            dbmgr.ExecuteNonQuery(query, param);

            query = @"DELETE FROM meta_nodes WHERE type_id=2 AND parent_id=$parent_id";
            param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", id),
            };
            return dbmgr.ExecuteNonQuery(query, param);
        }

        public int GetMetaNodeChildCount(long id) {
            var query = "SELECT COUNT(id) as 'child_count' FROM meta_nodes WHERE type_id=2 AND parent_id = $parent_id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", id),
            };
            var dt = dbmgr.Select(query, param);
            var count = 0;
            if(dt.Rows.Count > 0) {
                count = Convert.ToInt32(dt.Rows[0]["child_count"]);
            }
            return count;
        }

        public int GetMetaImageNextOrder(long id) {
            var query = "SELECT MAX(`order`) AS last_order FROM meta_nodes WHERE type_id=2 AND parent_id = $parent_id";
            dbmgr.Open();
            var param = new SqliteParameter[] {
                new SqliteParameter("$parent_id", id),
            };
            var dt = dbmgr.Select(query, param);
            var order = 1;
            if(dt.Rows.Count > 0 && Convert.ToString(dt.Rows[0]["last_order"]) != string.Empty) {
                order = Convert.ToInt32(dt.Rows[0]["last_order"]) + 1;
            }
            return order;
        }


        private Dictionary<string, string> GetExif(Image img) {
            var exifData = new Dictionary<string, string>();
            if (img.Metadata.ExifProfile != null) {
                foreach (ExifTag tag in img.Metadata.ExifProfile.Values) {
                    //TODO: Extract tags
                }
            }
            return exifData;
        }
    }
}
