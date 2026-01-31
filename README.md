# Land Record Search System (भू-उपयोग क्षेत्र वर्गीकरण खोज प्रणाली)

A browser-based Land Record Search System for Nepal built with Python (Streamlit) and Pandas.

## Features
- **Dynamic Filtering**: Filter by 'साविक गा.' (VDC), 'वडा नं.' (Ward), 'कित्ता नं.' (Plot), and 'भूउपयोग क्षेत्र' (Land Use).
- **Localization**: Full Nepali language support (Unicode).
- **Live Data**: Connects directly to Google Sheets CSV.
- **Cross-Platform**: Runs locally, via Docker, or directly in the browser (GitHub Pages/Stlite).

## Project Structure
```
land_record_system/
├── app.py              # Main application logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── index.html          # Browser-based runner (Stlite)
└── README.md           # Documentation
```

## How to Run

### 1. Run Locally (Python)
Ensure you have Python 3.9+ installed.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 2. Run with Docker
Build and run the containerizable application.

```bash
# Build the image
docker build -t land-record .

# Run the container
docker run -p 8501:8501 land-record
```

### 3. Deploy to GitHub Pages (Serverless)
This project uses **Stlite** (Streamlit for WebAssembly) to run Python code directly in the browser without any backend server.

#### Detailed Deployment Steps:
1.  **Create a GitHub Repository**: 
    - Create a new repository on GitHub (e.g., `land-record-system`).
2.  **Upload Files**:
    - Push all files (`app.py`, `index.html`, `requirements.txt`, etc.) to the `main` branch.
3.  **Enable GitHub Pages**:
    - Go to your repository **Settings** > **Pages**.
    - Under **Build and deployment** > **Source**, ensure it is set to "Deploy from a branch".
    - Select branch `main` and folder `/ (root)`.
    - Click **Save**.
4.  **Wait for Build**:
    - GitHub Actions will start a workflow to deploy your site. You can monitor this in the **Actions** tab.
5.  **Access Your Site**:
    - Once finished, your site will be live at `https://<your-username>.github.io/<repo-name>/`.

> **Note**: The `index.html` file acts as the entry point. It loads `stlite`, which then reads your `app.py` and runs it using WebAssembly. There is no cost for hosting and it works instantly!

## Data Source
The application pulls data from a public Google Sheet:
[CSV Export Link](https://docs.google.com/spreadsheets/d/1YQmkQzvpoFUBxXLuc9QWsgRqmRn3YZOBED6UmCuqsXk/export?format=csv)
