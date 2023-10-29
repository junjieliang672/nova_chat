import subprocess

if __name__ == "__main__":
    PORT = "11434"
    subprocess.call(["ssh", "-N", "-f", "-L",f"localhost:{PORT}:localhost:{PORT}","ai"])