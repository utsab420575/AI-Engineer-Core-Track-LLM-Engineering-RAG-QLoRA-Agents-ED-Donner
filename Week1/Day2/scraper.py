
# Code	                                    What it does
# requests.get()	                        Downloads website HTML
# BeautifulSoup()	                        Parses HTML
# soup.title	                            Finds website title
# soup.body	                                Finds website body
# .decompose()	                            Removes HTML elements
# .get_text()	                            Extracts readable text
# find_all("a")	                            Finds all hyperlinks
# .get("href")	                            Extracts link URL
# [:2000]	                                Limits output to 2,000 characters




# Import BeautifulSoup from bs4
# WHY: BeautifulSoup helps us read and extract information
# from HTML documents (website source code).
from bs4 import BeautifulSoup

# Import requests library
# WHY: Requests allows Python to visit websites
# and download their HTML content.
import requests


# Create HTTP headers
# WHY: A User-Agent identifies the client making the request.
# We use a browser-like User-Agent because some websites
# restrict requests that look like automated scripts.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


# FUNCTION 1: Fetch website title and text content
# WHY: We create a reusable function so we can extract
# content from different websites by passing their URLs.
def fetch_website_contents(url):

    # Docstring: Explains the purpose of this function.
    # It returns the website title and text,
    # with a maximum limit of 2,000 characters.
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """

    # Send an HTTP GET request to the website.
    # WHY: We need to download the website's HTML.
    # url = The website address we want to visit.
    # headers = Browser-like information sent with our request.
    # response = Stores the server's response.
    response = requests.get(url, headers=headers)

    # Convert the downloaded HTML into a BeautifulSoup object.
    # WHY: Raw HTML is difficult to search and extract information from.
    # BeautifulSoup makes it easier to find titles, paragraphs, links, etc.
    # "html.parser" tells Python that the downloaded content is HTML.
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the website title.
    # soup.title = Finds the HTML <title> element.
    # .string = Extracts the text inside the title element.
    # if soup.title = Checks whether a title exists.
    # else = Returns "No title found" if there is no title.
    title = soup.title.string if soup.title else "No title found"

    # Check whether the website has a <body> element.
    # WHY: The body generally contains the main visible website content.
    if soup.body:

        # Find and remove unnecessary HTML elements.
        # WHY: We only want readable text, not scripts, styling,
        # images or form input elements.
        #
        # <script> = JavaScript code
        # <style>  = CSS styling
        # <img>    = Images
        # <input>  = Form input fields
        for irrelevant in soup.body(["script", "style", "img", "input"]):

            # Permanently remove the selected HTML element.
            # WHY: Prevents unwanted content from appearing
            # when we extract the website text.
            irrelevant.decompose()

        # Extract readable text from the website body.
        # get_text() = Extracts text from HTML elements.
        # separator="\n" = Puts a new line between extracted text.
        # strip=True = Removes unnecessary whitespace.
        text = soup.body.get_text(separator="\n", strip=True)

    else:

        # If the website has no body element,
        # assign an empty string instead of extracting text.
        text = ""

    # Combine the website title and extracted text.
    # "\n\n" = Adds two new lines between title and content.
    # [:2_000] = Keeps only the first 2,000 characters.
    # WHY: Limits the amount of website content returned,
    # which is useful when sending text to an AI model.
    return (title + "\n\n" + text)[:2_000]


# FUNCTION 2: Fetch website links
# WHY: This function collects hyperlinks from a website.
# It is separate from the first function because sometimes
# we need links rather than the website's text.
def fetch_website_links(url):

    # Docstring: Explains what the function does.
    """
    Return the links on the website at the given url.
    """

    # Send an HTTP GET request to download the website HTML.
    # We use the same headers to identify our client.
    response = requests.get(url, headers=headers)

    # Parse the downloaded HTML using BeautifulSoup.
    # WHY: We need to search the HTML for anchor (<a>) tags.
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all anchor tags and extract their href attributes.
    #
    # soup.find_all("a") = Finds every <a> tag on the page.
    # link.get("href") = Extracts the URL stored in href.
    #
    # This is called LIST COMPREHENSION in Python.
    # It creates a list of all extracted link values.
    links = [link.get("href") for link in soup.find_all("a")]

    # Remove empty values and None from the links list.
    # WHY: Some anchor tags may not contain an href attribute.
    # "if link" keeps only values that are not empty.
    return [link for link in links if link]
