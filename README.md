# Gray Wolf System (GWS)

A lightweight personal cloud and file management system built with Flask.

Gray Wolf System (GWS) is a web-based file manager designed to transform almost any device into a personal storage server.

Whether running on an old desktop, Raspberry Pi, Linux server or even Android (Termux), GWS allows you to organize, browse, upload and manage files through a modern web interface.

---

# Features

### File Explorer

- Folder navigation
- Automatic directory sorting
- Current path navigation
- Protected user root
- Create folders
- Create text documents
- Rename files and folders
- Delete files and folders

### 📤 Upload Center

Two upload modes:

- Upload directly into the current folder
- Upload using organized categories

Default categories:

- Audio
- Videos
- Images
- Text
- Documents

Each category supports user-defined subfolders for better organization.

### File Support

| File Type | Open | Download | Information | Edit |
|-----------|:----:|:--------:|:-----------:|:----:|
| Text (.txt, source code) | ✅ | ✅ | ✅ | ✅ |
| Images | ✅ | ✅ | ✅ | ❌ |
| Videos | ✅ | ✅ | ✅ | ❌ |
| Audio | 🚧 | ✅ | ✅ | ❌ |
| Other files | ❌ | ✅ | ✅ | ❌ |

### Storage

Every user receives their own workspace.

Example:

```
gwhome/
└── users/
    ├── admin/
    ├── rx4n/
    └── user/
```

Each new account automatically creates:

```
audio/
documents/
images/
text/
videos/
```

---

# Project Goals

Gray Wolf System aims to provide a simple, lightweight and self-hosted cloud storage solution.

Main objectives include:

- Personal cloud
- LAN file sharing
- File organization
- Old computer repurposing
- Raspberry Pi server
- Linux home server
- Android (Termux) server
- Educational Flask project

---

# Technologies

- Python
- Flask
- HTML5
- CSS3
- JavaScript

---

# Current Development Status

**v0.9.8 (Pre-release)**
This version is considered feature-complete for the core system.
Remaining work before v1.0.0 includes:

- Image thumbnails
- Audio player
- Video improvements
- Better file preview
- UI polishing
- Performance optimizations
- Code cleanup

---

# Installation

Clone the repository

```bash
git clone https://github.com/Rian-Batista-Rx4n/GWS.git
```

Enter the project

```bash
cd GWS
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

Open

```
http://127.0.0.1:7777
```

---

> *"Follow the Gray Wolf..."*