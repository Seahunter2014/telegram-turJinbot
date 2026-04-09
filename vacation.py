from urllib.parse import urlencode
from app.config import TRAVELPAYOUTS_MARKER


def with_marker(url: str) -> str:
    sep = '&' if '?' in url else '?'
    return f"{url}{sep}marker={TRAVELPAYOUTS_MARKER}"


def slugify_ru(text: str) -> str:
    m = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',' ':'-'
    }
    return ''.join(m.get(ch, ch) for ch in text.lower()).strip('-')


def query_url(base: str, params: dict) -> str:
    clean = {k: v for k, v in params.items() if v not in (None, '', 0)}
    if not clean:
        return base
    return f"{base}?{urlencode(clean, doseq=True)}"
