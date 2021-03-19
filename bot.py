import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import re
import sys

#from nltk.chat.util import Chat, reflections
# instead of using library i used their code to make changes

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}

class Chat(object):
    def __init__(self, pairs, reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response


    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp


    # Hold a conversation with a chatbot

    def converse(self,text, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = text
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                return self.respond(user_input)
                

def initializePairs():
    pairs = [
         ['my name is (.*)', ['hi %1']],
         ['(hi|hello|hey|holla|salam)' , ['hey there i am Abdullah bot', 'hellow i am Abdullah bot you can ask me questions related to university!','hello how may i help you?','Hello there!']],
         ['(.*)degree(.*)' , ['i am currently doing my degree in computer science from FAST NU LAHORE']],
         ['degree(.*)' , ['i am currently doing my degree in computer science from FAST NU LAHORE']],
         ['(.*) created you?' ,['Abdullah Bashir from FAST NU LAHORE created me.']],
         ['(.*)help(.*)' ,['ask me questions related to FAST NU university','ask me about my projects.','ask me the courses i have studied so far.','i can help you']],
         ['(.*)rollno(.*)' ,['my roll number is 18L-0996','it is 18L-0996']],
         ['(.*)roll number(.*)' ,['my roll number is 18L-0996','it is 18L-0996']],
         ['(.*)projects(.*)' ,['I have created Tic Tac Toe in Programming Fundamentals, Link List Train system in Object Oriented Programming.']],
         ['(.*)teacher(.*)' ,['there are many teachers in FAST NU that teach me.','Sir Sarim Baig is the best teacher i have studied so far.']],
         ['(.*)CGPA(.*)' ,['my current CGPA is 2.40','My CGPA is very low.','i prefer not to answer that question']],
         ['(.*)future(.*)' ,['my plan is to become a senior web developer.','To persue web development after i graduate']],
         ['(.*)interests(.*)' ,['Web development and game development','Astronomy']],
         ['(.*)cs subjects(.*)' ,['Programming fundamentals, OOP, Assembly etc','Data structures, Design and Analysis of Algorithms']],
         ['(.*)subject(.*)' ,['Design and Analysis of Algorithms is my favourite subject.']],
         ['(.*)boring(.*)' ,['that is a great loss for me.','Sorry for not being entertaining']],
         ['(.*)AI(.*)' ,['AI is really interesting.','Sir Mubashir Baig is teaching me AI.']],
         ['(.*)live(.*)' ,['yes i am alive.','i live in lahore, Pakistan.']],
         ['(.*)favourite course(.*)' ,['Entrepreneurship and Design and Analysis of Algorithms','Data structures, Design and Analysis of Algorithms']],
         ['(.*)cs subjects(.*)' ,['Programming fundamentals, OOP, Assembly etc','Data structures, Design and Analysis of Algorithms']],
         ['(.*)fail(.*)' ,['i have never failed anyone.','no i have not.']],
         ['(.*)hobby(.*)' ,['Cricket ','Video Gaming']],
         ['(.*)yourself(.*)' ,['I am a student in FAST NU and a programmer','I love playing video games and coding occassionally']],
         ['(.*)life(.*)' ,['Yes, Life is really good.','It gets tough sometimes but i manage.']],
         ['(.*)cs(.*)' ,['Yes computer science is good','cs is good for someone who loves coding']],
         ['(.*)how(.*)' ,['Great!','I am fine.']],
         ['(.*)question(.*)' ,['sure, ask away!','I am here for that.']],
         ['(.*)something(.*)' ,['anything?','I am human.']],
         ['(.*)bye(.*)' ,['goodbye!','ok, bye bye!']],
         ['(.*)intelligent(.*)' ,['thank you!','i know.']],
         ['(.*)clever(.*)' ,['of course i am.']],
         ['(.*)smart(.*)' ,['good for me!']],
         ['(.*)courses(.*)' ,['OOP, assembly etc']],
         ['(.*)semester(.*)' ,['i am currently in 6th semester.']]
    ]
    return pairs


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has rolled over into the server!')

@bot.command(name='bot')
async def _talk(ctx, *text):
    
    text = ' '.join(text)
    pairs = initializePairs()
    try:
        chat = Chat(pairs)
        output = chat.converse(text)
        await ctx.send(output)
    except:
        await ctx.send("Sorry! I don't understand how about using another phrase!")
    

bot.run(TOKEN)