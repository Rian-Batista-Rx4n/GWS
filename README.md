# 🐺 Gray Wolf System (GWS) – v0.8.2 Beta
A personal file management system built with Flask, featuring audio, video, image players and more – all accessible through a responsive web interface.
---
## 🐺 Gray Wolf System

A web-based file manager built with **Flask (Python)**, ideal for personal use or local networks. Features include:
- File upload and download
- Embedded audio player
- Embedded video player
- Embedded image viewer
- Recent upload preview
- Category-based file navigation
- Responsive interface with HTML, CSS, and JS

![Last commit](https://img.shields.io/github/last-commit/Rian-Batista-Rx4n/web-files-manager-graywolfsystem)
![Repo size](https://img.shields.io/github/repo-size/Rian-Batista-Rx4n/web-files-manager-graywolfsystem)
![License](https://img.shields.io/github/license/Rian-Batista-Rx4n/web-files-manager-graywolfsystem)
![Top Language](https://img.shields.io/github/languages/top/Rian-Batista-Rx4n/web-files-manager-graywolfsystem)

---
## 📁 About the Project

**Gray Wolf System (GWS)** is a lightweight web application built with Flask, designed to turn any Linux device (old PC, server, or even a Termux-based Android phone) into a local file server.

Key features:
- File upload and download
- Built-in media players (video, audio, image)
- Category-based file visualization
- Responsive and modern interface (HTML + CSS + JS)
---
## 🎯 Project Goals

- Access your files remotely via browser and local IP
- Organize files by type and category
- Save space on mobile devices
- Reuse old hardware as a local server
- Keep a simple and user-friendly interface
---
## 📸 Screenshots

### Login (old picture)
![Tela de Login](static/images/1_login.png)

### Homepage (old picture)
![Interface da Homepage](static/images/2_homepage.png)

### Movie (old picture)
![Subcategoria movie](static/images/4_movie.png)

### Photo (old picture)
![Subcategoria photo](static/images/6_photo.png)
---
## 🚀 How to Use

1. Install and run the application on a Linux-based system:
   - Can be a server
   - An old phone (repurposed)
   - An unused computer

2. Run it using Python 3 with Flask installed

3. Your server's local storage becomes remote-accessible over the local network

4. Access via device IP or: `http://127.0.0.1:8080`
---
## 🚧 Status: Beta v0.8.2

✅ Available Features:
- [x] File upload and download
- [x] Video playback
- [x] Image viewer
- [x] Audio player
- [x] Recently uploaded file list

🛠️ Planned Features:
- [ ] Real-time chat
- [ ] Web Terminal (remote system access)
- [ ] Trash bin and file deletion
- [ ] User registration
- [ ] Secure login system
- [ ] Read and edit .txt files
- [ ] Show and Download Documents
---
## ⚙️ Technologies Used

- [x] Flask (Python)
- [x] HTML + CSS + JavaScript
- [x] Local hosting on Linux/Android (Termux)
- [x] Lightweight and minimal structure
---
# 🚀 Installation Guide

## Clone the repository

```bash
git clone https://github.com/Rian-Batista-Rx4n/web-files-manager-graywolfsystem
cd web-files-manager-graywolfsystem
pip install -r requirements.txt
python3 main.py
