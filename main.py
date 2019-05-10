import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, splitname
import re

def main():
    with open("references.bib") as f:
        parser = BibTexParser()
        parser.customization = customizations
        bibdb = bibtexparser.load(f, parser)
        for bib in bibdb.entries:
            if isPublication(bib):
                authors = parseAuthors(bib["author"])
                title = bib["title"]
                etype = bib["ENTRYTYPE"]
                year = bib["year"]
                journal = bib.get("journal", None)
                volume = bib.get("volume", None)
                number = bib.get("number", None)
                pages = bib.get("pages", None)
                proceedings = bib.get("booktitle", None)
                editor = bib.get("editor", None)
                location = bib.get("location", None)
                eventDate = bib.get("eventdate", None)
                publisher = bib.get("publisher", None)

                printCitation(authors, title, etype, year, journal, volume, number, pages, proceedings, editor, location, eventDate, publisher)

def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = convert_to_unicode(record)

    return record
        
def printCitation(authors, title, etype, year, journal=None, volume=None, number=None, pages=None, proceedings=None, editor=None, location=None, eventDate = None, publisher=None):
    citation = ""
    authorStr=""
    journalStr=""
    eventDateStr = "" if eventDate == None else eventDate
    locationStr = "" if location == None else location
    editorStr = "" if editor == None else formatAuthors(parseAuthors(editor)) + " (eds.): "
    proceedingsStr = "" if proceedings == None else proceedings
    publisherStr = "" if publisher == None else publisher
    
    authorStr = formatAuthors(authors) + ": "

    title += ". "

    if etype == "article":

        journalStr+=journal + ", " + volume
         
        if number != None:
            journalStr +="("+number+")"
        
        pages = pages.replace("--","-")
        
        journalStr+=":"+pages+", "
    
    if etype == "inproceedings" or etype == "incollection":
        proceedingsStr = "In " + editorStr + proceedingsStr + ", " + publisherStr + ", " + locationStr +", " + eventDateStr + ", "

    key = generateKey(authors, year)

    citation+=key + authorStr + title + journalStr + proceedingsStr +  year
    print(citation+"\n\n")

def generateKey(authors, year):
    keyStr = "[key] "
    
    if len(authors) == 1:
        keyStr = keyStr.replace("key", authors[0]["lastName"]+", "+year)
    elif len(authors) == 2:
        keyStr = keyStr.replace("key", authors[0]["lastName"]+" and "+authors[1]["lastName"]+", "+ year)
    elif len(authors) > 2:
        keyStr = keyStr.replace("key", authors[0]["lastName"]+" et al., "+year)

    return keyStr


def formatAuthors(authors):
    temp=""
    for author in authors:
        temp+=author["firstName"][0]+". "+ author["lastName"]
        if len(authors) > 1 and author == authors[-2]:
            temp+=" and "
        elif author != authors[-1]:
            temp+=", "
        else:
            temp+=""
    return temp

def parseAuthors(bib_author):
    
    authors = []
    fullNames = re.compile(" and | and\n").split(bib_author)
    for fn in fullNames:
        fnList = fn.split(", ")
        if len(fnList) > 1:
            authors.append({"firstName": fnList[1], "lastName": fnList[0]})
        else:
            fnList = fn.split(" ")
            authors.append({"firstName": " ".join(fnList[:-1]), "lastName": fnList[-1]})
   
    return authors
    
def isPublication(bib):
        if bib["ENTRYTYPE"] in ("article", "inproceedings", "incollection", "techreport"):
            return True
        else:
            return False

if __name__ == "__main__":
    main()