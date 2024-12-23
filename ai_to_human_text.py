import subprocess
import sys
import os

# Function to install required libraries
def install_packages():
    required_packages = ["openai", "tqdm"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required libraries before proceeding
install_packages()

# Import libraries after installation
import openai
from tqdm import tqdm
import threading
from queue import Queue

# Set up the OpenAI API key
openai.api_key = 'your-api-key-here'

# Parameters
MAX_TOKENS = 150
CHUNK_SIZE = 3000
THREAD_COUNT = 5

def print_banner():
    """Prints a colorful custom banner."""
    banner = """
\033[91m      **     **       **********                **      **                                              **********                   **  
\033[93m     ****   //       /////**///                /**     /**                                             /////**///                   /**  
\033[92m    **//**   **          /**      ******       /**     /** **   ** **********   ******   *******           /**      *****  **   ** ******  
\033[96m   **  //** /**          /**     **////**      /**********/**  /**//**//**//** //////** //**///**          /**     **///**//** ** ///**/   
\033[94m  **********/**          /**    /**   /**      /**//////**/**  /** /** /** /**  *******  /**  /**          /**    /******* //***    /**    
\033[95m /**//////**/**          /**    /**   /**      /**     /**/**  /** /** /** /** **////**  /**  /**          /**    /**////   **/**   /**    
\033[91m /**     /**/**          /**    //******       /**     /**//****** *** /** /**//******** ***  /**          /**    //****** ** //**  //**   
\033[93m //      // //           //      //////        //      //  ////// ///  //  //  //////// ///   //           //      ////// //   //    //    
\033[94m       AI Text to Human Text Converter - Created by Shaid Mahamud
\033[0m
"""
    print(banner)  # Prints the colorful banner

def convert_ai_to_human_text(ai_text):
    """Send AI-generated text to OpenAI API for conversion."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Rewrite the following AI-generated text to make it sound more human-like:\n\n{ai_text}",
            max_tokens=MAX_TOKENS,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

def process_large_file(input_file, output_file):
    """Process a large file in chunks."""
    try:
        queue = Queue()
        threads = []
        progress_bar = None
        output_lines = []

        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        total_chunks = len(chunks)

        progress_bar = tqdm(total=total_chunks, desc="Processing Chunks", unit="chunk")

        def worker():
            while not queue.empty():
                chunk = queue.get()
                result = convert_ai_to_human_text(chunk)
                output_lines.append(result)
                progress_bar.update(1)
                queue.task_done()

        for chunk in chunks:
            queue.put(chunk)

        for _ in range(THREAD_COUNT):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n\n".join(output_lines))

        progress_bar.close()
        print(f"Processing complete. Output saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print_banner()  # Display the colorful banner
    print("\033[92mAdvanced AI to Human Text Converter for Large Files\033[0m")
    input_file = input("Enter the path to the input file: ").strip()
    output_file = input("Enter the path to save the output file: ").strip()

    if not os.path.exists(input_file):
        print("\033[91mError: Input file does not exist.\033[0m")
        return

    process_large_file(input_file, output_file)

if __name__ == "__main__":
    main()
              
