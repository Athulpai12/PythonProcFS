
# Instructions to Run
##### There are two ways to run the following
1. If you are in linux you can install python3.6+ and open a shell the readme.md diretory

2. If you are using any other varient of the os then install docker for the os
and run the following commands
   
        docker build -t <build_name> .
        docker run -it <build_name>



To print all the processes running in the system

        python3 main.py 

To print only the stat of specified processes use the command line argument ``` --pids``` and then 
pass the integer process id number


        python main.py --pids 1 2 3 4


The output would be a table as shown below

processID | processName | utime                | stime                | parentProcessId | virtualMemory | processCreator
--------- | ----------- | -------------------- | -------------------- | --------------- | ------------- | --------------
1         | 'bash'      | 0 H : 0 M : 0.0025 S | 0 H : 0 M : 0.0000 S | 0               | 5.85 MB       | root          
10        | 'python3'   | 0 H : 0 M : 0.0020 S | 0 H : 0 M : 0.0000 S | 1               | 14.3 MB       | root  





# SimpleProcParser Modules

SimpleProcParser Library Contains the following Modules

1. CustomException

   This modules contains the custom exception which are raised when a exception occurs

2. platfromOperations

   This module contains the platform specific operations.Currently only linux is supported 
    Contains the core implementation for each platform
   
3. models
    
   This module contains the abstract models whose concrete implementation takes place in the platform related module.
    It is present in the platfromOperations

4. prettyPrint
 
   This module helps in printing the data in table format

5. tests

    This module contains the tests for the core implementation


# Note:
1. How dynamic process destruction is handled 

While getting stats if the process gets destroyed (then /proc/[pid] diappears) then the module logs the process 
id along with the error and continues to get the stats of other variables.

2. How Race Condition is handled.

In case of a race condition(ie the kernel updates the value so the data we read is corrupted). The module always checks 
   correctness of data and rejects if data is corrupted and logs the corrupted process id and continues to 
   get data of other processes

3. How permission error is handled 

In case of insufficient permission to read a file then we log the error 
and continue to get stats of other processes

4. How testing is handled.

Some libraries are mocked using ```MagicMock``` and a folder called fixtures contained 
   dummydata and this location was injected into the controller to emulate procfs 
  
   
      