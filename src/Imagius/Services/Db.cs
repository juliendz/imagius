using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLitePCL;
using System.Data;

namespace Imagius.Services {
    public class DbMgr {
        string dbPath;
        SqliteConnection conn;
        SqliteTransaction tran;
        SqliteCommand cmd;

        private static string schema = @" 
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS `scan_dirs` (
                `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `abspath` TEXT NOT NULL UNIQUE,
                `name` TEXT NOT NULL ,
                `img_count` INTEGER DEFAULT(0)
            );
            CREATE TABLE IF NOT EXISTS `meta_nodes` (
                `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `parent_id` INTEGER,
                `type_id` INTEGER,
                `abspath` TEXT NOT NULL,
                `thumb_abspath` TEXT,
                `name` TEXT NOT NULL,
                `child_count` INTEGER DEFAULT(0),
                `mtime` INTEGER,
                `integrity_check` INTEGER,
                `order` INTEGER
            );
            CREATE TABLE IF NOT EXISTS `settings` (
                `key` TEXT UNIQUE,
                `value` TEXT 
            );
        ";

        public DbMgr(string dbPath) {
            this.dbPath = dbPath;
        }
        public static void InitDatabase(string dbPath) {
            try {
                using (var connection = new SqliteConnection(string.Format("Data Source={0}", dbPath))) {
                    connection.Open();

                    var command = connection.CreateCommand();
                    command.CommandText = schema;
                    command.ExecuteNonQuery();
                }
            }
            catch(Exception ex) {
                //TODO: Logging
                throw;
            }
        }

        public void Open() {
            if(conn == null || conn.State != System.Data.ConnectionState.Open) {
                conn = new SqliteConnection(string.Format("Data Source={0}", dbPath));
                conn.Open();
            }
        }

        public async Task OpenAsync() {
            if(conn == null || conn.State != System.Data.ConnectionState.Open) {
                conn = new SqliteConnection(string.Format("Data Source={0}", dbPath));
                await conn.OpenAsync();
            }
        }

        public void BeginTransaction() {
            tran = conn.BeginTransaction(deferred: true);
        }

        public void CommitTransaction() {
            tran.Commit();
        }
        public async Task CloseAsync() {
            await conn.CloseAsync();
        }
        public void Close() {
            conn.Close();
        }

        //public async void Commit() {
        //}

        public long Insert(string query, SqliteParameter[] param) {
            long? lastId;
            try {
                Open();
                var command = conn.CreateCommand();
                command.CommandText = query;
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }

                command.ExecuteNonQuery();

                command = conn.CreateCommand();
                command.CommandText = "SELECT last_insert_rowid();";
                lastId = (long)command.ExecuteScalar();
                return lastId ?? 0L;

            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
        }

        public async Task<long> InsertAsync(string query, SqliteParameter[] param) {
            long? lastId;
            try {
                await OpenAsync();
                var command = conn.CreateCommand();
                command.CommandText = query;
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }
                await command.ExecuteNonQueryAsync();

                command = conn.CreateCommand();
                command.CommandText = "SELECT last_insert_rowid();";
                lastId = (long)await command.ExecuteScalarAsync();
                return lastId ?? 0L;

            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
        }

        public int ExecuteNonQuery(string query, SqliteParameter[] param) {
            try {
                Open();
                var command = conn.CreateCommand();
                command.CommandText = query;
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }
                return command.ExecuteNonQuery();
            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
        }

        public async Task<int> ExecuteNonQueryAsync(string query, SqliteParameter[] param) {
            try {
                await OpenAsync();
                var command = conn.CreateCommand();
                command.CommandText = query;
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }
                return await command.ExecuteNonQueryAsync();
            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
        }

        public DataTable Select(string query, SqliteParameter[]? param = null) {
            var dt = new DataTable();
            try {
                Open();
                var command = conn.CreateCommand();
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }
                command.CommandText = query;
                using (var dr = command.ExecuteReader()) {
                    dt.Load(dr);
                }
            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
            return dt;
        }

        public async Task<DataTable> SelectAsync(string query, SqliteParameter[]? param = null) {
            var dt = new DataTable();
            try {
                await OpenAsync();
                var command = conn.CreateCommand();
                if(param != null && param.Length > 0) {
                    foreach(var p in param) {
                        command.Parameters.Add(p);
                    }
                }
                command.CommandText = query;
                using (var dr = await command.ExecuteReaderAsync()) {
                    dt.Load(dr);
                }
            } catch (Exception ex) {
                //TODO: Logging
                throw;
            }
            return dt;
        }
    }
}
