# IWantLinux

**IWantLinux** is a simple, beginner-friendly tool for Windows that helps you get started with Linux. Choose a distro from a curated list, and IWantLinux will download it and write it to a USB drive — ready to boot.

Supported distros:
- Linux Mint
- Ubuntu
- Zorin OS
- Pop!_OS

🌐 [iwantlinux.com](https://iwantlinux.com) &nbsp;|&nbsp; 📦 [Latest Release](https://github.com/njcabral/iwantlinux/releases/latest)

---

## ⚠️ Beta Notice

IWantLinux is currently in early/beta release (version 2026.02.20). It appears stable based on testing, but you may encounter issues. Please [open an issue](https://github.com/njcabral/iwantlinux/issues) if you do.

---

## Requirements

- Windows 10 (build 1809 or higher) or Windows 11
- A USB drive of 8GB or larger — **all data on it will be erased**
- An internet connection to download the ISO

---

## How to Use

1. Download and run **IWantLinux.exe** from the [Releases page](https://github.com/njcabral/iwantlinux/releases/latest).
2. When prompted by a UAC dialog, click **Yes** to allow the app to run as Administrator (required to write to the USB drive).
3. Click the tile for your chosen Linux distro, then click **Next**.
4. While the ISO downloads, plug in your USB drive.
5. Once the download is complete, confirm that IWantLinux has identified the correct USB drive.
6. Check the box that reads *"I understand that my files on this USB drive will be erased"*, then click **Next**.
7. Wait while the ISO is written to the USB drive.
8. When it's done, restart your computer, boot from the USB drive, and enjoy Linux!

> **Note:** IWantLinux must be run as Administrator. The UAC prompt will appear automatically on launch.

---

## Building from Source

If you'd prefer to compile IWantLinux yourself:

**Requirements:**
- Python 3.10 or higher
- pip

**Install dependencies:**

```bash
pip install PySide6 requests wmi pywin32
```

**Run the app:**

```bash
python IWL.py
```

---

## Versioning

IWantLinux uses date-based version numbers in the format `YYYY.MM.DD`, corresponding to the date each release was built.

Current version: **2026.02.20**

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please visit the [issues page](https://github.com/njcabral/iwantlinux/issues) to get involved.

---

## License

IWantLinux is licensed under the [GNU General Public License v3.0](LICENSE). You are free to use, modify, and distribute this software, provided that any derivative works are also distributed under the GPL-3.0 license.
