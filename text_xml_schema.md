# Text xml markup

## Allowable tags
- <text title="Title"> parent element for a text
    -<kovol> phonetic or orthographic text. Commas are permissible for punctuation to help indicate flow. This field is always for imɛngis dialect, even if the audio recording is matat
    - <literal> a literal translation of the kovol. Must have the same number of words as kovol (see literal formatting). Punctuation must match
	- <free> a free translation of the text
	- <speaker> the speaker
	- <transcriber> the name of the team member who did the initial transcription
	- <filename> the relative path of the audio file transcribed from (eg audio/Audio_1.mp3)
	- <date> the date transcribed yy-mm-dd
	- <trans_quality> a number of 0-5 representing the confidence you have in the transcription. 0 being none, 5 being 100% confidence
	- <notes> personal notes you may want to add
	- <genre> Narrative, Hortatory, Procedural, Expository or Descriptive
	- <matat>If the text is to record the matat version (if the audio was first given in matat)
	
## Literal formatting
Literal translations have to have the same number of words as the Kovol. To do this you can use underscores for compound words:
> sibalig = bush_knife

Verbs should be written like this, actor-tns-mode-english
> liβigom =  1s-p-come_up

Short verbs are written like this:
> oβoβ = sh-get

### Tenses
- f (future)
- p (recent past)
- rp (remote past)

### Actors
1s, 2s, 3s, 1p, 2p, 3p

### Mode
- imp (imperative)

> nɛle = 2s-f-imp-throw

Just leave blank for declaratives; they're 90% of verbs - we can save typing

### Aspect
- jam (continual)

> alugejam = 3s-p-clean-cont

### Unknown tenses and actors
Use a ? if you're not sureː
> manda = ?-walk

You can use ? for words you don't know too
