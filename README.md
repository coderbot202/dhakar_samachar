
# 📰 News Portal (Full-Stack)

This repository contains the complete source code for the Dhakar Samachar News Portal, built with a **Django REST Framework (DRF)** backend and a **React** frontend.

## 🚀 Project Overview

The application is split into two main components:

| Directory | Technology | Role | Local Access Point |
| :--- | :--- | :--- | :--- |
| `newsportal_backEnd` | Django, Python, DRF | **API & Database:** Handles data logic, security, and the Django Admin. | `http://127.0.0.1:8000/` |
| `newsportal_frontEnd` | React, JavaScript | **User Interface (UI):** Consumes the API to render the news portal. | `http://localhost:3000/` |

-----

## 🛠️ Local Development Setup

Follow these steps to set up and run the application locally. Requires **Node.js/npm** and **Python/pip**.

### Prerequisites

1.  Clone the repository:
    ```bash
    git clone https://github.com/coderbot202/dhakar_samachar.git
    cd dhakar_samachar
    ```

### 1\. Backend Setup (`newsportal_backEnd`)

1.  **Navigate and Environment:**
    ```bash
    cd newsportal_backEnd
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Linux/macOS
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Database and Superuser:**
    *The local environment uses SQLite.*
    ```bash
    python manage.py migrate
    python manage.py createsuperuser # Create an Admin account
    ```

### 2\. Frontend Setup (`newsportal_frontEnd`)

1.  **Navigate and Install:**
    ```bash
    cd ../newsportal_frontEnd
    npm install
    ```
2.  **Verify API Endpoint (`src/api.js`):**
    *Ensure the `baseURL` points to the local Django server:*
    ```javascript
    baseURL: 'http://127.0.0.1:8000/api/',
    ```

-----

## ▶️ Running the Application

You must run **two separate terminals** simultaneously.

| Terminal | Directory | Command | Status |
| :--- | :--- | :--- | :--- |
| **Terminal 1** | `newsportal_backEnd` | `python manage.py runserver` | API is serving data on port 8000. |
| **Terminal 2** | `newsportal_frontEnd` | `npm start` | UI loads in browser on port 3000. |

### Access Points

  * **User Portal:** `http://localhost:3000/`
  * **Django Admin:** `http://127.0.0.1:8000/admin/`

-----

## ✅ Post-Deployment Checks (For Operations Team)

The following steps should be performed on the **live domain (`https://yourcompany.com`)** after deployment to confirm successful integration and data connectivity.

### 1\. Basic Connectivity Test

| Check | URL | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| **Frontend Load** | `https://yourcompany.com/` | **News Portal UI loads** (not a blank page). | 🟢 |
| **API Check** | `https://yourcompany.com/api/articles/` | Returns **JSON data** (list of articles). | 🟢 |
| **Admin Panel** | `https://yourcompany.com/admin/` | **Admin login page** loads. | 🟢 |

### 2\. Data Integrity and Functionality Test

1.  **Article Detail:** Click an article title to confirm the full content and media load (checks full-stack read operation).
2.  **Search:** Use the search bar to search for an article title (checks backend search filter).
3.  **Comments:** Submit a new comment on an article (checks full-stack write operation to the production database).
