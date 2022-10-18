# rhymes
I made this Python program to create some fun rhymes. When thinking of how I would do that, I originally planned on finding the rhyming word using an API, then I would write a grammar text file which contained the forms that could create the atomics of a sentence:
```<noun> <verb> <article> <adjective> <noun>```for example. I would create a sentence structure ending in the part of the speech of the rhyme, then fill in the words. However, I found an easier way to do this. The Datamuse API provided the most common words that precede a given word, and I was able to use this to make jumbled sentences that sound like they could maybe make sense, and most importantly, rhyme. 

Status
In Progress: The computer will read out the lines
In Progress: The user will have the option to create different types of poems, like limericks or haikus, for example.
