

# Django Backend Setup & API Testing  

## 🚀 Setup Instructions  

### 1. Create GitHub Repository  
- Create a new repository on GitHub.  
- Clone it to your local machine using:  
  ```sh
  git clone <repository_url>
  cd <repository_name>
  ```

### 2. Set Up Virtual Environment  
- Create a virtual environment:  
  ```sh
  python -m venv venv
  ```
- Activate the virtual environment:  
  - **Windows:**  
    ```sh
    venv\Scripts\activate
    ```
  - **macOS/Linux:**  
    ```sh
    source venv/bin/activate
    ```

### 3. Install Django & Required Packages  
```sh
pip install django psycopg2 djangorestframework
```

### 4. Create Django Project & App  
```sh
django-admin startproject myproject
cd myproject
python manage.py startapp api
```

### 5. Install Dependencies  
```sh
pip install -r requirements.txt
```

### 6. Set Up Database Migrations  
```sh
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser  
```sh
python manage.py createsuperuser
```

### 8. Run Server  
```sh
python manage.py runserver
```

---

## 🛠 Environment Variables (`.env` File)  
Ensure `.env` contains your database credentials:  
```ini
DJANGO_SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🔐 API Authentication & Testing  

### **Get Token**  
**Request:**  
```http
POST http://localhost:8000/api/token/
Content-Type: application/json
```
**Body:**  
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
**Response (JWT):**  
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```
![WhatsApp Image 2025-01-29 at 14 19 51_c107fab2](https://github.com/user-attachments/assets/27d09207-575b-4263-bbf4-828d747017e2)

### **Use Token for API Requests**  
```http
GET http://localhost:8000/api/responses/
Authorization: Bearer <your_access_token>
```
![WhatsApp Image 2025-01-29 at 14 20 50_91aacb8f](https://github.com/user-attachments/assets/7fdbd842-1b22-4084-96bc-133b3e44ce60)

### **POST Request Example**  
```http
POST http://localhost:8000/api/responses/
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

**Body:**  
```json
{
    "prompt": "What is AI?",
    "model_used": "gpt-3.5"
}
```
![WhatsApp Image 2025-01-29 at 14 22 30_306f6450](https://github.com/user-attachments/assets/50d220d2-daa9-405e-8b46-d56e52228b95)

---

## ✅ **Test Cases for Authentication**  

### 1️⃣ **Login with Valid Credentials**  
- **Request:**  
  ```http
  POST /api/token/
  ```
- **Body:**  
  ```json
  {
    "username": "testuser",
    "password": "testpassword123"
  }
  ```
- **Expected Response:**  
  ```json
  {
    "access": "abcd1234efgh5678ijkl91011",
    "refresh": "mnop1234qrst5678uvwx91011"
  }
  ```
- **Status Code:** `200 OK`
  ![WhatsApp Image 2025-01-29 at 14 19 51_3f3b825f](https://github.com/user-attachments/assets/c8254ef1-1fce-4902-ac7b-a70f17024391)


### 2️⃣ **Login with Invalid Credentials**  
- **Body:**  
  ```json
  {
    "username": "testuser",
    "password": "wrongpassword"
  }
  ```
- **Expected Response:**  
  ```json
  {
    "non_field_errors": ["Unable to log in with provided credentials."]
  }
  ```
- **Status Code:** `401 Unauthorized`
  ![WhatsApp Image 2025-01-29 at 14 24 17_256aaea3](https://github.com/user-attachments/assets/74132901-d244-4936-ba14-e7c79b98a72f)


### 3️⃣ **Login with Missing Fields**  
- **Body:**  
  ```json
  {
    "username": "testuser"
  }
  ```
- **Expected Response:**  
  ```json
  {
    "password": ["This field is required."]
  }
  ```
- **Status Code:** `400 Bad Request`
  ![WhatsApp Image 2025-01-29 at 14 24 49_def063ac](https://github.com/user-attachments/assets/89a6955a-4a21-4ab6-a006-2c24827dccae)


### 4️⃣ **Login with Non-Existent User**  
- **Body:**  
  ```json
  {
    "username": "unknownuser",
    "password": "randompassword"
  }
  ```
- **Expected Response:**  
  ```json
  {
    "non_field_errors": ["Unable to log in with provided credentials."]
  }
  ```
- **Status Code:** `401 Unauthorized`
  ![WhatsApp Image 2025-01-29 at 14 25 49_f8211709](https://github.com/user-attachments/assets/08f749b6-aded-450e-b11e-3dbedbbbf422)


### 5️⃣ **Login with Inactive User**  
- **Body:**  
  ```json
  {
    "username": "inactiveuser",
    "password": "inactivepassword"
  }
  ```
- **Expected Response:**  
  ```json
  {
    "non_field_errors": ["User account is disabled."]
  }
  ```
- **Status Code:** `401 Unauthorized`

---

## 🔎 **Test Cases for `/api/responses/{id}/` and `/api/responses/{wrongid}/`**  

### 1️⃣ **Get Response by Valid ID**  
- **Request:**  
  ```http
  GET /api/responses/1/
  Authorization: Bearer <your_access_token>
  ```
- **Expected Response:**  
  ```json
  {
    "id": 1,
    "prompt": "What is AI?",
    "model_used": "gpt-3.5",
    "response": "Artificial Intelligence (AI) is a branch of computer science...",
    "created_at": "2024-01-29T12:00:00Z"
  }
  ```
- **Status Code:** `200 OK`
  ![WhatsApp Image 2025-01-29 at 14 26 56_79a2d3b3](https://github.com/user-attachments/assets/fde3d2cb-7bd4-4fab-9793-e652931ffdda)


### 2️⃣ **Get Response by Invalid ID (`/api/responses/{wrongid}/`)**  
- **Request:**  
  ```http
  GET /api/responses/9999/
  Authorization: Bearer <your_access_token>
  ```
- **Expected Response:**  
  ```json
  {
    "detail": "Not found."
  }
  ```
- **Status Code:** `404 Not Found`
![WhatsApp Image 2025-01-29 at 14 27 25_7d706195](https://github.com/user-attachments/assets/c0ed6b64-39a9-40ce-aae3-f26f2eb09687)

---

## 🔎 **Test Case with openai**  

### 1️⃣ **Get Valid Responses**  
**Post:**  
```http
POST http://localhost:8000/api/responses/
Content-Type: application/json
```
**Body:**  
```json
{
    "prompt": "What is AI?",
    "model_used": "gpt-3.5"
}
```
**Response:**  
```json
{
  "id": 1,
  "prompt": "What is AI?",
  "model_used": "gpt-3.5",
  "response": "Artificial Intelligence (AI) is a branch of computer science...",
  "created_at": "2024-01-29T12:00:00Z"
}
```
![WhatsApp Image 2025-01-29 at 00 54 13_a8d5e4e8](https://github.com/user-attachments/assets/5400e27f-cf3e-41f7-b664-9cebb9009bcd)


## 🧪 **Run Tests Using Postman**  
1. Import the API endpoints into Postman.  
2. Use `Bearer <your_access_token>` for authentication.  
3. Test each scenario from the above test cases.  

---
