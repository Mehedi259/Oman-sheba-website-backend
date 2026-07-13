#!/bin/bash

# ================================================
# Sheba Backend - Migration & Setup Script
# ================================================

echo "🚀 Starting Sheba Backend Migration & Setup..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success message
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print warning message
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to print error message
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    warning "Virtual environment not activated!"
    echo "Activating virtual environment..."
    source venv/bin/activate
    if [[ $? -ne 0 ]]; then
        error "Failed to activate virtual environment"
        echo "Please run: source venv/bin/activate"
        exit 1
    fi
    success "Virtual environment activated"
fi

echo ""
echo "📋 Step 1: Checking dependencies..."
echo ""

# Check if Django is installed
python -c "import django" 2>/dev/null
if [[ $? -ne 0 ]]; then
    error "Django not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [[ $? -ne 0 ]]; then
        error "Failed to install dependencies"
        exit 1
    fi
    success "Dependencies installed"
else
    success "Django is installed"
fi

echo ""
echo "💾 Step 2: Creating database backup..."
echo ""

# Backup database if exists
if [[ -f "db.sqlite3" ]]; then
    BACKUP_NAME="db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    cp db.sqlite3 "$BACKUP_NAME"
    success "Database backed up to $BACKUP_NAME"
else
    warning "No existing database found (fresh installation)"
fi

echo ""
echo "🗂️  Step 3: Creating migrations..."
echo ""

# Create migrations for each app
apps=("users" "classifieds" "community" "news" "emergency" "system")

for app in "${apps[@]}"; do
    echo "Creating migrations for $app..."
    python manage.py makemigrations $app
    if [[ $? -ne 0 ]]; then
        error "Failed to create migrations for $app"
        exit 1
    fi
    success "Migrations created for $app"
done

echo ""
echo "🚀 Step 4: Applying migrations..."
echo ""

# Apply migrations
python manage.py migrate
if [[ $? -ne 0 ]]; then
    error "Failed to apply migrations"
    echo "Check the errors above and fix them"
    exit 1
fi
success "All migrations applied successfully"

echo ""
echo "📦 Step 5: Collecting static files..."
echo ""

# Collect static files
python manage.py collectstatic --noinput
if [[ $? -ne 0 ]]; then
    warning "Failed to collect static files (non-critical)"
else
    success "Static files collected"
fi

echo ""
echo "👤 Step 6: Creating superuser..."
echo ""

# Check if superuser exists
echo "from users.models import User; print(User.objects.filter(is_superuser=True).exists())" | python manage.py shell > /tmp/superuser_check.txt
SUPERUSER_EXISTS=$(cat /tmp/superuser_check.txt | grep "True")

if [[ -z "$SUPERUSER_EXISTS" ]]; then
    warning "No superuser found"
    echo "Would you like to create a superuser now? (y/n)"
    read -r response
    if [[ "$response" == "y" ]] || [[ "$response" == "Y" ]]; then
        python manage.py createsuperuser
        if [[ $? -eq 0 ]]; then
            success "Superuser created"
        fi
    else
        warning "Skipped superuser creation"
    fi
else
    success "Superuser already exists"
fi

echo ""
echo "🏗️  Step 7: Creating initial data..."
echo ""

# Create initial data using Django shell
python manage.py shell <<EOF
from classifieds.models import JobCategory, ServiceCategory
from community.models import ForumCategory, ClassifiedCategory
from news.models import ArticleCategory, ArticleType

# Create Job Categories
job_categories = [
    {'name': 'Engineering', 'name_bn': 'প্রকৌশল', 'slug': 'engineering', 'icon': '⚙️'},
    {'name': 'Healthcare', 'name_bn': 'স্বাস্থ্যসেবা', 'slug': 'healthcare', 'icon': '🏥'},
    {'name': 'Education', 'name_bn': 'শিক্ষা', 'slug': 'education', 'icon': '📚'},
    {'name': 'IT & Software', 'name_bn': 'আইটি ও সফটওয়্যার', 'slug': 'it-software', 'icon': '💻'},
    {'name': 'Sales & Marketing', 'name_bn': 'বিক্রয় ও বিপণন', 'slug': 'sales-marketing', 'icon': '📊'},
]

for cat in job_categories:
    JobCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults=cat
    )

# Create Service Categories
service_categories = [
    {'name': 'Medical Services', 'name_bn': 'চিকিৎসা সেবা', 'slug': 'medical', 'icon': '⚕️', 'featured': True},
    {'name': 'Visa Services', 'name_bn': 'ভিসা সেবা', 'slug': 'visa', 'icon': '🛂', 'featured': True},
    {'name': 'Travel Agency', 'name_bn': 'ট্রাভেল এজেন্সি', 'slug': 'travel', 'icon': '✈️', 'featured': True},
    {'name': 'Legal Services', 'name_bn': 'আইনি সেবা', 'slug': 'legal', 'icon': '⚖️'},
    {'name': 'Educational Institutions', 'name_bn': 'শিক্ষা প্রতিষ্ঠান', 'slug': 'education', 'icon': '🎓'},
]

for cat in service_categories:
    ServiceCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults=cat
    )

# Create Forum Categories
forum_categories = [
    {'name': 'General Discussion', 'name_bn': 'সাধারণ আলোচনা', 'slug': 'general', 'icon': '💬'},
    {'name': 'Jobs & Career', 'name_bn': 'চাকরি ও ক্যারিয়ার', 'slug': 'jobs-career', 'icon': '💼'},
    {'name': 'Housing', 'name_bn': 'বাসস্থান', 'slug': 'housing', 'icon': '🏠'},
    {'name': 'Help & Support', 'name_bn': 'সাহায্য ও সহায়তা', 'slug': 'help-support', 'icon': '🤝'},
]

for cat in forum_categories:
    ForumCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults=cat
    )

# Create Classified Categories
classified_categories = [
    {'name': 'Electronics', 'name_bn': 'ইলেকট্রনিক্স', 'slug': 'electronics', 'icon': '📱'},
    {'name': 'Furniture', 'name_bn': 'ফার্নিচার', 'slug': 'furniture', 'icon': '🪑'},
    {'name': 'Clothing', 'name_bn': 'পোশাক', 'slug': 'clothing', 'icon': '👔'},
    {'name': 'Books', 'name_bn': 'বই', 'slug': 'books', 'icon': '📖'},
]

for cat in classified_categories:
    ClassifiedCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults=cat
    )

# Create Article Categories
article_categories = [
    {'name': 'Local News', 'name_bn': 'স্থানীয় সংবাদ', 'slug': 'local-news', 'type': ArticleType.NEWS},
    {'name': 'National News', 'name_bn': 'জাতীয় সংবাদ', 'slug': 'national-news', 'type': ArticleType.NEWS},
    {'name': 'Community', 'name_bn': 'কমিউনিটি', 'slug': 'community', 'type': ArticleType.NEWS},
    {'name': 'Announcements', 'name_bn': 'ঘোষণা', 'slug': 'announcements', 'type': ArticleType.ANNOUNCEMENT},
]

for cat in article_categories:
    ArticleCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults=cat
    )

print("✅ Initial data created successfully!")
EOF

if [[ $? -eq 0 ]]; then
    success "Initial data created"
else
    warning "Failed to create initial data (non-critical)"
fi

echo ""
echo "🧪 Step 8: Running system checks..."
echo ""

# Run Django system check
python manage.py check
if [[ $? -eq 0 ]]; then
    success "System check passed"
else
    error "System check failed"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════"
echo ""
success "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Start development server:"
echo "     python manage.py runserver"
echo ""
echo "  2. Access admin panel:"
echo "     http://localhost:8000/admin/"
echo ""
echo "  3. Access API:"
echo "     http://localhost:8000/api/"
echo ""
echo "  4. API Documentation:"
echo "     http://localhost:8000/swagger/"
echo ""
echo "  5. Before deploying to production:"
echo "     - Read DEPLOYMENT_GUIDE.md"
echo "     - Update environment variables"
echo "     - Setup PostgreSQL"
echo "     - Configure domain & SSL"
echo ""
echo "═══════════════════════════════════════════════"
echo ""
