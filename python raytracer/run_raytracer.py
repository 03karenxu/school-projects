import os
import subprocess

input_files_directory = "Tests-and-Keys"
raytracer_script = "Raytracer.py"

# list all .txt files in the input directory
input_files = [f for f in os.listdir(input_files_directory) if f.endswith(".txt")]

# run Raytracer for each input file
for input_file in input_files:
    command = ["python", raytracer_script, input_file]

    try:
        # run Raytracer for the current input file
        subprocess.run(command, check=True)
        print(f"Raytracer executed successfully for {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Raytracer for {input_file}: {e}")

