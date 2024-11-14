import streamlit as st
import google.generativeai as genai
import pandas as pd
import time

# Configure the API key
genai.configure(api_key="AIzaSyDUKuFJ49VVqgPIfVJAzwcw2Q6NCKiDRtI")  # Replace "YOUR_API_KEY" with your actual API key

# Function to load and preview Excel data
def load_excel_data(file):
    # Load the Excel file into a DataFrame
    data = pd.read_excel(file)
    # Convert the entire DataFrame to a readable string format for the prompt
    data_context = data.to_string(index=False)
    return data_context

# Function to send a request to the model
def send_request(chat, context, question):
    try:
        # Combine context and question into a single prompt
        prompt = f"Here is the data:\n\n{context}\n\nQuestion: {question}"
        response = chat.send_message(prompt)
        return response
    except Exception as e:
        st.error(f"Error occurred: {e}")
        time.sleep(5)  # Wait before retrying
        return None

# Main function to load data, format it, preview it, and ask a query
def ask_model_with_excel(file, question):
    # Load Excel data, format it, and print a preview
    data_context = load_excel_data(file)
    
    # Start a chat with the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    chat = model.start_chat()
    
    # Send the request with the data context and question
    response = send_request(chat, data_context, question)
    
    if response:
        # Extract and return the answer from the model's response
        return response.candidates[0].content.parts[0].text
    else:
        return "No response received."

# Streamlit UI
st.title("Excel Question-Answer System")
st.write("Upload an Excel file and ask questions about the data.")

# File uploader component
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Show a preview of the uploaded file
    st.subheader("Excel Data Preview")
    data = pd.read_excel(uploaded_file)
    st.dataframe(data)  # Display the Excel data as a table

    # Question input
    question = st.text_input("Enter your question:")

    # Process the question when the user clicks the "Ask" button
    if st.button("Ask"):
        if question:
            with st.spinner("Processing your question..."):
                # Get the answer from the model
                answer = ask_model_with_excel(uploaded_file, question)
                # Display the answer
                st.subheader("Answer")
                st.write(answer)
        else:
            st.warning("Please enter a question.")
