# muz.py
Anki-like program to learn music theory by heart.

The values for tones, notes, and scales are determined algorithmically, meaning there is no stored value for, say 4th tone of D♯ Minor scale (G♯), but instead the algorithm goes through the notes in an octave and determines that value. This makes the script easily extendable to the entirety of music theory.
Right now the script is useful for learning all the different tones of any scale, so playing music becomes intuitive.
I will be adding other aspects of music theory later on.

Usage:
python3 muz.py -\<argument> \<difficulty level>

Arguments:
-b    - replaces UTF-8 symbols for sharp and flat with '#' and 'b'
  
-c    - prints out a cheat sheet for all the scales. Can be used with '-b' to print the notes with 'basic' notation, 
        like so: '-cb' | '-bc' | '-c -b', doesn't matter.

\<difficulty level> - A number from 1-5 with optional 'a' and 'b' options for some levels of difficulty to specify only some of the scales.
                     Can be used independently of other arguments or in conjunction with them. Used to skip the level selection menu.

(showcase is of the old version of a program)
https://user-images.githubusercontent.com/34137807/134750508-3fab04a4-0cc7-4ba4-b55b-bc5792447169.mov

