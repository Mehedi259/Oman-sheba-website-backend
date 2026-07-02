# 🎨 Django Unfold - Modern Admin Theme

## ✨ Django Unfold Installed!

আপনার admin panel এখন **Django Unfold** use করছে - সবচেয়ে modern, clean এবং professional admin theme!

### 🌐 Access Admin Panel
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

---

## 🎯 Key Features

### ✅ Modern Design
- **Tailwind CSS** based - Latest design trends
- **Clean & Minimal** - No clutter, very professional
- **Responsive** - Works perfectly on mobile
- **Dark Mode Support** - Eye-friendly

### ✅ Professional UI Elements
- Material Design Icons (Google Icons)
- Smooth animations
- Better form layouts
- Advanced filters
- Custom navigation sidebar
- Breadcrumbs
- Search functionality

### ✅ Developer Friendly
- Easy to customize
- Well documented
- Active development
- Modern codebase

---

## 🎨 Customization

### 1. Change Color Scheme

Unfold uses Tailwind CSS colors. আপনি `COLORS` section customize করতে পারেন:

```python
# settings.py
UNFOLD = {
    "COLORS": {
        "primary": {
            # Blue theme
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",  # Main color
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
        },
    },
}
```

### Popular Color Schemes:

#### 🔵 Professional Blue (Default)
```python
"500": "59 130 246",  # Blue
```

#### 🟢 Success Green
```python
"500": "34 197 94",  # Green
```

#### 🟣 Creative Purple
```python
"500": "168 85 247",  # Purple
```

#### 🔴 Bold Red
```python
"500": "239 68 68",  # Red
```

#### ⚫ Dark Theme
```python
"500": "71 85 105",  # Slate grey
```

### 2. Customize Site Branding

```python
UNFOLD = {
    "SITE_TITLE": "Your Company Admin",
    "SITE_HEADER": "Your Company Platform",
    "SITE_URL": "/",
    
    # Add your logo
    "SITE_LOGO": {
        "light": "/static/logo-light.svg",
        "dark": "/static/logo-dark.svg",
    },
    
    # Change icon
    "SITE_SYMBOL": "business",  # Google Material icon name
}
```

### 3. Customize Sidebar Navigation

Already configured for your Sheba app! But you can modify:

```python
"SIDEBAR": {
    "show_search": True,
    "show_all_applications": True,
    "navigation": [
        {
            "title": "Dashboard",
            "items": [
                {
                    "title": "Home",
                    "icon": "dashboard",
                    "link": lambda request: "/admin/",
                },
            ],
        },
        # Add more sections...
    ],
}
```

### 4. Material Design Icons

Unfold uses Google Material Icons. Some popular ones:

**General:**
- `dashboard` - Dashboard
- `settings` - Settings
- `analytics` - Analytics
- `notifications` - Notifications

**User Related:**
- `person` - User
- `group` - Groups
- `account_circle` - Account
- `badge` - Profile

**Content:**
- `article` - Articles/News
- `forum` - Community
- `chat` - Comments
- `favorite` - Favorites

**Business:**
- `work` - Jobs
- `home` - Properties
- `directions_car` - Vehicles
- `build` - Services
- `local_hospital` - Emergency

**Actions:**
- `add` - Add
- `edit` - Edit
- `delete` - Delete
- `save` - Save
- `search` - Search

Full icon list: https://fonts.google.com/icons

---

## 🌙 Dark Mode

Unfold automatically supports dark mode! Users can toggle it from their browser/system settings.

To set a default theme:
```python
# settings.py
UNFOLD = {
    "THEME": "dark",  # or "light" or "auto"
}
```

---

## 🎯 Advanced Customization

### Custom CSS

Create a custom CSS file:

```css
/* static/admin/custom.css */
:root {
    --color-primary-500: 245 158 11; /* Custom orange */
}

.unfold-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Add to settings:
```python
UNFOLD = {
    "STYLES": [
        lambda request: "/static/admin/custom.css",
    ],
}
```

### Custom JavaScript

```python
UNFOLD = {
    "SCRIPTS": [
        lambda request: "/static/admin/custom.js",
    ],
}
```

---

## 📊 Dashboard Widgets

### Add Custom Dashboard

Create `admin.py`:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

class JobAdmin(ModelAdmin):
    list_display = ['title', 'company_name', 'status_badge']
    
    @display(description="Status", label=True)
    def status_badge(self, obj):
        colors = {
            'active': 'success',
            'sold': 'info',
            'expired': 'warning',
        }
        return obj.status, colors.get(obj.status, 'default')
```

---

## 🎨 Color Themes Ready to Use

### 1. Modern Blue (Current)
```python
"primary": {
    "500": "59 130 246",  # Blue
}
```

### 2. Success Green
```python
"primary": {
    "500": "34 197 94",  # Green
}
```

### 3. Creative Purple
```python
"primary": {
    "500": "168 85 247",  # Purple
}
```

### 4. Professional Indigo
```python
"primary": {
    "500": "99 102 241",  # Indigo
}
```

### 5. Vibrant Orange
```python
"primary": {
    "500": "249 115 22",  # Orange
}
```

### 6. Modern Teal
```python
"primary": {
    "500": "20 184 166",  # Teal
}
```

---

## 🚀 Quick Customization Tips

### Change Primary Color in 30 Seconds:

1. Open: `sheba_backend/settings.py`
2. Find: `UNFOLD` section
3. Change: `"500": "59 130 246"` to your color
4. Save and refresh browser

### Tailwind Color Picker:
https://tailwindcss.com/docs/customizing-colors

---

## 📱 Mobile Responsive

Unfold is fully responsive! Your admin panel looks great on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktop monitors

---

## 🔧 Admin Model Customization

Unfold provides enhanced admin features:

```python
from unfold.admin import ModelAdmin
from unfold.decorators import display

@admin.register(Job)
class JobAdmin(ModelAdmin):
    # Unfold features
    list_filter_submit = True  # Add filter button
    list_fullwidth = True      # Full width list
    
    # Custom displays
    @display(description="Company", header=True)
    def company_header(self, obj):
        return obj.company_name.upper()
```

---

## 💡 Pro Tips

1. **Use Material Icons** - Makes navigation intuitive
2. **Customize Colors** - Match your brand
3. **Dark Mode** - Professional and eye-friendly
4. **Custom Dashboard** - Add your own widgets
5. **Mobile First** - Works great on all devices

---

## 🎨 Compare with Other Themes

| Feature | Unfold | Jazzmin | Default |
|---------|--------|---------|---------|
| Design | Modern ⭐⭐⭐⭐⭐ | Good ⭐⭐⭐ | Basic ⭐ |
| Dark Mode | ✅ Built-in | ❌ Limited | ❌ No |
| Mobile | ✅ Perfect | ✅ Good | ⚠️ Basic |
| Icons | Material Design | FontAwesome | None |
| Customization | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Performance | ⚡ Fast | ⚡ Good | ⚡ Fast |
| Modern Look | ✅ 2024 | ⚠️ 2020 | ❌ 2008 |

---

## 📚 Resources

- Unfold Docs: https://unfoldadmin.com/
- Material Icons: https://fonts.google.com/icons
- Tailwind Colors: https://tailwindcss.com/docs/customizing-colors
- GitHub: https://github.com/unfoldadmin/django-unfold

---

## ✅ Current Status

**✅ Django Unfold Installed & Configured!**

Your admin panel now has:
- Modern Tailwind CSS design
- Material Design icons
- Custom navigation sidebar
- Organized sections for all your apps
- Professional color scheme
- Responsive layout

**Go check it out**: http://localhost:8000/admin/

Login and see the difference! 🚀
