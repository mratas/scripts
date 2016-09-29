import subprocess, signal, sys

# Install Ctrl+C handler
def signal_handler(signal, frame):
        print("[ Ctrl+C hit ]")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Get all processes
ps_out = subprocess.check_output(["ps", "--sort","pid", "-e", "H", "-o","pid,tid,ppid,comm,policy,pri,rtprio,psr"]).splitlines()

# Print header
print("%s\t%s" %(ps_out[0], "AFFINITY"))

ps_out = ps_out[1:]
for line in ps_out:
        lsplit = line.split()

        try:
                # Ignore ps since it'll be gone
                if lsplit[3] == 'ps':
                        raise Exception

                ts_out = subprocess.check_output(["taskset", "-cp", lsplit[0]]).strip().split(":")
                affinity = ts_out[1].strip()
        except:
                affinity = "NA"

        print("%s\t%s" %(line, affinity))

