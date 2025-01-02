#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

# Constants
VENV_DIR = Path.home() / ".ai_to_human_env"  # Virtual environment directory
REQUIRED_PACKAGES = ["openai", "tqdm"]
MAX_TOKENS = 150
CHUNK_SIZE = 3000
THREAD_COUNT = 5

def setup_virtual_environment():
    """Create a virtual environment and install required packages."""
    if not VENV_DIR.exists():
        print("Setting up the environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    pip_executable = VENV_DIR / "bin" / "pip"
    for package in REQUIRED_PACKAGES:
        print(f"Installing {package}...")
        subprocess.check_call([str(pip_executable), "install", package])

def run_in_virtualenv():
    """Restart the script within the virtual environment."""
    python_executable = VENV_DIR / "bin" / "python"
    subprocess.check_call([str(python_executable), __file__] + sys.argv[1:])

def print_banner():
    """Display a colorful banner."""
    banner = """
\033[96m ooooo   ooooo                                                          ooooooooooooo                           .   
 `888'   `888'                                                          8'   888   `8                         .o8   
  888     888  oooo  oooo  ooo. .oo.  .oo.    .oooo.   ooo. .oo.             888       .ooooo.  oooo    ooo .o888oo 
  888ooooo888  `888  `888  `888P"Y88bP"Y88b  `P  )88b  `888P"Y88b            888      d88' `88b  `88b..8P'    888   
  888     888   888   888   888   888   888   .oP"888   888   888            888      888ooo888    Y888'      888   
  888     888   888   888   888   888   888  d8(  888   888   888            888      888    .o  .o8"'88b     888 . 
 o888o   o888o  `V88V"V8P' o888o o888o o888o `Y888""8o o888o o888o          o888o     `Y8bod8P' o88'   888o   "888" 
\033[92m                                                                                                               
Advanced AI Text to Human Text Converter - Created by Shaid Mahamud
\033[0m
"""
    print(banner)

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
    # Ensure the script runs in the virtual environment
    if not VENV_DIR.exists() or not (VENV_DIR / "bin" / "python").exists():
        setup_virtual_environment()
        run_in_virtualenv()
    else:
        main()
            
