# Tonton Auto Grabber

Skrip ini digunakan untuk auto-login ke Tonton, pergi ke Live TV → TV3, dan grab link `master_1080.m3u8` setiap 6 jam secara automatik menggunakan GitHub Actions.

## Cara Guna
1. Fork atau upload repo ini ke GitHub anda.
2. Masuk ke `Settings > Secrets > Actions`
   - Tambah `TONTON_EMAIL` dan `TONTON_PASSWORD`
3. Pergi ke tab `Actions` dan run workflow pertama secara manual (untuk test).