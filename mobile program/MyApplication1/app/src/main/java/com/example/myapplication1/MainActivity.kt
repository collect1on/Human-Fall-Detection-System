package com.example.myapplication1

//import java.util.Base64

import android.app.Activity
import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.media.MediaPlayer
import android.net.ConnectivityManager
import android.net.Uri
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.util.Base64
import android.util.Log
import android.view.View
import android.view.ViewGroup
import android.view.ViewGroup.LayoutParams.MATCH_PARENT
import android.view.ViewGroup.LayoutParams.WRAP_CONTENT
import android.widget.Button
import android.widget.EditText
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
import android.widget.Toast
import android.widget.VideoView
import org.json.JSONArray
import java.io.BufferedReader
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.security.NoSuchAlgorithmException
import java.util.zip.Inflater
import javax.net.ssl.HttpsURLConnection
import javax.net.ssl.SSLContext
import java.io.OutputStreamWriter

import android.net.NetworkInfo
import android.app.NotificationChannel
import android.app.NotificationManager

import android.os.Build
import androidx.core.app.NotificationCompat
import java.net.NetworkInterface
import java.net.SocketException
import android.content.pm.PackageManager
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicInteger


var rollnumberGOOD: AtomicInteger = AtomicInteger()
var index123: Int = 1
var globalurl: String=""


var connecttopc: AtomicBoolean = AtomicBoolean(false)
var serverip: String="http://100.86.59.179:8765"

class MainActivity : Activity() {

    lateinit var httpFetcher: HttpFetcher

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        Log.d("MyActivity", "onCreate() method is called")
        rollnumberGOOD.set(-1)

        try {
            //var sslContext123 = SSLContext.getInstance("TLSv1.2")
            val sslContext123 = SSLContext.getInstance("TLSv1.2")
            sslContext123.init(null, null, null)
            //configureTLS()
            HttpsURLConnection.setDefaultSSLSocketFactory(sslContext123.socketFactory)
        } catch (e: NoSuchAlgorithmException) {
            e.printStackTrace()
            // 如果无法获取 SSLContext，可能需要进行适当的处理
        }
        //val sslContext = SSLContext.getInstance("TLS")

        //var sslContext123 =configureTLS()
        //HttpsURLConnection.setDefaultSSLSocketFactory(sslContext123.socketFactory)



        val editTextNumber2 = findViewById<EditText>(R.id.editTextNumber2)
        val button = findViewById<Button>(R.id.button)

        Log.d("MyActivity", "创建数据库表")
        // 创建数据库表
        val dbHelper = DatabaseHelper(this)
        val db = dbHelper.writableDatabase
        db.disableWriteAheadLogging()
        val tableName = dbHelper.getTableName()

        // 判断表是否已经存在
        val tableExists = dbHelper.tableExists(tableName, db)
        if (!tableExists) {
            // 如果表不存在，则创建表
            dbHelper.onCreate(db)
        }



        Log.d("MyActivity", "獲得数据")
        httpFetcher = HttpFetcher()
        httpFetcher.context = this
        //dbHelper.updateRecordBase64ToURL()
        Log.d("MyActivity", "獲得数据")
        // 在 Activity 中调用 fetchDataFromServer 方法
        //httpFetcher.startFetching()
        //var aa=httpFetcher.fetchDataFromServer()
        //httpFetcher.processData(aa)
        val tableLayout = findViewById<TableLayout>(R.id.tableLayout)
        val tableCreator = TableCreator(this, tableLayout)
        tableCreator.createTable1()
        Log.d("MyActivity12345", "createTable1")




        button.setOnClickListener {
            // Get the text from the EditText
            val password = editTextNumber2.getText().toString()

            // Check if the password is not empty
            if (!password.isEmpty()) {
                // Perform your action here, such as pairing the device
                // For demonstration, just showing the entered password in a Toast message
                Log.d("MyActivity123456", "httpFetcher.submitcode(password)")
                Log.d("MyActivity123456", "httpFetcher$password")
                var aaa=getDeviceIpAddress(this)
                if (aaa.isNotEmpty()) {
                    // 字符串不为空的情况下执行的代码
                    Log.d("MyActivity123456", "IpAddress$aaa")

                    httpFetcher.submitcode(password,aaa){ responseData ->

                        if(responseData=="連接失敗") {connecttopc.set(false)
                        }else{
                            connecttopc.set(true)
                            Log.d("MyActivity12345689", "connecttopc")
                        }


                        runOnUiThread {
                            Toast.makeText(this@MainActivity, responseData, Toast.LENGTH_SHORT).show()
                        }



                    }




                } else {
                    // 字符串为空的情况下执行的代码
                    Toast.makeText(this@MainActivity, "請先連接網路", Toast.LENGTH_SHORT)
                        .show()

                }

            } else {
                // If the password is empty, show a message
                Toast.makeText(this@MainActivity, "请输入配对码", Toast.LENGTH_SHORT)
                    .show()
            }
        }
        val refreshButton = findViewById<Button>(R.id.refreshButton1)
        refreshButton.setOnClickListener {
            // 移除現有的表格
            tableLayout.removeAllViews()
            val tableCreator12 = TableCreator(this, tableLayout)
            // 重新創建表格
            tableCreator12.createTable1()
            Log.d("MyActivity12345", "createTable1 after refresh")


            tableCreator.createTable1()

        }


    }

    override fun onStart() {
        super.onStart()
        // 在 Activity 开始时启动数据获取
        httpFetcher.startFetching()
    }

    override fun onStop() {
        super.onStop()
        // 在 Activity 停止时停止数据获取
        httpFetcher.stopFetching()
    }

    private val PERMISSION_REQUEST_CODE = 100

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // 权限已授予，现在可以发布通知
                NotificationHelper.showNotification(this, "标题", "消息")
            } else {
                // 权限被拒绝
                // 处理拒绝或向用户说明权限的必要性
            }
        }
    }








}

fun getDeviceIpAddress(context: Context): String {
    val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    val activeNetwork: NetworkInfo? = connectivityManager.activeNetworkInfo
    if (activeNetwork != null && activeNetwork.isConnected) {
        // 如果有网络连接，获取当前连接的IP地址
        val wifiManager = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val ipAddress = wifiManager.connectionInfo.ipAddress
        // 格式化IP地址并返回
        return String.format("%d.%d.%d.%d",
            ipAddress and 0xff,
            ipAddress shr 8 and 0xff,
            ipAddress shr 16 and 0xff,
            ipAddress shr 24 and 0xff)
    }
    // 如果没有网络连接，返回空字符串或者其他默认值
    return ""
}

class HttpFetcher {
    private val SERVER_URL = serverip
    private val INTERVAL: Long = 10000 // 100 seconds

    lateinit var context: Context // 上下文变量

    private val handler = Handler(Looper.getMainLooper())
    private val fetchRunnable = object : Runnable {
        override fun run() {
            if(connecttopc.get()){fetchDataFromServer()
                Log.d("MyActivity7070", "start get roll")
            }

            //processData(roll)
            var aaa=getDeviceIpAddress(context)
            Log.d("MyActivity1234567", "IpAddress123 $aaa")

            handler.postDelayed(this, INTERVAL)
        }
    }




    fun submitcode(code: String, param2: String, callback: (String) -> Unit) {
        var aa=Thread {
            try {
                val url = URL(SERVER_URL + "/user/api/submitcode")
                val connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.doOutput = true

                val postData = "code=$code&param2=$param2"
                val outputStream = connection.outputStream
                val writer = OutputStreamWriter(outputStream)
                writer.write(postData)
                writer.flush()
                Log.d("MyActivity123456", "writer.flush()")
                val responseCode = connection.responseCode
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    val inputStream = connection.inputStream
                    val reader = BufferedReader(InputStreamReader(inputStream))
                    val response = StringBuilder()
                    var line: String?
                    while (reader.readLine().also { line = it } != null) {
                        response.append(line)
                    }
                    reader.close()
                    // 可以在这里处理服务器的响应
                    val responseData = response.toString()
                    callback(responseData)
                } else {
                    // 处理HTTP请求失败的情况
                    Log.d("MyActivity123456", "处理HTTP请求失败的情况")
                }

                connection.disconnect()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        aa.start()
        aa.join()
    }

    fun submitip(ip: String) {
        Thread {
            try {
                val url = URL(SERVER_URL + "/user/api/submitip")
                val connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.doOutput = true

                val postData = "ip=$ip"
                val outputStream = connection.outputStream
                val writer = OutputStreamWriter(outputStream)
                writer.write(postData)
                writer.flush()
                Log.d("MyActivity123456", "writer.flush()")
                val responseCode = connection.responseCode
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    val inputStream = connection.inputStream
                    val reader = BufferedReader(InputStreamReader(inputStream))
                    val response = StringBuilder()
                    var line: String?
                    while (reader.readLine().also { line = it } != null) {
                        response.append(line)
                    }
                    reader.close()
                    // 可以在这里处理服务器的响应
                    val responseData = response.toString()
                } else {
                    // 处理HTTP请求失败的情况
                    Log.d("MyActivity123456", "处理HTTP请求失败的情况")
                }

                connection.disconnect()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }














    fun startFetching() {
        handler.postDelayed(fetchRunnable, 0)
    }

    fun stopFetching() {
        handler.removeCallbacks(fetchRunnable)
    }

    // 使用当前上下文对象
    fun fetchDataFromServer() : Int {
        var rollnumber = 0
        Thread {
            try {
                Log.d("MyActivity123", "獲得数据库行數1")
                var aaa=getDeviceIpAddress(context)

                val url12 = URL(SERVER_URL+"/user/api/getrollnumberV2?ip=$aaa")
                val connection12 = url12.openConnection() as HttpURLConnection
                connection12.requestMethod = "GET"
                val reader12 = BufferedReader(InputStreamReader(connection12.inputStream))
                val response12 = StringBuilder()
                var line12: String?
                while (reader12.readLine().also { line12 = it } != null) {
                    response12.append(line12)
                }
                Log.d("MyActivity123", "獲得数据库行數2")
                rollnumber=response12.toString().toInt()
                Log.d("MyActivity2020", "rollnumber")
                Log.d("MyActivity2020", "$rollnumber")





                """
                val url1 = URL(SERVER_URL+"/user/api/getroll?$aaa")
                val connection1 = url1.openConnection() as HttpURLConnection
                connection1.requestMethod = "GET"
                val reader1 = BufferedReader(InputStreamReader(connection1.inputStream))
                val response1 = StringBuilder()
                var line1: String?
                while (reader1.readLine().also { line1 = it } != null) {
                    response1.append(line1)
                }
                Log.d("MyActivity123", "獲得数据库行數2")
                rollnumber=response1.toString().toInt()
                """

                //if(rollnumber!=0){rollnumberGOOD.set(rollnumber)}

                rollnumberGOOD.set(rollnumber)
                Log.d("MyActivity2020", "$rollnumber")


                Log.d("MyActivity123", "数据库行數12111111111111111111111111111111")
                Log.d("MyActivity123", "数据库行數rollnumber?$rollnumber")
                Log.d("MyActivity123", "数据库行數rollnumberGOOD?$rollnumberGOOD")
                //if (rollnumber!=0){processData(rollnumber)}
                processData(rollnumber)
            } catch (e: Exception) {
                Log.d("MyActivity2020", "rollnumber")
                e.printStackTrace()
                rollnumberGOOD.set(-1)
                Log.d("MyActivity2020", "rollnumber")

            }
        }.start()

        return rollnumber

    }
    fun processData(rollnumber: Int) {//獲得表的id時間來源
        index123=1
        Log.d("MyActivity123", "一行数据1231231231321332")
        for (i in 1 until rollnumber + 1) {
            while(true){
                if(index123==i){
                    break
                }
            }
            Log.d("MyActivity123", "一行数据1231231231321332  /user/api/getvideo")

            Thread {
                Log.d("MyActivity123", "嘗試插入数据到数据库?id=$i")
                // 创建URL对象
                //val url = URL(SERVER_URL+"/user/api/getdatabase")
                var ip=getDeviceIpAddress(context)
                val url1 = URL("$SERVER_URL/user/api/getdatabaseV2?id=$i&ip=$ip")
                // 创建HttpURLConnection对象
                val connection = url1.openConnection() as HttpURLConnection
                // 设置请求方法
                connection.requestMethod = "GET"

                // 获取输入流
                val reader = BufferedReader(InputStreamReader(connection.inputStream))
                val response = StringBuilder()
                var line: String?

                // 读取服务器响应数据
                while (reader.readLine().also { line = it } != null) {
                    response.append(line)
                }

                //var json = response.toString()
                val jsonArray = JSONArray(response.toString())
                val dbHelper = DatabaseHelper(context) // 使用当前上下文对象
                //val jsonObject = jsonArray.getJSONObject(0)
                val jsonObject= jsonArray.getJSONArray(0)
                //val id = jsonObject.getInt("id")
                //val source = jsonObject.getString("source")
                //val time = jsonObject.getString("time")
                //val record = jsonObject.getString("record_column")
                //val recordBase64 = jsonObject.getString("recordbase64_column")
                val id = jsonObject.getInt(0)
                val source = jsonObject.getString(1)
                val time = jsonObject.getString(2)
                //val record = jsonObject.getString("record_column")
                //val recordBase64 = jsonObject.getString(3)


                // 插入数据到数据库
                dbHelper.insertRecord2(id, source, time)
                // 关闭资源

                reader.close()
                connection.disconnect()
                //Thread.sleep(1000)
                index123+=1
            }.start()
            Log.d("MyActivity", "插入数据到数据库")
            //print("插入数据到数据库")
        }


        // 处理服务器响应数据，你可以根据自己的需求进行处理
        //val responseData = response.toString()
        // TODO: 处理服务器响应数据

    }
}
class TableCreator(private val context: Context, private val tableLayout: TableLayout) {

    fun createTable1() {
        tableLayout.removeAllViews() // 清空现有的表格行

        val dbHelper = DatabaseHelper(context)
        val db = dbHelper.writableDatabase
        var Rows1 = dbHelper.getTotalRows()


        // 循环遍历数据列表，为每条数据创建一个新的TableRow并添加到TableLayout中
        for (i in 1 until Rows1 + 1) {
            val tableRow = TableRow(context)
            //設定TableRow<TableRow
            //                android:layout_width="1dp"
            //                android:layout_height="1dp"
            //                android:background="@drawable/table_row_bg">
            tableRow.layoutParams = TableRow.LayoutParams(
                TableRow.LayoutParams.MATCH_PARENT,
                TableRow.LayoutParams.WRAP_CONTENT
            )
            tableRow.setBackgroundResource(R.drawable.table_row_bg)


            val textView1 = TextView(context)
            textView1.layoutParams = TableRow.LayoutParams(
                TableRow.LayoutParams.WRAP_CONTENT,
                TableRow.LayoutParams.WRAP_CONTENT
            )
            textView1.text = " ${i}" // 假设id表示行号
            textView1.setTextColor(Color.parseColor("#009E00"))

            val view = View(context)
            view.layoutParams = TableRow.LayoutParams(1, TableRow.LayoutParams.MATCH_PARENT)
            view.setBackgroundColor(Color.parseColor("#009E00"))

            val textView2 = TextView(context)
            textView2.layoutParams = TableRow.LayoutParams(
               100,
                TableRow.LayoutParams.WRAP_CONTENT
            )
            textView2.text = dbHelper.getSourceById(i) // 假设id表示行号
            textView2.setTextColor(Color.parseColor("#009E00"))

            val view2 = View(context)
            view2.layoutParams = TableRow.LayoutParams(1, TableRow.LayoutParams.MATCH_PARENT)
            view2.setBackgroundColor(Color.parseColor("#009E00"))

            val textView3 = TextView(context)
            textView3.layoutParams = TableRow.LayoutParams(
                TableRow.LayoutParams.WRAP_CONTENT,
                TableRow.LayoutParams.WRAP_CONTENT
            )
            textView3.text = dbHelper.getTimeById(i) // 假设id表示行号
            textView3.setTextColor(Color.parseColor("#009E00"))
            // 创建一个大小为5000000字节的CursorWindow


// 将Cursor转换为AbstractWindowedCursor

            val view3 = View(context)
            view3.layoutParams = TableRow.LayoutParams(1, TableRow.LayoutParams.MATCH_PARENT)
            view3.setBackgroundColor(Color.parseColor("#009E00"))


            //val button=Button(context)
            //var aa=dbHelper.getRecordBase64ById(i)


            val button = Button(context)
            //val layoutParams = ViewGroup.LayoutParams(
             //   ViewGroup.LayoutParams.WRAP_CONTENT,
            //    ViewGroup.LayoutParams.WRAP_CONTENT
            //)
            button.layoutParams = TableRow.LayoutParams(
                TableRow.LayoutParams.WRAP_CONTENT,
                TableRow.LayoutParams.WRAP_CONTENT
            )
            //button.layoutParams = layoutParams
            button.text = "播放"
            button.setOnClickListener {
                Log.d("MyActivity123", "一行数据1231231231321332  /user/api/getvideo")
                var rollnumber = rollnumberGOOD.get()
                Log.d("MyActivity4040", "$rollnumber")
                if (rollnumber != -1){


                var aaa = getDeviceIpAddress(context)

                var tt = Thread {
                    Log.d("MyActivity123", "嘗試點数据id=$i")
                    // 创建URL对象
                    //val url = URL(SERVER_URL+"/user/api/getdatabase")
                    val SERVER_URL = serverip
                    val url1 = URL("$SERVER_URL/user/api/getvideo?id=$i&ip=$aaa")
                    // 创建HttpURLConnection对象
                    val connection = url1.openConnection() as HttpURLConnection
                    // 设置请求方法
                    connection.requestMethod = "GET"
                    Log.d("MyActivity123", "请求方法")
                    // 获取输入流
                    val reader = BufferedReader(InputStreamReader(connection.inputStream))
                    val response = StringBuilder()
                    var line: String?
                    Log.d("MyActivity123", "获取输入流")
                    // 读取服务器响应数据
                    while (reader.readLine().also { line = it } != null) {
                        response.append(line)
                    }

                    //var json = response.toString()
                    val jsonArray = JSONArray(response.toString())
                    //val dbHelper = DatabaseHelper(context) // 使用当前上下文对象
                    //val jsonObject = jsonArray.getJSONObject(0)
                    val jsonObject = jsonArray.getJSONArray(0)
                    //val id = jsonObject.getInt("id")
                    //val source = jsonObject.getString("source")
                    //val time = jsonObject.getString("time")
                    //val record = jsonObject.getString("record_column")
                    //val recordBase64 = jsonObject.getString("recordbase64_column")

                    val mp4_base64 = jsonObject.getString(0)
                    Log.d("MyActivity123", "getString")
                    globalurl = mp4_base64

                    Log.d("MyActivity123", "check=true")


                }
                //Thread.currentThread().join()
                tt.start()
                tt.join()


                Log.d("MyActivity123", "轉換")
                //var comopressbase64Bytes=globalurl.toByteArray(Charsets.UTF_8)

                //var decodedBytes = Base64.decode(comopressbase64Bytes, Base64.DEFAULT)
                var decodedBytes = Base64.decode(globalurl, Base64.DEFAULT)
                //var origin =decompressData(decodedBytes)
                //var url =bytetourl(origin)
                Log.d("MyActivity123", "準備show")
                val dialog = CustomDialog(context, decodedBytes)
                dialog.show()


                //val dialog = CustomDialog(context,i)
                //dialog.show()
            } else{
                    Toast.makeText(context, "請先配對電腦", Toast.LENGTH_SHORT)
                        .show()
             }


            }
            tableRow.addView(textView1)
            tableRow.addView(view)
            tableRow.addView(textView2)
            tableRow.addView(view2)
            tableRow.addView(textView3)
            tableRow.addView(view3)
            tableRow.addView(button)


            tableLayout.addView(tableRow)
        }
    }
    fun bytetourl(bytes: ByteArray): String {
        // 将字节数组转换为 Base64 编码的字符串
        val base64String = Base64.encodeToString(bytes, Base64.DEFAULT)
        // 构建 URL 字符串
        return "data:image/jpeg;base64,$base64String"
    }

}

fun decompressData(compressedData: ByteArray): ByteArray {
    val inflater = Inflater()
    inflater.setInput(compressedData)

    val buffer = ByteArray(1024)
    val outputStream = ByteArrayOutputStream()

    while (!inflater.finished()) {
        val count = inflater.inflate(buffer)
        outputStream.write(buffer, 0, count)
    }

    inflater.end()
    return outputStream.toByteArray()
}







fun createTempVideoFile(context: Context, videoBlob: ByteArray): File {
    val tempVideoFile = File.createTempFile("temp_video", ".mp4", context.cacheDir)
    tempVideoFile.writeBytes(videoBlob)
    return tempVideoFile
}
fun showVideoDialog(context: Context, videoUri: Uri) {
    val dialog = Dialog(context)
    dialog.setContentView(R.layout.dialog_video)

    val videoView = dialog.findViewById<VideoView>(R.id.videoView)
    videoView.layoutParams = ViewGroup.LayoutParams(MATCH_PARENT, WRAP_CONTENT)
    videoView.setVideoURI(videoUri)
    videoView.setOnPreparedListener { mp -> mp.isLooping = true } // 循环播放
    videoView.start()

    dialog.show()
}
class CustomDialog(context: Context, private val videoBlobData: ByteArray) : Dialog(context) {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_video)
        Log.d("MyActivity123", "{videoBlobData}")
        val videoView = findViewById<VideoView>(R.id.videoView)
        val closeButton = findViewById<Button>(R.id.closeButton)
        Log.d("MyActivity123", "$videoBlobData")
        //val file = File(context.filesDir,"output.txt")



        try {
            // 获取内部存储目录
            val file = File(context.filesDir, "abc.mp4")

            // 创建文件输出流
            val fileOutputStream = FileOutputStream(file)

            // 将数据写入文件
            fileOutputStream.write(videoBlobData)
            println("视频数据已成功写入文件 abc.mp4")

            // 关闭文件输出流
            fileOutputStream.close()

            val videoUri = Uri.fromFile(file)
            videoView.setVideoURI(videoUri)
            videoView.start()

            Log.d("MyActivity123", "videoView.setVideoURI(videoUri)")
            // 准备播放视频
            videoView.setOnPreparedListener { mp: MediaPlayer ->
                mp.isLooping = true
                videoView.start()
            }
        } catch (e: Exception) {
            println("写入文件时出错: ${e.message}")
        }
        // 将 Blob 数据存储到文件中，并获取文件的 URI
        //val videoUri = saveBlobDataToFileAndReturnUri(context,videoBlobData) // 从文件中获取视频的 URI
        //Log.d("MyActivity123", "${videoBlobData}")
       // val success = convertByteBlobToMP4(context, videoBlobData)
        //if (success) {
            //Log.d("MyActivity123", "转换成功，执行某些操作")
            // 转换成功，执行某些操作
       // } else {
            //Log.d("MyActivity123", "转换失败，处理错误")
            // 转换失败，处理错误
        //}
        //val videoUri =blobToVideo(videoBlobData)
        //val fileUri = Uri.fromFile(tempFile)

        Log.d("MyActivity123", "准备播放视频")
        // 关闭对话框
        closeButton.setOnClickListener {
            dismiss()
        }
    }

    // 将 Blob 数据存储到文件中，并获取文件的 URI
    private fun saveBlobDataToFileAndReturnUri(context: Context,videoBlobData: ByteArray): Uri {
        //val videoBlobData: ByteArray = fetchVideoBlobFromDatabase(context,videoBlobData) // 从数据库中获取 Blob 数据
        val fileDir = context.getExternalFilesDir(Environment.DIRECTORY_MOVIES)
        val videoFile = File(fileDir, "video.mp4")

        // 将 Blob 数据写入文件
        val outputStream = FileOutputStream(videoFile)
        outputStream.write(videoBlobData)
        outputStream.close()

        // 返回文件的 URI
        return Uri.fromFile(videoFile)
    }
    private fun decompressData(compressedData: ByteArray): ByteArray {
        val inflater = Inflater()
        inflater.setInput(compressedData)
        val outputStream = ByteArrayOutputStream(compressedData.size)
        val buffer = ByteArray(1024)
        while (!inflater.finished()) {
            val count = inflater.inflate(buffer)
            outputStream.write(buffer, 0, count)
        }
        outputStream.close()
        return outputStream.toByteArray()
    }


    // 从数据库中获取 Blob 数据
    private fun fetchVideoBlobFromDatabase(context: Context,id:Int): ByteArray {
        Log.d("MyActivity", "還原blob1")
        val dbHelper = DatabaseHelper(context)
        // 这里是一个假设的方法，用于从数据库中获取 Blob 数据
        // 实际情况下，你需要使用你的数据库访问方法来获取 Blob 数据
        // 下面的代码仅供示例，假设从数据库中获取 Blob 数据的操作
        // 返回一个示例的 ByteArray
        var recordBase64=dbHelper.getRecordBase64ById(id)
        Log.d("MyActivity", "還原blob2")
        //var comopressbase64Bytes=recordBase64.toByteArray(Charsets.UTF_8)
        val comopressbase64Bytes = recordBase64!!.toByteArray(Charsets.UTF_8)
        Log.d("MyActivity", "還原blob3")

        var decodedBytes =Base64.decode(comopressbase64Bytes,Base64.DEFAULT)
        Log.d("MyActivity", "還原blob4")

        return decompressData(decodedBytes)
    }
}
fun blobToVideo(blobData: ByteArray): Uri? {
    try {
        // 将blob数据写入临时文件
        val tempFile = File.createTempFile("temp", ".mp4")
        val outputStream = FileOutputStream(tempFile)
        outputStream.write(blobData)
        outputStream.close()

        // 使用FFmpeg将blob转换为视频
        val ffmpegCommand = "ffmpeg -f rawvideo -pix_fmt rgba -s 1920x1080 -r 30 -i ${tempFile.absolutePath} output.mp4"
        val process = Runtime.getRuntime().exec(ffmpegCommand)
        process.waitFor()

        // 检查是否成功转换
        if (process.exitValue() == 0) {
            println("Blob成功转换为视频")

            val fileUri = Uri.fromFile(tempFile)
            return fileUri
            val fileURI = tempFile.toURI()
            //return fileURI.toURL()
            //return tempFile.absolutePath
        } else {
            println("转换过程中出现错误")
            return null
        }
    } catch (e: Exception) {
        println("转换过程中出现异常: ${e.message}")
        return null
    }
}

object ByteBlobToMP4Converter {
    fun convertByteBlobToMP4(context: Context, byteBlob: ByteArray?): Boolean {
        return try {
            // 创建文件以存储MP4
            val file = File(context.filesDir, "output123.mp4")
            // 将字节数组写入文件
            val outputStream = FileOutputStream(file)
            outputStream.write(byteBlob)
            outputStream.close()
            true
        } catch (e: IOException) {
            Log.e("ByteBlobToMP4Converter", "转换Byte Blob到MP4时出错：" + e.message)
            false
        }
    }
}



object NotificationHelper {
    private const val NOTIFICATION_ID = 1
    private const val CHANNEL_ID = "Your_channel_id"

    fun showNotification(context: Context, title: String, message: String) {
        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification) // 设置通知图标
            .setContentTitle(title) // 设置通知标题
            .setContentText(message) // 设置通知内容
            .setPriority(NotificationCompat.PRIORITY_DEFAULT) // 设置通知优先级

        val notificationManager =
            context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // 创建通知渠道（适用于 Android 8.0 及以上版本）
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Channel Name",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            notificationManager.createNotificationChannel(channel)
        }

        val notification = builder.build()

        // 显示通知
        notificationManager.notify(NOTIFICATION_ID, notification)
    }
}










