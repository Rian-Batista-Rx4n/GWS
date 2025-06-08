# 🐺 Gray Wolf System – v0.9.4 Beta

A personal file management system built with Flask, featuring audio, video, image players and more — all accessible through a responsive web interface.

---

## Table of Contents
- [Gray Wolf System](#-gray-wolf-system)
- [Project Goals](#-project-goals)
- [How to Use](#-how-to-use)
- [Status](#-status-beta-v094)
- [Technologies Used](#️-technologies-used)
- [Installation Guide](#-installation-guide)
  - [Cloning the repository](#cloning-the-repository)
  - [Installing with installer script](#download-installers)
- [License](#-license)

---

## 🐺 Gray Wolf System  
is a lightweight web application built with **Flask (Python)**, designed to turn any Linux device (old PC, server, or even a Termux-based Android phone) into a local file server. Main features include:

- File upload and download
- Integrated viewers for images, videos, audio, documents, and text
- Category-based file organization
- Recent uploads preview
- Responsive web interface (HTML + CSS + JS)
- **Admin panel and user statistics**
- **Action logging system**
- **Simple user management and access control**

![Last commit](https://img.shields.io/github/last-commit/Rian-Batista-Rx4n/GWS)
![Repo size](https://img.shields.io/github/repo-size/Rian-Batista-Rx4n/GWS)
![License](https://img.shields.io/github/license/Rian-Batista-Rx4n/GWS)
![Top Language](https://img.shields.io/github/languages/top/Rian-Batista-Rx4n/GWS)

---

## 🎯 Project Goals

- Access your files remotely via browser (local IP)
- Organize files by type and category
- Repurpose old devices as personal servers
- Free up mobile storage by offloading files to server
- Provide a simple and clean web interface
- Enable the server to be used as an online backup
- Basic user management (admin / normal user)
- Simple logs and activity history

---

## 🚀 How to Use

1. Install and run the application on a Linux-based system:
   - PC, laptop, Raspberry Pi, old phone (Termux), or server

2. Run it using Python 3 with Flask installed.

3. Your server's local storage becomes accessible over your local network.

4. Access via browser using your server’s IP or: `http://127.0.0.1:8080`

---

## 🚧 Status: Beta v0.9.4

✅ Available Features:

- [x] File upload and download
- [x] Video playback
- [x] Image viewer
- [x] Audio player
- [x] Document viewer (PDF, DOC, XLS, PPT)
- [x] Recently uploaded files list
- [x] Show files only if public or owned by user
- [x] User registration system (Admin or Regular User)
- [x] **File deletion system (with user quota updates)**
- [x] **User statistics page (visible only to Admin)**
- [x] System logs (action logging system)
- [x] Deny some reserved usernames
- [x] **Logout system**
- [x] **Back button redesigned (icon in top-left corner)**
- [x] **Improved installer (setup admin on first run, update system without losing personal files/config)**

🛠️ Planned Features:

- [ ] Real-time chat
- [ ] Web Terminal (remote system access)
- [ ] Trash bin (soft delete / file recovery)
- [ ] Secure login system with hashed passwords
- [ ] Read and edit .txt files

---

## ⚙️ Technologies Used

- Flask (Python)
- HTML + CSS + JavaScript
- Local hosting on Linux / Android (Termux)
- Lightweight and minimal structure

---

## 🚀 Installation Guide

### Cloning the repository

```bash
git clone https://github.com/Rian-Batista-Rx4n/GWS
cd GWS
python3 main.py
```
### 🔽 Download Installers
- [🇺🇸 install_EN.sh](https://github.com/Rian-Batista-Rx4n/GWS/raw/main/install_EN.sh) — Installer script in English
- [🇧🇷 install_PT.sh](https://github.com/Rian-Batista-Rx4n/GWS/raw/main/install_PT.sh) — Script de instalação em português  
---
## 🧾 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
