import os
import PyPDF2
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

# Load environment variables from .env file 
load_dotenv()

class DocReader:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def read_pdf(self, file_path):
        """
        Reads and extracts text from a PDF file.
        """
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
            print("Error: The specified PDF file was not found.")
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return None

    def read_word(self, file_path):
        """
        Reads and extracts text from a Word (.docx) file.
        """
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except FileNotFoundError:
            print("Error: The specified Word file was not found.")
        except Exception as e:
            print(f"Error reading Word file: {e}")
        return None

    def process_with_llm(self, text, prompt):
        """
        Processes the extracted text with the OpenAI LLM.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}:\n{text}"}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error processing with LLM: {e}")
        return None


def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        print("Error: OpenAI API key not found. Set OPENAI_API_KEY in your environment or .env file.")
        return

    doc_reader = DocReader(OPENAI_API_KEY)

    file_path = input("Enter the full path to your PDF or DOCX file: ").strip()

    if not os.path.exists(file_path):
        print("Error: File not found! Please provide a valid file path.")
        return

    if file_path.lower().endswith('.pdf'):
        content = doc_reader.read_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        content = doc_reader.read_word(file_path)
    else:
        print("Error: Unsupported file format. Please provide a PDF or DOCX file.")
        return

    if not content:
        print("Error: Failed to extract content from the file.")
        return

    print("\nFile content extracted successfully!\n")

    prompt = input("Enter a prompt for the LLM (e.g., summarize this document): ").strip()
    if not prompt:
        print("Error: Prompt cannot be empty.")
        return

    processed_result = doc_reader.process_with_llm(content, prompt)

    if processed_result:
        print("\nLLM Response:\n")
        print(processed_result)
    else:
        print("Error: Failed to process the content with the LLM.")


if __name__ == "__main__":
    main()
