# 🤖 AI Assistant Guide - BioMuseum

## Overview

The AI Assistant is an intelligent feature integrated into the **Add New Organism** admin panel that auto-fills organism information using a combination of:
- Built-in organism database (pre-populated with 5 core organisms)
- Wikipedia API for additional information
- Image fetching capabilities
- Smart data prediction and validation

## Features

### 1. **One-Click Organism Search**
Enter the name of any organism and the AI Assistant will:
- Search the internal database
- Generate relevant taxonomic classification
- Provide detailed descriptions of morphology, physiology, and general information
- Suggest images from free image sources

### 2. **Pre-populated Database**
The following organisms are included with complete, accurate data:
- 🦁 **Lion** (Panthera leo)
- 🐘 **African Elephant** (Loxodonta africana)
- 🐯 **Tiger** (Panthera tigris)
- 🐬 **Bottlenose Dolphin** (Tursiops truncatus)
- 🐧 **Emperor Penguin** (Aptenodytes forsteri)

### 3. **Intelligent Form Auto-Fill**
When you select AI-generated data:
- Common name is auto-filled
- Scientific name is populated
- Taxonomic classification (Kingdom, Phylum, Class, Order, Family, Genus, Species) is auto-filled
- Detailed descriptions (Morphology, Physiology, General Description) are inserted
- Images are automatically added to the form

### 4. **Image Selection**
The AI Assistant displays multiple image options. You can:
- Preview images before selection
- Choose the best image for your organism
- See image attribution and photographer credits
- Upload additional images manually if needed

## How to Use

### Step 1: Navigate to Add Organism Tab
1. Go to the Admin Panel (lock icon in navbar)
2. Click **➕ Add Organism** tab
3. You'll see the "🤖 AI Assistant" button in the top right

### Step 2: Launch AI Assistant
Click the **🤖 AI Assistant** button to open the modal

### Step 3: Enter Organism Name
1. Type the name of the organism (e.g., "Lion", "Tiger", "Dolphin")
2. Press **Enter** or click the **✨ Generate** button

### Step 4: Review Generated Data
The AI Assistant will display:
- **📋 Organism Data** section with all taxonomic information
- **🖼️ Select Image** gallery with multiple options
- A note explaining that AI data is a suggestion

### Step 5: Select Image (Optional)
1. Click on an image to select it
2. The selected image will show a blue border and glow effect
3. View the photographer attribution at the bottom

### Step 6: Apply Data to Form
Click the **✅ Use This Data** button to:
- Auto-fill all organism information into the main form
- Close the AI Assistant modal
- Return to the form for any manual edits

### Step 7: Review and Edit (Important!)
- **Always review** the auto-filled data for accuracy
- Edit any fields as needed
- You can modify:
  - Species names
  - Classification details
  - Descriptions and morphology
  - Images

### Step 8: Submit
Click **✅ Add Organism** to save to the database

## Built-in Organisms Database

### 1. Lion (Panthera leo)
```
Scientific Name: Panthera leo
Kingdom: Animalia | Phylum: Chordata | Class: Mammalia
Order: Carnivora | Family: Felidae | Genus: Panthera
```
- **Morphology**: Largest carnivorous land mammals, males with distinctive manes
- **Physiology**: Apex predators, can roar 114 decibels, sleep 16-20 hours daily
- **Status**: Vulnerable

### 2. African Elephant (Loxodonta africana)
```
Scientific Name: Loxodonta africana
Kingdom: Animalia | Phylum: Chordata | Class: Mammalia
Order: Proboscidea | Family: Elephantidae
```
- **Morphology**: Largest land animal, 3-4m tall, weighing 4,000-7,000kg
- **Physiology**: Herbivorous, exceptional memory, 40,000 muscles in trunk
- **Status**: Vulnerable

### 3. Tiger (Panthera tigris)
```
Scientific Name: Panthera tigris
Kingdom: Animalia | Phylum: Chordata | Class: Mammalia
Order: Carnivora | Family: Felidae
```
- **Morphology**: Largest felids, 90-300kg, distinctive orange coat with stripes
- **Physiology**: Solitary hunters, 5-10% success rate, can eat 30kg in one meal
- **Status**: Critically Endangered (~3,900 remain)

### 4. Bottlenose Dolphin (Tursiops truncatus)
```
Scientific Name: Tursiops truncatus
Kingdom: Animalia | Phylum: Chordata | Class: Mammalia
Order: Cetacea | Family: Delphinidae
```
- **Morphology**: 2-4m length, 150-650kg, robust body with curved dorsal fin
- **Physiology**: Highly intelligent, use echolocation, live 40-50 years
- **Status**: Least Concern

### 5. Emperor Penguin (Aptenodytes forsteri)
```
Scientific Name: Aptenodytes forsteri
Kingdom: Animalia | Phylum: Chordata | Class: Aves
Order: Sphenisciformes | Family: Spheniscidae
```
- **Morphology**: 1.1-1.3m tall, 23-45kg, dense feathers for insulation
- **Physiology**: Flightless, dive to 500m, hold breath 20+ minutes
- **Status**: Near Threatened

## Adding New Organisms (Not in Database)

If you enter an organism not in the built-in database:
1. The AI Assistant shows a **template** with placeholders
2. Fill in the details manually
3. The form guide provides helpful hints for each field
4. Click **✅ Use This Data** to apply the template

Example message:
```
"Lion not in database. Showing template to fill manually. 
Feel free to add the details!"
```

## Customizing the Database

### To Add More Organisms:

Edit `/frontend/src/services/aiService.js`:

```javascript
const ORGANISM_DATABASE = {
  // Existing organisms...
  
  // Add your new organism here:
  "giraffe": {
    name: 'Giraffe',
    scientific_name: 'Giraffa camelopardalis',
    kingdom: 'Animalia',
    phylum: 'Chordata',
    class: 'Mammalia',
    order: 'Artiodactyla',
    family: 'Giraffidae',
    genus: 'Giraffa',
    species: 'G. camelopardalis',
    morphology: 'Tallest land animal...',
    physiology: 'Herbivorous, feed on acacia...',
    description: 'The giraffe is an African artiodactyl...'
  }
};
```

### Steps:
1. Open `frontend/src/services/aiService.js`
2. Find the `ORGANISM_DATABASE` object
3. Add a new entry with the organism's common name (lowercase) as the key
4. Fill in all required fields:
   - `name`: Common name (capitalized)
   - `scientific_name`: Latin binomial name (italicized)
   - Classification fields (kingdom through species)
   - `morphology`: 1-2 paragraph description of physical structure
   - `physiology`: 1-2 paragraph description of biology and behavior
   - `description`: 1-2 paragraph general description and facts

### Example Template:
```javascript
"organism_name": {
  name: 'Common Name',
  scientific_name: 'Genus species',
  kingdom: 'Animalia',
  phylum: 'Chordata',
  class: 'Mammalia',
  order: 'Order Name',
  family: 'Family Name',
  genus: 'Genus',
  species: 'S. species',
  morphology: 'Physical description...',
  physiology: 'Biological functions...',
  description: 'General information...'
}
```

## API Integrations

### 1. Wikipedia API
- **Used for**: Additional organism information retrieval
- **Endpoint**: `https://en.wikipedia.org/api/rest_v1/page/summary/[organism_name]`
- **Status**: Optional (fallback to database)
- **Cost**: Free

### 2. Unsplash API
- **Used for**: Animal image search and retrieval
- **Endpoint**: `https://api.unsplash.com/search/photos`
- **Status**: Optional (manual upload still available)
- **Cost**: Free for development (requires API key for production)
- **How to Add Key**:
  ```javascript
  // In aiService.js, replace:
  const UNSPLASH_KEY = 'YOUR_UNSPLASH_KEY';
  // With your actual Unsplash API key from: https://unsplash.com/api
  ```

## Error Handling

### No Organism Found
```
⚠️ Error: [organism_name] not in database. Showing template to fill manually.
```
**Solution**: Fill in the template fields manually

### Image Fetch Failed
```
Could not fetch images. You can upload manually.
```
**Solution**: Upload images using the drag-and-drop area below

### Network Error
```
An error occurred. Please try again.
```
**Solution**: Check internet connection and retry

## Tips for Best Results

1. **Use Common Names**: Use the English common name (e.g., "Tiger" not "Panthera tigris")
2. **Verify Information**: Always review AI-generated data for accuracy
3. **Edit as Needed**: Don't hesitate to modify descriptions and classifications
4. **Add Images**: Include high-quality images for better user experience
5. **Check Spelling**: Ensure organism names are spelled correctly

## Limitations & Future Improvements

### Current Limitations:
- ✗ Limited to 5 pre-built organisms
- ✗ No real-time AI API (using template/database only)
- ✗ Images depend on API availability
- ✗ No multilingual support

### Planned Improvements:
- ✓ Integration with real AI APIs (GPT-4, Gemini)
- ✓ Extended organism database (100+ species)
- ✓ Automatic taxonomy lookup from NCBI
- ✓ Multi-language support
- ✓ Advanced image recognition
- ✓ Citation and reference integration
- ✓ Biodiversity data feeds

## Technical Details

### Component Structure:
```
App.js
├── AddOrganismForm
│   ├── AI Assistant Button
│   └── AIAssistant Modal (conditional render)
├── AIAssistant.jsx (Modal Component)
└── aiService.js (Data Logic)
```

### Key Files:
- **Frontend**: `src/components/AIAssistant.jsx`
- **Services**: `src/services/aiService.js`
- **Main App**: `src/App.js` (AddOrganismForm component)

### State Management:
- `showAIAssistant`: Boolean to show/hide modal
- `generatedData`: Organism data from AI service
- `selectedImage`: Currently selected image
- `loading`: Loading state during API calls

### API Calls:
```javascript
generateOrganismData(animalName)  // Main AI function
fetchOrganismImages(animalName)   // Image search
fetchWikipediaInfo(animalName)    // Additional info
```

## Support & Troubleshooting

### Q: The AI Assistant button doesn't appear?
**A**: Make sure you're in the "➕ Add Organism" tab of the Admin Panel

### Q: Data isn't being filled in the form?
**A**: Click "✅ Use This Data" button after reviewing the generated information

### Q: Images aren't loading?
**A**: This is normal if the Unsplash API key isn't configured. You can still upload images manually.

### Q: Can I delete data after using AI Assistant?
**A**: Yes! Click the "Clear" button to reset the AI Assistant, or edit individual form fields

### Q: How do I report incorrect organism data?
**A**: Edit the organism entry in the database and update the information in `aiService.js`

## Contributing

Want to add more organisms to the database? Follow these steps:

1. Research the organism thoroughly (use scientific sources)
2. Edit `frontend/src/services/aiService.js`
3. Add the new organism following the template format
4. Test the AI Assistant with the new organism name
5. Verify all information is accurate

For open-source contributions, please submit a pull request with:
- New organism entries
- Accurate taxonomic information
- Detailed morphology and physiology descriptions
- References and sources

---

**Last Updated**: 2024  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
