# flask_project
simple api for video uploader in onepanel workspaces

**COMMANDS:**
```bash
export FLASK_APP=server.py
flask run
or
python server.py

* Serving Flask app "server" (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: on
* Restarting with windowsapi reloader
* Debugger is active!
* Debugger PIN: 230-078-479
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```
```bash
curl http://localhost:5000/file -d "filename=test_video.mp4" -X PUT
curl http://localhost:5000/file
```
