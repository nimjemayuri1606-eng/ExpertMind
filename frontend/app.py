import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ExpertMind",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ExpertMind")
st.caption("Your AI-powered RAG Knowledge Mentor")

# Session management
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# API helper
def api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=120,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"API connection error: {error}")
        return None


# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "Upload Documents",
        "Ask ExpertMind",
        "Knowledge Gaps",
        "Learning Recommendations"
    ]
)

session_id = st.session_state.session_id


# 1. Dashboard
if page == "Dashboard":

    st.header("📊 Performance Dashboard")

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

    with st.spinner("Loading dashboard..."):

        data = api_request("GET", "/api/v1/dashboard")

    if data is None:
        st.error("Unable to load dashboard data. Check that the FastAPI server is running.")
    
    elif not isinstance(data, dict) or "summary" not in data:
        st.error("Dashboard API returned an invalid response.")

    else:
        summary = data["summary"]

        # Dashboard metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="📁 Documents",
                value=summary.get("total_documents", 0)
            )

        with col2:
            st.metric(
                label="📦 Total Chunks",
                value=summary.get("total_chunks", 0)
            )

        with col3:
            st.metric(
                label="🎯 Knowledge Gaps",
                value=summary.get("total_knowledge_gaps", 0)
            )

        with col4:
            st.metric(
                label="📚 Topics to Improve",
                value=summary.get("total_topics_to_improve", 0)
            )

        st.divider()

        # Uploaded Documents
        st.subheader("📄 Uploaded Documents")

        documents = data.get("documents", [])

        if documents:
            for document in documents:
                with st.container(border=True):
                    st.write(f"📄 **{document.get('filename', 'Unknown file')}**")
                    st.caption(
                        f"Document ID: {document.get('document_id', 'N/A')}"
                    )
                    st.write(f"📦 Chunks: {document.get('chunks', 0)}")
        else:
            st.info("No documents uploaded yet.")

        st.divider()

        # Recent Unanswered Questions
        st.subheader("❓ Recent Unanswered Questions")

        recent_questions = data.get(
            "knowledge_gaps", {}
        ).get("recent_questions", [])

        if recent_questions:
            for index, gap in enumerate(recent_questions, start=1):
                st.write(f"**{index}.** {gap['question']}")
        else:
            st.info("No unanswered questions recorded yet.")

        st.divider()

        # Learning Topics
        st.subheader("🎓 Learning Topics")

        learning_topics = data.get("learning_topics", [])

        if learning_topics:
            st.dataframe(
                learning_topics,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No learning topics identified yet.")


# 2. Upload Documents
elif page == "Upload Documents":

    st.header("Upload Learning Documents")

    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"]
    )

    if uploaded_file and st.button("Upload Document"):

        with st.spinner("Processing document..."):

            result = api_request(
                "POST",
                "/api/v1/documents/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }
            )

        if result:
            st.success("Document uploaded successfully!")
            st.json(result)
            st.rerun()


# 3. Ask ExpertMind
elif page == "Ask ExpertMind":

    st.header("Chat with Your Documents")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

            if message.get("sources"):
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.write(
                            f"File: {source['source']} | "
                            f"Page: {source.get('page')} | "
                            f"Chunk: {source.get('chunk')}"
                        )

    question = st.chat_input("Ask a question about your documents...")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("ExpertMind is thinking..."):

                result = api_request(
                    "POST",
                    "/api/v1/chat",
                    json={
                        "question": question,
                        "session_id": session_id
                    }
                )

            if result:

                answer = result["answer"]
                sources = result.get("sources", [])

                st.write(answer)

                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.write(
                                f"File: {source['source']} | "
                                f"Page: {source.get('page')} | "
                                f"Chunk: {source.get('chunk')}"
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            else:
                st.warning("Could not generate an answer.")

        st.rerun()


# 4. Knowledge Gaps
elif page == "Knowledge Gaps":

    st.header("Knowledge Gap Analysis")

    data = api_request(
        "GET",
        "/api/v1/knowledge-gaps/analyze",
        params={"session_id": session_id}
    )

    if data:
        st.metric(
            "Unanswered Questions",
            data["total_questions"]
        )

        st.subheader("Identified Topics")

        if data["recommendations"]:
            st.dataframe(
                data["recommendations"],
                use_container_width=True
            )
        else:
            st.info("No knowledge gaps identified yet.")


# 5. Learning Recommendations
elif page == "Learning Recommendations":

    st.header("Personalized Learning Recommendations")

    data = api_request(
        "GET",
        "/api/v1/learning-recommendations",
        params={"session_id": session_id}
    )

    if data:

        recommendations = data.get("recommendations", [])

        if recommendations:

            for item in recommendations:

                with st.container(border=True):

                    st.subheader(item["topic"])

                    st.write("**Why study this?**")
                    st.write(item["reason"])

                    st.write("**Suggested activity**")
                    st.write(item["activity"])

        else:
            st.info(
                "No recommendations available. "
                "Ask questions that are not answered by your documents "
                "to identify learning gaps."
            )