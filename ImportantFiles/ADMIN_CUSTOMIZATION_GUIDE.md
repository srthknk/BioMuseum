# Admin Customization Guide - BioMuseum

This guide explains how administrators can customize the UI/UX, change username/password, and modify font styles in the BioMuseum application.

---

## Table of Contents
1. [Admin Login Credentials](#admin-login-credentials)
2. [Changing Admin Username & Password](#changing-admin-username--password)
3. [UI/UX Customization](#uiux-customization)
4. [Font Styles Customization](#font-styles-customization)
5. [Color Schemes](#color-schemes)
6. [Responsive Design Adjustments](#responsive-design-adjustments)

---

## Admin Login Credentials

### Default Credentials
- **Username**: `admin` (by default)
- **Password**: Check your backend configuration or `.env` file

### Where to Find
- **Backend File**: `backend/server.py`
- **Configuration**: Check environment variables or hardcoded credentials in the auth section

### How to Login
1. Go to the BioMuseum homepage
2. Click the **🔐 Admin** button in the top-right corner
3. Enter your username and password
4. Click **Login** to access the admin panel

---

## Changing Admin Username & Password

### Step 1: Access Backend Configuration
**File Location**: `backend/server.py`

### Step 2: Find Authentication Section
Look for the admin authentication logic in the backend. Search for:
```python
# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_password"
```

### Step 3: Update Credentials
Replace the default values with your new username and password:
```python
ADMIN_USERNAME = "your_new_username"
ADMIN_PASSWORD = "your_new_password"
```

### Step 4: Restart Backend Server
```bash
cd backend
python server.py
```

### Security Note
- Use strong passwords (mix of letters, numbers, and symbols)
- Change credentials regularly
- Never commit passwords to version control
- Use environment variables for sensitive data

---

## UI/UX Customization

### Main Files to Edit
1. **Frontend Components**: `frontend/src/App.js`
2. **Styling**: `frontend/src/App.css`
3. **UI Library Components**: `frontend/src/components/ui/`

### Homepage Organism Cards

**File**: `frontend/src/App.js` (Lines ~142-165)

**Current Grid Layout**:
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**To Change Number of Columns**:
- `grid-cols-1`: 1 column on mobile
- `md:grid-cols-2`: 2 columns on medium screens
- `lg:grid-cols-4`: 4 columns on large screens

**Example**: To show 3 columns on large screens instead of 4:
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

**Card Styling**:
```javascript
className="bg-white rounded-xl shadow-lg hover:shadow-xl border-2 hover:border-green-300"
```
- `bg-white`: Background color
- `rounded-xl`: Border radius (roundness)
- `shadow-lg`: Shadow depth
- `border-2 hover:border-green-300`: Border color on hover

### Admin Panel Colors

**File**: `frontend/src/App.js` (Search for "Admin Panel")

**Header Background**:
```javascript
className="bg-linear-to-br from-purple-50 to-blue-50"
```

**Button Colors**:
- `bg-green-600`: Green button (Add Organism)
- `bg-blue-600`: Blue button (Save/Update)
- `bg-red-600`: Red button (Delete)
- `bg-gray-600`: Gray button (Cancel/Back)

**To Change Colors**:
Replace color names:
- `green` → `blue`, `red`, `purple`, `yellow`, `pink`, etc.
- `600` → `500` (lighter) or `700` (darker)

### Example: Change "Add Organism" Button Color
Find this line:
```javascript
className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold"
```

Change to:
```javascript
className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold"
```

---

## Font Styles Customization

### Global Font Settings

**File**: `frontend/src/App.css`

**Default Font Stack**:
```css
.App {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
}
```

### How to Change Global Font

1. Open `frontend/src/App.css`
2. Find the `.App` selector
3. Replace the `font-family` with your desired font:

**Example: Using Google Fonts (Playfair Display)**
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

.App {
    font-family: 'Playfair Display', serif;
}
```

### Heading Font Sizes

**File**: `frontend/src/App.js` (Tailwind classes)

Common heading size classes:
- `text-lg`: 18px
- `text-xl`: 20px
- `text-2xl`: 24px
- `text-3xl`: 30px
- `text-4xl`: 36px

**Example**: To make organism names smaller
Find:
```javascript
<h3 className="text-xl font-bold">{organism.name}</h3>
```

Change to:
```javascript
<h3 className="text-lg font-bold">{organism.name}</h3>
```

### Font Weights

Tailwind font weight classes:
- `font-light`: 300
- `font-normal`: 400
- `font-semibold`: 600
- `font-bold`: 700

**Example**: Make scientific names bold
Find:
```javascript
<p className="text-sm text-gray-600 italic">{organism.scientific_name}</p>
```

Change to:
```javascript
<p className="text-sm text-gray-600 italic font-semibold">{organism.scientific_name}</p>
```

### Custom CSS for Fonts

**File**: `frontend/src/App.css`

Add custom font rules:
```css
/* Custom heading styles */
h1, h2, h3 {
    font-family: 'Your Font Name', sans-serif;
    letter-spacing: 0.05em;
    line-height: 1.2;
}

/* Scientific names styling */
.scientific-name {
    font-style: italic;
    font-weight: 600;
    letter-spacing: 0.02em;
}
```

---

## Color Schemes

### Available Tailwind Colors

**Primary Colors**:
- `green`: Used for buttons and highlights
- `blue`: Used for links and secondary buttons
- `red`: Used for delete/warning actions
- `gray`: Used for neutral elements

**Color Intensity** (100-900):
- `50`: Lightest
- `100`, `200`, `300`: Light
- `400`, `500`, `600`: Medium
- `700`, `800`, `900`: Dark

### Change Header Background

**File**: `frontend/src/App.js` (Homepage Header)

Find:
```javascript
className="bg-white shadow-lg border-b-4 border-green-600"
```

Change to any combination:
```javascript
className="bg-blue-50 shadow-lg border-b-4 border-blue-600"
```

### Change Search Button Color

Find:
```javascript
className="bg-green-600 hover:bg-green-700 text-white"
```

Change to:
```javascript
className="bg-purple-600 hover:bg-purple-700 text-white"
```

---

## Responsive Design Adjustments

### Breakpoints

**File**: `frontend/src/App.js` and `frontend/src/App.css`

Tailwind breakpoints:
- No prefix: Mobile (< 640px)
- `sm:`: Small (≥ 640px)
- `md:`: Medium (≥ 768px)
- `lg:`: Large (≥ 1024px)
- `xl:`: Extra Large (≥ 1280px)

### Example: Change Mobile Layout

**Current**:
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**To show 2 columns on mobile instead of 1**:
```javascript
<div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

### Adjust Spacing on Different Screens

**File**: `frontend/src/App.css`

```css
@media (max-width: 768px) {
    .card-padding {
        padding: 1rem;  /* Reduce padding on mobile */
    }
}

@media (min-width: 1024px) {
    .card-padding {
        padding: 2rem;  /* More padding on desktop */
    }
}
```

---

## Step-by-Step: Complete Customization Example

### Task: Make Admin Panel More Professional

1. **Change Button Colors to Blue**
   - File: `frontend/src/App.js`
   - Search: `bg-green-600`
   - Replace with: `bg-blue-600`

2. **Change Header Color to Dark**
   - Find: `from-purple-50 to-blue-50`
   - Replace with: `from-slate-800 to-slate-900`

3. **Increase Font Size for Headings**
   - Find: `text-3xl`
   - Replace with: `text-4xl`

4. **Update Card Border Color**
   - Find: `border-green-300`
   - Replace with: `border-blue-300`

5. **Restart Frontend**
   ```bash
   cd frontend
   npm start
   ```

---

## Quick Reference: Common Changes

| Change | File | Search For | Replace With |
|--------|------|-----------|--------------|
| Button color | App.js | `bg-green-600` | `bg-blue-600` |
| Card shadow | App.js | `shadow-lg` | `shadow-xl` |
| Text color | App.js | `text-gray-800` | `text-gray-900` |
| Border radius | App.js | `rounded-xl` | `rounded-lg` |
| Padding | App.js | `p-6` | `p-4` |
| Gap between items | App.js | `gap-6` | `gap-4` |

---

## Troubleshooting

### Changes Not Appearing?
1. **Clear browser cache**: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
2. **Restart dev server**: Stop and run `npm start` again
3. **Check for typos**: Ensure Tailwind class names are correct

### Need to Revert Changes?
1. Use Git: `git checkout frontend/src/App.js`
2. Or manually undo edits

### Want to Preview Changes?
1. Edit files
2. Save
3. Dev server auto-reloads
4. Check browser for live updates

---

## Support & Resources

- **Tailwind CSS**: https://tailwindcss.com/docs
- **React Documentation**: https://react.dev
- **Font Resources**: https://fonts.google.com

---

**Last Updated**: November 26, 2025
