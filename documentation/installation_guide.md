# Installation Guide for News Website

## Prerequisites
- Node.js (version X.X.X)
- MongoDB (version X.X)
- Git

## Steps to Install
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/coderbot202/dhakar_samachar.git
   ```  
2. **Navigate to the project directory:**  
   ```bash
   cd dhakar_samachar
   ```  
3. **Install Dependencies:**  
   ```bash
   npm install
   ```  
4. **Set up environment variables:**  
   Create a `.env` file at the root with the following configurations:
   ```
   DB_URL=mongodb://localhost:27017/news_website
   PORT=3000
   ```  
5. **Run the application:**  
   ```bash
   npm start
   ```  
6. **Open your browser and navigate to:**  
   `http://localhost:3000`

## Database Setup
Make sure MongoDB is running before starting the application.