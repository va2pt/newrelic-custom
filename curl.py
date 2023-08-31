import subprocess

def get_metric(command):

    # Use subprocess to run the command in the background
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to complete and capture the output
    stdout, stderr = process.communicate()

    # Print the captured output
    #print("Standard Output:")
    return  stdout.decode()


   
