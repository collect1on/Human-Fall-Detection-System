package com.example.myapplication1

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.content.ContentValues
import android.util.Base64


class DatabaseHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        private const val DATABASE_VERSION = 1
        private const val DATABASE_NAME = "MyDatabase.db"

        // Define your table and columns
        private const val TABLE_NAME = "recordph5"
        private const val COLUMN_ID = "id"
        private const val COLUMN_SOURCE = "source"
        private const val COLUMN_TIME = "time"
        private const val COLUMN_RECORD = "record_column"
        private const val COLUMN_RECORDBASE64= "recordbase64_column"
        private const val COLUMN_URL= "url"


    }


    override fun onCreate(db: SQLiteDatabase) {
        // 创建表
        val CREATE_TABLE = "CREATE TABLE $TABLE_NAME ($COLUMN_ID INTEGER PRIMARY KEY, " +
                "$COLUMN_SOURCE TEXT, " +
                "$COLUMN_TIME TEXT, " +
                "$COLUMN_RECORD BLOB, " +
                "$COLUMN_RECORDBASE64 LONGTEXT, " + // Added comma here
                "$COLUMN_URL LONGTEXT)"

        db.execSQL(CREATE_TABLE)
    }

    fun getTableName(): String {
        return TABLE_NAME
    }
    fun tableExists(tableName: String, db: SQLiteDatabase): Boolean {
        val cursor = db.rawQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='$tableName'", null)
        val tableExists = cursor.count > 0
        cursor.close()
        return tableExists
    }



    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Drop older table if existed
        db.execSQL("DROP TABLE IF EXISTS $TABLE_NAME")

        // Create tables again
        onCreate(db)
    }

    fun insertRecord(source: String, time: String, record: ByteArray, recordBase64: String) {
        val db = this.writableDatabase
        val values = ContentValues().apply {
            put(COLUMN_SOURCE, source)
            put(COLUMN_TIME, time)
            put(COLUMN_RECORD, record)
            put(COLUMN_RECORDBASE64, recordBase64)
        }
        db.insert(TABLE_NAME, null, values)
        db.close()
    }

    fun insertRecord2(id: Int,source: String, time: String) {
        val db = this.writableDatabase
        val values = ContentValues().apply {
            put(COLUMN_ID, id)
            put(COLUMN_SOURCE, source)
            put(COLUMN_TIME, time)
            //put(COLUMN_RECORD, record)
            //put(COLUMN_RECORDBASE64, recordBase64)
        }
        db.replace(TABLE_NAME, null, values)
        db.close()
    }
    fun replaceRecord(source: String, time: String, record: ByteArray, recordBase64: String) {
        val db = this.writableDatabase
        val values = ContentValues().apply {
            put(COLUMN_SOURCE, source)
            put(COLUMN_TIME, time)
            put(COLUMN_RECORD, record)
            put(COLUMN_RECORDBASE64, recordBase64)
        }
        db.replace(TABLE_NAME, null, values)
        db.close()
    }
    fun getTotalRows(): Int {
        var totalRows = 0
        val query = "SELECT COUNT(*) FROM $TABLE_NAME"
        val db = readableDatabase
        val cursor = db.rawQuery(query, null)
        if (cursor != null && cursor.moveToFirst()) {
            totalRows = cursor.getInt(0)
            cursor.close()
        }
        return totalRows
    }



    fun getRowCount(): Int {
        val db = this.readableDatabase
        val cursor = db.rawQuery("SELECT COUNT(*) FROM $TABLE_NAME", null)
        var count = 0
        if (cursor != null) {
            cursor.moveToFirst()
            count = cursor.getInt(0)
            cursor.close()
        }
        return count
    }

    fun getTimeById(id: Int): String? {
        val db = readableDatabase
        var time: String? = null
        val selection = "$COLUMN_ID = ?"
        val selectionArgs = arrayOf(id.toString())
        val cursor = db.query(
            TABLE_NAME,
            arrayOf(COLUMN_TIME),
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        cursor.use {
            if (it != null && it.moveToFirst()) {
                val columnIndex = it.getColumnIndex(COLUMN_TIME)
                if (columnIndex > -1) {
                    time = it.getString(columnIndex)
                }
            }
        }
        return time
    }
    fun getSourceById(id: Int): String? {
        val db = readableDatabase
        var source: String? = null
        val selection = "$COLUMN_ID = ?"
        val selectionArgs = arrayOf(id.toString())
        val cursor = db.query(
            TABLE_NAME,
            arrayOf(COLUMN_SOURCE),
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        cursor.use {
            if (it != null && it.moveToFirst()) {
                val columnIndex = it.getColumnIndex(COLUMN_SOURCE)
                if (columnIndex > -1) {
                    source = it.getString(columnIndex)
                }
            }
        }
        return source
    }
    fun getRecordBase64ById(id: Int): String? {
        val db = readableDatabase
        var recordBase64: String? = null
        val selection = "$COLUMN_ID = ?"
        val selectionArgs = arrayOf(id.toString())
        val cursor = db.query(
            TABLE_NAME,
            arrayOf(COLUMN_RECORDBASE64),
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        cursor.use {
            if (it != null && it.moveToFirst()) {
                val columnIndex = it.getColumnIndex(COLUMN_RECORDBASE64)
                if (columnIndex > -1) {
                    recordBase64 = it.getString(columnIndex)
                }
            }
        }
        return recordBase64
    }



    fun updateRecordBase64ToURL() {
        val db = writableDatabase
        val cursor = db.rawQuery("SELECT $COLUMN_ID, $COLUMN_RECORDBASE64 FROM $TABLE_NAME", null)

        cursor.use {
            val idIndex = it.getColumnIndex(COLUMN_ID)
            val recordBase64Index = it.getColumnIndex(COLUMN_RECORDBASE64)

            while (it.moveToNext()) {
                val id = if (idIndex != -1) it.getInt(idIndex) else -1
                val recordBase64 = if (recordBase64Index != -1) it.getString(recordBase64Index) else null

                if (id != -1 && recordBase64 != null) {
                    // 在这里编写你的逻辑来处理recordBase64并生成对应的URL
                    var comopressbase64Bytes=recordBase64.toByteArray(Charsets.UTF_8)
                    var decodedBytes = Base64.decode(comopressbase64Bytes, Base64.DEFAULT)
                    var origin =decompressData(decodedBytes)
                    var url =bytetourl(origin)

                    // 更新数据表中的URL列
                    val contentValues = ContentValues().apply {
                        put(COLUMN_URL, url as String)
                    }
                    val whereClause = "$COLUMN_ID = ?"
                    val whereArgs = arrayOf(id.toString())
                    db.update(TABLE_NAME, contentValues, whereClause, whereArgs)
                } else {
                    // 处理无效的列索引或缺少的数据
                }
            }
        }


    }


    fun bytetourl(bytes: ByteArray): String {
        // 将字节数组转换为 Base64 编码的字符串
        val base64String = Base64.encodeToString(bytes, Base64.DEFAULT)
        // 构建 URL 字符串
        return "data:image/jpeg;base64,$base64String"
    }







}
