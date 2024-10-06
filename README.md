API DOCUMENTATION = https://documenter.getpostman.com/view/23480640/2sAXxMftZv

# CoHire AI

CoHire AI is a simple Django application designed for efficient recruitment processes. This README provides a step-by-step guide to set up and run the project on a Windows operating system.

## API Documentation

For detailed API documentation, visit: [CoHire AI API Documentation](https://documenter.getpostman.com/view/23480640/2sAXxMftZv)

## Simple Django Application Setup

### Steps to Run the Project on Windows OS

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ompakash/cohireai.git

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv_cohire

3. **Activate the Virtual Environment**
   ```bash
   .\venv_cohire\Scripts\activate

4. **Navigate to the Project Directory**
   ```bash
   cd .\cohireai\

5. **Install the Required Packages**
   ```bash
   pip install -r .\requirements.txt

6. **Create Migrations**
   ```bash
   python .\manage.py makemigrations

7. **Apply Migrations**
   ```bash
   python .\manage.py migrate

8. **Create a Superuser**
   ```bash
   python .\manage.py createsuperuser
- Email: admin@gmail.com

9. **Run the Development Server**
   ```bash
   python .\manage.py runserver
