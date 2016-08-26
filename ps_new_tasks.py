import subprocess, signal, sys, datetime

# Install Ctrl+C handler
def signal_handler(signal, frame):
        print("[ Ctrl+C hit ]")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_curr_ps():
        ps_out = subprocess.check_output(["ps", "--sort","pid", "-e", "H", "-o","pid,tid,ppid,comm,policy,pri,rtprio,psr"]).splitlines()
        ps_out = ps_out[1:]
        return ps_out

proc_dict = {}

# Init dict struct
ps_out = get_curr_ps()
for line in ps_out:
        lsplit = line.split()
        proc_dict[lsplit[0]] = lsplit

print("*** New processes/threads being spawned ***")
while True:
        new_proc_dict = {}
        ps_out = get_curr_ps()

        for line in ps_out:
                lsplit = line.split()

                if lsplit[3] == 'ps':
                        # Ignore ps tasks
                        continue

                if not lsplit[0] in proc_dict:
                        # Found a new process. Print it.
                        print("%s [%s]" % (line, datetime.datetime.now()))

                new_proc_dict[lsplit[0]] = lsplit

        proc_dict = new_proc_dict

