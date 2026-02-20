# IWantLinux
# Copyright (C) 2026 Nathanael Cabral. Licensed under GPL-3.
#
# This program is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation; either
# Version 3 of the License, or (at your option) any later version.
#
# This program comes with ABSOLUTELY NO WARRANTY!
# However, it has been tested repeatedly and found to be safe and effective.

import sys
import os
import shutil
import time
import ctypes
import wmi
import subprocess
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QStackedWidget, QPushButton, QLabel, 
                               QFrame, QProgressBar, QMessageBox, QComboBox, 
                               QCheckBox, QGridLayout, QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal, QSize, QObject, QByteArray
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QPixmap

myappid='njcabral.iwantlinux.2026.02.28'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
# --- Configuration & Constants ---
APP_NAME = "IWantLinux"
APP_DATE = time.strftime("%Y-%m-%d")
WEBSITE_URL = "iwantlinux.com"
GITHUB_URL = "github.com/njcabral/iwantlinux"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 660
DOWNLOAD_DIR = r"C:\IWantLinux"

# Beginner-friendly colors
COLOR_PRIMARY = "#4A90E2"
COLOR_BG = "#FFFFFF"
COLOR_TEXT = "#333333"
COLOR_SUCCESS = "#2ECC71"
COLOR_WARNING = "#E74C3C"

# Supported Distros (Using official or reliable mirror links for the example)
DISTROS = [
    {
        "name": "Linux Mint",
        "desc": "The friendliest starting point. Feels familiar if you're used to Windows.",
        "url": "https://pub.linuxmint.io/stable/22.3/linuxmint-22.3-cinnamon-64bit.iso",
        "logo_b64": "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"
    },
    {
        "name": "Ubuntu",
        "desc": "The world's most widely used Linux. Huge community, tons of tutorials.",
        "url": "https://releases.ubuntu.com/24.04.4/ubuntu-24.04.4-desktop-amd64.iso",
        "logo_b64": "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAANY0lEQVR4AdRaCXhTxRb+J12B0kKbFMpOW0BFEVBAPgVXaIrCQ4WHKLiAbPoQcWEVROChIiL4VDZ5fIAigiiy2FRcQFxweYLKY+vK1tI2gZbuW+adc2lC0tykvUmKvnxz7sycc+bMzH/nzpyZiQ4N/EtJbGlIS9DfnWY0zExNMKxPM+q/IUoh3gWKq4gkUSlRTlqi4Y/UBP1naYlRy1IS9I+nJ0Rf38DNQ4MAkGY03JKWqH+VOnlQJ6tyIbALkIuEkA9Th/oRxROvGcUBRBxC6RENKa8VAomQYopOYI0U1kNpRn0O0cb0RMMw0vF78BsApxPCIzMSo6bTGzxCnd0PiWnUye5+aHE02RglpdxKQFiIXk8bYOhEPL8EnwE4PriVPt2oX1yO4HNWKV6hN3i1X1qmbiSS2M8gQJ4goFcfG9iiI+V9Cj4BQG/jmYDKigwJPE8dD/KpJRoLU33jgnTV6alGwwsaizqpewVAZqKhR3qifh9Zel0AYRT/aUFALiAQfkgzRvXyphGaAUg16idUS/mrlOjvTYUNUYZAuAkQP2VQ26DxpwkAGvL8xldqrOOKqVuBlfSCXtNSYb0BoM5vJMPPEP2lA32Sz9HnsK6+jawXANT5LWRwFNEVD00HPoi27x5AbFIe2m8+CsPTyxBy1Q11tEM8SiNhUx1KirhOANKN+g2kOZzoigfuvGHqcgS1jlPqDojQo2nCQ4h5eRsa32RUeO4eNBJGpiVErXUnt/E9AkBv/nVa4kbblK9krGvaHJFjX1StUhfaBM2GT1aVOTGFGJNmNCxy4tXKuAWA3NiJpPunffMRQx5HQHgkNUE9hF7TW13gwpUzU41Rj7iwaxiqAKQN0t9IbuyKGh2/RgHNDAjp3B1Nbr4HEfdORMR9kxB261A06nYzgtp2gi6MtwhAZVa63+oVEKsyBkZdpWZQFQBplW+qKXvLa9x7IPhbbv/hcbT/4AhaL9+DFi+sQ9T4BYgaNx/RM9Yg5tXtaLv6e3TYmoLg9l1QeSbVY3UlPyZ7lNcShkideKMWT8m6AJBmjJpJiPVVpD4+gjt2VWbvli+9D57QPA1px6rC7hyB8pTfcDGJ519HyeV00f5PL2fqkaK5zEgrw4Taqk4ApA6MbCsh5tdW0poPu32YUqQi478o2Pa2ktbyaHrXCGUUmN98FvlblkOWldiLy/JSXHhvMYq+3Grn1TchgHkpifEhjvpOAAhdwAxSCnRU0JqOnrYCTOGDeOsPFOx4F9UX8jSZCWgejeiZaxUQzq9biMwHuiB7+lCFMkd0xoX3NTl7jnW3FNb8aY4MOwDpg5q1B+QTjkKt6Q5bTsD29sOHjFeKV+WeQcH2VUpay4PnAQaB54lG3fuj9PfvUHH6BIJaxWkx46or5JSvb4P9JdsBgAy41GLXIvXitJi1Frx225S5A5GPzVGyF3evQ0XmUSXNj9Jf9ypDmD+PizvXovTQN6iyZLPIidgGrxQt570PxRPcdARt3tmLqAn/dNLTkhEQUe0aRY2zlbEDQIcZj9qYWuPwwWPRpN8Ql2LNhv1DAcVafBEXd62DZcUsZP69M7JnD0fukidgeXcezO/MQPbM+3FqVDecGt0NOfMfRvnxX11sOTIiho4H1+nI05IWUmd37hQAyOm5WwCttBix6YZe2xf6J16xZZ1jnQ5RNd4cj4KCHWtgLbzgrOOQqzJno/iHJGQ9Nxg80cmqCgepc5Lr5LqdufXLSci+KQmRXVlbAUAKuL4+ltaDmo+c6laLO2RZM9et3J2AO84THQPBgLjT81S3uzI2vk6IwZxWAKDHAM5oJfbiGvW8XbUYf/PZ04aAh7+qQj2Y/CnkLp6I8rQ/VLW5bm6DqrBOplD6rEtJjI6TgObDRREQiIi/jVetRlZVwrJqNiqzM1XlWpjsA7A/wOu/WrmIwY9DBPOpuprUI6//luEI0AnIGz2quRGG3TEMgdFtVKWW1XNoZt+vKvOGWX7iIMxvOy3fdjOBLdvRvuJue15DIrBHUWQvnU5ar9VQyK5qW+/tjJoED1te2mqyfosK92xG0b5PVO3xxkpVUAeTVoNuOgkR70lPBIWADyRCOvcA7+RsuvwJ2NKOccnPXzhm/Zou+019VDEAtl2klgpp5etC8x/auivEW9S2a38EH0m1Xv65spOLnrFaUee1vIy8MyXj8PC0gXFQ8ypZdvQ/bssFxZAj61bqTiA6MAAGqPzYC4uhLWqgobWTNOzWe8kTWwie6M6vdz5sqco7i+rzOU76/sxUZB5B2eEDqiYDW2oHgEZADAMQrmZR/9RSNbbCixg6QTmTq8g4ouRtj7r28DY9X2KeEHnk1aaglh00myWHKIoBcNoe2qwEtfE4NSCIELeWFjkdXFwJANixyqKdYW3K36p+hmPrj1pMIyCMAahSE8KDG8r69nWZrog4//9Ikra/DMBFtcbziYwa38arPHdSObTkczwbr65RY9PzJTbQvQDvDGsTH5drtSskLuroltWsVtCyyv2la/H3u1F6cB9Cr7/FqWhDAyACg+DuNLjKC6+T9kBmnZQiy6kXNRl2Y3l7WvzdrhoOwCe1ecunImfBowi9+kbwGYBdSAleMdw1kMQ+h9CufZSTYzVDVXmq3VBTtfNoBGTRJyAz7JxaCd7N5Sx8DJnD4nHmydtxemwfFJreU7RaLU1S4tqPxn0Ta7P8lg+9po+qreoCC6rM2gGQQmTQCMAxVasOTGtxASrSDztwQAcc/3bK2zJN6riysul5E4d2Vb8M4VEqK8s1m5SwHqM5QB7SXJIKFO3bTk/XwPNA1KRFrgIfOZFj5qLRDXeoWmEAVAV1MK3Vut90cSbLz6RXRqQplB3+we3RVcSQcWA3WpNBD8pNB4yEu7tAdoz4jNFDcVWRBAo778k7RHMAQFviffDiV/DppX2BWtGYV7eDb3PVZFp4IfHdoH9ysdsi+Vv/5VbmSUAd38tyioFqiM85o5WKvt4GT8OP7/N9GQnhgx5BiznrIULUDzwKkzai+NudWput6FulVPqsACCk2KFwvXgUbHvHY6mQet/iXjYT0qUnWszdAP3kJW4PXSqzMnBh89LLhTSmRLVV6bMCQHxyXiqV/4pIcyg7+jNq7wptRsqO/oLC5EvLZlPjaDR/6HmEdOpuE9tjERCA4Ljr6FLlfkWn1ZKdaFLHcspHbnzpAi9+EjI57osLp7ioAgAnhJDrOfaG8je/geLvP3MpWvj5JvC1mAgIRORjs9F81DS0fnMPOu7MQrsNh5R0m1XfoeOOs2jz1ld0pbZS0RGBwS62ePdXmZ0BXu4sK2eh5Kc9Ljr1ZQgIe1/tAMQmWTaQgZNEXoWcBY/A8TCEr68LTRsVW80emIqA8CglzQ9BLi17jTwagtt1BnQBzHah4v07cO6l0ci4tz1493d6TG9kDGmDgk/XuOjWmyGQEmcyf2DTtwOgMASWwYcfn97yzQ6b4EtRjtkv4DfPaS3Enc9ZNBYlB0wIpeM4/nyYQskd1mLHRVdKpz46ARCXZGbhcZdCGhh8kXFq1HWwrc3NR2r/l01lVjq481wt7zd4SWUQmVot2YXo6e4vW7mMWxLicJzJ4jRrOwHABck1fJFjX6jKck4p3rj3AATSsbWS0fAo+eVLRdswdbnqnWPYbfcpk6WipOUhrS59cwGgY1Leh2TT/o1Q2uvAE1XWs/fgzMR+yP/oLZoQcz3aspYWozz1d+RvXoZGPW4F/6vEXYHGve5yJ1LlSyk20Nv/uLbQBQBWaCwCp1B8lsgvoeLkMZxf+xJOPtgVJ0deg7NTBoB3mXyBwjfG5+Y8oOw0M+/rgLOT71SACorxfMbHvkJ9GycgMksCK55W01cFICbpXB4kJqgV8JVXnZ+H8hOHwB5kwScrwTfGPOT5u3e0bS0pdMz6lhbVE7rtLlC9llYFgGuLSzbvpk2C+6tfVmpAKtr7sQKUuyoYPHcyR76UcnJs0nnF7XXk29JuAWCFOGVVEC9z+s+g82vnqVZbcfK43cNUVahhSoEF8cmWt2qyqpFHALhEnClvFsXeO91U2NtQSjdPZ5+6S3Gw+IiO/1xR9PVHyH15LBgET3ap84vjk8xzPemwrE4AWCnOZH6WXGX/n3Kw8TqIT6fZwTo9phf47zW5iyfV2Xmav+ZT56fXYVoR1wsA1oxNsszWSaE6k7L8r0L8zdP85bLeu2tfvQFgAx2T85YTuvcIQPsJJBtoWDqtg85Y1zdfuwmaAODChO5uBOt6SmAL5/8SJLCpKii4Z0dTbrLW9mgGgCuI3ZGbE28yjxCQo2k0uD1WZ90GJj7HeJBWq4e67Mwye1OXVwDYKoo1Wd6LNZljATmTeJ79XFLwYzhHwE+jybkTkU9uu08A2DoUZ7K8EnuTOQZC8l9tf7Lx/R1LiAMSmBhnMsfEmsyv+cO+XwDghoh5sMYlWVZQ4/pUV4seQmIu8b8l8jXslxBzBHTXx5vy+tKn5+VeGKo/vwHgaJ3P22OTzQsIjH45BaGNhRT9a0bHG/S5fCSAfUQHhcRRhYCD8hJvK9lZSivNJED0s4pmoWSjP3V8Yawp93eo/Hxl/Q8AAP//3MnU9AAAAAZJREFUAwDZ9pLTANr56QAAAABJRU5ErkJggg=="
    },
    {
        "name": "Zorin OS",
        "desc": "Polished and lightweight. Great for older or slower computers.",
        "url": "https://mirrors.edge.kernel.org/zorinos-isos/18/Zorin-OS-18-Core-64-bit-r3.iso",
        "logo_b64": "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEW0lEQVR4AexZXYhVVRT+1nGUsaKEiB6CHoKCJogSCnoInJeITHLCe2eiBxl8DKzphyIfRnsoi1KJiIokkH6cO1KREEQPV1BEUFEQUfBBZEBERQZBRWFm+e17nLlzftC7977nnnPm3sP+7j5r3bX32utb69x7zj4BuvzoEdDlBQD/CvhDVyFPeGbQj4A9uhFLUM8VE/qBDwfuBNS1H7PY5uO8LWMFX2Gv3uc6lzsBl7CVTpcQebcA1/Gd6yLcCKjpAB2+SxSjCUaxR593WYwbAXBn3GWRLY2ZxQ8t2cWM7AmY1Nc5xyBRtPYiJnXEdlH2BCh+t3XSMXvFz7a+7AiY0M1Q/vIrtrAvIr5mFYzbkGBHwLBsRtFRkS3ZEWAzc0ls7SqgJEHZLLPrCIiT0yMgzki3yb0K6LaMx+PtVUCckYZsnvYmtc67qihqKbo0u4U6lzFm/ISubazF52O3vjcfw259Om2q9ApQbOWt7qoEgKRO76GzHQMcRx+GeMf5N1yPmj6Hmv7FDb/t8zEE+CJtuiQBNV0NwZo044x1x7nYIVRkDEMy7ezLZB2oc3y8gt5gNbxCfaQlCQC+jFh0QhDswFIMYljak3VgBdIORaIKogRM6Dsc9wzRqZZ11uNxrOSlsWGhsklAXfsg2L7wy0zPO5X1ZBCRKmgScJm7q2AhJge0W9PprMfX/wjMvsYdbdDof9MnoRhrnGf5kV/Wo1EJxvGrPmiUIQFLkXXp5511E2sUy7izRU3AH4VX2a8msmlFyXoyug2MfSCA4Nvkd23RFCLr94hkW0CD/4n2tuJmPR6nBujHR3Gth1yGrDfDCzAWYI1c52Wwqal1PCtP1sMABT9inZw2lwBQkc+pvUK4tHJlfS7CO3/7IQFGKfjQdFYoW9bnghN8iqrcMGKTgIr8QsUJopVWzqyHkU2x4udvh5sEmC8Vn5jurihr1ptBRWKMEjAs/9LuPyKtlTnrc/HsZ+lHXu5GCQjNkv8I5c96GJkkKzxJQFWOQrGLf437GlAM8Zrx36Uxj9qCFRCE83a+38U4DiJ2JAkwBsOynsaDDfjs0pi5DEZkR2OuioRz5tOvN0uJI52AuNUilnsELOLkthRarwJaoqlERrZL7VWALWOLzb5XAVYZNfvpZYBFUHYVIJjirex4wbHXIn7YEVCVnQz+pI2DjtoK/uTT3lEbn3YEmJlnMGq6QuIW3rddlz0BI3KYTnYSRWs/4W05Z7soewKMh2sO+4dmXJZYDqd3m24EjMo0XDZRsyPgs8b2vsP8bgQYRxX5ht1pIt8mmOYP3zgcD3cCQocfh12un5t8vPsRUJV/6LwPF9CP5bgfD+Ahyg+jD49iBo9hGR6n/AQCPIVZDPD8WepXUn6B8kuUX6Y86IWKfM95nJsfAcZtVWawUW7CvGJ7Ta6iKlfwplzEW3Iea2WK8lmskzMYkVM8P0H9McpHKB+ifIDyPi/A7/AnwM9/7qNLT4Avg7cBAAD//6IKuUkAAAAGSURBVAMAZl0OrmOm3TMAAAAASUVORK5CYII="
    },
    {
        "name": "Pop!_OS",
        "desc": "Made for developers, creators, and gamers. Powerful and modern.",
        "url": "https://iso.pop-os.org/24.04/amd64/nvidia/23/pop-os_24.04_amd64_nvidia_23.iso",
        "logo_b64": "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFiklEQVR4AeyYZ4glRRDHR/GDWUFMiAkEs4giJjAhcgZEMGHCcJ9UUMzhzFlRMSEqKmJExHRiPDPmgFlMX0QQxZxFRf39hq6lr3fe7nvs24WbN0v9u0L39puprqrunoWrEf/rHDDiAVB1EdBFwIh7oEuBEQ+Argh2KdClwIh7oEuBEQ+AbhcYuRQoI75zQOmRUdO7CBi1FS/ft1cE7MjAO8Gz4EFwGdgGtI5KB2zNG34I5oH9wLZgd3AseA7okGXgraHcASfyVi+AdUEv0iFP07ksaAXpgEV5k4fBxaAf2oRBd4CZoD34kV/Bf+ADYFTChkc64Eqm2wXk9B7KQuBo0ESOX6+pY8i2U5lvCSD5e9al5VSGBR2wT8NkHyXbVfCTQBMd1WTsw2aKmW6nMNb6siS8F21WdPyM/hsYGumAtxpmWyezXYL8Mihpq9LQh34BYyyyppuyO8wv2C4EJa1SGtBNvT/hQyMd4CqXE26IYXUQ5MOGHHyFEAquY6wrhblaDYOrDhtHJ2O5HOS0Zq4k+YbEh8Z0wAPM9ioo6bDM8Ewmh/hHCIkfBzc8X4R/D84HOa2VKUbBrZmueAzNRiCojIDn6XgbDJV0gBOeZVPgBPRYZV8MdT56P9P2R74ULA6kxWgsYFfAg34PAa7TD4afAXLaIVNWzWTF422GjXDAY0xceteXuA27B5/N4SXdnhlOz+RcdBfZNBnczpJY/ZsEt98k1ixPnXC+HXfRvA6GTuEAJz7bpsBO6O6/r8BzMhzvTgZDOy+aZcE8II2z2CWxiq1sjTAkHruP6lI2Cb12otTdm03WkzvAsHyn4R/KXPyUMXuCIAtmyK64RdAVC9usJOQO0GGu9pmpT/YTzeMgKKLkcAxfgGmh3AH+wBybCWCqeF/4NhsTBxVNHqXl59kkuO8rWhjlYnsai2he9NwatdFVk0dua8h1tTZNTekAc/K1ht8yNHfDvjP4BuT0T6Ysn+S/Eg8Wd4f8BaPPlT8HpTwL3IvNnQE2fVQ6wF/ylCbP8TeKzoGNI50TRiu/cr6Fqkc4/6gCLIhug55CdU6eCnRXK9J4A7UQI04fNTnAa+8jxU+a5+WxNIa4e7iK6n4zMNfzA4/bn0dY+yN1PkNxG7wH3kSuvt8gjmzqnMC2MX0e7B6Fmzp5imGq9qLxMDUX7lF+6SYH0Fd5MpPnmJ0rhewRNUzl2T7qgv0/2AAvWrCeFA7N60bPwanDl/MQ5pnlWmxGm3XE2ytqZXSei2AkewF0Aeb0coC3QT3I+DHad0waLzjxl+PNtcXiVgs0XwMpUkK5CQdiNOJuhvdLvvQhDDb6HoK7iNfAbwLSdjTuMt4/nkL28DevlwPor06j0YuwmszVfPurjan5Ch5nBsSaDHejxlWoDTThpKZiSPcYGSlvjGmTC16VLcB+ycpHP4FiWsAqF9Rt2me1/qyM8aWJHPAdA8riFIcausaRB6YNsK4NVgI+ULmC4YC8cDJ0yrRIjxn8kBJd9yF4wXO3cXEuQr9+IgfQX1lQPlZIyM/qyTSOfYIlQh1xPvJS5SpdPZ916oqHM+uGEZfP5m5kFGi7kcbFMf/dYbzrzJrMAfxPtTeNk8Oq3KPqg8LzvKniztHv/5p25msTfAnnMaUORfBC9mTi/pbbbIxxJ3P1Yx4vV3P7cYAFcQsm9fLj53LEGSVz2ALWC3ESvZ+n8oT5OXx9oAO2hL8LJL8+GX0xzy0YZ/fjAMZV5uxBCG+CmSZvmvHQJd+Vh3Hbg9XkZ3vTwBPrEVj87gCrybR0h4g56t2pXwfUM7Sx6RzQtlUd9H26CBjUY20b30VA21Z00PfpImBQj7VtfBcBbVvRQd+ni4BBPda28V0EtG1FB32fLgIG9VjbxncRsKCv6FSf/38AAAD///z6PI4AAAAGSURBVAMA4nrkgTPfigUAAAAASUVORK5CYII="
    }
]

# --- Worker Threads (Background Tasks) ---

class DownloadWorker(QThread):
    progress = Signal(int, int) # downloaded_mb, total_mb
    finished = Signal(str) # path to file
    error = Signal(str)

    def __init__(self, url, dest_folder):
        super().__init__()
        self.url = url
        self.dest_folder = dest_folder

    def run(self):
        import requests
        try:
            # 1. Clean/Create Directory
            if os.path.exists(self.dest_folder):
                try:
                    shutil.rmtree(self.dest_folder)
                except Exception as e:
                    self.error.emit(f"Could not clear folder: {str(e)}")
                    return
            os.makedirs(self.dest_folder, exist_ok=True)

            # 2. Start Download
            local_filename = self.url.split('/')[-1]
            if not local_filename.endswith('.iso'):
                local_filename = "linux_distro.iso"
            
            full_path = os.path.join(self.dest_folder, local_filename)
            
            response = requests.get(self.url, stream=True, timeout=10)
            response.raise_for_status()
            
            total_length = response.headers.get('content-length')
            
            if total_length is None: # no content length header
                self.error.emit("Could not determine file size.")
                return

            total_mb = int(total_length) // (1024 * 1024)
            dl = 0
            
            with open(full_path, "wb") as f:
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    current_mb = dl // (1024 * 1024)
                    self.progress.emit(current_mb, total_mb)
            
            self.finished.emit(full_path)
            
        except Exception as e:
            self.error.emit(str(e))

class BurnWorker(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, iso_path, drive_letter, physical_drive_path):
        super().__init__()
        self.iso_path = iso_path
        self.drive_letter = drive_letter
        self.physical_drive_path = physical_drive_path

    def run(self):
        try:
            if not os.path.exists(self.iso_path):
                self.error.emit("ISO file not found.")
                return

            # STEP 1: WIPE THE PARTITION TABLE
            # We must force Windows to release its grip on the "weird" Linux partitions
            # currently on the drive.
            self.progress.emit(0) # Start at 0
            
            # Extract the disk number (e.g., from \\.\PHYSICALDRIVE2 -> 2)
            # This regex finds the last number in the string
            match = re.search(r"PHYSICALDRIVE(\d+)$", self.physical_drive_path)
            if not match:
                self.error.emit("Could not determine disk number.")
                return
            
            disk_num = match.group(1)
            
            # Run the wipe
            wipe_success, wipe_msg = self.wipe_drive_with_diskpart(disk_num)
            if not wipe_success:
                self.error.emit(f"Failed to clear drive: {wipe_msg}")
                return

            # Short pause to let Windows refresh its device list
            time.sleep(2)

            # STEP 2: RAW WRITE
            iso_size = os.path.getsize(self.iso_path)
            
            with open(self.iso_path, 'rb') as iso_file:
                # We open the physical drive again. Now that it's "Clean", 
                # Windows treats it as a raw, empty device with no conflicting handles.
                with open(self.physical_drive_path, 'r+b') as device_file:
                    copied = 0
                    chunk_size = 1024 * 1024  # 1MB chunks
                    
                    while True:
                        data = iso_file.read(chunk_size)
                        if not data:
                            break
                        device_file.write(data)
                        copied += len(data)
                        
                        percent = int((copied / iso_size) * 100)
                        self.progress.emit(percent)
                        
            self.finished.emit()

        except PermissionError:
            self.error.emit("Access Denied. Please run as Administrator.")
        except Exception as e:
            self.error.emit(f"Write error: {str(e)}")

    def wipe_drive_with_diskpart(self, disk_num):
        """
        Robustly wipes the drive using diskpart with retries.
        """
        max_retries = 3
        
        # We use 'noerr' to prevent script abort, but the text output 
        # still contains the word "error", which we must ignore.
        script_cmds = [
            f"select disk {disk_num}",
            "attributes disk clear readonly", # unlock read-only drives
            "online disk noerr",              # ensure it's online
            "clean",                          # THE IMPORTANT PART
            "rescan"
        ]
        
        script_content = "\n".join(script_cmds)
        
        # Temp script file
        script_path = os.path.join(os.environ['TEMP'], f'iwantlinux_wipe_{disk_num}.txt')
        
        last_output = ""

        for attempt in range(1, max_retries + 1):
            try:
                with open(script_path, "w") as f:
                    f.write(script_content)
                
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                process = subprocess.Popen(
                    ["diskpart", "/s", script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    text=True 
                )
                stdout, stderr = process.communicate()
                last_output = stdout + stderr

                # --- IMPROVED SUCCESS CHECK ---
                # 1. Did it explicitly say it cleaned the disk?
                if "This disk is already online" in last_output:
                    return True, "Success"
                # 2. If not, did it fail?
                # We wait and retry.
                time.sleep(2)
                
            except Exception as e:
                last_output = str(e)
                time.sleep(2)
            finally:
                if os.path.exists(script_path):
                    try:
                        os.remove(script_path)
                    except:
                        pass
        
        return False, f"DiskPart failed after {max_retries} attempts.\nOutput: {last_output}"
        
# --- UI Components ---

class DistroCard(QFrame):
    def __init__(self, name, desc, base64_data, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("DistroCard")
        # Fixed size for grid consistency
        self.setFixedSize(250, 180)
        self.setStyleSheet("""
                #DistroCard { 
                    background-color: #fcfcfc; 
                    border: 3px solid #e0e0e0; 
                    border-radius: 15px;
                }
            """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        # 1. Logo Image
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(64, 64)
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        # Decode Base64 to Pixmap
        if base64_data and len(base64_data) > 50: # Simple check if data exists
            byte_data = QByteArray.fromBase64(base64_data.encode())
            pixmap = QPixmap()
            pixmap.loadFromData(byte_data)
            # Scale it smoothly to fit the label
            self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Fallback if Base64 is missing (Gray circle with letter)
            self.icon_label.setText(name[0])
            self.icon_label.setStyleSheet("background-color: #ddd; color: #555; border-radius: 40px; font-size: 30px; font-weight: bold;")

        # 2. Distro Name
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font-size: 18px; font-weight: 800; color: #2c3e50; margin-top: 5px;")
        self.lbl_name.setAlignment(Qt.AlignCenter)

        # 3. Description
        self.lbl_desc = QLabel(desc)
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setAlignment(Qt.AlignCenter)
        self.lbl_desc.setStyleSheet("color: #7f8c8d; font-size: 13px; line-height: 1.2;")

        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_desc)

    def set_selected(self, selected):
        # Using ID selectors for precise styling
        if selected:
            self.setStyleSheet("""
                #DistroCard { 
                    background-color: #ffffff; 
                    border: 3px solid #4A90E2; 
                    border-radius: 15px;
                }
            """)
        else:
            self.setStyleSheet("""
                #DistroCard { 
                    background-color: #fcfcfc; 
                    border: 3px solid #e0e0e0; 
                    border-radius: 15px;
                }
                #DistroCard:hover {
                    background-color: #f0f7ff;
                    border: 3px solid #b3d7ff;
                    transform: scale(1.02); /* Qt doesn't support CSS transform naturally, but the color change works */
                }
            """)
            
class Page1_Selection(QWidget):
    distro_selected = Signal(dict)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        title = QLabel("Choose Your New Operating System")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #1a2a3a; margin-bottom: 5px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Select a version of Linux to get started.")
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # GRID LAYOUT for cards
        grid_container = QWidget()
        self.grid = QGridLayout(grid_container)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignCenter)

        self.cards = []
        
        for i, d in enumerate(DISTROS):
            # Pass the base64 string here
            card = DistroCard(d['name'], d['desc'], d.get('logo_b64', ""))
            card.mousePressEvent = lambda e, data=d, c=card: self.select_distro(data, c)
            
            # Smart Grid Placement (3 columns max)
            row = i // 2
            col = i % 2
            self.grid.addWidget(card, row, col)
            self.cards.append(card)
            
        layout.addWidget(grid_container)
        layout.addStretch()

    def select_distro(self, data, active_card):
        for c in self.cards:
            c.set_selected(False)
        active_card.set_selected(True)
        self.distro_selected.emit(data)

    def clear_selection(self):
        for c in self.cards:
            c.set_selected(False)
            
class Page2_Download(QWidget):
    download_complete = Signal(str) # Path to ISO
    request_start_over = Signal()   # Signal to tell Main Window to go back

    def __init__(self):
        super().__init__()
        self.current_url = None # specific URL we are trying to download
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Status Text
        self.status_label = QLabel("Preparing...")
        self.status_label.setStyleSheet("font-size: 18px; margin-bottom: 10px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        
        self.info_box = QFrame()
        self.info_box.setStyleSheet("background-color: #f0f8ff; border-radius: 8px; padding: 15px;")
        self.ib_layout = QVBoxLayout(self.info_box)
        self.info_lbl = QLabel("ℹ️ While you wait, look for an 8GB or larger USB drive and plug it in. Make sure there's nothing on it you need to keep.")
        self.info_lbl.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 14px;")
        self.ib_layout.addWidget(self.info_lbl)
        
        # Progress Bar
        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(30)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("""
            QProgressBar { border: none; background-color: #ecf0f1; border-radius: 15px; }
            QProgressBar::chunk { background-color: #4A90E2; border-radius: 15px; }
        """)

        # MB Counter
        self.detail_label = QLabel("0 MB / 0 MB")
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setStyleSheet("color: #7f8c8d; margin-top: 5px;")

        # --- Error Handling Controls (Hidden by default) ---
        self.error_widget = QWidget()
        err_layout = QHBoxLayout(self.error_widget)
        
        self.btn_retry = QPushButton("Try Download Again")
        self.btn_retry.setCursor(Qt.PointingHandCursor)
        self.btn_retry.setFixedSize(160, 40)
        self.btn_retry.setStyleSheet("""
            background-color: #4A90E2; color: white; border-radius: 5px; font-weight: bold;
        """)
        self.btn_retry.clicked.connect(self.retry_download)

        self.btn_start_over = QPushButton("Start Over")
        self.btn_start_over.setCursor(Qt.PointingHandCursor)
        self.btn_start_over.setFixedSize(120, 40)
        self.btn_start_over.setStyleSheet("""
            background-color: white; color: #7f8c8d; border: 1px solid #bdc3c7; border-radius: 5px; font-weight: bold;
        """)
        self.btn_start_over.clicked.connect(self.request_start_over.emit)

        err_layout.addStretch()
        err_layout.addWidget(self.btn_start_over)
        err_layout.addWidget(self.btn_retry)
        err_layout.addStretch()
        
        self.error_widget.setVisible(False) 
        # ---------------------------------------------------

        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addWidget(self.pbar)
        layout.addWidget(self.detail_label)
        layout.addWidget(self.error_widget)
        layout.addWidget(self.info_box)
        layout.addStretch()

    def start_download(self, url):
        self.current_url = url
        
        # Reset UI State
        self.error_widget.setVisible(False)
        self.pbar.setVisible(True)
        self.detail_label.setVisible(True)
        self.pbar.setValue(0)
        self.status_label.setStyleSheet("font-size: 18px; margin-bottom: 10px; font-weight: bold; color: #2c3e50;")
        self.status_label.setText("Downloading Linux...")
        
        # Start Worker
        self.worker = DownloadWorker(url, DOWNLOAD_DIR)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def retry_download(self):
        if self.current_url:
            self.start_download(self.current_url)

    def update_progress(self, current, total):
        if total > 0:
            pct = int((current / total) * 100)
            self.pbar.setValue(pct)
        self.detail_label.setText(f"{current} MB / {total} MB")

    def on_finished(self, path):
        self.status_label.setText("Download Complete!")
        self.detail_label.setText("Verifying...")
        self.download_complete.emit(path)

    def on_error(self, msg):
        # Stop loading animation
        self.pbar.setVisible(False)
        self.detail_label.setVisible(False)
        
        # Show friendly error
        self.status_label.setText("Oops! The download was interrupted.\nPlease check your internet connection.")
        self.status_label.setStyleSheet("font-size: 18px; margin-bottom: 10px; font-weight: bold; color: #E74C3C;")
        
        # Allow user to see technical details if they hover (optional, good for support)
        self.status_label.setToolTip(f"Technical Error: {msg}")
        
        # Show Action Buttons
        self.error_widget.setVisible(True)
        
class Page3_USB(QWidget):
    write_complete = Signal()
    
    def __init__(self):
        super().__init__()
        self.iso_path = None
        self.selected_drive = None # Tuple (device_id, caption)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("Select Your USB Drive")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)
        
        self.drive_combo = QComboBox()
        self.drive_combo.setFixedHeight(40)
        self.drive_combo.setStyleSheet("font-size: 16px; padding: 5px;")
        
        self.refresh_btn = QPushButton("Nothing in the box above? Make sure your USB drive is plugged in, then click here to refresh")
        self.refresh_btn.clicked.connect(self.scan_drives)
        
        self.warn_box = QFrame()
        self.warn_box.setStyleSheet("background-color: #fde8e7; border-radius: 8px; padding: 15px;")
        self.wb_layout = QVBoxLayout(self.warn_box)
        self.warn_lbl = QLabel("⚠️ WARNING: This will erase EVERYTHING on the USB drive.")
        self.warn_lbl.setStyleSheet("color: #c0392b; font-weight: bold; font-size: 14px;")
        self.wb_layout.addWidget(self.warn_lbl)

        self.confirm_chk = QCheckBox("I understand that my files on this USB drive will be erased. (Make sure you've backed up anything important!)")
        self.confirm_chk.setStyleSheet("font-size: 14px; margin-top: 10px;")
        self.confirm_chk.toggled.connect(self.check_ready)

        self.write_btn = QPushButton("Write to USB Drive")
        self.write_btn.setFixedHeight(50)
        self.write_btn.setStyleSheet("""
            QPushButton { background-color: #E74C3C; color: white; border-radius: 8px; font-size: 16px; font-weight: bold; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)
        self.write_btn.setEnabled(False)
        self.write_btn.clicked.connect(self.start_writing)

        self.pbar = QProgressBar()
        self.pbar.setVisible(False)

        layout.addWidget(self.title)
        layout.addWidget(self.drive_combo)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.warn_box)
        layout.addWidget(self.confirm_chk)
        layout.addWidget(self.write_btn)
        layout.addWidget(self.pbar)
        
        # Defer scan until page is actually shown
        pass

    def scan_drives(self):
        self.drive_combo.clear()
        self.drives_map = [] # List of dicts
        
        try:
            c = wmi.WMI()
            # Win32_DiskDrive where InterfaceType='USB' is the safest filter
            for drive in c.Win32_DiskDrive(InterfaceType="USB"):
                # Size in GB
                size_gb = int(drive.Size) / (1024**3)
                
                # Basic check: Skip if massive (likely external HDD backup) or tiny
                # But rely mainly on InterfaceType="USB"
                
                label = f"{drive.Caption} ({size_gb:.1f} GB)"
                self.drive_combo.addItem(label)
                self.drives_map.append({
                    "device_id": drive.DeviceID, # e.g. \\.\PHYSICALDRIVE1
                    "caption": drive.Caption
                })
        except Exception as e:
            self.drive_combo.addItem(f"Error scanning drives: {e}")

    def check_ready(self):
        self.write_btn.setEnabled(self.confirm_chk.isChecked() and self.drive_combo.count() > 0)

    def start_writing(self):
        if self.drive_combo.currentIndex() < 0:
            return

        drive_info = self.drives_map[self.drive_combo.currentIndex()]
        
        # Disable UI
        self.write_btn.setVisible(False)
        self.refresh_btn.setVisible(False)
        self.confirm_chk.setVisible(False)
        self.drive_combo.setEnabled(False)
        self.pbar.setVisible(True)
        self.pbar.setValue(0)
        
        self.title.setText("Writing Linux Installer to Your USB Drive")
        self.warn_lbl.setText("⚠️ Keep your USB drive plugged in while writing.")
        
        self.worker = BurnWorker(self.iso_path, "USB", drive_info['device_id'])
        self.worker.progress.connect(self.pbar.setValue)
        self.worker.finished.connect(self.write_complete.emit)
        self.worker.error.connect(lambda e: QMessageBox.critical(self, "Write Error", e))
        self.worker.start()

class Page4_Instructions(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # Detect Manufacturer
        manufacturer = "Unknown"
        boot_key = "F12"
        try:
            c = wmi.WMI()
            sys_info = c.Win32_ComputerSystem()[0]
            manufacturer = sys_info.Manufacturer.strip()
        except:
            pass

        # Simple heuristics
        m_lower = manufacturer.lower()
        if "dell" in m_lower: boot_key = "F12"
        elif "hp" in m_lower: boot_key = "Esc or F9"
        elif "lenovo" in m_lower: boot_key = "F12 or Novo Button"
        elif "acer" in m_lower: boot_key = "F12"
        elif "asus" in m_lower: boot_key = "F8 or Esc"
        
        title = QLabel("You're Ready to Try Linux!")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #27ae60;")
        title.setAlignment(Qt.AlignCenter)

        steps = QLabel(f"""
        <ol style='font-size: 18px; line-height: 1.6;'>
            <li>Leave the USB drive plugged in.</li>
            <li>Restart your computer.</li>
            <li>As it turns on, repeatedly press <b>{boot_key}</b>.</li>
            <li>If a menu appears, select your USB drive.</li>
        </ol>
        """)
        steps.setTextFormat(Qt.RichText)
        
        tip = QLabel(f"<b>Tip:</b> Your computer is made by <b>{manufacturer}</b>.<br>If {boot_key} doesn't work, try Esc, F10, or Del.")
        tip.setStyleSheet("background-color: #fff3cd; padding: 15px; border-radius: 5px; font-size: 14px;")
        tip.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(steps)
        layout.addWidget(tip)
        layout.addStretch()

# --- Main Window ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Central Widget & Stack
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.header = QLabel(APP_NAME)
        self.header.setStyleSheet(f"background-color: {COLOR_PRIMARY}; color: white; padding: 15px; font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.header)

        # Content Stack
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Pages
        self.page1 = Page1_Selection()
        self.page2 = Page2_Download()
        self.page3 = Page3_USB()
        self.page4 = Page4_Instructions()

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.stack.addWidget(self.page4)

        # Footer / Nav
        self.footer = QWidget()
        self.footer.setFixedHeight(80)
        self.footer.setStyleSheet("background-color: #ecf0f1;")
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(30, 10, 30, 10)
        footer_layout.setSpacing(15)
        
        self.footer_info = QLabel(f'<a href="{WEBSITE_URL}">iwantlinux.com</a> <br> 'f'<a href="{GITHUB_URL}">github.com/njcabral/iwantlinux</a> <br> 'f'Last updated {APP_DATE}')
        self.footer_info.setOpenExternalLinks(True)
        self.footer_info.setStyleSheet("""
            QLabel {
                color: #555;
                font-size: 12px;
                }
            QLabel a {
                color: #4A90E2;
                text-decoration: none;
                }
            QLabel a:hover {
                text-decoration: underline;
                }
            """)
        
        self.btn_restart = QPushButton("Restart Now")
        self.btn_restart.setFixedSize(120, 50)
        self.btn_restart.setStyleSheet(f"background-color: {COLOR_SUCCESS}; color: white; font-weight: bold; font-size: 16px; border-radius: 5px;")
        self.btn_restart.clicked.connect(self.restart_windows)
        self.btn_restart.setEnabled(True)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setFixedSize(120, 50)
        self.btn_next.setStyleSheet(f"background-color: {COLOR_PRIMARY}; color: white; font-weight: bold; font-size: 16px; border-radius: 5px;")
        self.btn_next.clicked.connect(self.go_next)
        self.btn_next.setEnabled(False) # Disabled until distro selected

        footer_layout.addWidget(self.footer_info)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_restart)
        footer_layout.addWidget(self.btn_next)
        
        self.main_layout.addWidget(self.footer)

        # State Management
        self.selected_distro = None
        self.iso_path = None
        
        # Signal Connections
        self.page1.distro_selected.connect(self.on_distro_selected)
        self.page2.download_complete.connect(self.on_download_finished)
        self.page2.request_start_over.connect(self.reset_to_start)
        self.page3.write_complete.connect(self.on_write_finished)

        self.stack.currentChanged.connect(self._on_page_changed)

        self.update_nav_buttons()


    def _on_page_changed(self, index):
        if index == 2:
            self.page3.scan_drives()

    def update_nav_buttons(self):
        idx = self.stack.currentIndex()

        
        # Handle Next Button Visibility & Text
        # We need to make sure it's VISIBLE on Page 0 so the user can see it's disabled.
        if idx == 0:
            self.btn_restart.setVisible(False) 
            self.btn_next.setVisible(True) # Force visibility back on
            self.btn_next.setText("Next")
            self.btn_next.setEnabled(self.selected_distro is not None)
            
        elif idx == 1:
            # Hide Next while downloading; Page 2 signals completion to advance
            # UNLESS there is an error (but your UI uses internal buttons for that)
            self.btn_restart.setVisible(False) 
            self.btn_next.setVisible(False)
            
        elif idx == 2:
            # Page 3 has its own "Write to USB" button
            self.btn_restart.setVisible(False) 
            self.btn_next.setVisible(False)
            
        elif idx == 3:
            # Final celebratory page
            self.btn_restart.setVisible(True) 
            self.btn_next.setVisible(True)
            self.btn_next.setText("Close")
            self.btn_next.setEnabled(True)

    def on_distro_selected(self, data):
        self.selected_distro = data
        self.update_nav_buttons()

    def go_next(self):
        curr = self.stack.currentIndex()
        if curr == 0:
            self.stack.setCurrentIndex(1)
            self.update_nav_buttons()
            # Start download immediately upon entering page 2
            self.page2.start_download(self.selected_distro['url'])
        elif curr == 3:
            self.close()

    def go_back(self):
        curr = self.stack.currentIndex()
        if curr > 0:
            self.stack.setCurrentIndex(curr - 1)
            self.update_nav_buttons()

    def reset_to_start(self):
        self.selected_distro = None
        self.iso_path = None
        self.page1.clear_selection() # Deselect cards
        self.stack.setCurrentIndex(0) # Go to Page 1
        self.update_nav_buttons()    # Refresh footer state
        
    def on_download_finished(self, path):
        self.iso_path = path
        self.page3.iso_path = path
        # Auto advance
        self.stack.setCurrentIndex(2)
        self.update_nav_buttons()

    def on_write_finished(self):
        self.stack.setCurrentIndex(3)
        self.update_nav_buttons()
        
    def restart_windows(self):
        yousure = QMessageBox.question(self, "Ready to restart?", "Are you sure you're ready to restart the computer?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
        )
        
        if yousure == QMessageBox.StandardButton.Yes:
            os.system("shutdown /r /t 0")

# --- Entry Point ---

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app_icon = QIcon(resource_path("IWLIcon.ico"))
    app.setWindowIcon(app_icon)
    
    app.setFont(QFont(["Segoe UI", "Arial"], 10))

    # Global CSS for buttons
    app.setStyleSheet("""
        QPushButton {
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }
        QProgressBar {
            border-radius: 10px;
            background-color: #edf2f7;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4A90E2;
            border-radius: 10px;
        }
    """)

    if not is_admin():
        QMessageBox.critical(None, "Administrator Required", 
                             "IWantLinux needs to write to a USB drive.\n"
                             "Please right-click the app and select 'Run as Administrator'.")
        sys.exit()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
