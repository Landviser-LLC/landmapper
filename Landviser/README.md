In this sub project created prototype of site. You can authorize or register on this site. As a Database used SQLite3 because it's simple to use in next time will changed. As a framework used Flask, because it's simple to use too next time can be changed.

First of all install python. For that you can use this commands:
```bash
  press button win + R
  in pop up window write cmd.exe
  in terminal write python
  in windows store press get
```

Creating Enviroment:
  ```bash
    pip install virtualenv
    python -m venv env
    env\Scripts\activate.bat
    pip install -r requirements.txt
  ```
  
  For run application use next command:
  ```bash
    python main.py
  ```
  In terminal logs find this row ```bash Running on http://127.0.0.1:5000/ ```
  Next copy http://127.0.0.1:5000/ and paste it into adress line of your browser.
  You are on the main page of a prototype. Click on button "sign up" and sign up.
  After sign up sign in. After sign in in top menu you can see Upload button. You can press that button and come to uploads page. On this page you can choose file and send it to server. After sending server gets your file and save it in local directory, but it wiil be changed.
