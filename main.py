"""

My AI friend chatbot:
Approach the simplest way possible to create a chatbot.
Using only Python and text files.
All the operations are done in the command line.

Author : Fire Of Ender
Update : 12/01/2024
    
"""

import os # For file management
import random # For random responses
import colorama # For color text
from datetime import datetime # For time

# Text colors modifiers
cError = colorama.Fore.LIGHTRED_EX
cWarn = colorama.Fore.LIGHTYELLOW_EX
cInfo = colorama.Fore.LIGHTBLUE_EX
cAiChat = colorama.Fore.LIGHTGREEN_EX
cUserChat = colorama.Fore.LIGHTWHITE_EX
cHeader1 = colorama.Fore.BLUE
cHeader2 = colorama.Fore.GREEN
cHint =  colorama.Fore.LIGHTBLACK_EX

# Check if the data folder exists, if not, create it
if not os.path.exists("data"):
    os.makedirs("data")

dataResponse = open(r"data\responses.txt", mode="a+") # Append and read mode to make sure the file is created
dataSeparator = ":$:"
responseDict = {"__unknown__" : ["Sorry, I couldn't understand.", "Sorry, but I don't know how to reply."]}; # General responses

dataHistory = open(r"data\history.txt", mode="a+") # Append and read mode to make sure the file is created

aiName = "My Friend" # Default name

# Utility functions

def removeQuotationMark(targetString): # Return the string without quotation marks, index of the second quotation mark, and success status
    targetString = targetString.strip()
    newString = ""
    hasTargetString = False
    if len(targetString) > 2:
        if targetString[:1] == "\"" and targetString[2:].find("\"") != -1: # Make sure it contains at least one character
            endTargetIndex = targetString[1:].find("\"") + 1
            newString = targetString[1:endTargetIndex].strip()
            hasTargetString = (newString != "") # True when it is not empty
    return newString, endTargetIndex, hasTargetString

# Initialize functions

def getResponsesLists():
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
    dataHistory.seek(0) #Take the file to the beginning
    lastHistory = dataHistory.readlines() # Make a list of all the lines in the file
    displayHistory = []
    for line in lastHistory:
        # Get the name and remove it from the list
        if line.strip().find("_aiName") == 0:
            lastAiName = line.split(":")
            if len(lastAiName) > 1:
                lastAiName, endNameIndex, hasLastNameString = removeQuotationMark(lastAiName[1])
                if hasLastNameString:
                    global aiName
                    aiName = lastAiName
        
        # Color the text
        if line.strip().find("[") == 0 and line.strip().find("]") != -1:
            speaker = line[line.strip().find("[") + 1: line.strip().find("]")]
            if speaker != "You":
                line = cAiChat + line
            else:
                line = cUserChat + line
            displayHistory.append(line)
                
    dataResponse.close() # Close the file after reading
    displayHistory.append(cInfo + "[System] : History restored.")
    print("".join(displayHistory))

def init():
    getResponsesLists()
    restoreHistory()

# Command functions

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
    hasNameString = False
    
    # Solve the new name from inline arguments
    if len(args) > 0:
        newAiName = " ".join(args).strip() # Join the list into a string
        newAiName, endNameIndex, hasNameString = removeQuotationMark(newAiName)
        
    # If the name is not successfully acquired, then prompt specifically
    if not hasNameString:
        newAiName = input(colorama.Fore.LIGHTBLUE_EX + "[System] : New name : ").strip()
        
    # Throw error messages if the name is still empty
    if newAiName == "":
        return cError + "Unable to solve for my new name, Please try again."
    
    aiName = newAiName
    return "From now on, my name is " + aiName + "!"

def insertResponse(args):
    keyword = ""
    hasKeyword = False # To check if the keyword is successfully acquired
    newResponse = ""
    hasNewResponse = False # To check if the response is successfully acquired
    
    # Solve the input and response from inline arguments
    if len(args) > 0:
        argText = " ".join(args).strip() # Join the list into a string
        
        keyword, endKeywordIndex, hasKeyword = removeQuotationMark(argText)
                
        if len(argText[endKeywordIndex:]) > 1 and hasKeyword:
            newResponse, endResponseIndex, hasNewResponse = removeQuotationMark(argText[endKeywordIndex + 1:].strip())
    
    # If the input is not successfully acquired, then prompt specifically
    if not hasKeyword:
        keyword = input(cInfo + "[System] : What's your desire input? : " + cUserChat).strip()
        
    # Throw error messages if the input is still empty
    if keyword == "":
        return cError + "Unable to solve for your input, Please try again."
    
    # If the input is not successfully acquired, then prompt specifically
    if not hasNewResponse:
        newResponse = input(cInfo + "[System] : I must reply : " + cAiChat).strip()
    
    # Throw error messages if the input is still empty
    if newResponse == "":
        return cError + "Unable to solve for my appropriate reply, Please try again."
    
    # Check if the keyword has already reserved a responses list
    if keyword in responseDict:
        responseDict[keyword].append(newResponse)
    else:
        if keyword[0] != "/":
            responseDict[keyword] = [newResponse]
        else:
            return cWarn + "I'm sorry, but new command is not allowed."
    
    # Write data to the file
    dataResponse = open(r"data\responses.txt", mode="r+") # Switch to write and read mode
    lines = dataResponse.readlines()
    isOverwrited = False
    
    # Check if the keyword is reserved, then overwrite it
    for i in range(len(lines)):
        if lines[i].strip().find(keyword) == 0:
            newLines = [lines[j] for j in range(i)]
            newLines += [keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]" + ("\n" if i + 1 <= len(lines) - 1 else "")]
            newLines += [lines[j] for j in range(i + 1 if i + 1 <= len(lines) - 1 else len(lines), len(lines))] # If it's at the bottom, add an empty line
            dataResponse.seek(0) # Take the file to the beginning
            dataResponse.writelines(newLines)
            isOverwrited = True
    
    # Check if the keyword is not reserved, then append it
    if not isOverwrited:
        dataResponse.close()
        dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
        dataResponse.write("\n" + keyword + " " + dataSeparator + " [" + "; ".join(responseDict[keyword]) + "]")
    
    # Close the file after writing
    dataResponse.close()
        
    return "Recorded. Thanks for your feedback!"

def viewData(args):
    dataResponse = open(r"data\responses.txt", mode="r") # Switch to write and read mode
    dataFromFile = dataResponse.read()
    dataResponse.close()
    return "From \"\\data\\responses.txt\"\n" + dataFromFile

# Commands list to run specific functions
commandDict = {
    "help" : helpCmd,
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
    "v" : viewData
    }

# General functions

def respond(text):
    if len(text) != 0: # Check if the input is not empty
        isCmd = (text[0] == "/") # If it is a command, it contains a slash
        if isCmd and len(text) > 1: # Check for commands slash
            cmdKey = text.lower()[1:].split()[0]
            cmdArgs = text[1:].split()
            cmdArgs.pop(0) # Remove the command name from the list
            if (cmdKey in commandDict):
                return cInfo + commandDict[cmdKey](cmdArgs) # Run the command
            else:
                return cError + "I cannot recognize the command."
        elif text in responseDict: # Else check for general responses
            if len(responseDict[text]) > 0:
                return random.choice(responseDict[text])
        
    # Unknown input or no response reserved
    global aiName
    print(cAiChat + "[" + aiName + "] : " + random.choice(responseDict["__unknown__"]))
    newResponse = input(cInfo + "Can you tell me what to respond next time? (leave it blank to deny) : " + cAiChat).strip()
    if (newResponse.strip() != "") and (text.strip() != ""):
        if newResponse[0] != "/":
            responseDict[text] = [newResponse]
            dataResponse = open(r"data\responses.txt", mode="a") # Switch to append mode
            dataResponse.write("\n" + text + " " + dataSeparator + " [" + newResponse + "]")
            dataResponse.close() # Close the file after writing
            return cInfo + "Thanks for your feedback!"
        else:
            return cWarn + "I'm sorry, but new command is not allowed."
    else:
        return cInfo + "Okay. I won't record it."

def updateHistory(userText, aiText):
    dataHistory = open(r"data\history.txt", mode="r+") # Switch to read and write mode
    lastHistory = dataHistory.readlines()
    newHistory = lastHistory.copy()
    
    for line in lastHistory:
        # Remove comments and name data
        if line.strip().find("#") == 0 or line.strip().find("_aiName") == 0 or line.strip() == "":
            newHistory.remove(line)
    global aiName
    newHistory.append("[You] : " + userText + "\n")
    newHistory.append("[" + aiName + "] : " + aiText + "\n")
    newHistory = ["# Last update : " + datetime.now().strftime("%H:%M:%S %d/%m/%Y") + "\n","_aiName : \"" + aiName + "\"\n\n"] + newHistory
    dataHistory.seek(0)
    dataHistory.writelines(newHistory)
    dataHistory.close()

def talk():
    implicitInput = ""
    while (True):
        global aiName
        userText = input(cUserChat + "[You] : ")
        aiResponse = respond(userText.strip())
        if implicitInput != "" and userText.strip().find("/") != 0:
            # Learn from user input
            insertResponse(["\"" + implicitInput + "\"", "\"" + userText + "\""])
        
        print(cAiChat + "[" + aiName + "] : " + aiResponse)
        updateHistory(userText, aiResponse.strip())
        implicitInput = aiResponse

if __name__ == "__main__":
    colorama.init(convert=True)
    print(cHeader1 + "Welcome to " + cHeader2 + "\"My A.I. Friend\"" + cHeader1 + " Chatbot!")
    print(cHint + "Type \"/h\" to see the list of commands.")
    init() # Initialize the chatbot
    talk() # Start the chat