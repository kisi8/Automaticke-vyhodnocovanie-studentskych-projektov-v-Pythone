'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: constants.py

File containing constants used throughout
whole system.
'''

# SHEBANG
SHEBANG = ("#!/usr/bin/env python", "#!/usr/bin/env python3")

# DOVOLENÉ PRÍPONY SÚBOROV
ALLOWED_EXTENSIONS = set(['py'])

# CESTA K PRIEČINKU PRE ULOŽENIE PROJEKTOV
UPLOAD_FOLDER = '/mnt/data/isj-2017-18/public/app/projects'

# POPISY IDIÓMOV
SHEBANG_POPIS = 'Úlohou Shebangu je označiť daný skript tak, aby bol spustiteľný ako samostatný súbor bez písania "python" pred skript, ak ho spúšťame napríklad cez terminál. Používa sa výhradne na prvom riadku skriptu. Shebang je využívaný v oblasti unixových systémov. Presnejšie a obsiahlejšie vysvetlenie nájdete na: https://en.wikipedia.org/wiki/Shebang_(Unix)'
WITH_OPEN = 'Bezpečnejšie je použiť variantu with open, kde je zavretie súboru vykonané automaticky. Viac na: https://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html'
NESTED_IF = 'Snažte sa vyvarovať použitiu viacnásobných if konštrukcii za sebou. Kód je horšie čitateľný a v zanorení sa dá ľahko stratiť.'
CHAIN_COMPARISON = 'Treba si dávať pozor, aké premenné porovnávate. Namiesto "x < y and y < z" sa dá efektívne napísať "x < y < z".'
REPEATING_VARIABLE = 'Ak chcete porovnávať premennú oproti väčšiemu počtu hodnôt, je vhodné použiť štruktúru list alebo set. Napríklad: "if item in my_list:"'
COMPARE_TO_BOOL = 'Porovnávanie premenných, funkcii alebo objektov k True, False alebo k prázdnym listom, tuplom je zbytočné. Stačí jednoducho porovnať danú premennú napr.: "if foo:". Viac na: https://docs.quantifiedcode.com/python-anti-patterns/readability/comparison_to_true.html'
IN_ITERABLE = 'Ak chcete iterovať cez dĺžku nejakej štruktúry, je vhodné použiť kľúčové slovo "in" spolu s cyklom for. Toto bude mať rovnaký efekt ako foreach v iných jazykoch: "for item in list:". Viac na: http://www.jworks.nl/2013/11/07/python-goodness-the-in-keyword/'
MUTABLE_DEFAULT_VALUE = 'Snažte sa nepoužívať defaultné hodnoty parametrov funkcii v podobe prázdnych listov, setov alebo dictov. Je lepšie použiť hodnotu None. Inak môžu nastať nepríjemnosti, ktoré sú najlepšie popísané tu: https://docs.quantifiedcode.com/python-anti-patterns/correctness/mutable_default_value_as_argument.html'
RETURN_EXPRESSION = 'Skúste využívať return na vyhodnocovanie výrazov alebo funkcii, nie len na vracanie hodnôt von z funkcie. Porozmýšľajte či to nie je váš prípad.'
USE_EXCEPTIONS = 'Ak je to vhodné, tak sa snažte využívať plný potenciál návratovej funkcie raise v try-except bloku, ktorá uchováva užitočné informácie o vyskytnutej chybe. Viac napríklad na: https://docs.python.org/3.6/tutorial/errors.html'
CORE_EXCEPTIONS = 'Nemali by ste vyhadzovať výnimky, ktoré sú nejak špecifické pre interpret. Problém je lepšie popísaný tu: https://utcc.utoronto.ca/~cks/space/blog/python/NeverRaiseCoreExceptions'
CHAIN_ASSIGNMENT = 'Python podporuje viacnásobné priradenie, kde je viacerým premenným priradená rovnaká hodnota. Príklad: " x = y = z = "foo" "'
VARIABLES_SWAP = 'Výmena hodnoty dvoch premenných sa dá v pythone uskutočniť pomocou tuples nasledovne: " (foo, bar) = (bar, foo) ". Viac na: https://www.pythoncentral.io/swapping-values-in-python/'
CHAIN_COMPARISON_IF = 'Pri porovnávaní premenných voči rovnakej hodnote je možné využiť nasledujúcu konštrukciu: " if y == x == z == "foo": ". Následne budú všetky premenné porovnané voči hodnote foo.'
REMOVE_DUPLICATES_LIST = 'Ak sa snažíte z listu zmazať duplikáty, je vhodnejšie použiť datovú štruktúru set(), ktorá je nezoradená kolekcia unikátnych čiže neopakujúcich sa prvkov. Viac na: https://www.programiz.com/python-programming/set'
CHAIN_STRING_FUNCTIONS = 'Pri používaní jednoduchým funkcii na úpravu stringov je ich vhodné reťaziť za sebou, ak používame viac funkcii na jeden prvok. Napr.: " foo.strip().upper().lower() "'
JOIN_STRINGS = 'Ak sa snažíte spojiť stringy nachádzajúce sa v liste, je vhodnejšie, rýchlejšie použiť konštrukciu " ''.join() ", ktorá používa menej pamäte. Stačí teda funkcii join predať celý list stringov nasledovne: " result = ''.join(my_list) ".'
DONT_USE_MAP = 'V "pythonovksom" kóde by ste použitie funkcie map() a filter() mali vymeniť za list comprehension napr. nasledovne príklad pre map(): " map(f, iterable) ---> [f(x) for x in iterable] ". Viac o list comprehensions: http://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/'
USE_SUM_LIST = 'Ak sa snažíte spočítať hodnoty v liste, presne na to existuje built-in funkcia sum(). Jednoducho do nej pridáte list, ktorý obsahuje čisto čísla: " sum(my_list) ". Viac na: https://docs.python.org/3.6/library/functions.html#sum'

# PROJ 01
ASSERT = 'Výsledok nesedí s očakávaním riešením. Skúste opraviť vaše riešenie. Bez fungujúcich assertov prídete o body.'
FIRST_TASK_REGEX = 'V tomto konkrétnom prípade je vhodné použiť negative lookahead ako aj positive lookbehind. Viac o nich na: http://www.rexegg.com/regex-lookarounds.html'
SECOND_TASK_REGEX = 'V tomto konkrétnom prípade je vhodné použiť negative lookahead, positive lookbehind ako aj positive lookahead. Viac o nich na: http://www.rexegg.com/regex-lookarounds.html'
SECOND_TASK_STRING = 'Podstatou úlohy je napísať regex tak, aby vyhovoval vopred pripravenému assertu. Zmena testovacích stringov môže negatívne dopadnúť v konečnom hodnotení.'

# PROJ 02
GLOBAL_LIST = 'Podstatou úlohy je doplniť kód podľa zadania tak, aby vyhovoval vopred pripravenej podmienke na konci projektu. Zmena testovacieho listu eskymo môže negatívne dopadnúť v konečnom hodnotení.'
FUNGUJE_NEFUNGUJE = 'Funkcia nevracia očakávané údaje. Skúste prekontrolovať vaše riešenie.'
FIRST_TASK_RETURN = 'Podstatou úlohy je doplniť kód podľa zadania tak, aby vyhovoval vopred pripravenej podmienke na konci projektu. Zmena predpripravejen hodnoty môže negatívne dopadnúť v konečnom hodnotení.'
FIRST_TASK_SET = 'Ak sa snažíte z listu zmazať duplikáty, je vhodnejšie použiť datovú štruktúru set(), ktorá je nezoradená kolekcia unikátnych čiže neopakujúcich sa prvkov. Viac na: https://www.programiz.com/python-programming/set'
FIRST_TASK_LENGHT = 'Pre spočítanie prvkov v liste existuje špeciálna metóda. Je ju možno nájsť tu: https://docs.python.org/3/library/functions.html'
SECOND_TASK_LIST = 'Podstatou úlohy je doplniť kód podľa zadania tak, aby vyhovoval vopred pripravenej podmienke na konci projektu. Zmena predpripravejen hodnoty môže negatívne dopadnúť v konečnom hodnotení.'
SECOND_TASK_AND = 'V danom príklade je vhodné použiť dátovú štruktúru set() s jej špeciálnou operáciou intersection. Viac na: https://docs.python.org/2/library/sets.html'
THIRD_TASK_COLL = 'V tomto prípade je najvhodnejšie použiť funkciu z knižnice collections s názvom Counter. Viac na: https://docs.python.org/3/library/collections.html'
FOURTH_TASK_SLICE = 'Pri práci so stringami existuje veľmi šikovná metóda orezávania, ktorá sa nazýva slicing. V danej úlohe je potreba použiť jej kombináciu. Viac o slicingu na: https://www.digitalocean.com/community/tutorials/how-to-index-and-slice-strings-in-python-3'
FIFTH_TASK_SPLIT = 'V tomto prípade je najvhodnejšie použiť metódu split(), ktorá vráti list všetkých slov v stringu, rozdelených pomocou určeného separátora. Viac na: https://www.tutorialspoint.com/python/string_split.htm'
FIFTH_TASK_SLICE = 'Pri práci s listami existuje veľmi šikovná metóda orezávania, ktorá sa nazýva slicing. Viac o slicingu na: https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python/'
FIFTH_TASK_JOIN = 'V tomto prípade je najvhodnejšie použiť metódu join(), ktorá je v podstate opak metódy split(), čiže vráti string zo všetkých prvkov v danej dátovej štruktúre rozdelených pomocou určeného separátora. Viac na: https://www.tutorialspoint.com/python/string_join.htm'

# PROJ 03
PLUR2SING_ZIP = 'Správne riešenie si vyžaduje použitie funkcie zip().'
MATCH_PERMUTATIONS_SORTED = 'Presne pre tento účel existuje funkcia, ktorá vytvorí list so zoradenými prvkami. Je ju možno nájsť tu: https://docs.python.org/3/howto/sorting.html'

# PROJ 04
DOCSTRINGS = 'Nezabudnite ku každej funkcii doplniť docstringy. Ich formát a použitie je spísané v doporučení PEP 257: https://www.python.org/dev/peps/pep-0257/'
DONT_IMPORT = 'Vo funkcii all_subsets nesmú byť použité importy. Viď zadanie projektu.'
FUNCTIONS = 'Váš skript musí obsahovať funkcie, can_be_a_set_member_or_frozenset, all_subsets a all_subsets_excl_empty. Viď zadanie.'
ASSERT_ERROR = 'Tento test vám neprešiel. Upravte funkciu, aby assert fungoval.'
ISINSTANCE = 'Použitie funkcie isinstance() nie je vhodné. Problém je komplexnejší a súvisí s témou "duck typing". Viac o nej na: http://www.voidspace.org.uk/python/articles/duck_typing.shtml'
LIMIT_ARGS = 'Ľubovolný počet parametrov nie je pre túto funkciu povolený.'

# PROJ 05
FUNCTIONS5 = 'Váš skript musí obsahovať triedu Polynomial, rovnako ako funkcie derivative a at_value.'
TYPE = 'Pre zisťovanie typu objektu v objektovo orientovanom programovaní je lepšie použiť isinstance() funkciu nakoľko type nevráti žiadaný výsledok pri porovnávaní podtriedy. Viac na: https://stereochro.me/ideas/type-vs-isinstance'

# PROJ 06
FUNCTIONS6 = 'Váš skript musí obsahovať funkciu first_nonrepeating a combine4.'
NON_ARG_2 = 'Táto funkcia by mala vyžadovať iba jeden argument.'

# PROJ 07
FUNCTIONS7 = 'Váš skript musí obsahovať dekorátor obecných funkcii limit_calls, generétorovú funkciu ordered_merge ako aj triedu Log s metódou logging.'
LIMIT_CALLS_ARGS = 'Dekorátor limit_calls musí mať práve 2 parametre a to max_calls a error_message_tail.'
LIMIT_CALLS_DEFAULTS = 'Parameter max_calls musí mať defaultnú hodnotu 2 a parameter error_message_tail defaultnú hodnotu "called too often". Viac na: https://www.programiz.com/python-programming/function-argument#def'
ORDERED_MERGE_ARGS = 'Pri ľubovoľnom počte vstupných parametrov vo funkcii je dobré definovať špeciálny typ parametru s názvom arbitrary argument. Taktiež musí funkcia obsahovať parameter selector. Viac o arbitrary argumentoch na: https://www.programiz.com/python-programming/function-argument#arb'