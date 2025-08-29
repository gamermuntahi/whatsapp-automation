
# WhatsApp Business Automation Tool

This is a simple **Flask-based web tool** to manage requests stored in a text file (`requests/request.txt`).  
It provides a clean and modern web interface to view, add, and delete requests.

---

## ✨ Features
- 📋 List all requests with a modern UI
- 🗑️ Delete individual requests
- 📱 Responsive design (works on mobile and desktop)
- 📝 Requests stored in a plain text file (`request.txt`)

---

## 📂 Project Structure

project/
│
├── app.py # Main Flask application
├── templates/
│ ├── request_ls.html # UI for listing requests
│ └── base.html # (optional) base template
├── requests/
│ └── request.txt # Storage file for requests
└── static/ # Static assets (CSS/JS if needed)

By default, it will run on:

Local: http://127.0.0.1:5000

Network (LAN): http://192.168.x.x:5000

🛠️ Usage

Open /request_ls in your browser to see all requests.

Each request will have:

📌 Serial number

📄 Request details

🗑️ Delete button

Click Delete to remove a request (it updates request.txt automatically).

📦 Example Request Format

Requests are stored in requests/request.txt like this:

1919192144, cap - price:- 50tk . ---- That's a cap ----
1234567890, shoes - price:- 200tk . ---- Sports Shoes ----


Each line = one request.
⚠️ Notes

This app is for local/internal use only.

If you plan to deploy, use a production WSGI server (e.g., Gunicorn) instead of Flask’s built-in server.

Deletion is permanent (removes the line from request.txt).
