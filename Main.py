import random
import discord

bot_token = "secret"

word_list = []
global vocab, name_list, mode, leaderboard

mode = "singleplayer"
name_list = []
leaderboard = {}
vocab = []

with open('word_list.txt', "r") as f:
    data = f.read()
    word_list = data.split()

with open('vocab.txt', "r") as f:
    vocab_data = f.read()
    vocab = vocab_data.split()
    print(len(vocab))


global word, game
game = False
word = random.choice(word_list)
print(word)

client = discord.Client()


def check(guess, actual_word):
    global vocab
    guess_list = []
    actual_word_list = []
    return_emoji_list = ['', '', '', '', '']
    for letter in guess:
        guess_list.append(letter)

    for letter1 in actual_word:
        actual_word_list.append(letter1)

    if len(guess_list) > 5 or len(guess_list) < 5:
        return "Give 5 letter word pls 🥺🙏"
    else:
        print(guess)
        if guess.lower() in vocab:
            for i in range(0, 5):
                if guess_list[i] != actual_word_list[i]:
                    return_emoji_list[i] = '⬛'

                if guess_list[i] in actual_word_list:
                    return_emoji_list[i] = '🟨'

                if guess_list[i] == actual_word_list[i]:
                    return_emoji_list[i] = '🟩'

            return return_emoji_list
        else:
            return "Not In Vocabulary 😡👿💢"


def reset_vars():
    global name_list, mode, leaderboard, score_mode
    mode = "singleplayer"
    name_list = []
    leaderboard = {}
    score_mode = False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global word, game, name_list, mode, leaderboard

    if message.author == client.user:
        return
    if message.content.startswith('!start'):
        game = True
        await message.channel.send("*Tip: If playing Multiplayer, use `!mulstart` 😉*")
        await message.channel.send("Starting the Wordle 🥰")

    if message.content.startswith('!guess'):
        if game:
            if mode == "singleplayer":
                test_word = message.content.replace("!guess ", "")
                if test_word != word:
                    return_string = check(test_word, word)
                    await message.channel.send(' '.join(return_string))

                if test_word == word:
                    old_word = word
                    word = random.choice(word_list)
                    if word == old_word:
                        word = random.choice(word_list)
                    print(word)
                    await message.channel.send("Guessed the Word Correctly! You can go again")
            elif mode == "multiplayer":
                test_word = message.content.replace("!guess ", "")
                if test_word.lower() != word:
                    return_string = check(test_word, word)
                    await message.channel.send(' '.join(return_string))

                if test_word == word:
                    old_word = word
                    word = random.choice(word_list)
                    if word == old_word:
                        word = random.choice(word_list)
                    print(word)
                    user_id = message.author.id
                    username = "<@" + str(user_id) + ">"
                    await message.channel.send(
                        username + " Guessed the Word Correctly! +5 points :) lets see who wins the next one 🤷")
                    leaderboard[message.author.name] = leaderboard[message.author.name] + 5

    if message.content.startswith('!end'):
        if mode == "singleplayer":
            reset_vars()
            game = False
            await message.channel.send("Game Ended... Hoping to see you again!")
        elif mode == "multiplayer":
            game = False

            formatted_msg = []
            for i in leaderboard.keys():
                formatted_msg.append(i)
                formatted_msg.append(" : ")
                formatted_msg.append(str(leaderboard[i]))
                formatted_msg.append("\n")
            await message.channel.send("Game Ended Final Scores :-")
            await message.channel.send(''.join(formatted_msg))
            reset_vars()

    if message.content.startswith("!mulstart"):

        if name_list != []:
            await message.channel.send("Multiplayer war declared 🪖⚠️ lets see who wins :)")
            await message.channel.send("GUESS THE WORD NOW FIRST ONE TO GUESS WINS :)")
            mode = "multiplayer"
            game = True
        else:

            await message.channel.send("Brudda atleast add some people 😁")
    if message.content.startswith("!add"):
        stripped_msg = message.content.replace("!add ", "")
        name_list.append(stripped_msg)

        user_id = message.author.id
        username = "<@" + str(user_id) + ">"
        leaderboard[stripped_msg] = 0

        await message.channel.send(username + " added: " + stripped_msg)


if __name__ == '__main__':
    client.run(bot_token)
