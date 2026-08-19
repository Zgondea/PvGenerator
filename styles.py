def load_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* RESET & GENERAL BASE */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            color: #F3F4F6 !important;
            background-color: #0B0F19 !important;
        }

        .stApp {
            background-color: #0B0F19 !important;
        }

        /* HEADER PRINCIPAL */
        h1 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
            letter-spacing: -0.02em !important;
            color: #FFFFFF !important;
            margin-bottom: 24px !important;
            padding-bottom: 12px !important;
            border-bottom: 1px solid #1F2937 !important;
        }

        /* SUBSECTIUNI & CARDURI */
        h2, h3, .stSubheader {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            color: #818CF8 !important;
            margin-bottom: 16px !important;
            border-left: none !important;
            padding-left: 0 !important;
        }

        /* CONTAINER SECȚIUNI (ENTERPRISE CARDS) */
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
            background-color: #111827 !important;
            border: 1px solid #1F2937 !important;
            border-radius: 8px !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1) !important;
        }

        /* LABELS & ETICHETE INPUT */
        label, .stWidgetLabel {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            color: #9CA3AF !important;
            margin-bottom: 6px !important;
        }

        /* CÂMPURI DE INPUT & DROPDOWNS */
        div[data-baseweb="input"], 
        div[data-baseweb="select"], 
        div[data-baseweb="base-input"] {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 6px !important;
            transition: all 0.15s ease !important;
        }

        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="select"]:focus-within {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
        }

        input, textarea {
            color: #F9FAFB !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
        }

        /* MENIU DROPDOWN (POPUP) */
        div[data-baseweb="popover"], ul[role="listbox"] {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 6px !important;
        }

        li[role="option"] {
            color: #E5E7EB !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
        }

        li[role="option"]:hover, li[aria-selected="true"] {
            background-color: #374151 !important;
            color: #FFFFFF !important;
        }

        /* SIDEBAR PRO */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1E293B !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #F3F4F6 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }

        /* FILE UPLOADER SIDEBAR FIX */
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background-color: #1E293B !important;
            border: 1px dashed #475569 !important;
            border-radius: 6px !important;
            padding: 12px !important;
        }

        /* BUTOANE */
        .stButton > button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            border-radius: 6px !important;
            background-color: #1F2937 !important;
            color: #E5E7EB !important;
            border: 1px solid #374151 !important;
            padding: 8px 16px !important;
            transition: all 0.15s ease !important;
        }

        .stButton > button:hover {
            background-color: #374151 !important;
            color: #FFFFFF !important;
            border-color: #4B5563 !important;
        }

        /* BUTON PRINCIPAL (PRIMARY ACTION) */
        .stButton > button[kind="primary"] {
            background-color: #4F46E5 !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #4338CA !important;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3) !important;
        }

        /* TAG-URI & CHIPS IN MULTISELECT */
        span[data-baseweb="tag"] {
            background-color: #312E81 !important;
            border: 1px solid #4338CA !important;
            border-radius: 4px !important;
        }

        span[data-baseweb="tag"] span {
            color: #E0E7FF !important;
        }

        /* SCROLLBAR MODERNA */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0B0F19;
        }
        ::-webkit-scrollbar-thumb {
            background: #1F2937;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #374151;
        }
    </style>
    """