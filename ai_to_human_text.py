import os
import subprocess
import sys
from pathlib import Path

# Constants
VENV_DIR = Path("venv")
REQUIRED_PACKAGES = ["openai", "tqdm"]
MAX_TOKENS = 150
CHUNK_SIZE = 3000
THREAD_COUNT = 5

def setup_virtual_environment():
    """Creates a virtual environment and installs required packages."""
    if not VENV_DIR.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    pip_executable = VENV_DIR / "bin" / "pip" if os.name != "nt" else VENV_DIR / "Scripts" / "pip"
    for package in REQUIRED_PACKAGES:
        print(f"Installing {package}...")
        subprocess.check_call([str(pip_executable), "install", package])

def run_script():
    """Runs the main script inside the virtual environment."""
    python_executable = VENV_DIR / "bin" / "python" if os.name != "nt" else VENV_DIR / "Scripts" / "python"
    subprocess.check_call([str(python_executable), __file__])

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
        import openai
        openai.api_key = "your-api-key-here"  # Replace with your OpenAI API key
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
        from tqdm import tqdm
        import threading
        from queue import Queue

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
    if not VENV_DIR.exists():
        setup_virtual_environment()
    elif sys.prefix != str(VENV_DIR):
        run_script()
    else:
        main()
        
