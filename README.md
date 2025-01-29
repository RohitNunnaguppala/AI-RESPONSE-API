

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

### **Use Token for API Requests**  
```http
GET http://localhost:8000/api/responses/
Authorization: Bearer <your_access_token>
```

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
![WhatsApp Image 2025-01-29 at 00 54 14_83ddac12](https://github.com/user-attachments/assets/4a6a711d-a702-4d90-8004-e9b48ef4c2f4)


## 🧪 **Run Tests Using Postman**  
1. Import the API endpoints into Postman.  
2. Use `Bearer <your_access_token>` for authentication.  
3. Test each scenario from the above test cases.  

---

### 🎯 **You're now ready to test and deploy your Django backend!** 🚀  
