# 🐺 Gray Wolf System – v0.9.7 Beta

A personal file management system built with Flask, featuring audio, video, image players and more — all accessible through a responsive web interface.

---

## Table of Contents
- [Gray Wolf System](#-gray-wolf-system)
- [Project Goals](#-project-goals)
- [How to Use](#-how-to-use)
- [Status](#-status-beta-v096)
- [Technologies Used](#️-technologies-used)
- [Installation Guide](#-installation-guide)
  - [Cloning the repository](#-cloning-the-repository)
  - [Installing with installer script](#-download-installers)
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

4. Access via browser using your server’s IP or: `http://127.0.0.1:7777`

---

## 🚧 Status: Beta v0.9.7

### ✅ Available Features

- [x] Upload and download files
- [x] Video playback (MP4)
- [x] Image viewer
- [x] Audio player (MP3, WAV)
- [x] Document viewer (PDF, DOC, XLS, PPT)
- [x] Text file viewer (`.txt`)
- [x] Recently uploaded files list (per user)
- [x] Show files only if public or owned by the user
- [x] Rename files (video, document, text) — keeps owner/public prefix
- [x] File deletion system with size tracking per user
- [x] User registration system (Admin or Regular)
- [x] System logs (user actions, access attempts, uploads)
- [x] Reserved usernames protection
- [x] Logout button (top-right)
- [x] Back button redesigned (top-left icon)
- [x] System Status Page (shows memory & usage; admin-only)
- [x] Installer with admin setup and update mode (no data loss)
- [x] Edit `.txt` files directly from browser
- [x] Add base rename logic improvements
- [x] Info button to view file metadata
- [x] Enhanced system stats page
- [x] **Log Viewer page** (linked from admin stats panel)

## 🛠️ Planned Features (Coming Soon)

- [ ] **Start development of real-time chat**
- [ ] **File permission system** (similar to Linux: read/delete/upload control)
  - Add new "Guest" user level (view-only)
- [ ] **Per-user storage quota configuration** (e.g., 50GB per user from 1TB)
- [ ] **Edit documents online (DOC/XLS)**  
  - Investigate possible APIs or JS-based editors (especially for Excel)
- [ ] **Improve security**  
  - Basic brute-force protection  
  - Optional login persistence or 2FA/email verification
- [ ] **Better video support** (MKV and other formats)
- [ ] **Add search, filters, and sort by name/date/size**
- [ ] **Admin web terminal** (remote control of host machine)
- [ ] **Trash bin system** (soft delete with restore)
- [ ] **Music player UI** for `AUDIO >> MUSIC`  
  - Style similar to YouTube Music or Spotify

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

```bash
chmod +x install_(LANGUAGE).sh
./install_(LAGUAGE).sh
```
---
## 🧾 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
