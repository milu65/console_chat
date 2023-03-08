# ConsoleChat

Use the OpenAI API to interact with ChatGPT on the console


### Installation

Clone the repository:   
```
git clone https://github.com/milu65/console_chat.git
```
Navigate to the directory:   
```
cd console_chat
```
Install the required libraries:  
```
pip install -r requirements.txt  
```

### Configuration
Create file config.json in the current directory.
#### Template: config.json
```json
{
  "api_key": "00000000000000000000000000000000000000000000000"
}
```

### Usage
Run the program:  
```
python main.py 
```
The program will print a welcome message, and you can start chatting by entering your message and pressing Enter.  
To clear the chat history, enter "clear".  
To quit the application, enter "q".