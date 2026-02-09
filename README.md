# BookShop Project

A full-stack book management and e-commerce platform consisting of a Django-based web application and an Electron-based desktop application.

## 🚀 Features

### Customer Web App (`web_app`)
- **Browse Books**: View a collection of available books with details.
- **Search & Filter**: Find books by category or title.
- **Cart System**: Add books to a shopping cart for purchase.
- **Checkout & Payment**: Secure checkout process with payment integration.
- **User Accounts**: Sign up and sign in to manage orders.

### Admin Dashboard (`admin_app`)
- **Inventory Management**: Add, edit, and delete books and categories.
- **Order Tracking**: View and manage customer purchases.
- **Dashboard**: Overview of shop performance.

### Desktop App (`desktop-app`)
- **Standalone Experience**: A dedicated desktop application built with Electron for easier access to the bookshop.
- **Note** : need to add node modules which is for to setup how to work the exe (not added here) 

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Database**: SQLite
- **Web Frontend**: HTML5, CSS3, JavaScript
- **Desktop**: Electron

## ⚙️ Setup Instructions

### Backend (Django)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BookShop
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   *(Note: Ensure you have a requirements.txt file or install manually)*
   ```bash
   pip install django
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Desktop Application (Electron)

1. **Navigate to the desktop-app directory**:
   ```bash
   cd desktop-app
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Start the application**:
   ```bash
   npm start
   ```

## 📂 Project Structure

- `admin_app/`: Django application for administrative tasks.
- `web_app/`: Django application for the customer-facing website.
- `desktop-app/`: Electron application source code.
- `BookShop/`: Main project configuration directory.
- `media/`: Directory for uploaded book cover images and other media.
- `manage.py`: Django's command-line utility.

---
*Created by BookShop Team*
