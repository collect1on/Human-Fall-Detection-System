package com.example.myapplication1

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class DatabaseHelper2(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        private const val DATABASE_VERSION = 1
        private const val DATABASE_NAME = "MyDatabase.db"
    }

    override fun onCreate(db: SQLiteDatabase) {
        // 创建表
        val CREATE_TABLE = "CREATE TABLE IF NOT EXISTS recordstest (" +
                "id INTEGER PRIMARY KEY," +
                "source TEXT," +
                "time TEXT," +
                "record BLOB," +
                "recordbase64 TEXT" +

                ")"
        db.execSQL(CREATE_TABLE)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // 如果需要升级数据库，可以在这里添加升级逻辑
        // 例如，删除旧表并重新创建
        db.execSQL("DROP TABLE IF EXISTS recordstest")
        onCreate(db)
    }
}
