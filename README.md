okay hi this is like the very base of the project yay we are likely gonna have to rewrite all of this LOL

anyway, ill list the purpose of each folder and file...

## config 
contains whitelist.yaml,,,,, idek what yaml is LOL
basically it is supposed to define which files ingest.py can read, and transform into json files. 

## logs 
is supposed to keep a record of every time the ai is called? i think

## raw-data 
is jst that,,, raw data. 

## transformed-data
should contain a json file that is seperated into chunks of 512 bytes for llms to process, explain more later

## agent.py
this is the executable to call the agent to do actual stuff. for now it is empty

## gateway.py 
i believe this is wher the fastapi nonsense goes

## ingest.py
this is the data processing part. basically it splits files into 512 byte chunks that the llm can understand. currently theres no ai functionality built into it yet because i dont have openai api keys, but we can add that in later. if we decide to run ollama locally, we need to figure out how to do that too. 

## venv
im running a python venv for this project. i dont know if this is required but its best practice apparently? anyway i have setup a requirements.txt as well so u can install the packages easily. pls update when we include more libs

## Step-by-Step Guide
Open your terminal or command prompt.
Navigate to the directory containing your requirements.txt file using the cd command

<cd path/to/your/project>

Activate your virtual environment (highly recommended to keep your packages isolated)

<Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate>

Run the installation command: 

<pip install -r requirements.txt>