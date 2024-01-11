"""

My AI friend chatbot:
Approach the simplest way possible to create a chatbot.
Using only Python and text files.
All the operations are done in the command line.

Author : Fire Of Ender
Update : 11/01/2024
    
"""

import random # For random responses
import colorama

# Check if the data folder exists, if not, create it
import os
if not os.path.exists("data"):
    os.makedirs("data")
dataResponse = open(r"data\responses.txt", mode="a+") # Append and read mode to make sure the file is created
dataSeparator = ":$:"
responseDict = {"__unknown__" : ["Sorry, I couldn't understand.", "Sorry, but I don't know how to reply."]}; # General responses
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
    print(colorama.Fore.YELLOW + "[System] : History restoring function is currently unavailable.")

def init():
    getLists()
    restoreHistory()

def helpCmd(args):
    return "\n".join([
        "These are currently available commands:",
        "/help, /h : Show list of commands.",
        "/exit, /quit, /q : Exit the chat.",
        "/rename, /rn : Change AI name. (e.g. /rn \"Not my friend\")",
        "/more, /add, /insert, /a : Add new response data. (e.g. /a \"Hi\" \"Good morning!\")",
        "/view, /data, /v : View all response data.",
    ])

def exitChat(args):
    print(colorama.Fore.LIGHTGREEN_EX + "[My Friend] : Goodbye!")
    dataResponse.close()
    exit()
    
def rename(args):
    global aiName
    namePromptText = colorama.Fore.LIGHTBLUE_EX + "[System] : Enter new name : "
    if len(args) > 1:
        args.pop(0) # Remove the command name from the list
        newAiName = " ".join(args).strip() # Join the list into a string
        if len(newAiName) > 2: # Make sure the input is not empty
            if newAiName[:1] == "\"" and newAiName[2:].find("\"") != -1: # Need to start from index 2 to prevent empty string
                endNameIndex = newAiName[1:].find("\"") + 1
                newAiName = newAiName[1:endNameIndex].strip()
            else:
                newAiName = input(namePromptText).strip()
        else:
            newAiName = input(namePromptText).strip()
    else:
        newAiName = input(namePromptText).strip()
    if newAiName != "":
        aiName = newAiName
    return "From now on, my name is " + aiName + "!"

def insertResponse(args):
    keyword = ""
    newResponse = ""
    keywordPromptText = colorama.Fore.LIGHTBLUE_EX + "[System] : What's your desire input? : " + colorama.Fore.LIGHTWHITE_EX
    if len(args) > 1:
        args.pop(0) # Remove the command name from the list
        argText = " ".join(args).strip() # Join the list into a string
        keyword = argText
        if len(keyword) > 2: # Make sure the input is not empty
            if keyword[:1] == "\"" and keyword[2:].find("\"") != -1: # Need to start from index 2 to prevent empty string
                endKeywordIndex = keyword[1:].find("\"") + 1
                keyword = keyword[1:endKeywordIndex].strip()
                if len(argText[endKeywordIndex:]) > 1 and len(keyword) > 0:
                    newResponse = argText[endKeywordIndex + 1:].strip() # Just roughly reserve the response
                    if len(newResponse) > 2: # Make sure the input is not empty
                        if newResponse[:1] == "\"" and newResponse[2:].find("\"") != -1: # Need to start from index 2 to prevent empty string
                            endNewResponseIndex = newResponse[1:].find("\"") + 1
                            newResponse = newResponse[1:endNewResponseIndex].strip()
                        else:
                            newResponse = ""
                    else:
                        newResponse = ""
                elif len(keyword) <= 0:
                    keyword = input(keywordPromptText).strip() # Keyword was invalid
            else:
                keyword = input(keywordPromptText).strip()
        else:
            keyword = input(keywordPromptText).strip()
    else:
        keyword = input(keywordPromptText).strip()
        
    if keyword != "":
        if newResponse != "":
            try:
                if responseDict[keyword] != []: # Check if the keyword has already reserved responses
                    responseDict[keyword].append(newResponse)
                else:
                    responseDict[keyword] = [newResponse]
            except:
                responseDict[keyword] = [newResponse]
                
        else:
            responsePromptText = colorama.Fore.LIGHTBLUE_EX + "[System] : I must reply : " + colorama.Fore.LIGHTGREEN_EX
            try:
                if responseDict[keyword] != []: # Check if the keyword already reserved responses
                    responseDict[keyword].append(input(responsePromptText).strip())
                else:
                    responseDict[keyword] = [input(responsePromptText).strip()]
            except:
                responseDict[keyword] = [input(responsePromptText).strip()]
            
        dataResponse = open(r"data\responses.txt", mode="r+") # Switch to write and read mode
        lines = dataResponse.readlines()
        isOverwrited = False
        for i in range(len(lines)):
            if lines[i].strip().find(keyword) == 0:
                newLines = [lines[j] for j in range(i)]
                newLines += [keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]" + ("\n" if i + 1 <= len(lines) - 1 else "")]
                newLines += [lines[j] for j in range(i + 1 if i + 1 <= len(lines) - 1 else len(lines), len(lines))] # If it's at the bottom, add an empty line
                dataResponse.seek(0) # Take the file to the beginning
                dataResponse.writelines(newLines)
                isOverwrited = True
        if not isOverwrited:
            dataResponse.close()
            dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
            dataResponse.write("\n" + keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]")
        dataResponse.close() # Close the file after writing
        
    return "Recorded. Thanks for your feedback!"

def viewData(args):
    dataResponse = open(r"data\responses.txt", mode="r") # Switch to write and read mode
    dataFromFile = dataResponse.read()
    dataResponse.close()
    return "From \"\\data\\responses.txt\"\n" + dataFromFile

commandDict = {"help" : helpCmd,
               "h" : helpCmd,
               "quit" : exitChat,
               "exit" : exitChat,
               "q" : exitChat,
               "rename" : rename,
               "rn" : rename,
               "more" : insertResponse,
               "add" : insertResponse,
               "insert" : insertResponse,
               "a" : insertResponse,
               "data" : viewData,
               "view" : viewData,
               "v" : viewData} # Commands to run specific functions

def respond(text):
    if len(text) != 0: # Check if the input is not empty
        if (text[0] == "/") and (text.lower()[1:].split()[0] in commandDict): # Check for commands first
            return colorama.Fore.LIGHTBLUE_EX + commandDict[text.lower()[1:].split()[0]](text[1:].split()) # Run the command
        elif text in responseDict: # Else check for general responses
            if len(responseDict[text]) > 0:
                return random.choice(responseDict[text])
        
    # Unknown input or no response reserved
    global aiName
    print(colorama.Fore.LIGHTGREEN_EX + "[" + aiName + "] : " + random.choice(responseDict["__unknown__"]))
    newResponse = input(colorama.Fore.LIGHTBLUE_EX + "Can you tell me what to respond next time? ('/n' to deny.) : " + colorama.Fore.LIGHTGREEN_EX).strip()
    if (newResponse.strip().lower() != "/n") and (newResponse.strip() != "") and (text.strip() != ""):
        responseDict[text] = [newResponse]
        dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
        dataResponse.write("\n" + text + " " + dataSeparator + " [" + newResponse + "]")
        dataResponse.close() # Close the file after writing
    return colorama.Fore.LIGHTBLUE_EX + "Thanks for your feedback!" # Unknown input
def talk():
    while (True):
        userText = input(colorama.Fore.LIGHTWHITE_EX + "[You] : ").strip()
        global aiName
        print(colorama.Fore.LIGHTGREEN_EX + "[" + aiName + "] : " + respond(userText))

if __name__ == "__main__":
    colorama.init(convert=True)
    print(colorama.Fore.BLUE + "Welcome to " + colorama.Fore.GREEN + "\"My A.I. Friend\"" + colorama.Fore.BLUE + " Chatbot!")
    print(colorama.Fore.LIGHTBLACK_EX + "Type \"/h\" to see the list of commands.")
    init() # Initialize the chatbot
    talk() # Start the chat