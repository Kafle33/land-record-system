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

### 2. Run with Docker (Recommended for Stability)
For a robust production environment, use Docker. This keeps the application logic running on a stable Python backend.

#### Using Docker Compose:
```bash
# Build and start the container
docker-compose up -d
```
Access the app at `http://localhost:8501`.

#### Using Docker CLI:
```bash
# Build the image
docker build -t land-record .

# Run the container
docker run -p 8501:8501 land-record
```


### 3. Deploy to GitHub Pages (Free & Easy)
You can deploy this directly to GitHub Pages using **Stlite**. This allows the app to run entirely in the browser (Client-side) without a backend server.

**How it works:**
The `index.html` file loads a lightweight runtime (Stlite) that executes your `app.py` directly in the user's browser using WebAssembly.

#### Step-by-Step Deployment Guide:
1.  **Create a Repository**:
    - Go to GitHub and create a new public repository (e.g., `land-record-system`).
2.  **Upload Files**:
    - Push the following files to your repository's `main` branch:
        - `app.py`
        - `index.html` (Required for Stlite)
        - `requirements.txt`
3.  **Enable GitHub Pages**:
    - Go to your repository's **Settings** tab.
    - Click **Pages** in the left sidebar.
    - Under **Source**, select **"Deploy from a branch"**.
    - Verify that **Branch** is set to `main` and folder is `/(root)`.
    - Click **Save**.
4.  **Wait & Visit**:
    - Wait about 1-2 minutes for the "GitHub Actions" deployment to finish.
    - Refresh the Pages settings page to see your live URL (e.g., `https://yourname.github.io/land-record-system/`).

### 4. Deploy to Streamlit Community Cloud (Alternative)
For the most stable and performant experience with a real Python backend:
1.  Push your code to a GitHub repository.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Connect your GitHub account and select your repository and `app.py`.
4.  Click **Deploy**. This provides a custom URL and better performance than WebAssembly.

## Troubleshooting
If you encounter `AttributeError: module 'streamlit' has no attribute 'rerun'` in older environments:
- This is now handled automatically in `app.py` with a fallback to `st.experimental_rerun()`.
- Ensure your `index.html` uses the latest Stlite version (currently `0.76.3`).

## Data Source
The application pulls data from a public Google Sheet:
[CSV Export Link](https://docs.google.com/spreadsheets/d/1YQmkQzvpoFUBxXLuc9QWsgRqmRn3YZOBED6UmCuqsXk/export?format=csv)
