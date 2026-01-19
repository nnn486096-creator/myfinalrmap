[app]
title = SK42 Map
package.name = sk42map
package.domain = org.myapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy==2.2.1,pyproj,pillow,certifi,openssl

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
fullscreen = 1
orientation = portrait
