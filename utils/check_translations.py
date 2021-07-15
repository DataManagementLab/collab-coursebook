# Check translation files for missing or fuzzy translations

import polib
import sys

APPS = ["collab_coursebook", "base", "frontend", "content"]
LANGUAGES = ["de_DE"]
problem = False

for app in APPS:
    for lang in LANGUAGES:
        print("======================================================================")
        print(f"{app} ({lang})")
        print("======================================================================")
        po = polib.pofile(f'{app}/locale/{lang}/LC_MESSAGES/django.po')

        percent_translated = po.percent_translated()
        print(f"{percent_translated} % translated\n")
        if percent_translated < 95:
            problem = True

        untranslated = po.untranslated_entries()
        if len(untranslated) > 0:
            print("Found the following untranslated entries:")
            for ue in untranslated:
                print(ue)

        fes = po.fuzzy_entries()
        if len(fes) > 0:
            problem = True
            print("Found the following fuzzy entries:")
            for fe in fes:
                print(fe)

if problem:
    sys.exit(1)
sys.exit(0)
