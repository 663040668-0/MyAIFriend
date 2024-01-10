"""

My AI friend chatbot:
Approach the simplest way possible to create a chatbot.
Using only Python and text files.
All the operations are done in the command line.
    
"""

import random # For random responses

dataResponse = open(r"data\responses.txt", mode="a+") # Append and read mode to make sure the file is created
dataSeparator = ":$:"
responseDict = {"__unknown__" : ["Sorry, I couldn't understand.", "Sorry, but I don't know how can I respond."]}; # General responses
aiName = "My Friend"

def getLists():
    dataResponse.seek(0) #Take the file to the beginning
    lines = dataResponse.readlines() # Make a list of all the lines in the file
    for line in lines:
        if (dataSeparator in line) and (line.strip().find("#") != 0): # Check if the line is a data chunk and not a comment
            splitedLine = line.split(dataSeparator)
            
            # Get the key for the response dictionary
            responseKey = splitedLine[0].strip()
            
            # Get the response list in the form of a string list
            tempResponseList = splitedLine[1]
            startListIndex = tempResponseList.find("[") + 1;
            endListIndex = tempResponseList.find("]");
            
            if startListIndex <= endListIndex: # Check if the list is existed
                tempResponseList = tempResponseList[startListIndex:endListIndex].split(";") # Replace with actual string list
                while ("" in tempResponseList): # Remove empty string
                    tempResponseList.remove("")
                tempResponseList = [text.strip() for text in tempResponseList] # Remove whitespace
                responseDict[responseKey] = tempResponseList
            else:
                responseDict[responseKey] = [] # Add empty list if no response is reserved
                
    dataResponse.close() # Close the file after reading
                
def restoreHistory():
    print("[System] : History restoring function is currently unavailable.")

def init():
    getLists()
    restoreHistory()

def exitChat(args):
    print("[My Friend] : Goodbye!")
    dataResponse.close()
    exit()
    
def rename(args):
    global aiName
    aiName = input("[System] : Enter new name : ").strip()
    return "From now on, my name is " + aiName + "!"

def insertResponse(args):
    global aiName
    keyword = input("[System] : What's your desire input? : ").strip()
    if keyword != "":
        try:
            if responseDict[keyword] != []: # Check if the keyword already reserved responses
                responseDict[keyword].append(input("[System] : Enter new response : ").strip())
            else:
                responseDict[keyword] = [input("[System] : Enter new response : ").strip()]
        except:
            responseDict[keyword] = [input("[System] : Enter new response : ").strip()]
            
        dataResponse = open(r"data\responses.txt", mode="r+") # Switch to write and read mode
        lines = dataResponse.readlines()
        isOverwrited = False
        for i in range(len(lines)):
            if lines[i].strip().find(keyword) == 0:
                newLines = [lines[j] for j in range(i)]
                newLines += [keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]\n"]
                newLines += [lines[j] for j in range(i + 1, len(lines))]
                dataResponse.seek(0) # Take the file to the beginning
                dataResponse.writelines(newLines)
                isOverwrited = True
        if not isOverwrited:
            dataResponse.close()
            dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
            dataResponse.write("\n" + keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]")
        dataResponse.close() # Close the file after writing
    return "Recorded. Thanks for your feedback!"

commandDict = {"quit" : exitChat,
               "exit" : exitChat,
               "q" : exitChat,
               "rename" : rename,
               "more" : insertResponse,
               "add" : insertResponse,
               "insert" : insertResponse}; # Commands to run specific functions

def respond(text):
    if len(text) != 0: # Check if the input is not empty
        if (text[0] == "/") and (text.lower()[1:].split()[0] in commandDict): # Check for commands first
            return commandDict[text.lower()[1:].split()[0]](text.lower()[1:].split()) # Run the command
        elif text in responseDict: # Else check for general responses
            if len(responseDict[text]) > 0:
                return random.choice(responseDict[text])
        
    # Unknown input or no response reserved
    global aiName
    print("[" + aiName + "] : " + random.choice(responseDict["__unknown__"]))
    newResponse = input("Can you tell me what to respond next time? ('/n' to deny.) : ").strip()
    if (newResponse.lower() != "/n") and (newResponse != ""):
        responseDict[text] = [newResponse]
        dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
        dataResponse.write("\n" + text + " " + dataSeparator + " [" + newResponse + "]")
        dataResponse.close() # Close the file after writing
    return "Thanks for your feedback!" # Unknown input
def talk():
    while (True):
        userText = input("[You] : ").strip()
        global aiName
        print("[" + aiName + "] : " + respond(userText))

if __name__ == "__main__":
    init() # Initialize the chatbot
    talk() # Start the chat