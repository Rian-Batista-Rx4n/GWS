# Changelog

All major changes to this project will be documented here.

## [0.9.7] - 2025-07-01

### ✨ Added
- File **filter system** in the interface for easier file organization and searching.

### 🛠️ Changed
- **Default server port changed from 8080 to 7777** (can still be configured manually).
- Started **reworking and improving the GWS installer** for better compatibility with different environments, including Termux.
- Adjusted the **"Back" button size** for improved usability.
- General **CSS visual improvements**, making the interface cleaner and more polished.

### 🐛 Fixed
- CSS issues that **made parts of the interface inaccessible** on certain resolutions.
- Bug that **prevented the STATS category from working on Termux**.

---

## [0.9.6] - 2025-06-21
### Added
- File information is now viewable in the Uploads section
- You can now edit .txt files directly in the browser and save changes
- Font size adjustment (increase/decrease) in the text reader and .txt editor
- Added a Logs button on the Stats page to view server logs
- Server resource stats are now visible: RAM, CPU, Disk usage, Uptime, and System load

### Changed
- Minor updates and improvements to the CSS (still in progress)

---

## [0.9.5] - 2025-06-14
### Added
- Text viewer system by category and type (e.g., organized access to .txt files)
- Ability to rename files (Video, Text, Document) through the interface

### Changed
- Minor CSS improvements and visual polish for better consistency and readability

---

## [0.9.4] - 2025-06-08
### Added
- **Logout system** with a button available on the homepage
- **System Status page** (shows memory usage and user stats, accessible only to Admins)
- Automatic creation of the **users.json** file when starting the system (`main.py`), requiring initial Admin configuration

### Changed
- **Back button** redesigned (now an icon in the top-left corner)
- Various **CSS improvements and visual adjustments**
- **Installer updated**:
  - Now allows setting up an Admin user during installation (no longer default `rx4n/rx4n`)
  - Now supports updating GWS without losing personal files or configuration

---

## [0.9.3] - 2025-06-06
### Added
- File deletion system (Video, Image, Document)
- Deny some user's name

### Changed
- Only admin can upload public files
- Directory name
- Private recent uploads viewer
- Updated links
- README.md

---

## [0.9.2] - 2025-06-04
### Added
- **Action Logging System**: 
  - Logs user login attempts (success/failure)
  - Logs file uploads and visibility settings
  - Logs error access attempts and permission issues
  - Stored as plaintext in `/GWLogs/*GrayWolf.log`

--- 

## [0.9.1] - 2025-06-01
### Added
- User creation system with role assignment (**Admin** or **Regular User**)
- Custom **404 - Not Found** error page
- Registered users are now stored in a **JSON** database
- File visibility control: only the **owner** of the file or if it's marked as **public** can view it

### Changed
- Minor **CSS** fixes and visual adjustments

---

## [0.9.0] - 2025-05-29
### Added
- Document viewer and download support (PDF, Word, Excel, PowerPoint)
- Installer script (`install.sh`) available in **Portuguese** and **English**
- Full English translation of the entire system (UI and content)
- More extensions alloweds

### Changed
- Internal improvements for easier setup
- Structure ready for future internationalization (i18n)

---

## [0.8.2] - 2025-05-29
### Added
- Support for selecting multiple files for upload
- Optimized video preview
- `CHANGELOG.md` file created

---

## [0.8.1] - 2025-05-26
### Changed
- Improved responsive styling with CSS
- Improved preview on mobile and other devices

---

## [0.8.0] - 2025-05-24
### Initial
- Beta release
- Support for file uploads
- Preview of Videos, Images, and Audio
- Download of uploaded files
- File preview in "Recent Uploads"
