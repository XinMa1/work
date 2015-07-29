#!/bin/bash

keytool -genkeypair -keystore $1 -storepass Whhe2013 -dname "CN=wiaapp.cn, OU=wiaapp.cn, O=wiaapp.cn, L=Beijing, L=Beijing, C=CN" -alias scg -keypass Whhe2013 -validity 3650
