import argparse
import sys
import time
import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


def printResults(ut, dt, count, s_count, e_count, timeout):
    total_time = ut + dt
    print("Total number of queries made: %d" % count)
    print("Number of successful queries: %d \t Number of error or timed out queries: %d" %(s_count, e_count))
    print("Timeout was set to %d second(s)\n\n*****************************************\n\n" %(timeout))
    print("Total seconds of application uptime: %.4f" % (ut))
    print("Total seconds of application downtime: %.4f" %(dt))
    print("%.2f%% Application uptime \t %.2f%% Application downtime" %((ut/total_time) * 100, (dt/total_time) * 100))


def header_check(url, timeout):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.SSL_VERIFYPEER, 0)   
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.CONNECTTIMEOUT, timeout)
    # Set our header function.
    c.perform()
    status = c.getinfo(c.RESPONSE_CODE)
    c.close()
    return status

def run_test(t_time,url, timeout):
    t_end = time.time() + t_time
    ut_start = 0 # uptime timer 
    dt_start = 0 # downtime timer
    ut_flag = False
    dt_flag = False
    cumulative_ut = 0
    cumulative_dt = 0
    count = 0
    success_count = 0
    error_count = 0
    while(time.time() < t_end):
        try:
            rsp_code = header_check(url, timeout)
            if(rsp_code == 200):
                success_count += 1
                if(ut_flag == False and dt_flag == False): # If both timers are off, this is a fresh run, just need to start the uptime timer
                    ut_start = time.time()
                    ut_flag = True
                elif(ut_flag == False and dt_flag == True): # Server downtime has ended, stop downtime timer and start updtime timer
                    dt_flag = False
                    cumulative_dt += (time.time() - dt_start)
                    ut_start = time.time()
                    ut_flag = True
            else:
                if(ut_flag == False and dt_flag == False):
                    dt_start = time.time()
                    dt_flag = True
                elif(ut_flag == True and dt_flag == False):
                    ut_flag = False
                    cumulative_ut += (time.time() - ut_start)
                    dt_start = time.time()
                    dt_flag = True
                error_count += 1
        except: # Assuming Failed to connect to <host> error
            if(ut_flag == False and dt_flag == False):
                    dt_start = time.time()
                    dt_flag = True
            elif(ut_flag == True and dt_flag == False):
                ut_flag = False
                cumulative_ut += (time.time() - ut_start)
                dt_start = time.time()
                dt_flag = True
            error_count += 1

        count += 1

    if(ut_flag == True and dt_flag == False):
        cumulative_ut += (time.time() - ut_start)
    if(ut_flag == False and dt_flag == True):
        cumulative_dt += (time.time() - dt_start)
    
    printResults(cumulative_ut, cumulative_dt, count, success_count, error_count, timeout)
        

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Adhoc tool that can be used to quickly measure the uptime (and inversely the downtime) of a HTTP/HTTPS application")
    parser.add_argument('--url', type=str, help="URL to connect to", required=True)
    parser.add_argument('-s', '--seconds', type=int, default=10, help="Length of the desired total time of test in seconds")
    parser.add_argument('-t', '--time-out', type=int, default=1, help="Length of time to wait before timeout in seconds")
    args = parser.parse_args() 
    run_test(args.seconds, args.url, args.time_out)