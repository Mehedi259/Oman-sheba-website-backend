# 🎨 Django Admin Customization Guide

## ✅ Jazzmin Theme Installed!

Your admin panel is now using **Django Jazzmin** - a modern, clean, and beautiful admin theme!

### 🌐 Access Admin Panel
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

---

## 🎨 Available Themes

আপনি `settings.py` এর `JAZZMIN_SETTINGS` এ `"theme"` পরিবর্তন করে বিভিন্ন themes try করতে পারেন:

### Light Themes:
- **`flatly`** (current) - Modern flat design ✨
- **`cosmo`** - Clean and professional
- **`lumen`** - Light and elegant
- **`litera`** - Minimalist design
- **`minty`** - Fresh green accent
- **`simplex`** - Simple and clean
- **`united`** - Ubuntu-inspired
- **`yeti`** - Crisp and modern

### Dark Themes:
- **`darkly`** - Dark mode
- **`cyborg`** - Blue-grey dark theme
- **`slate`** - Professional dark
- **`solar`** - Yellow accents on dark
- **`superhero`** - Comic book inspired

### Other Themes:
- **`cerulean`** - Blue professional
- **`journal`** - Newspaper style
- **`pulse`** - Purple accents
- **`sandstone`** - Warm earthy tones
- **`spacelab`** - Space-themed

---

## 🛠️ How to Change Theme

### Option 1: Change in settings.py
```python
# sheba_backend/settings.py
JAZZMIN_SETTINGS = {
    # ... other settings ...
    "theme": "darkly",  # Change this to any theme name
}
```

### Option 2: Try Multiple Themes
```python
JAZZMIN_UI_TWEAKS = {
    "theme": "superhero",  # Change this
    "dark_mode_theme": "darkly",  # For dark mode
}
```

---

## 🎯 Customization Options

### 1. Change Site Title & Logo
```python
JAZZMIN_SETTINGS = {
    "site_title": "Your Company Admin",
    "site_header": "Your Company",
    "site_brand": "Your Company Name",
    "site_logo": "images/logo.png",  # Add your logo
    "welcome_sign": "Welcome to Your Admin Panel",
}
```

### 2. Customize Colors
```python
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",  # Blue navbar
    # or
    "navbar": "navbar-dark navbar-success",  # Green navbar
    # or
    "navbar": "navbar-white navbar-light",   # Light navbar
    
    "sidebar": "sidebar-dark-primary",       # Dark sidebar
    # or
    "sidebar": "sidebar-light-primary",      # Light sidebar
}
```

### 3. Add Custom Icons
Icons already configured for your models! You can change them:

```python
JAZZMIN_SETTINGS = {
    "icons": {
        "auth.User": "fas fa-user",
        "classifieds.Job": "fas fa-briefcase",
        "classifieds.Property": "fas fa-building",
        # Add more...
    }
}
```

**Icon Resources:**
- FontAwesome Icons: https://fontawesome.com/icons
- Format: `"fas fa-icon-name"` (solid) or `"fab fa-icon-name"` (brands)

### 4. Sidebar Navigation
```python
JAZZMIN_SETTINGS = {
    "show_sidebar": True,           # Show/hide sidebar
    "navigation_expanded": True,    # Expand by default
    "sidebar_fixed": True,          # Fix sidebar position
}
```

### 5. Custom CSS
Create a custom CSS file:

```css
/* static/admin/custom.css */
.sidebar-dark-primary {
    background-color: #2c3e50 !important;
}

.navbar {
    background: linear-gradient(to right, #667eea 0%, #764ba2 100%) !important;
}
```

Then add to settings:
```python
JAZZMIN_SETTINGS = {
    "custom_css": "admin/custom.css",
}
```

---

## 🎨 Popular Theme Combinations

### 1. Modern Blue (Professional)
```python
JAZZMIN_SETTINGS = {
    "theme": "flatly",
}
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-dark-primary",
}
```

### 2. Dark Mode (Developer Friendly)
```python
JAZZMIN_SETTINGS = {
    "theme": "darkly",
}
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-dark",
    "sidebar": "sidebar-dark-info",
}
```

### 3. Minimalist (Clean)
```python
JAZZMIN_SETTINGS = {
    "theme": "lumen",
}
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-light-primary",
}
```

### 4. Vibrant (Colorful)
```python
JAZZMIN_SETTINGS = {
    "theme": "superhero",
}
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-success",
    "sidebar": "sidebar-dark-success",
}
```

---

## 📊 Admin Dashboard Widgets

### Add Custom Links to Top Menu
```python
JAZZMIN_SETTINGS = {
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "API Docs", "url": "/swagger/", "new_window": True},
        {"name": "Website", "url": "http://localhost:3000", "new_window": True},
        {"app": "classifieds"},
    ],
}
```

### Customize User Menu
```python
JAZZMIN_SETTINGS = {
    "usermenu_links": [
        {"name": "View Site", "url": "http://localhost:3000", "new_window": True},
        {"name": "API Documentation", "url": "/swagger/", "new_window": True},
    ],
}
```

---

## 🔧 Advanced Customization

### Change Form Layout
```python
JAZZMIN_SETTINGS = {
    "changeform_format": "horizontal_tabs",  # or "vertical_tabs", "collapsible", "carousel"
}
```

### Hide/Show Apps
```python
JAZZMIN_SETTINGS = {
    "hide_apps": ["auth.Group"],  # Hide specific apps
    "hide_models": ["auth.Group"],  # Hide specific models
}
```

### Reorder Apps
```python
JAZZMIN_SETTINGS = {
    "order_with_respect_to": [
        "users",
        "classifieds", 
        "news",
        "community",
        "emergency",
        "auth"
    ],
}
```

---

## 🚀 Quick Theme Test

Theme পরিবর্তন করতে শুধু `settings.py` এ যাও এবং এই line টা change করো:

```python
"theme": "superhero",  # Try: darkly, flatly, cosmo, pulse, etc.
```

Save করে browser refresh দাও (Ctrl+Shift+R)!

---

## 📸 Screenshots

### Current Theme: Flatly
- Modern flat design
- Clean interface
- Professional look
- Light color scheme

### Try These Popular Themes:
1. **darkly** - For night owls 🌙
2. **superhero** - Bold and colorful 🦸
3. **cosmo** - Professional and clean 💼
4. **pulse** - Modern with purple accents 💜

---

## 🎨 Color Customization

### Navbar Colors
- `navbar-primary` - Blue
- `navbar-success` - Green
- `navbar-info` - Cyan
- `navbar-warning` - Yellow
- `navbar-danger` - Red
- `navbar-dark` - Dark grey
- `navbar-light` - Light grey

### Accent Colors
Same options: `accent-primary`, `accent-success`, etc.

---

## 💡 Tips

1. **Test themes quickly**: Just change the theme name and refresh
2. **Mix & match**: Combine different navbar and sidebar colors
3. **Use icons**: Makes navigation more intuitive
4. **Custom CSS**: For complete control over appearance
5. **Dark mode**: Popular with developers - try "darkly" or "cyborg"

---

## 📚 Resources

- Jazzmin Docs: https://django-jazzmin.readthedocs.io/
- Bootstrap Themes: https://bootswatch.com/
- FontAwesome Icons: https://fontawesome.com/icons

---

**Current Status**: ✅ Jazzmin theme installed and configured!

Try different themes and customize to match your brand! 🎨
