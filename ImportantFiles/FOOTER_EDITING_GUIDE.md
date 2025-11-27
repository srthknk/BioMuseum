# Footer Editing Guide - BioMuseum

This guide explains how to customize and edit the footer section on the BioMuseum homepage.

---

## Table of Contents
1. [Footer Structure](#footer-structure)
2. [Editing Footer Content](#editing-footer-content)
3. [Changing Footer Colors](#changing-footer-colors)
4. [Customizing Sections](#customizing-sections)
5. [Adding Social Media Links](#adding-social-media-links)
6. [Responsive Design](#responsive-design)
7. [Quick Reference](#quick-reference)

---

## Footer Structure

The footer is divided into 3 main sections:

```
┌─────────────────────────────────────────────┐
│  BioMuseum    │  Quick Links  │  Contact   │
│  Description  │  - Home       │  - Email   │
│               │  - QR Scanner │  - Phone   │
│               │  - Admin      │  - Location│
├─────────────────────────────────────────────┤
│  © 2025 Copyright  │  Privacy | Terms       │
└─────────────────────────────────────────────┘
```

---

## Editing Footer Content

### File Location
**File**: `frontend/src/App.js`

**Search for**: `{/* Footer */}` (around line 181)

### Finding the Footer Code

```javascript
{/* Footer */}
<footer className="bg-gray-800 text-white mt-16">
  <div className="max-w-7xl mx-auto px-4 py-12">
    {/* Three columns content */}
  </div>
</footer>
```

---

## Changing Footer Information

### 1. Change Company Name & Description

**Find this section**:
```javascript
{/* About Section */}
<div>
  <h3 className="text-2xl font-bold mb-4">🧬 BioMuseum</h3>
  <p className="text-gray-300 text-sm">
    Discover the wonders of life science through our interactive biology museum. 
    Learn about diverse organisms and their fascinating characteristics.
  </p>
</div>
```

**To edit**:
- Replace `🧬 BioMuseum` with your organization name
- Update the description paragraph with your content

**Example**:
```javascript
<h3 className="text-2xl font-bold mb-4">🔬 Natural History Museum</h3>
<p className="text-gray-300 text-sm">
  Your museum description goes here...
</p>
```

### 2. Change Contact Information

**Find this section**:
```javascript
{/* Contact Info */}
<div>
  <h4 className="text-lg font-semibold mb-4">Contact & Social</h4>
  <ul className="space-y-2 text-gray-300 text-sm">
    <li>📧 Email: info@biomuseum.com</li>
    <li>📱 Phone: +1 (555) 123-4567</li>
    <li>📍 Location: Biology Department, Museum Street</li>
  </ul>
</div>
```

**To edit**:
- Update email address
- Update phone number
- Update location

**Example**:
```javascript
<li>📧 Email: contact@yourmuseum.org</li>
<li>📱 Phone: +1 (555) 987-6543</li>
<li>📍 Location: 123 Science Ave, New York, NY 10001</li>
```

### 3. Change Copyright Year & Company

**Find this section**:
```javascript
<p className="text-gray-400 text-sm">
  © 2025 BioMuseum. All rights reserved.
</p>
```

**To edit**:
```javascript
<p className="text-gray-400 text-sm">
  © 2025 Your Company Name. All rights reserved.
</p>
```

### 4. Update Privacy & Terms Links

**Find this section**:
```javascript
<div className="text-right text-gray-400 text-sm">
  <a href="#" className="hover:text-green-400 mr-4">Privacy Policy</a>
  <a href="#" className="hover:text-green-400">Terms of Service</a>
</div>
```

**To update links**:
```javascript
<a href="https://yoursite.com/privacy" className="hover:text-green-400 mr-4">Privacy Policy</a>
<a href="https://yoursite.com/terms" className="hover:text-green-400">Terms of Service</a>
```

---

## Changing Footer Colors

### Current Color Scheme
- Background: `bg-gray-800` (dark gray)
- Text: `text-white` (white)
- Hover: `hover:text-green-400` (green on hover)
- Divider: `border-gray-700` (gray border)

### Change Background Color

**Find**: `<footer className="bg-gray-800 text-white mt-16">`

**Change to**:
```javascript
<footer className="bg-blue-800 text-white mt-16">     {/* Dark blue */}
<footer className="bg-green-800 text-white mt-16">    {/* Dark green */}
<footer className="bg-purple-800 text-white mt-16">  {/* Dark purple */}
<footer className="bg-black text-white mt-16">       {/* Black */}
```

### Change Hover Link Color

**Find**: All instances of `hover:text-green-400`

**Change to**:
```javascript
hover:text-blue-400    {/* Blue on hover */}
hover:text-yellow-400  {/* Yellow on hover */}
hover:text-red-400     {/* Red on hover */}
```

### Example: Change to Blue Theme
```javascript
<footer className="bg-blue-800 text-white mt-16">
  {/* ... */}
  <a href="/" className="hover:text-blue-300 transition-colors">🏠 Home</a>
  {/* ... */}
</footer>
```

---

## Customizing Sections

### Change "Quick Links" Section

**Current**:
```javascript
<div>
  <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
  <ul className="space-y-2 text-gray-300 text-sm">
    <li><a href="/" className="hover:text-green-400 transition-colors">🏠 Home</a></li>
    <li><a href="/scanner" className="hover:text-green-400 transition-colors">📱 QR Scanner</a></li>
    <li><a onClick={() => setShowAdminLogin(true)} className="hover:text-green-400 transition-colors cursor-pointer">🔐 Admin Panel</a></li>
  </ul>
</div>
```

**To add more links**:
```javascript
<li><a href="/about" className="hover:text-green-400 transition-colors">ℹ️ About Us</a></li>
<li><a href="/gallery" className="hover:text-green-400 transition-colors">🖼️ Gallery</a></li>
<li><a href="/contact" className="hover:text-green-400 transition-colors">✉️ Contact</a></li>
```

### Change "Contact & Social" to "Newsletter"

```javascript
{/* Newsletter Signup */}
<div>
  <h4 className="text-lg font-semibold mb-4">Newsletter</h4>
  <p className="text-gray-300 text-sm mb-3">Subscribe to our updates</p>
  <div className="flex">
    <input 
      type="email" 
      placeholder="Your email" 
      className="flex-1 px-3 py-2 rounded-l text-black"
    />
    <button className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-r transition-colors">
      Subscribe
    </button>
  </div>
</div>
```

---

## Adding Social Media Links

### Add Social Media Section

Replace the Contact Info section with:

```javascript
{/* Social Media */}
<div>
  <h4 className="text-lg font-semibold mb-4">Follow Us</h4>
  <div className="flex gap-4 text-2xl">
    <a href="https://facebook.com/biomuseum" className="hover:text-blue-400 transition-colors">f</a>
    <a href="https://twitter.com/biomuseum" className="hover:text-blue-400 transition-colors">𝕏</a>
    <a href="https://instagram.com/biomuseum" className="hover:text-pink-400 transition-colors">📷</a>
    <a href="https://youtube.com/biomuseum" className="hover:text-red-400 transition-colors">▶️</a>
    <a href="https://linkedin.com/company/biomuseum" className="hover:text-blue-600 transition-colors">in</a>
  </div>
  <p className="text-gray-300 text-sm mt-4">
    📧 Email: info@biomuseum.com<br/>
    📱 Phone: +1 (555) 123-4567
  </p>
</div>
```

---

## Responsive Design

### How the Footer Responds

- **Mobile** (1 column): All sections stack vertically
- **Tablet** (md: 3 columns): 3 columns side by side
- **Desktop** (md: up): Full 3-column layout

**CSS Class**: `grid grid-cols-1 md:grid-cols-3`

### To Change Columns

**Current** (3 columns on desktop):
```javascript
<div className="grid grid-cols-1 md:grid-cols-3 gap-8">
```

**Change to 2 columns**:
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 gap-8">
```

**Change to 4 columns**:
```javascript
<div className="grid grid-cols-1 md:grid-cols-4 gap-8">
```

---

## Quick Reference: Common Edits

| What | File | Search For | Change |
|------|------|-----------|--------|
| Company Name | App.js | `🧬 BioMuseum` | Your name |
| Email | App.js | `info@biomuseum.com` | Your email |
| Phone | App.js | `+1 (555) 123-4567` | Your phone |
| Background Color | App.js | `bg-gray-800` | `bg-blue-800` |
| Hover Color | App.js | `hover:text-green-400` | `hover:text-blue-400` |
| Copyright Year | App.js | `© 2025` | Current year |
| Copyright Name | App.js | `BioMuseum` | Your company |

---

## Step-by-Step Examples

### Example 1: Change to Your Organization

1. Open `frontend/src/App.js`
2. Find `{/* Footer */}` section
3. Change:
   - Title: `🧬 BioMuseum` → `🏛️ Your Museum`
   - Description: Update text
   - Email: Update to your email
   - Phone: Update to your phone
   - Location: Update to your address
   - Copyright: Update company name

4. Save and restart `npm start`

### Example 2: Add Newsletter Signup

1. Find the Contact Info section
2. Replace with Newsletter section (see above)
3. Add form submission handler in state if needed
4. Test on localhost:3000

### Example 3: Change to Blue & White Theme

1. Change: `bg-gray-800` → `bg-blue-900`
2. Change: All `hover:text-green-400` → `hover:text-blue-300`
3. Change: `border-gray-700` → `border-blue-700`
4. Keep: `text-white` for contrast

---

## Styling Guide

### Font Sizes
- `text-2xl`: Large titles (Company name)
- `text-lg`: Section headers
- `text-sm`: Body text

### Spacing
- `mb-4`: Margin bottom (space below)
- `py-12`: Padding top & bottom
- `px-4`: Padding left & right
- `gap-8`: Space between columns

### Hover Effects
- Add: `transition-colors` for smooth hover
- Example: `hover:text-green-400 transition-colors`

---

## Testing Your Changes

1. **Save the file**: `Ctrl+S`
2. **Dev server reloads**: Auto-refresh in browser
3. **Check footer**: Scroll to bottom of homepage
4. **Test links**: Click to verify they work
5. **Test hover**: Mouse over links to see effects
6. **Test mobile**: Use DevTools (F12) to check responsive design

---

## Troubleshooting

### Footer Not Showing?
- Make sure closing `</footer>` tag is present
- Check that it's inside the main component
- Clear browser cache (Ctrl+Shift+Delete)

### Colors Not Changing?
- Verify exact Tailwind class name spelling
- Example: `gray-800` not `gray800`
- Restart dev server after changes

### Links Not Working?
- Check URL format: `href="/"` or `href="https://..."`
- For internal routes: use `navigate()` or `href="/"`
- For external: use full URL with `https://`

### Mobile Footer Broken?
- Check `grid-cols-1 md:grid-cols-3` classes
- Verify spacing classes are correct
- Test with DevTools responsive mode

---

## Advanced: Custom Footer Component

To make footer reusable, create a separate component:

**File**: `frontend/src/components/Footer.js`

```javascript
export const Footer = ({ organizationName, email, phone, location }) => {
  return (
    <footer className="bg-gray-800 text-white mt-16">
      {/* Footer content */}
    </footer>
  );
};
```

Then use in App.js:
```javascript
<Footer 
  organizationName="BioMuseum"
  email="info@biomuseum.com"
  phone="+1 (555) 123-4567"
  location="Museum Street"
/>
```

---

## Live Preview

After editing:
1. Homepage footer appears at bottom
2. All 3 columns visible on desktop
3. Stacks to 1 column on mobile
4. Links are clickable
5. Hover effects work smoothly

---

**Last Updated**: November 26, 2025
**Compatible with**: React 18+, Tailwind CSS
