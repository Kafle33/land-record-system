import streamlit as st
import pandas as pd
import io
import requests

# Page configuration
st.set_page_config(
    page_title="Land Record Search System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
DATA_URL = "https://docs.google.com/spreadsheets/d/1YQmkQzvpoFUBxXLuc9QWsgRqmRn3YZOBED6UmCuqsXk/export?format=csv"

# Localization
HEADER_TITLE = "भू-उपयोग क्षेत्र वर्गीकरण खोज प्रणाली"
SIDEBAR_TITLE = "फिल्टरहरू र नियन्त्रणहरू (Filters & Controls)"
REFRESH_BUTTON_LABEL = "डाटा रिफ्रेस गर्नुहोस् (Refresh Data)"
ERROR_MSG_CONNECTION = "तथ्याङ्क लोड गर्न सकिएन। कृपया इन्टरनेट जडान जाँच गर्नुहोस् वा पुनः प्रयास गर्नुहोस्।"
SUCCESS_MSG_LOADED = "तथ्याङ्क सफलतापूर्वक लोड भयो!"

# Function to load data
@st.cache_data(ttl=600)
def load_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))
        return df
    except Exception as e:
        st.error(f"{ERROR_MSG_CONNECTION}: {e}")
        return None

def main():
    st.title(HEADER_TITLE)

    # Load data
    df = load_data()

    if df is not None:
        # Normalize column names to strip spaces if any
        df.columns = df.columns.str.strip()
        
        # Sidebar for filtering and controls
        st.sidebar.title(SIDEBAR_TITLE)
        
        # Fresh Data Refresh Button
        if st.sidebar.button(REFRESH_BUTTON_LABEL, type="primary", use_container_width=True):
            st.cache_data.clear()
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()

        st.sidebar.divider()
        # 'साविक गा.' (VDC), 'वडा नं.' (Ward), 'कित्ता नं.' (Plot), 'भूउपयोग क्षेत्र' (Land Use)
        # We need to map these to the actual CSV columns. 
        # Since I cannot see the CSV content right now, I will try to infer or use the exact names provided 
        # and if they don't exist, I'll display available columns for debugging or fall back gracefully.
        
        # Expected column names in the CSV (based on standard Nepali datasets or the prompt request)
        # Adjust these if the CSV headers are different.
        col_vdc = 'साविक गा.'
        col_ward = 'वडा नं.'
        col_plot = 'कित्ता नं.'
        col_land_use = 'भूउपयोग क्षेत्र'
        
        available_columns = df.columns.tolist()
        
        # Remove any artifact columns like 'Unnamed: 0'
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        available_columns = df.columns.tolist()

        # Create dynamic filters
        filtered_df = df.copy()

        # 1. Plot Filter (Moved to Top)
        if col_plot in available_columns:
            # User requested "search as i type" which is best supported by selectbox with index=None
            # Convert to string options for consistent searching
            plot_options = sorted(df[col_plot].dropna().unique().astype(str).tolist())
            selected_plot = st.sidebar.selectbox(
                f"{col_plot}", 
                plot_options,
                index=None,
                placeholder="छान्नुहोस् (Select)"
            )
            if selected_plot:
                 # Search against string version of the column
                filtered_df = filtered_df[filtered_df[col_plot].astype(str) == selected_plot]

        # 2. VDC Filter
        if col_vdc in available_columns:
            # Use index=None to default to empty
            vdc_options = sorted(df[col_vdc].dropna().unique().tolist())
            selected_vdc = st.sidebar.selectbox(
                f"{col_vdc}", 
                vdc_options, 
                index=None, 
                placeholder="छान्नुहोस् (Select)"
            )
            if selected_vdc:
                filtered_df = filtered_df[filtered_df[col_vdc] == selected_vdc]
        
        # 3. Ward Filter based on VDC selection
        if col_ward in available_columns:
            # Update options based on current filtered data
            ward_options = sorted(filtered_df[col_ward].dropna().unique().tolist())
            selected_ward = st.sidebar.selectbox(
                f"{col_ward}", 
                ward_options, 
                index=None, 
                placeholder="छान्नुहोस् (Select)"
            )
            if selected_ward:
                filtered_df = filtered_df[filtered_df[col_ward] == selected_ward]

        # Land Use Filter removed as per user request (it is an output field)
        
        # Reorder Columns for Display
        # Move Kit Number, VDC, Ward to the front
        priority_cols = [c for c in [col_plot, col_vdc, col_ward] if c in filtered_df.columns]
        other_cols = [c for c in filtered_df.columns if c not in priority_cols]
        final_cols = priority_cols + other_cols
        filtered_df = filtered_df[final_cols]

        # Display data
        st.write(f"जम्मा नतिजा (Total Results): {len(filtered_df)}")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Debugging: Show all columns if expected ones aren't found
        missing_cols = [c for c in [col_vdc, col_ward, col_plot, col_land_use] if c not in available_columns]
        if missing_cols:
            st.warning(f"केही स्तम्भहरू फेला परेनन् (Some columns missing): {', '.join(missing_cols)}")
            st.info(f"उपलब्ध स्तम्भहरू (Available Columns): {', '.join(available_columns)}")

if __name__ == "__main__":
    main()
