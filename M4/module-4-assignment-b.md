# Module 4: Assignment B
## Cracking the Bible Code
-------------------------------------------------------------------------------

The Bible code is a purported set of encoded words within a Hebrew text of the Torah that, according to proponents, has predicted significant historical events. The statistical likelihood of the Bible code predictions arising by chance has been thoroughly researched, and it is now widely considered to be statistically insignificant, as similar phenomena can be observed in any sufficiently lengthy text[1]. Although Bible codes have been postulated and studied for centuries, the subject has been popularized in modern times by Michael Drosnin's book "The Bible Code" and the movie "The Omega Code".

In 1994, a peer-reviewed academic journal reported statistically significant codes in the Bible was published as a "challenging puzzle"[2]. It was pronounced "solved" in a subsequent 1999 paper published in the same journal.[3]

In the original paper, the authors used Equidistant Letter Sequences (ELS) to identify words and names within the text.  Using this technique others have claimed to have correlated names, dates, and historical events, such as the assassination of John F. Kennedy or the September 11 attacks in New York.

Today, the Bible Code has been largely dismissed as statistically insignificant and simply an amusing byproduct of searching a large body of text. Read the excerpt of "[The Baltimore Stockbroker and the Bible Code](https://canvas.uchicago.edu/files/9921711/)" from "How Not to Be Wrong" by Jordan Ellenberg for historical context. *Despite the underlying statistics, there are still two distinct camps of people when it comes to the Bible Code: those who believe and those who don't.*

<p><iframe title="YouTube video player" src="https://www.youtube.com/embed/Lk3VgQgxiqE" width="560" height="315" allowfullscreen="allowfullscreen" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe></p>


Write a program using the ELS algorithm to predict the future, understand the past, or prove this was just a text anomaly. Just like some of the skeptics, you will be using texts from the King James Bible, War and Peace, and Moby Dick. The texts are all available in the module and in `/projects2/mpcs56430/bible_code` on the RCC.

As an example, given the string, `In the beginning God created the heaven and the earth`, from Genesis 1:1 we apply the ELS algorithm with a stride of 2, 3 and 4:

```
stride:   2
string:   iteeinngdraeteevnnteat
words:    it, tee, in, tea

stride:   3
string:   ihennortthvatet
words:    i, hen, or, vat

stride:   4
string:   ieindatenta
words:    in, date
```


While the ELS algorithm is straightforward it should be implemented to make use of parallel programming modes and run using SLURM on the RCC. Your program should exhaustively search through the text and collect any words. The resulting strings can be compared to the list of the 10,000 most commonly used words in the English language. Feel free to use any other approaches to making sense of your words or to include any other reference strings (eg. names, dates, etc.).

Collect all the words for each stride into a file that should be stored in our project folders. Create a directory with your CNET id in the project folder and use the following naming convention:

```
/project2/mpcs56430/<cnetid>/biblecode/stride-2-moby.txt
/project2/mpcs56430/<cnetid>/biblecode/stride-2-bible.txt
/project2/mpcs56430/<cnetid>/biblecode/stride-2-warandpeace.txt

/project2/mpcs56430/<cnetid>/biblecode/stride-3-moby.txt
/project2/mpcs56430/<cnetid>/biblecode/stride-3-bible.txt
/project2/mpcs56430/<cnetid>/biblecode/stride-3-warandpeace.txt
...
```

Include all of your code and scripts in your repository. Include a `README.md` file that explains your overall approach and includes any "interesting words or phrases" that you uncover. Note that the original Bible Code research was conducted on a Hebrew version of the Torah, so our use of English texts might not be as fruitful.

From the King James translation of Matthew 7:7: "seek, and ye shall find; knock, and it shall be opened unto you".


---

[1] McKay, Brendan; Bar-Natan, Dror; Bar-Hillel, Maya; Kalai, Gil (May 1999). "Solving the Bible Code Puzzle". Statistical Science. 14 (2): 150–173. doi:10.1214/ss/1009212243. ISSN 0883-4237.
[2] "Equidistant Letter Sequences in the Book of Genesis" ([PDF](http://www.torahcode.co.il/pdf_files/pub/wrr.pdf)).
[3] Kass, Robert E. (May 1999). "Introduction to "Solving the Bible Code Puzzle" by Brendan McKay, Dror BarNatan, Maya BarHillel and Gil Kalai". Statistical Science. 14 (2): 149. doi:10.1214/ss/1009212242. ISSN 0883-4237.