import streamlit as st
import pandas as pd
import os
from langchain_community.document_loaders import DataFrameLoader, TextLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from utils import process_text
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Set Page Config
st.set_page_config(
    page_title="Political-RAG Indonesia",
    page_icon="🗳️",
    layout="wide"
)

@st.cache_data
def load_data(uploaded_files):
    all_docs = []
    dataframe_preview = pd.DataFrame()

    if not uploaded_files:
        # Load sample data
        if os.path.exists("sample_politics.csv"):
            df = pd.read_csv("sample_politics.csv")
            loader = DataFrameLoader(df, page_content_column="content")
            all_docs.extend(loader.load())
            dataframe_preview = df
    else:
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.name.split('.')[-1].lower()

            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
                # Try to find a text column
                text_col = next((col for col in df.columns if 'content' in col.lower() or 'text' in col.lower() or 'berita' in col.lower()), df.columns[0])
                loader = DataFrameLoader(df, page_content_column=text_col)
                all_docs.extend(loader.load())
                dataframe_preview = pd.concat([dataframe_preview, df], ignore_index=True)

            elif file_type == 'xlsx':
                df = pd.read_excel(uploaded_file)
                text_col = next((col for col in df.columns if 'content' in col.lower() or 'text' in col.lower() or 'berita' in col.lower()), df.columns[0])
                loader = DataFrameLoader(df, page_content_column=text_col)
                all_docs.extend(loader.load())
                dataframe_preview = pd.concat([dataframe_preview, df], ignore_index=True)

            elif file_type == 'txt':
                text = uploaded_file.read().decode("utf-8")
                all_docs.append(Document(page_content=text, metadata={"source": uploaded_file.name}))
                # For preview, just add a row
                new_row = pd.DataFrame({"source": [uploaded_file.name], "content": [text[:200] + "..."]})
                dataframe_preview = pd.concat([dataframe_preview, new_row], ignore_index=True)

    return all_docs, dataframe_preview

def main():
    st.title("🗳️ Political-RAG: Asisten Politik Indonesia")
    st.write("Generative AI untuk ekstraksi informasi politik dari media konten.")

    # Sidebar
    with st.sidebar:
        st.header("Konfigurasi")
        openai_api_key = st.text_input("OpenAI API Key", type="password")

        st.header("Unggah Data")
        uploaded_files = st.file_uploader(
            "Upload file CSV, Excel, atau TXT",
            type=["csv", "xlsx", "txt"],
            accept_multiple_files=True
        )

        st.info("Jika tidak ada file yang diunggah, aplikasi akan menggunakan data sampel default.")

        if st.button("Reset Knowledge Base"):
            st.session_state.pop("vectorstore", None)
            st.session_state.pop("qa_chain", None)
            st.session_state.pop("chat_history", None)
            st.session_state.pop("messages", None)
            st.rerun()

    # Tabs
    tab1, tab2 = st.tabs(["📊 Dashboard Insight", "💬 Chat RAG AI"])

    # Load Data
    docs, df_preview = load_data(uploaded_files)

    with tab1:
        st.header("Dashboard Analisis Politik")
        if not df_preview.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Preview Data")
                st.dataframe(df_preview)

            with col2:
                st.subheader("Statistik")
                st.metric("Total Dokumen", len(docs))
                # Simple word count visualization
                if 'content' in df_preview.columns:
                    all_text = " ".join(df_preview['content'].astype(str).tolist())
                    words = pd.Series(all_text.lower().split()).value_counts().head(20)
                    st.bar_chart(words)
        else:
            st.write("Belum ada data yang diproses.")

    with tab2:
        st.header("Tanya Jawab Politik")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if not openai_api_key:
            st.warning("Silakan masukkan OpenAI API Key untuk memulai chat.")
        else:
            if docs:
                # Process text & Setup Vector Store (Cached resource would be better but this works for demo)
                # We use a hash of the content to check if we need to rebuild
                # For simplicity in this demo, we rebuild if not in session state or simple check

                if "vectorstore" not in st.session_state:
                    with st.spinner("Memproses dokumen..."):
                        splits = process_text(docs)
                        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
                        st.session_state.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

                        st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
                            llm=ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0.2),
                            retriever=st.session_state.vectorstore.as_retriever(),
                            return_source_documents=True
                        )
                        st.session_state.chat_history = []

                # React to user input
                if prompt := st.chat_input("Apa yang ingin Anda ketahui tentang situasi politik?"):
                    st.chat_message("user").markdown(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    with st.chat_message("assistant"):
                        with st.spinner("Sedang menganalisis..."):
                            # Run the chain
                            response = st.session_state.qa_chain({
                                "question": prompt,
                                "chat_history": st.session_state.chat_history
                            })
                            answer = response['answer']

                            # Update chat history for the chain
                            st.session_state.chat_history.append((prompt, answer))

                            st.markdown(answer)

                            # Show sources (optional but insightful)
                            with st.expander("Sumber Referensi"):
                                for doc in response['source_documents']:
                                    st.caption(f"Sumber: {doc.metadata.get('source', 'Unknown')}")
                                    st.text(doc.page_content[:200] + "...")

                    st.session_state.messages.append({"role": "assistant", "content": answer})

            else:
                st.error("Tidak ada dokumen yang dimuat.")

if __name__ == "__main__":
    main()
