import streamlit as st
import pandas as pd
import io
import requests

# Set page settings
st.set_page_config(
    page_title="Land Record Search System",
    layout="wide",
    initial_sidebar_state="expanded"
)


    


# Fixed values
DATA_URL = "https://docs.google.com/spreadsheets/d/1YQmkQzvpoFUBxXLuc9QWsgRqmRn3YZOBED6UmCuqsXk/export?format=csv"

# Dictionary for languages
TRANSLATIONS = {
    'NP': {
        'header_title': "भू-उपयोग क्षेत्र वर्गीकरण खोज प्रणाली",
        'sidebar_title': "फिल्टरहरू र नियन्त्रणहरू",
        'refresh_button': "डाटा रिफ्रेस गर्नुहोस्",
        'loading_msg': "तथ्याङ्क लोड हुँदैछ...",
        'connection_error': "तथ्याङ्क लोड गर्न सकिएन। कृपया इन्टरनेट जडान जाँच गर्नुहोस् वा पुनः प्रयास गर्नुहोस्।",
        'total_results': "जम्मा नतिजा",
        'kit_number': "कित्ता नं.",
        'vdc': "साविक गा.",
        'ward': "वडा नं.",
        'land_use': "भूउपयोग क्षेत्र",
        'select_placeholder': "टाईप गर्नुहोस् या छान्नुहोस्",
        'missing_cols_msg': "केही columns फेला परेनन्",
        'available_cols_msg': "उपलब्ध columns"
    },
    'EN': {
        'header_title': "Land Use Classification Search System",
        'sidebar_title': "Filters & Controls",
        'refresh_button': "Refresh Data",
        'loading_msg': "Loading Data...",
        'connection_error': "Could not load data. Please check internet connection or try again.",
        'total_results': "Total Results",
        'kit_number': "Plot/Kitta No.",
        'vdc': "VDC",
        'ward': "Ward No.",
        'land_use': "Land Use",
        'select_placeholder': "Type or Select",
        'missing_cols_msg': "Some columns missing",
        'available_cols_msg': "Available Columns"
    }
}

# This function gets data
@st.cache_data(ttl=600, show_spinner=False)
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
    # Button to switch language
    # Start with Nepali language
    lang_choice = st.sidebar.radio("भाषा (Language)", options=["नेपाली", "English"], horizontal=True)
    lang_code = 'NP' if lang_choice == "नेपाली" else 'EN'
    t = TRANSLATIONS[lang_code]

    # Dynamic animation name to force re-triggering on language change
    anim_name = f"textFadeIn_{lang_code}"

    # Custom CSS for UI Animations
    st.markdown(f"""
    <style>
        /* Global Fade In */
        .stApp {{
            animation: fadeIn 0.8s ease-in-out;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}

        /* Smooth Sidebar Transition ("Well") */
        section[data-testid="stSidebar"] {{
            transition: all 0.5s ease;
        }}

        /* Smooth Transitions for Buttons */
        div.stButton > button {{
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }}
        div.stButton > button:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        /* Dropdown & Input Animation */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
        }}
        div[data-baseweb="select"]:hover,
        div[data-baseweb="input"]:hover {{
            transform: translateY(-1px);
        }}

        /* Dropdown Menu Items (Popovers) */
        li[data-baseweb="menu-item"], div[data-baseweb="menu-item"] {{
            transition: background-color 0.2s ease !important;
        }}

        /* DataFrame/Table styling - Subtler, Faster Animation for "Reflow" feel */
        div[data-testid="stDataFrame"] {{
            transition: opacity 0.3s ease;
            animation: slideUp 0.4s ease-out;
        }}
        @keyframes slideUp {{
            0% {{ transform: translateY(10px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}

        /* Metric/Card hover effects */
        div[data-testid="metric-container"] {{
            transition: transform 0.2s ease;
        }}
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-2px);
        }}

        /* Smooth Text Transitions for Language Change */
        /* We change the animation name based on language to FORCE it to replay */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stButton button, div[data-baseweb="select"] div, span {{
            animation: {anim_name} 0.6s ease-in-out;
        }}

        @keyframes {anim_name} {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}

        /* Smooth transition for the whole sidebar */
        section[data-testid="stSidebar"] > div {{
             transition: all 0.5s ease-in-out;
        }}
    </style>
""", unsafe_allow_html=True)

    st.title(t['header_title'])

    # Get the data now
    with st.spinner(t['loading_msg']):
        df = load_data()

    if df is not None:
        # Fix column names, remove spaces
        df.columns = df.columns.str.strip()
        
        # Side menu for options
        st.sidebar.title(t['sidebar_title'])
        
        # Button to get new data
        if st.sidebar.button(t['refresh_button'], type="primary", use_container_width=True):
            st.cache_data.clear()
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()

        st.sidebar.divider()
        # Map the names to file columns. If name wrong, show error.
        
        # Names we look for in file
        # Change if file has different names.
        col_vdc = 'साविक गा.'
        col_ward = 'वडा नं.'
        col_plot = 'कित्ता नं.'
        col_land_use = 'भूउपयोग क्षेत्र'
        
        available_columns = df.columns.tolist()
        
        # Delete bad columns starting with Unnamed
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        available_columns = df.columns.tolist()

        # Make filters work
        filtered_df = df.copy()

        # 1. Filter for Plot (First one)
        if col_plot in available_columns:
            # User want type to search. We make list of all plots.
            # Make sure all are text.
            plot_options = sorted(df[col_plot].dropna().unique().astype(str).tolist())
            selected_plot = st.sidebar.selectbox(
                t['kit_number'], 
                plot_options,
                index=None,
                placeholder=t['select_placeholder']
            )
            if selected_plot:
                 # Check if text match plot name
                filtered_df = filtered_df[filtered_df[col_plot].astype(str) == selected_plot]

        # 2. Filter for VDC
        if col_vdc in available_columns:
            # Start with nothing selected
            vdc_options = sorted(df[col_vdc].dropna().unique().tolist())
            selected_vdc = st.sidebar.selectbox(
                t['vdc'], 
                vdc_options, 
                index=None, 
                placeholder=t['select_placeholder']
            )
            if selected_vdc:
                filtered_df = filtered_df[filtered_df[col_vdc] == selected_vdc]
        
        # 3. Filter for Ward (depends on VDC)
        if col_ward in available_columns:
            # Show only wards for this VDC
            ward_options = sorted(filtered_df[col_ward].dropna().unique().tolist())
            selected_ward = st.sidebar.selectbox(
                t['ward'], 
                ward_options, 
                index=None, 
                placeholder=t['select_placeholder']
            )
            if selected_ward:
                filtered_df = filtered_df[filtered_df[col_ward] == selected_ward]

        # No filter for Land Use. User said remove.
        
        # Put important columns first
        # Kit Number, VDC, Ward goes to front
        priority_cols = [c for c in [col_plot, col_vdc, col_ward] if c in filtered_df.columns]
        other_cols = [c for c in filtered_df.columns if c not in priority_cols]
        final_cols = priority_cols + other_cols
        filtered_df = filtered_df[final_cols]

        # Show the table
        st.write(f"जम्मा नतिजा (Total Results): {len(filtered_df)}")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=640)
        
        # Help fix if columns missing
        missing_cols = [c for c in [col_vdc, col_ward, col_plot, col_land_use] if c not in available_columns]
        if missing_cols:
            st.warning(f"केही स्तम्भहरू फेला परेनन् (Some columns missing): {', '.join(missing_cols)}")
            st.info(f"उपलब्ध स्तम्भहरू (Available Columns): {', '.join(available_columns)}")

if __name__ == "__main__":
    main()
