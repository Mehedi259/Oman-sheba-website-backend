import os
import re

apps = ['classifieds', 'community', 'news', 'emergency', 'system']
base_dir = '/Users/mehedihasanmridul/Backend/ShebaWebsiteBackend'

for app in apps:
    views_path = os.path.join(base_dir, app, 'views.py')
    if not os.path.exists(views_path): continue
    
    with open(views_path, 'r') as f:
        content = f.read()
        
    if "'system.filters.CountryFilterBackend'" not in content:
        content = re.sub(
            r'filter_backends\s*=\s*\[',
            r"filter_backends = ['system.filters.CountryFilterBackend', ",
            content
        )
        with open(views_path, 'w') as f:
            f.write(content)
        print(f"Patched {views_path}")
