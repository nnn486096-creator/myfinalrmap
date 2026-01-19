[app]
title = SK42 Map
package.name = sk42map
package.domain = org.myapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# ВАЖНО: pyproj удален, используем math в main.py
requirements = python3,kivy==2.2.1,pillow,certifi,openssl

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
fullscreen = 1
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
