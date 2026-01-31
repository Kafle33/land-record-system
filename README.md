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

### 3. Static Hosting on GitHub Pages (Experimental)
This project includes an `index.html` that uses **Stlite** (Streamlit for WebAssembly) to run Python code directly in the browser. 

> [!NOTE]
> GitHub Pages is **static hosting**. It does not run Docker or a real Python server. It uses your browser's CPU to run the code. For "Enterprise" or heavy use, the Dockerized method above is preferred on a dedicated server.

#### GitHub Pages Setup:
1.  **Create a GitHub Repository**: (e.g., `land-record-system`).
2.  **Upload Files**: Push all files to the `main` branch.
3.  **Enable GitHub Pages**: **Settings** > **Pages** > **Source: Deploy from branch** > **Save**.
4.  **Access**: `https://<your-username>.github.io/<repo-name>/`.

### 4. Deploy to Streamlit Community Cloud (Recommended for Production)
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
