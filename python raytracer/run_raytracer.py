import os
import subprocess

# Directory containing your input files
input_files_directory = "Assignment3-Tests-and-Keys"

# Path to your Raytracer script
raytracer_script = "Raytracer.py"

# List all .txt files in the input directory
input_files = [f for f in os.listdir(input_files_directory) if f.endswith(".txt")]

# Run Raytracer for each input file
for input_file in input_files:
    input_file_path = os.path.join(input_files_directory, input_file)
    command = ["python", raytracer_script, input_file_path]

    try:
        # Run the Raytracer script for the current input file
        subprocess.run(command, check=True)
        print(f"Raytracer executed successfully for {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Raytracer for {input_file}: {e}")
