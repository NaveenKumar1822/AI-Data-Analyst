import streamlit as st
from sql_assistant import generate_sql, db


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    [data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }

    .sidebar-section {
        font-size: 0.8rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 1.4rem;
        margin-bottom: 0.7rem;
    }


    /* -------------------------------------------------------
       HERO
    ------------------------------------------------------- */

    .hero {
        padding: 0.5rem 0 1.5rem 0;
    }

    .hero-title {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Helvetica, Arial, sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 2.2;
    margin-bottom: 0.6rem;
}

    .hero-subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        max-width: 720px;
        line-height: 1.6;
    }

    .status-row {
        margin-top: 1rem;
    }

    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        margin-right: 0.45rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        border: 1px solid #e5e7eb;
        background: #f8fafc;
    }

    .status-live {
        color: #15803d;
        background: #f0fdf4;
        border-color: #bbf7d0;
    }


    /* -------------------------------------------------------
       SECTION TITLES
    ------------------------------------------------------- */

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }


    /* -------------------------------------------------------
       QUERY AREA
    ------------------------------------------------------- */

    .query-label {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }


    /* -------------------------------------------------------
       RESULT AREA
    ------------------------------------------------------- */

    .analysis-header {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .result-card {
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.15rem;
        background: #ffffff;
        min-height: 100px;
    }

    .result-card-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
    }

    .result-card-content {
        font-size: 0.95rem;
        line-height: 1.5;
    }


    /* -------------------------------------------------------
       EMPTY STATE
    ------------------------------------------------------- */

    .empty-state {
        text-align: center;
        padding: 4rem 1rem;
        border: 1px dashed #d1d5db;
        border-radius: 16px;
        background: #fafafa;
        margin-top: 2rem;
    }

    .empty-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .empty-title {
        font-size: 1.1rem;
        font-weight: 700;
    }

    .empty-description {
        color: #6b7280;
        margin-top: 0.3rem;
    }


    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        border: 1px solid #e5e7eb;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #9ca3af;
    }


    /* -------------------------------------------------------
       INPUT
    ------------------------------------------------------- */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }


    /* -------------------------------------------------------
       EXPANDER
    ------------------------------------------------------- */

    .streamlit-expanderHeader {
        font-weight: 600;
    }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "last_sql" not in st.session_state:
    st.session_state.last_sql = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Apply any example-question click BEFORE the text_input widget
# (with key="question_input") is instantiated below. Setting
# st.session_state["question_input"] AFTER that widget has been
# created in the same run raises a StreamlitAPIException, which
# is what the example buttons used to trigger.
if st.session_state.pending_question is not None:
    st.session_state.question_input = st.session_state.pending_question
    st.session_state.pending_question = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        '<div class="sidebar-title">📊 AI Data Analyst</div>'
    )

    st.html(
        '<div class="sidebar-subtitle">'
        'Natural-language analytics assistant'
        '</div>'
    )

    st.divider()

    # Database

    st.html(
        '<div class="sidebar-section">Database</div>'
    )

    st.markdown(
        """
        **Retail Analytics Database**

        🧑‍💼 **100** customers

        📦 **30** products

        🧾 **5,000** orders

        📅 **2024–2025** data
        """
    )

    # Tables

    st.html(
        '<div class="sidebar-section">Tables</div>'
    )

    with st.expander("customers"):
        st.caption(
            "Customer profiles, regions and segments."
        )

    with st.expander("products"):
        st.caption(
            "Product names, categories and prices."
        )

    with st.expander("orders"):
        st.caption(
            "Order dates, quantities and revenue."
        )

    # Tech stack

    st.html(
        '<div class="sidebar-section">Technology</div>'
    )

    st.markdown(
        """
        `Python`  
        `LangChain`  
        `Code Llama`  
        `SQLite`  
        `Streamlit`
        """
    )

    st.divider()

    st.caption(
        "AI Data Analyst · Data Science Portfolio Project"
    )


# ============================================================
# HERO SECTION
# ============================================================

st.html(
    """
    <div class="hero">
        <div class="hero-title">
            📊 AI Data Analyst
        </div>
        <div class="hero-subtitle">
            Ask questions about your retail data in plain English.
            The assistant generates SQL, queries the database,
            and returns the relevant analysis.
        </div>
        <div class="status-row">
            <span class="status-badge status-live">
                ● Local AI
            </span>
            <span class="status-badge">
                SQLite
            </span>
            <span class="status-badge">
                LangChain
            </span>
            <span class="status-badge">
                Code Llama
            </span>
        </div>
    </div>
    """
)


# ============================================================
# QUESTION SECTION
# ============================================================

st.html(
    '<div class="section-title">Ask your data</div>'
)


# ============================================================
# QUESTION FORM
# ============================================================

with st.form("query_form"):

    question = st.text_input(
        "Question",
        key="question_input",
        placeholder=(
            "e.g. Which category generated the most revenue?"
        ),
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "Analyze →",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.html(
    '<div class="section-title">Try an example</div>'
)

example_columns = st.columns(4)

examples = [
    (
        "🏆",
        "Top product",
        "Which product generated the highest revenue?"
    ),
    (
        "🌎",
        "Revenue by region",
        "What is the total revenue by region?"
    ),
    (
        "📈",
        "Monthly revenue",
        "What were the monthly revenues in 2025?"
    ),
    (
        "👥",
        "Top customers",
        "Who are the top 10 customers by revenue?"
    )
]


for column, (icon, title, example) in zip(
    example_columns,
    examples
):

    with column:

        if st.button(
            f"{icon} {title}",
            use_container_width=True
        ):

            # Don't write to st.session_state.question_input here —
            # the text_input widget above already claimed that key
            # for this run. Stash the value and apply it on rerun,
            # before the widget is instantiated again.
            st.session_state.pending_question = example
            st.rerun()


# ============================================================
# PROCESS QUESTION
# ============================================================

if submitted and question.strip():

    st.session_state.last_question = question

    with st.spinner("🤖 Generating SQL..."):

        try:

            sql = generate_sql(question)

            st.session_state.last_sql = sql

            with st.spinner("🔎 Querying the database..."):

                result = db.run(sql)

            st.session_state.last_result = result

        except Exception as e:

            st.session_state.last_sql = None
            st.session_state.last_result = None

            st.error(
                f"Something went wrong: {e}"
            )


# ============================================================
# EMPTY STATE
# ============================================================

if st.session_state.last_question is None:

    st.html(
        """
        <div class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-title">
                Your data is ready to explore
            </div>
            <div class="empty-description">
                Ask a question above or choose one of the
                example queries to get started.
            </div>
        </div>
        """
    )


# ============================================================
# ANALYSIS RESULTS
# ============================================================

if st.session_state.last_question is not None:

    st.html(
        '<div class="analysis-header">Analysis</div>'
    )


    # --------------------------------------------------------
    # Question + Result
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="result-card">
                <div class="result-card-title">
                    💬 Your question
                </div>
            """
        )

        st.write(
            st.session_state.last_question
        )

        st.html("</div>")


    with col2:

        st.html(
            """
            <div class="result-card">
                <div class="result-card-title">
                    📋 Query result
                </div>
            """
        )

        st.write(
            st.session_state.last_result
        )

        st.html("</div>")


    # --------------------------------------------------------
    # Generated SQL
    # --------------------------------------------------------

    st.markdown("### 🔍 Generated SQL")

    with st.expander(
        "View the SQL generated by the AI",
        expanded=False
    ):

        st.code(
            st.session_state.last_sql,
            language="sql"
        )