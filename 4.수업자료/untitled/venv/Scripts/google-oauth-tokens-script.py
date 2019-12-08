#!C:\Users\MMT\Desktop\Sparta\4.수업자료\untitled\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'google-oauth2-desktop-flow==0.0.7','console_scripts','google-oauth-tokens'
__requires__ = 'google-oauth2-desktop-flow==0.0.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('google-oauth2-desktop-flow==0.0.7', 'console_scripts', 'google-oauth-tokens')()
    )
