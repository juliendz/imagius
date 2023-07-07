using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Imagius.Utils {
    public class DbTable {

        public static List<Dictionary<string, object?>> ToDictionary(DataTable dt) {
            var dictionaries = new List<Dictionary<string, object?>>();
            foreach (DataRow row in dt.Rows) {
                Dictionary<string, object?> dictionary = Enumerable.Range(0, dt.Columns.Count).ToDictionary(i => dt.Columns[i].ColumnName, i => row.ItemArray[i]);
                dictionaries.Add(dictionary);
            }

            return dictionaries;
        }

        public static Dictionary<string, object?> ToDictionarySingle(DataTable dt) {
            Dictionary<string, object?> ret = new Dictionary<string, object?>();
            if(dt.Rows.Count > 0) {
                ret = Enumerable.Range(0, dt.Columns.Count).ToDictionary(i => dt.Columns[i].ColumnName, i => dt.Rows[0].ItemArray[i]);
            }

            return ret;
        }
    }
}
