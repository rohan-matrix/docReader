import os
import PyPDF2
from docx import Document
import google.generativeai as genai

class DocReader:
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            raise

    def read_pdf(self, file_path):
        """Reads and extracts text from a PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                return text.strip()
        except FileNotFoundError:
            print(f"Error: The specified PDF file was not found at '{file_path}'.")
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return None

    def read_word(self, file_path):
        """Reads and extracts text from a DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except FileNotFoundError:
            print(f"Error: The specified Word file was not found at '{file_path}'.")
        except Exception as e:
            print(f"Error reading Word file: {e}")
        return None

    def process_with_llm(self, text, prompt):
        """Processes the extracted text with the Gemini model."""
        try:
            response = self.model.generate_content(f"{prompt}:\n{text}")
            return response.text.strip()
        except Exception as e:
            print(f"Error processing with Gemini: {e}")
        return None


def main():
    # Hardcoded Gemini API key (replace with your actual key)
    GEMINI_API_KEY = "AIzaSyBMwhDazSu0SpxyLcQBt8Rh5Pmu7cod3uM"  # Replace with your actual Gemini API key

    if not GEMINI_API_KEY:
        print("Error: Gemini API key is missing. Please add your API key to the script.")
        return

    # Initialize DocReader with the API key
    try:
        doc_reader = DocReader(GEMINI_API_KEY)
    except Exception as e:
        print(f"Failed to initialize DocReader: {e}")
        return

    # Get file path from user
    file_path = input("Enter the full path to your PDF or DOCX file: ").strip()

    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'. Please provide a valid file path.")
        return

    # Determine file type and extract content
    if file_path.lower().endswith('.pdf'):
        print("Extracting text from PDF...")
        content = doc_reader.read_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        print("Extracting text from DOCX...")
        content = doc_reader.read_word(file_path)
    else:
        print("Error: Unsupported file format. Please provide a PDF or DOCX file.")
        return

    if not content:
        print("Error: Failed to extract content from the file. Ensure the file is not corrupted.")
        return

    print("\nFile content extracted successfully!\n")

    # Get prompt from user
    prompt = input("Enter a prompt for Gemini (e.g., summarize this document): ").strip()
    if not prompt:
        print("Error: Prompt cannot be empty.")
        return

    # Process content with Gemini
    print("\nProcessing with Gemini. This may take a moment...\n")
    processed_result = doc_reader.process_with_llm(content, prompt)

    if processed_result:
        print("\nGemini Response:\n")
        print(processed_result)
    else:
        print("Error: Failed to process the content with Gemini.")


if __name__ == "__main__":
    main()
