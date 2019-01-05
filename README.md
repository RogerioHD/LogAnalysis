# LogAnalysis
## About
This python program named **newsdb.py** generates reports from a database.
It uses the `psycopg2` module.
The database contains information concerning authors and their articles 
and how many views each article have gotten.
## 3 Questions, 3 Answers
1. What are the three most popular articles of all time?
2. Who are the authors of most popular articles of all time?
3. On what days more than 1% of requests resulted in errors?
For each one of these question there is a SQL query implemented within the python program.
## How is it set?
### Step One How to get / install Python version 2 or 3 
Go to [https://www.python.org/downloads/]
One should notice that at first you need to have installed on your computer the VirtualBox and the Vagrant.
After that you'll need to download the virtual machine FSND-Virtual-Machine
provided by Udacity team on its _NanoDegree FullStack program_.
### Python File
The python file **newsdb.py** is located inside a folder named ***news***.
By the way the ***news*** folder is located inside the vagrant's folder. Here's the structure:
   <details>
      <summary>FSND-Virtual-Machine</summary> 
      <details>
            <summary>vagrant</summary>                
              <summary>* .vagrant</summary>                  
              <summary>* catalog</summary>                   
              <summary>* forum</summary>                  
       <details>
           <summary>news</summary>
           <p>newsdb.py</p>
        </details>
         </details>
    </details>
    
### Running the program
After the initial set up you should be able to login into your virtual machine
using `vagrant up` command and them `vagrant ssh` command.
If everthing is ok the output of your shell would seems like:
`vagrant@vagrant:/vagrant/news$`
Just wrtite `python newsdb.py` and you will get the reports!

  
