[app]
title = Quantum Mind
package.name = quantummind
package.domain = org.softnet
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,mp3,txt
version = 1.1.0
requirements = python3,kivy==2.3.0,pillow,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
p4a.branch = master
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
