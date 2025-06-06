# Changelog

All major changes to this project will be documented here.

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
