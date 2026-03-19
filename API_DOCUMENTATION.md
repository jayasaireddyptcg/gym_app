# Backend API Documentation for Frontend Development

## API Endpoints & Schema

### Base URL: `http://localhost:8000`

---

## Authentication Routes (`/auth`)

### POST `/auth/register`
**Request Body:**
```typescript
interface UserCreate {
  email: string;
  password: string; // min 8 chars, 1 uppercase, 1 lowercase, 1 digit
  name: string; // min 2 chars, max 50 chars
  age?: number; // 13-120
  weight?: number; // 20-500 (kg/lbs)
  height?: number; // 50-300 (cm/inches)
  goal?: string; // max 200 chars
}
```

**Response:**
```typescript
{
  "success": true
}
```

### POST `/auth/login`
**Request Body:**
```typescript
interface UserLogin {
  email: string;
  password: string;
}
```

**Response:**
```typescript
{
  "access_token": string
}
```

---

## Food Routes (`/food`)

### POST `/food/scan` (Updated for File Upload)
**Headers:** `Authorization: Bearer <token>`

**Request:** `multipart/form-data`
- `file`: Image file (required)

**File Requirements:**
- Must be an image file (jpg, png, gif, etc.)
- Maximum file size: 10MB
- Content-Type must start with `image/`

**Success Response:**
```typescript
{
  "success": true,
  "data": {
    "items": [
      {
        "name": string,
        "quantity": number,
        "macros": {
          "calories": number,
          "protein": number,
          "carbs": number,
          "fat": number,
          "fiber": number,
          "sugar": number
        },
        "micronutrients": {
          "vitamins": {
            "vitamin_c": number,
            "vitamin_a": number,
            "vitamin_k": number,
            "vitamin_e": number,
            "thiamine": number,
            "riboflavin": number,
            "niacin": number,
            "vitamin_b6": number,
            "folate": number,
            "vitamin_b12": number
          },
          "minerals": {
            "calcium": number,
            "iron": number,
            "magnesium": number,
            "phosphorus": number,
            "potassium": number,
            "sodium": number,
            "zinc": number,
            "copper": number,
            "manganese": number,
            "selenium": number
          }
        }
      }
    ],
    "total": {
      "macros": {
        "calories": number,
        "protein": number,
        "carbs": number,
        "fat": number,
        "fiber": number,
        "sugar": number
      },
      "micronutrients": {
        "vitamins": { /* same structure as above */ },
        "minerals": { /* same structure as above */ }
      }
    },
    "warning"?: string // Only present if AI parsing had issues
  },
  "error": null
}
```

**Error Responses:**
```typescript
// INVALID_FILE
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_FILE",
    "message": "File must be an image"
  }
}

// FILE_TOO_LARGE
{
  "success": false,
  "data": null,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Image file must be less than 10MB"
  }
}

// AI_TIMEOUT
{
  "success": false,
  "data": null,
  "error": {
    "code": "AI_TIMEOUT",
    "message": "AI service unavailable"
  }
}

// NOT_FOOD
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOOD",
    "message": "Image does not contain valid food items"
  }
}

// DB_ERROR
{
  "success": false,
  "data": null,
  "error": {
    "code": "DB_ERROR",
    "message": "Failed to save data"
  }
}

// PROCESSING_ERROR
{
  "success": false,
  "data": null,
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "Failed to process image: [specific error]"
  }
}
```

### POST `/food/debug-image` (Updated for File Upload)
**Headers:** `Authorization: Bearer <token>`

**Request:** `multipart/form-data`
- `image_url`: string (optional) - for testing URL-based images
- `file`: Image file (optional) - for testing file uploads

**Note:** Provide either `image_url` OR `file`, not both.

**Response:**
```typescript
{
  "success": true,
  "data": {
    "url": string | null,
    "filename": string | null, // only for file uploads
    "method": "url" | "file_upload",
    "accessible": boolean,
    "content_type": string | null,
    "size_bytes": number | null,
    "ai_test": boolean,
    "error": string | null,
    "ai_response_preview"?: string,
    "ai_error"?: string
  }
}
```

---

## Frontend Implementation Examples

### File Upload Implementation

#### JavaScript/TypeScript Example:
```typescript
const scanFood = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/food/scan', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  const result = await response.json();
  return result;
};

// Usage
const fileInput = document.getElementById('file-input') as HTMLInputElement;
const file = fileInput.files[0];

if (file) {
  const result = await scanFood(file);
  if (result.success) {
    console.log('Food items detected:', result.data.items);
  } else {
    console.error('Error:', result.error.message);
  }
}
```

#### React Example:
```typescript
const FoodScan = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/food/scan', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.error.message);
      }
    } catch (err) {
      setError('Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileUpload} />
      {loading && <p>Processing image...</p>}
      {error && <p>Error: {error}</p>}
      {result && (
        <div>
          <h3>Detected Food Items:</h3>
          {result.items.map((item, index) => (
            <div key={index}>
              <h4>{item.name}</h4>
              <p>Calories: {item.macros.calories}</p>
              <p>Protein: {item.macros.protein}g</p>
              <p>Carbs: {item.macros.carbs}g</p>
              <p>Fat: {item.macros.fat}g</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## Database Schema

### Users Table
```sql
- id: UUID (primary key)
- email: string (unique)
- password: string (hashed)
- name: string
- age: integer (optional)
- weight: integer (optional)
- height: integer (optional)
- goal: string (optional)
```

### Food Scans Table
```sql
- id: UUID (primary key)
- user_id: UUID (foreign key to users)
- items: JSON (food items array)
- total_calories: integer
```

---

## AI Food Analysis Prompt (Backend Logic)

The backend uses this prompt for AI food analysis:

```
You are a food recognition and nutrition analysis system. Identify all food items in the image and provide comprehensive nutritional information.

Return ONLY valid JSON:
{
  "items": [
    {
      "name": "apple",
      "quantity": 1,
      "macros": {
        "calories": 95,
        "protein": 0.5,
        "carbs": 25,
        "fat": 0.3,
        "fiber": 4.4,
        "sugar": 19
      },
      "micronutrients": {
        "vitamins": {
          "vitamin_c": 8.4,
          "vitamin_a": 98,
          "vitamin_k": 4,
          "vitamin_e": 0.5,
          "thiamine": 0.03,
          "riboflavin": 0.06,
          "niacin": 0.2,
          "vitamin_b6": 0.08,
          "folate": 5,
          "vitamin_b12": 0
        },
        "minerals": {
          "calcium": 11,
          "iron": 0.2,
          "magnesium": 8,
          "phosphorus": 20,
          "potassium": 195,
          "sodium": 1,
          "zinc": 0.1,
          "copper": 0.06,
          "manganese": 0.1,
          "selenium": 0
        }
      }
    }
  ],
  "total": {
    "macros": {
      "calories": 95,
      "protein": 0.5,
      "carbs": 25,
      "fat": 0.3,
      "fiber": 4.4,
      "sugar": 19
    },
    "micronutrients": {
      "vitamins": { /* same structure */ },
      "minerals": { /* same structure */ }
    }
  }
}

Rules:
- Identify all visible food items
- Estimate reasonable quantities (portions)
- Provide accurate nutritional values per standard serving
- Include comprehensive vitamins and minerals
- Calculate totals for all items
- Max 5 items per image
- If image is NOT food → return: {"items": [], "total": {"macros": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0}, "micronutrients": {"vitamins": {"vitamin_c": 0, "vitamin_a": 0, "vitamin_k": 0, "vitamin_e": 0, "thiamine": 0, "riboflavin": 0, "niacin": 0, "vitamin_b6": 0, "folate": 0, "vitamin_b12": 0}, "minerals": {"calcium": 0, "iron": 0, "magnesium": 0, "phosphorus": 0, "potassium": 0, "sodium": 0, "zinc": 0, "copper": 0, "manganese": 0, "selenium": 0}}}
- No explanations or extra text
- Use standard nutritional values in mg for vitamins/minerals
```

---

## Frontend Development Notes

1. **Authentication**: JWT tokens required for protected routes
2. **File Upload**: Use `FormData` for multipart file uploads
3. **File Validation**: 
   - Check file type (must start with `image/`)
   - Check file size (max 10MB)
   - Accept common image formats (jpg, png, gif, webp)
4. **Error Handling**: All responses follow consistent `{success, data, error}` format
5. **Image Processing**: Use `/food/debug-image` to test images before scanning
6. **Nutritional Data**: All values in standard units (calories, grams, mg for vitamins/minerals)
7. **Loading States**: Image processing can take 10-20 seconds, show appropriate loading indicators
8. **Fallback Handling**: Handle cases where AI parsing fails but the system still returns a response

---

## Testing

Use the debug endpoint to test image processing:
```bash
# Test file upload
curl -X POST "http://localhost:8000/food/debug-image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/your/image.jpg"

# Test URL
curl -X POST "http://localhost:8000/food/debug-image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image_url=https://example.com/food-image.jpg"
```

This documentation provides everything needed to build a frontend that works with direct file uploads for food scanning!
