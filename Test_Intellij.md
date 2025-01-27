# Running `spotify-playing.py` Locally on IntelliJ

This guide explains how to configure and run the `spotify-playing.py` file locally using IntelliJ without setting up a virtual environment.

---

## Prerequisites
Before starting, ensure you have the following installed:
1. **Python** (Recommended version: 3.10 or higher)
2. **IntelliJ IDEA** (Community or Ultimate Edition with Python plugin enabled)
3. **pip** for installing Python packages
4. **Spotify Developer Account** (to obtain `Client ID` and `Client Secret`)

---

## Steps to Run Locally

### 1. Clone the Repository
1. Clone the project repository to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/spotify-api-readme.git
   ```
2. Open the project folder in IntelliJ.

---

### 2. Install Required Python Packages
1. Open a terminal in IntelliJ.
2. Navigate to the project directory:
   ```bash
   cd /path/to/your/project
   ```
3. Install the dependencies listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Set Up Environment Variables
1. In the `api` directory of your project, create a new file named `.env`.
2. Add the following content to the `.env` file:
   ```
   SPOTIFY_CLIENT_ID=your-client-id
   SPOTIFY_SECRET_ID=your-secret-id
   SPOTIFY_REFRESH_TOKEN=your-refresh-token
   ```
   Replace `your-client-id`, `your-secret-id`, and `your-refresh-token` with the credentials from your Spotify Developer Dashboard.

---

### 4. Run the `spotify-playing.py` Script
1. In IntelliJ, navigate to the `spotify-playing.py` file located in the `api` directory.
2. Right-click on the `spotify-playing.py` file and select **Run 'spotify-playing'**.

---

### 5. Access the Application Locally
- Open your browser and go to:
  ```
  http://127.0.0.1:5000/
  ```

---

### 6. Troubleshooting
If you encounter issues:
1. Double-check that the `.env` file is in the correct location and contains valid values.
2. Ensure all required Python packages are installed properly.
3. Review the IntelliJ Run/Debug console logs for any errors.

---

You're now ready to run and test the `spotify-playing.py` script locally in IntelliJ!
