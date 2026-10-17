import os
import subprocess
import time

# Configurations
SRC_DIR = "src"
PARSER_FILE = os.path.join(SRC_DIR, "parser.c")

def fix_errors_in_source():
    """Reads source files and patches structural typos."""
    if not os.path.exists(PARSER_FILE):
        return False
        
    with open(PARSER_FILE, 'r') as file:
        lines = file.readlines()

    fixed = False
    for i, line in enumerate(lines):
        # Fix missing # instruction header typo
        if line.strip().startswith("include <stddef.h>"):
            lines[i] = "#include <stddef.h>\n"
            fixed = True
        # Fix accidental un-indexed pointer checks buffer -> buffer[index]
        if "buffer == " in line:
            lines[i] = line.replace("buffer == ", "buffer[0] == ")
            fixed = True

    if fixed:
        print("[create.py] Found and patched code discrepancies inside parser.c...")
        with open(PARSER_FILE, 'w') as file:
            file.writelines(lines)
    return fixed

def execute_build_command(command):
    """Executes compiler instructions dynamically."""
    print(f"[create.py] Executing: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stderr.decode()

def orchestration_loop():
    """Main compilation validation loop framework."""
    os.makedirs(SRC_DIR, exist_ok=True)
    
    # Validation instructions sequences matching target pipelines
    build_steps = [
        "gcc -m32 -c src/boot.s -o boot.o",
        "gcc -m32 -c src/parser.c -o parser.o"
    ]
    
    loop_active = True
    iteration = 1

    while loop_active:
        print(f"\n--- Compilation Loop Iteration Run #{iteration} ---")
        fix_errors_in_source()
        
        all_passed = True
        for step in build_steps:
            return_code, error_msg = execute_build_command(step)
            
            if return_code != 0:
                print(f"\n❌ Compilation Error caught during target execution: '{step}'")
                print(f"Error Context:\n{error_msg}")
                all_passed = False
                break # Break path step execution sequence to force self-healing execution patch
        
        if all_passed:
            print("\n==============================================")
            print("✅ SUCCESS: All low-level binary stages compiled cleanly!")
            print("==============================================")
            loop_active = False
        else:
            print("\n[create.py] System error status flag caught. Processing resolution loop in 2 seconds...")
            time.sleep(2)
            iteration += 1

if __name__ == "__main__":
    orchestration_loop()
