### 1. Configuration Process:

**1.1** Place the **Downloads** folder under the path `C:\Users\ricky\`, with the folder structure as `C:\Users\ricky\Downloads`.

**1.2. Server Program Configuration:**

* **1.2.1** In the *server program* folder, set up a Python virtual environment.
  Python interpreter version: **3.11.9 (tags/v311.9\:de54 Apr 2 2024, 10:12:12) \[MSC v.1938 64 bit (AMD64)]**
* **1.2.2** Install dependencies:

  ```bash
  pip install -r .\requirements.txt
  ```
* **1.2.3** Run the `server2.py` file.

**1.3. Computer Program Configuration:**

* **1.3.1** In the *computer program* folder, set up a Python virtual environment.
  Python interpreter version: **3.11.9 (tags/v311.9\:de54 Apr 2 2024, 10:12:12) \[MSC v.1938 64 bit (AMD64)]**
* **1.3.2** Install dependencies (adjust PyTorch according to GPU model):

  ```bash
  pip install -r .\requirements.txt
  ```
* **1.3.3** Configure the server IP address and port in `main.py` as needed.
* **1.3.4** Run the `ui4.py` file.

**1.4. Mobile Program Configuration:**

* **1.4.1** Install: **Android Studio Iguana | 2023.2.1**.
* **1.4.2** Open the project in Android Studio: *mobile program → MyApplication1* folder.
* **1.4.3** Configure the server IP address and port in `MainActivity.kt`, modifying `var serverip`.
* **1.4.4** Modify the domain in `network_security_config.xml` if necessary.
* **1.4.5** Run the project in Android Studio to install the mobile application.

---

### 2. User Instructions:

**2.1** Ensure the server program, computer program, and mobile program are all connected to the network.
**2.2** Run the server program.
**2.3** Run the computer program and the mobile program.
**2.4** Use the computer program to connect to the mobile device and view the pairing code.
**2.5** On the mobile program, use the “connect to computer” function and enter the pairing code to pair with the computer.
**2.6** Use the human fall detection function in the computer program.
**2.7** In the computer program, use the “view analysis results” function to check recorded fall detection analysis results.
**2.8** On the mobile program, click the refresh button to sync and view the latest fall detection analysis results from the computer program.


---

