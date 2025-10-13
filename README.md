# 🚀 MyJob - Job Portal System API

<div align="center">
  <img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/ef0c454d-7947-46ab-a5e6-64ffe964bb3a" width="200" alt="MyJob Logo" />
  
  **MyJob API** is a backend system for the **MyJob** job portal and recruitment platform, built with **Django REST Framework**.
</div>

---

## 📋 Table of Contents

- [📦 Installation Guide](#-installation-guide)
- [⚙️ Service Configuration](#️-service-configuration)
- [📚 API Documentation](#-api-documentation)

---

## 📦 Installation Guide

### 🔽 Step 1: Clone Project

```bash
# Clone repository
git clone https://github.com/BuiKhanhHuy/myjob_api.git

# Navigate to project directory
cd myjob_api

# Create environment configuration file
cp .env.example .env
```

### ⚙️ Step 2: Environment Configuration

1. Open `.env` file 
2. Fill in all information from the services configured above
3. Save file

### 🚀 Step 3: Launch Application

```bash
# Build and run containers
docker-compose up -d --build
```

### ✅ Step 4: Verification

- 🌐 **Application**: `https://<your-ngrok-domain>/`
- 📖 **API Documentation**: `https://<your-ngrok-domain>/swagger/`

---

## ⚙️ Service Configuration

> ⚠️ **Important Note**: You need to configure all the services below before running the application.

### 📧 1. Email Service (Gmail)

**Required environment variables:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=<Your email address>
EMAIL_HOST_PASSWORD=<App Password>
EMAIL_PORT=587
```

**📝 Configuration steps:**

1. **Access Google Account**: Go to [myaccount.google.com](https://myaccount.google.com/)
2. **Enable 2-Factor Authentication**: 
   - Select **Security** 
   - Enable **2-Step Verification**
3. **Create App Password**:
   - In **Security** section, find **App passwords**
   - Create new password for application
   - Use this password for `EMAIL_HOST_PASSWORD`

---

### ☁️ 2. Cloudinary (File Storage)

**Required environment variables:**
```env
CLOUDINARY_CLOUD_NAME=<Cloud Name>
CLOUDINARY_API_KEY=<API Key>
CLOUDINARY_API_SECRET=<API Secret>
```

**📝 Configuration steps:**

1. **Register account**: Visit [cloudinary.com](https://cloudinary.com/)
2. **Get API information**: 
   - Go to **Settings → API Keys**
   - Copy the information: Cloud Name, API Key, API Secret
3. **⚠️ Security configuration**:
   - Go to **Settings → Security**
   - ✅ Enable: **Allow delivery of PDF and ZIP files**

---

### 👥 3. Facebook Login

**Required environment variables:**
```env
SOCIAL_AUTH_FACEBOOK_KEY=<App ID>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret>
```

**📝 Configuration steps:**

1. **Create Facebook App**: 
   - Visit [developers.facebook.com](https://developers.facebook.com/)
   - Login and select **My Apps → Create App**
2. **Configure OAuth**:
   - Add **Facebook Login** product
   - Configure **Valid OAuth Redirect URIs** (frontend URL)
3. **Get credentials**:
   - Copy **App ID** and **App Secret**
   - Add to `.env` file

---

### 🔍 4. Google Login

**Required environment variables:**
```env
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<Client ID>
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=<Client Secret>
```

**📝 Configuration steps:**

1. **Create Google Project**: 
   - Visit [console.cloud.google.com](https://console.cloud.google.com/)
   - Create new project
2. **Configure OAuth Consent Screen**:
   - Fill in application information (name, logo, contact email, etc.)
3. **Create OAuth 2.0 Client ID**:
   - Go to **APIs & Services → Credentials → Create credentials → OAuth client ID**
   - Select **Application type**: Web application
   - **Authorized JavaScript origins**: `https://www.myjob.com`
   - **Authorized redirect URIs**: `https://www.myjob.com`
4. **Save credentials**: Copy Client ID and Client Secret to `.env`

---

### 🔥 5. Firebase (Push Notification)

**Required environment variables:**
```env
FIREBASE_API_KEY=<API Key>
FIREBASE_AUTH_DOMAIN=<Auth Domain>
FIREBASE_PROJECT_ID=<Project ID>
FIREBASE_STORAGE_BUCKET=<Storage Bucket>
FIREBASE_MESSAGING_SENDER_ID=<Sender ID>
FIREBASE_APP_ID=<App ID>
FIREBASE_CREDENTIALS_PATH=tmp/firebase-config.json
```

**📝 Configuration steps:**

1. **Create Firebase Project**: 
   - Visit [console.firebase.google.com](https://console.firebase.google.com/)
   - Create new project
2. **Create Service Account** (for Backend):
   - Go to **Project settings → Service accounts → Firebase Admin SDK**
   - Click **Generate new private key** → download JSON file
   - Save file to `tmp/firebase-config.json`
3. **Get Web App Config** (for Frontend):
   - Go to **Project settings → General → Your apps**
   - Click **Web (</>)** icon → **Register app**
   - Copy `firebaseConfig` information to environment variables

> 💡 **Note**: Service Account (step 2) is for server, Web App Config (step 3) is for frontend.

---

### 🌐 6. Ngrok (Development Tunnel)

**Required environment variables:**
```env
NGROK_AUTHTOKEN=<Auth Token>
```

**📝 Configuration steps:**

1. **Register Ngrok**: Visit [dashboard.ngrok.com](https://dashboard.ngrok.com/)
2. **Get Auth Token**: 
   - Go to **Your Authtoken** → copy token
   - Add to `NGROK_AUTHTOKEN` in `.env` file
3. **Get Domain**:
   - Go to **Domains** → copy assigned domain
   - Replace `<ngrok-domain>` in `ngrok.yml` file

---

## 📚 API Documentation

| Type | URL | Description |
|------|-----|-------------|
| 📊 **Swagger UI** | `https://<your-ngrok-domain>/swagger/` | Interactive API interface |
| 📋 **ReDoc** | `https://<your-ngrok-domain>/redoc/` | Detailed API documentation |

---

<div align="center">
  <p>🎉 <strong>Congratulations on successful installation!</strong> 🎉</p>
  <p>If you encounter issues, please check the service configuration steps again.</p>
</div>

---

<details>
<summary>🇻🇳 <strong>Vietnamese</strong></summary>

## 📋 Mục Lục

- [📦 Hướng Dẫn Cài Đặt](#-hướng-dẫn-cài-đặt-1)
- [⚙️ Cấu Hình Dịch Vụ](#️-cấu-hình-dịch-vụ-1)
- [📚 Tài Liệu API](#-tài-liệu-api-1)

---

## 📦 Hướng Dẫn Cài Đặt

### 🔽 Bước 1: Clone Dự Án

```bash
# Clone repository
git clone https://github.com/BuiKhanhHuy/myjob_api.git

# Di chuyển vào thư mục dự án
cd myjob_api

# Tạo file cấu hình môi trường
cp .env.example .env
```

### ⚙️ Bước 2: Cấu Hình Môi Trường

1. Mở file `.env` 
2. Điền đầy đủ thông tin từ các dịch vụ đã cấu hình ở trên
3. Lưu file

### 🚀 Bước 3: Khởi Chạy Ứng Dụng

```bash
# Build và chạy các container
docker-compose up -d --build
```

### ✅ Bước 4: Kiểm Tra

- 🌐 **Ứng dụng**: `https://<your-ngrok-domain>/`
- 📖 **API Documentation**: `https://<your-ngrok-domain>/swagger/`

---

## ⚙️ Cấu Hình Dịch Vụ

> ⚠️ **Lưu ý quan trọng**: Bạn cần cấu hình tất cả các dịch vụ bên dưới trước khi chạy ứng dụng.

### 📧 1. Email Service (Gmail)

**Biến môi trường cần thiết:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=<Địa chỉ email của bạn>
EMAIL_HOST_PASSWORD=<App Password>
EMAIL_PORT=587
```

**📝 Các bước cấu hình:**

1. **Truy cập Google Account**: Vào [myaccount.google.com](https://myaccount.google.com/)
2. **Bật bảo mật 2 lớp**: 
   - Chọn **Security (Bảo mật)** 
   - Bật **2-Step Verification**
3. **Tạo App Password**:
   - Trong mục **Security**, tìm **App passwords**
   - Tạo password mới cho ứng dụng
   - Sử dụng password này cho `EMAIL_HOST_PASSWORD`

---

### ☁️ 2. Cloudinary (Lưu trữ file)

**Biến môi trường cần thiết:**
```env
CLOUDINARY_CLOUD_NAME=<Tên cloud>
CLOUDINARY_API_KEY=<API Key>
CLOUDINARY_API_SECRET=<API Secret>
```

**📝 Các bước cấu hình:**

1. **Đăng ký tài khoản**: Truy cập [cloudinary.com](https://cloudinary.com/)
2. **Lấy thông tin API**: 
   - Vào **Settings → API Keys**
   - Copy các thông tin: Cloud Name, API Key, API Secret
3. **⚠️ Cấu hình bảo mật**:
   - Vào **Settings → Security**
   - ✅ Bật: **Allow delivery of PDF and ZIP files**

---

### 👥 3. Facebook Login

**Biến môi trường cần thiết:**
```env
SOCIAL_AUTH_FACEBOOK_KEY=<App ID>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret>
```

**📝 Các bước cấu hình:**

1. **Tạo Facebook App**: 
   - Truy cập [developers.facebook.com](https://developers.facebook.com/)
   - Đăng nhập và chọn **My Apps → Create App**
2. **Cấu hình OAuth**:
   - Thêm **Facebook Login** product
   - Cấu hình **Valid OAuth Redirect URIs** (URL frontend)
3. **Lấy thông tin**:
   - Copy **App ID** và **App Secret**
   - Thêm vào file `.env`

---

### 🔍 4. Google Login

**Biến môi trường cần thiết:**
```env
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<Client ID>
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=<Client Secret>
```

**📝 Các bước cấu hình:**

1. **Tạo Google Project**: 
   - Truy cập [console.cloud.google.com](https://console.cloud.google.com/)
   - Tạo project mới
2. **Cấu hình OAuth Consent Screen**:
   - Điền thông tin ứng dụng (tên, logo, email liên hệ)
3. **Tạo OAuth 2.0 Client ID**:
   - Vào **APIs & Services → Credentials → Create credentials → OAuth client ID**
   - Chọn **Application type**: Web application
   - **Authorized JavaScript origins**: `https://www.myjob.com`
   - **Authorized redirect URIs**: `https://www.myjob.com`
4. **Lưu thông tin**: Copy Client ID và Client Secret vào `.env`

---

### 🔥 5. Firebase (Push Notification)

**Biến môi trường cần thiết:**
```env
FIREBASE_API_KEY=<API Key>
FIREBASE_AUTH_DOMAIN=<Auth Domain>
FIREBASE_PROJECT_ID=<Project ID>
FIREBASE_STORAGE_BUCKET=<Storage Bucket>
FIREBASE_MESSAGING_SENDER_ID=<Sender ID>
FIREBASE_APP_ID=<App ID>
FIREBASE_CREDENTIALS_PATH=tmp/firebase-config.json
```

**📝 Các bước cấu hình:**

1. **Tạo Firebase Project**: 
   - Truy cập [console.firebase.google.com](https://console.firebase.google.com/)
   - Tạo project mới
2. **Tạo Service Account** (cho Backend):
   - Vào **Project settings → Service accounts → Firebase Admin SDK**
   - Nhấn **Generate new private key** → tải file JSON
   - Lưu file vào `tmp/firebase-config.json`
3. **Lấy Web App Config** (cho Frontend):
   - Vào **Project settings → General → Your apps**
   - Nhấn biểu tượng **Web (</>)** → **Register app**
   - Copy thông tin `firebaseConfig` vào các biến môi trường

> 💡 **Ghi chú**: Service Account (bước 2) dùng cho server, Web App Config (bước 3) dùng cho frontend.

---

### 🌐 6. Ngrok (Development Tunnel)

**Biến môi trường cần thiết:**
```env
NGROK_AUTHTOKEN=<Auth Token>
```

**📝 Các bước cấu hình:**

1. **Đăng ký Ngrok**: Truy cập [dashboard.ngrok.com](https://dashboard.ngrok.com/)
2. **Lấy Auth Token**: 
   - Vào **Your Authtoken** → copy token
   - Thêm vào `NGROK_AUTHTOKEN` trong file `.env`
3. **Lấy Domain**:
   - Vào **Domains** → copy domain được cấp
   - Thay thế `<ngrok-domain>` trong file `ngrok.yml`

---

## 📚 Tài Liệu API

| Loại | URL | Mô tả |
|------|-----|-------|
| 📊 **Swagger UI** | `https://<your-ngrok-domain>/swagger/` | Giao diện tương tác API |
| 📋 **ReDoc** | `https://<your-ngrok-domain>/redoc/` | Tài liệu API chi tiết |

---

<div align="center">
  <p>🎉 <strong>Chúc bạn cài đặt thành công!</strong> 🎉</p>
  <p>Nếu gặp vấn đề, hãy kiểm tra lại các bước cấu hình dịch vụ.</p>
</div>

</details>
