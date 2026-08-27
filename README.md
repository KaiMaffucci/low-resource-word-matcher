# low-resource-word-matcher
A writing similarity matcher/detector for finding cognates and writing variants in low-resource and endangered languages, particularly Cherokee.

**Navigation guide**
 - To view copyright and sovereignty notices, keep scrolling in this README.
 - To learn how to use the software, scroll even further.
 - To look at the dataset, testing process, and findings/discussion for the results of the Cherokee version, check the `data` directory (contained within the `data` directory to maintain clarity about copyright).
 - To look at the code, look at all of the other directories (I recommend starting with `main.py` in the root of this repository). 

## Important Copyright Information

DATA SOVEREIGNTY AND COPYRIGHT NOTICE: All Cherokee language material in the `data` folder does NOT fall under the MIT license of the rest of the repository. I do NOT own the data, and it is subject to the original copyright holders, detailed below. If any of the respective copyright holders of the data wish for me to take it down or modify it, feel free to email me [here](https://www.kaimaffucci.org/contact_form), and such matters will be handled immediately.

Syllabary writings for all non-clothing words found on the Cherokee Nation of Oklahoma Language Department's posters section of their website here: https://language.cherokee.org/posters/classroom/

Words on clothing found here: https://shiyo.org/clothing

All words were cross-referenced with entries in the Durbin Feeling dictionary here, based on the English translation: https://www.cherokeedictionary.net/

## Cherokee Sovereignty Notice

I am NOT Cherokee NOR indigenous, and I do not claim that identity, nor am I an authority in Cherokee linguistics. Take everything I say with a huge grain of salt. Furthermore, this research project is conducted in accordance with the CARE guidelines for researchers (https://www.navigating.art/articles-from-navigatingart/care-data-practices-for-art-researchers-an-introduction-to-ethical-digital-scholarship). Importantly, stressing these major points:

1. This research is done for the **collective benefit** of the community. Researchers must steer away from purely extractive research models for personal gain, and consider what their research does for the community from which they use data. In this case, the methods in this project may be used to discover relationships between words and detect writing variants. I will be as clear as possible about how this project works and how to use it, so that second-language learners can use the software if they wish. In addition, I hope it serves as inspiration to any aspiring indigenous scholars looking to learn more about writing software for their language. If you are, feel free to fork the repository and interact in general.
2. In addition to the copyright notice, in accordance with the **ability to control**, I encourage any community members who find this project to reach out. Input on the project's conduct and its datasets is welcome and encouraged.
3. In the name of **responsibility**, I will remain absolutely transparent about the results obtained from this project (`data/FINDINGS.md`). I am NOT an indigenous scholar, nor do I claim to be an authority on Cherokee or any indigenous language; I am merely an outside learner.
4. This project and its data will only be used for **ethical** purposes. It will NOT be used to appropriate or otherwise disparage in any way.

## Running the Program

### Setup

First, download/clone the repository. Make sure you have [Python 3](https://www.python.org/) installed, and also check that you have `pip install`ed these libraries:

- [NumPy](https://numpy.org/install/)
- [NetworkX](https://networkx.org/en/)

### Execution

Open a terminal/shell window in the root of the repository on your computer.

Your command will be of the general format:

``python3 main.py /absolute/directory/of/target/version``

`python3` is whatever command you use to run Python on your machine. For more information, visit `python.org`. The directory name is the absolute directory path of the version you want to use. It could be to the `generic` folder, or more likely, to the `cherokee` folder. Whichever version you execute will ask for additional instructions; see below for more information.

#### Dataset Formatting

For the Cherokee version, it expects a single file (eg., `data/cherokee_vocab`) where each line is a series of Latin characters and whitespace, followed by Cherokee syllabics and whitespace, followed by more Latin characters. This is because I was originally using data exported from my Anki deck as the dataset, which followed this format. The initial Latin characters are the English definition; the Cherokee syllabics are the Cherokee phrase; and the Latin characters after that are the phonetics of that phrase. From this, it generates two sets of words: the first with the syllabics and original phonetics, and the second with the syllabics plus transliterated phonetics from those syllabics. These are the two word sets it compares for similarity.

For the generic version, it simply expects two separate data files, where each line in each file is an individual word.

The final output of the program running will be a file called `results` in the root of the repository.
