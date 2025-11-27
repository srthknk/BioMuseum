# Legal Documents Integration Guide

This guide explains how to integrate the Privacy Policy and Terms of Service into your BioMuseum website.

---

## Files Created

1. **PRIVACY_POLICY.md** - Privacy Policy document
2. **TERMS_OF_SERVICE.md** - Terms of Service document
3. **LEGAL_DOCUMENTS_INTEGRATION_GUIDE.md** - This integration guide

---

## Option 1: Simple Approach (Current Setup)

### Current Footer Links

In `frontend/src/App.js`, the footer already has links:

```javascript
<a href="#" className="hover:text-green-400">Privacy Policy</a>
<a href="#" className="hover:text-green-400">Terms of Service</a>
```

### Step 1: Update Links

Replace the empty `href="#"` with actual links:

**Find**:
```javascript
<a href="#" className="hover:text-green-400 mr-4">Privacy Policy</a>
<a href="#" className="hover:text-green-400">Terms of Service</a>
```

**Replace with**:
```javascript
<a href="https://yoursite.com/privacy" className="hover:text-green-400 mr-4">Privacy Policy</a>
<a href="https://yoursite.com/terms" className="hover:text-green-400">Terms of Service</a>
```

### Step 2: Host the Documents

**Option A: External Hosting**
- Upload `.md` files to a document hosting service
- Services: GitHub Pages, GitBook, Notion, Wiki.js
- Get public URLs and use them

**Option B: Simple HTML**
- Convert markdown to HTML
- Host on your server
- Link to HTML versions

---

## Option 2: Create Legal Pages in React (Recommended)

### Step 1: Create Legal Components

**File**: `frontend/src/components/PrivacyPolicy.jsx`

```javascript
import React from 'react';
import { useNavigate } from 'react-router-dom';

export const PrivacyPolicy = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <button
          onClick={() => navigate('/')}
          className="mb-6 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </button>

        <div className="bg-white rounded-xl shadow-lg p-8 prose prose-sm max-w-none">
          <h1>Privacy Policy</h1>
          <p><strong>Last Updated:</strong> November 26, 2025</p>

          <h2>1. Introduction</h2>
          <p>BioMuseum ("we," "our," "us," or "Company") is committed to protecting your privacy...</p>

          {/* Copy all content from PRIVACY_POLICY.md here as JSX */}
          {/* Or use markdown-to-jsx library for dynamic rendering */}
        </div>
      </div>
    </div>
  );
};
```

### Step 2: Create Terms Component

**File**: `frontend/src/components/TermsOfService.jsx`

```javascript
import React from 'react';
import { useNavigate } from 'react-router-dom';

export const TermsOfService = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <button
          onClick={() => navigate('/')}
          className="mb-6 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </button>

        <div className="bg-white rounded-xl shadow-lg p-8 prose prose-sm max-w-none">
          <h1>Terms of Service</h1>
          <p><strong>Last Updated:</strong> November 26, 2025</p>

          {/* Copy all content from TERMS_OF_SERVICE.md here as JSX */}
        </div>
      </div>
    </div>
  );
};
```

### Step 3: Add Routes

**File**: `frontend/src/App.js`

Find the Routes section and add:

```javascript
<Route path="/privacy" element={<PrivacyPolicy />} />
<Route path="/terms" element={<TermsOfService />} />
```

### Step 4: Update Footer Links

**Find**:
```javascript
<a href="#" className="hover:text-green-400 mr-4">Privacy Policy</a>
<a href="#" className="hover:text-green-400">Terms of Service</a>
```

**Replace with**:
```javascript
<a href="/privacy" className="hover:text-green-400 mr-4">Privacy Policy</a>
<a href="/terms" className="hover:text-green-400">Terms of Service</a>
```

---

## Option 3: Using Markdown-to-JSX Library (Advanced)

### Install Package

```bash
npm install markdown-to-jsx
```

### Create Reusable Component

**File**: `frontend/src/components/LegalPage.jsx`

```javascript
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Markdown from 'markdown-to-jsx';

export const LegalPage = ({ title, content }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-blue-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <button
          onClick={() => navigate('/')}
          className="mb-6 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </button>

        <div className="bg-white rounded-xl shadow-lg p-8 prose prose-sm max-w-none">
          <Markdown>{content}</Markdown>
        </div>
      </div>
    </div>
  );
};
```

### Use in Routes

```javascript
import { PrivacyPolicy as PrivacyContent } from './path/to/PRIVACY_POLICY.md';
import { TermsOfService as TermsContent } from './path/to/TERMS_OF_SERVICE.md';

<Route path="/privacy" element={<LegalPage title="Privacy Policy" content={PrivacyContent} />} />
<Route path="/terms" element={<LegalPage title="Terms of Service" content={TermsContent} />} />
```

---

## Option 4: Use GitHub Raw Links (Simplest)

### Host on GitHub

1. Upload `.md` files to your GitHub repository
2. Get raw content URL:
   ```
   https://raw.githubusercontent.com/USERNAME/BioMuseum/main/PRIVACY_POLICY.md
   ```

### Create Simple Display Component

```javascript
import React, { useState, useEffect } from 'react';
import Markdown from 'markdown-to-jsx';

export const PrivacyPolicy = () => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://raw.githubusercontent.com/USERNAME/BioMuseum/main/PRIVACY_POLICY.md')
      .then(res => res.text())
      .then(data => {
        setContent(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Markdown>{content}</Markdown>
    </div>
  );
};
```

---

## Implementation Checklist

### Before Launch

- [ ] Choose integration method (Option 1-4)
- [ ] Set up routes/pages
- [ ] Update footer links
- [ ] Test links work
- [ ] Verify formatting looks good
- [ ] Check on mobile devices
- [ ] Verify content is accurate for your organization
- [ ] Update email addresses in documents
- [ ] Update company/location information
- [ ] Review for accuracy and compliance

### Customization Required

Edit both markdown files to:

1. **Email Addresses**
   - Change `privacy@biomuseum.com` → your email
   - Change `legal@biomuseum.com` → your email
   - Change `abuse@biomuseum.com` → your email

2. **Company Information**
   - Change company name to your organization
   - Update address/location
   - Update contact information

3. **Jurisdiction**
   - Update governing law (currently US)
   - Update state/country specific sections
   - Ensure GDPR/CCPA compliance for your region

4. **Services**
   - List your actual hosting providers
   - Update third-party integrations
   - Modify retention policies if needed

---

## Styling the Legal Pages

### Add Prose Styling

**File**: `frontend/src/App.css`

```css
.prose {
  max-width: 100%;
}

.prose h1 {
  color: #1f2937;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.prose h2 {
  color: #374151;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.prose h3 {
  color: #4b5563;
  margin-top: 1rem;
}

.prose p {
  color: #6b7280;
  line-height: 1.8;
}

.prose a {
  color: #10b981;
  text-decoration: none;
}

.prose a:hover {
  text-decoration: underline;
}

.prose ul, .prose ol {
  margin: 1rem 0;
  padding-left: 2rem;
}

.prose li {
  margin: 0.5rem 0;
}

.prose code {
  background: #f3f4f6;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.prose blockquote {
  border-left: 4px solid #10b981;
  padding-left: 1rem;
  margin-left: 0;
  color: #4b5563;
  font-style: italic;
}
```

---

## SEO Optimization

### Add Meta Tags

In `frontend/public/index.html`:

```html
<!-- Privacy Policy -->
<meta property="og:title" content="Privacy Policy - BioMuseum" />
<meta property="og:description" content="Learn how BioMuseum protects your privacy" />

<!-- Terms of Service -->
<meta property="og:title" content="Terms of Service - BioMuseum" />
<meta property="og:description" content="Review our terms and conditions" />
```

### Add to Sitemap

If using a sitemap (sitemap.xml):

```xml
<url>
  <loc>https://biomuseum.com/privacy</loc>
  <changefreq>yearly</changefreq>
</url>
<url>
  <loc>https://biomuseum.com/terms</loc>
  <changefreq>yearly</changefreq>
</url>
```

---

## Compliance Notes

### GDPR Compliance (EU)

- ✅ Privacy Policy addresses GDPR requirements
- ✅ Data processing basis explained
- ✅ User rights documented
- ✅ Consent mechanisms available
- ⚠️ Review for specific EU requirements

### CCPA Compliance (California)

- ✅ Privacy Policy includes CCPA sections
- ✅ Consumer rights explained
- ✅ Data sale opt-out addressed
- ⚠️ Customize for your specific business model

### COPPA Compliance (Children)

- ✅ Privacy Policy addresses COPPA
- ✅ Parental consent provisions included
- ⚠️ Implement age verification if needed

### FERPA Compliance (Education)

- ✅ Terms acknowledge educational use
- ✅ Student privacy protected
- ⚠️ Add institutional agreements if needed

---

## Maintenance

### Annual Review

- Review and update annually
- Check compliance with new laws
- Update contact information
- Verify accuracy of practices

### Significant Changes

- Update policy when practices change
- Notify users of material changes
- Maintain change log/version history
- Get legal review for major updates

### Version Control

```markdown
## Version History

**v1.0** - November 26, 2025
- Initial policy creation
- Privacy Policy established
- Terms of Service established
```

---

## Legal Review

### Highly Recommended

While these templates are comprehensive, consider:
- Consulting with a lawyer in your jurisdiction
- Getting specific legal review before launch
- Ensuring compliance with local laws
- Customizing for your specific use case
- Reviewing annually with legal counsel

### Cost Estimate

- Legal review: $500-$2000
- Worth the investment for compliance assurance
- Templates save time and provide structure

---

## Support & Questions

For questions about implementation:

1. Review the Markdown files
2. Check this guide
3. Consult legal resources
4. Consider legal counsel

---

**Last Updated**: November 26, 2025
**Status**: Ready for implementation
