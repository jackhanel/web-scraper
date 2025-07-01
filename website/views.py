from flask import Blueprint, render_template, request
from .functions import scrapeURL

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        url = request.form.get("url")
        content_mode = request.form.get("content_mode")
        soup = scrapeURL(url)

        if not soup or not hasattr(soup, "prettify"):
            result = f"Failed to fetch or parse content from: {url}"
            return render_template("scrape.html", result=result)

        if content_mode == "entire":
            presentation = request.form.get("presentation")
            if presentation == "prettify":
                result = soup.prettify()
            elif presentation == "get_text":
                result = soup.get_text(strip=True)
            else:
                result = "Invalid presentation option selected."

        elif content_mode == "bespoke":
            mode = request.form.get("mode")
            keyword = request.form.get("keyword", "").strip().lower()

            if mode == "text":
                matches = (
                    soup.find_all(string=lambda t: keyword in t.lower())
                    if keyword
                    else soup.stripped_strings
                )
                result = "\n\n".join([m.strip() for m in matches if m.strip()])

            elif mode == "images":
                images = soup.find_all("img")
                img_urls = [img.get("src") for img in images if img.get("src")]
                result = "\n".join(img_urls)

            elif mode == "links":
                links = soup.find_all("a", href=True)
                if keyword:
                    filtered = [
                        f"{a.get_text(strip=True)} → {a['href']}"
                        for a in links
                        if keyword in a.get_text(strip=True).lower()
                    ]
                else:
                    filtered = [
                        f"{a.get_text(strip=True)} → {a['href']}" for a in links
                    ]
                result = "\n".join(filtered)

            elif mode == "headers":
                headers = soup.find_all(["h1", "h2", "h3"])
                result = "\n".join([h.get_text(strip=True) for h in headers])

            else:
                result = "Invalid bespoke mode selected."

        else:
            result = "Please select a content mode."

    return render_template("scrape.html", result=result)
