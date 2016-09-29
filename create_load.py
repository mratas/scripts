import os, time, sys, signal, subprocess, datetime

# Install Ctrl+C handler
def signal_handler(signal, frame):
        print("[ Ctrl+C hit ]")   
        print("Ran for %d periods, schedule missed %d times & core changed %d times" % (i, missed, core_chg_cnt))
        sys.exit(0)                                                                                              

signal.signal(signal.SIGINT, signal_handler)


# Input sanity
try:          
        if len(sys.argv) != 4:
                raise ValueError

        T = int(sys.argv[1])
        C = int(sys.argv[2])
        U = float(C)/float(T)
        margin = int(sys.argv[3]) / float(100)

        if U > 1:
                raise ValueError
                                
except ValueError:              
        print("Usage: /usr/bin/python %s <period_us> <compute_time_us> <tolerance (perc)>" % sys.argv[0])
        sys.exit(-1)                                                                                     



i = 0
missed = 0
T = T / float(1000000)
C = C / float(1000000)

print("* Running with load factor = %f (%fs / %fs) & tolerance of %f" % (U, C, T, margin))
print("* Press Ctrl+c to stop")                                                           

T_margin = T * (1 + margin)

start = last_ping = time.time()
last_core = open("/proc/{pid}/stat".format(pid=os.getpid()), 'rb').read().split()[-9]
print("* Started on core %s" % last_core)                                            
core_chg_cnt = 0                                                                     
while True:                                                                          
        if time.time() - start >= C:                                                 
                sleep_time = start + T - time.time()
                if sleep_time > 0:
                        time.sleep(sleep_time)

                new_core = open("/proc/{pid}/stat".format(pid=os.getpid()), 'rb').read().split()[-9]
                if last_core != new_core:
                        core_chg_cnt = core_chg_cnt + 1
                        print("Core [%s->%s]" % (last_core, new_core))
                        last_core = new_core
                diff = time.time() - last_ping
                if  diff > T_margin:
                        print("Schedule missed at [i = %d] by %fus!! [%s]" % (i, (diff - T) * 1000000, str(datetime.datetime.now())))
                        out_file=open('out_file', 'w+')
                        print >> out_file, "missed"
                        out_file.close()
                        missed = missed + 1

                i = i + 1
                start = time.time()
        else:
                last_ping = time.time()

        pass

