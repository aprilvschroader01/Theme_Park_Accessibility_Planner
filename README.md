# Theme Park Accessibility Planner

Using AI and Azure OpenAI, this application helps guests with dietary restrictions and disabilities better navigate theme parks.

## 🎯 Project Vision

**Phase 1 (Current): Dietary Planning**
- Simple web app where users input their dietary needs
- Flexible plan showing recommended menu items organized by park section
- Uses AI to analyze theme park menus and provide tailored recommendations

**Phase 2 (Upcoming): Disability Accessibility**
- AI agent to provide ride accessibility accommodations
- Integrate Foundry IQ MCP server with real-time data sources
- Combined plan showing dietary + accessibility info per park section

**Phase 3 (Future): Advanced Features**
- Multi-agent orchestration with Foundry
- Real-time updates from theme park systems
- Advanced scheduling and planning

## 🏗️ Project Structure

```
Theme_Park_Accessibility_Planner/
├── app/
│   ├── agents/
│   │   ├── dietary_agent.py              # Azure OpenAI-powered agent
│   │   └── dietary_agent_instructions.md # Agent system prompt
│   ├── templates/
│   │   ├── index.html                    # Home page
│   │   └── results.html                  # Results page
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css                 # Styling
│   │   └── js/
│   │       └── app.js                    # Frontend logic
│   ├── main.py                           # Flask application
│   ├── config.py                         # Configuration
│   ├── database.py                       # SQLite setup
│   └── __init__.py
├── requirements.txt                      # Python dependencies
├── .env.example                          # Environment template
└── README.md                             # This file
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Azure OpenAI API key and endpoint
- Git

### 2. Clone & Setup

```bash
cd Theme_Park_Accessibility_Planner
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI details:

```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-35-turbo  # or your deployment name
AZURE_API_VERSION=2024-02-01
```

**Getting Azure OpenAI Credentials:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Create/navigate to Azure OpenAI Service
3. Deploy a model (e.g., gpt-3.5-turbo)
4. Copy API key and endpoint from "Keys and Endpoint"
5. Paste into `.env`

### 4. Run the Application

```bash
python app/main.py
```

The app will be available at `http://localhost:5000`

## 💻 Usage

1. **Visit Home Page**: `http://localhost:5000`
2. **Select Theme Park**: Choose from Magic Kingdom, EPCOT, Hollywood Studios, etc.
3. **Enter Dietary Needs**:
   - Dietary Restrictions (e.g., vegan, gluten-free)
   - Allergens to Avoid (e.g., peanuts, shellfish)
4. **Generate Plan**: Click "Generate Plan"
5. **View Results**: AI-powered recommendations organized by park section

### Example Input

- **Park**: Magic Kingdom
- **Dietary Restrictions**: vegan, gluten-free
- **Allergens**: peanuts, tree nuts

### Example Output

```
MAGIC KINGDOM - ADVENTURELAND
Restaurants: Aloha Isle, Sunshine Tree Terrace, Kusafiri Coffee Shop

Recommended Items:
- Aloha Isle:
  - POG Juice - Naturally vegan, dairy-free
  - Warm Cinnamon Roll - [Check ingredients]
  
- Sunshine Tree Terrace:
  - Orange Juice - Simple, no allergens
  - Florida Orange Slush - Citrus-based
```

## 🔧 Technology Stack

- **Backend**: Flask (Python web framework)
- **AI/LLM**: Azure OpenAI Service (gpt-3.5-turbo)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: RESTful endpoints

## 📊 Database Schema

### queries
- `id`: Primary key
- `park_name`: Theme park name
- `query_text`: Original query
- `dietary_restrictions`: User restrictions
- `allergens`: Allergens to avoid
- `created_at`: Timestamp

### results
- `id`: Primary key
- `query_id`: Foreign key to queries
- `park_section`: Land/section in park
- `restaurant_name`: Restaurant name
- `menu_items`: Recommended items
- `dietary_notes`: Allergen/safety notes
- `result_json`: Full AI response

### accessibility_accommodations (Phase 2)
- `id`: Primary key
- `park_name`: Theme park
- `land`: Land/section
- `ride_name`: Ride name
- `disability_type`: Type of disability
- `accommodation_details`: How it's accommodated

## 🤖 Dietary Agent Details

The dietary agent uses Azure OpenAI with specialized prompts to:

1. **Understand** user allergen sensitivities and dietary needs
2. **Source** accurate menus from theme parks
3. **Analyze** menu items comprehensively
4. **Validate** all recommendations before presenting
5. **Organize** output by park section with restaurant details

See `app/agents/dietary_agent_instructions.md` for the full system prompt.

## 🔄 API Endpoints

### `GET /`
Home page with query form

### `POST /api/generate-plan`
Generate a dietary plan

**Request**:
```json
{
  "park_name": "Magic Kingdom",
  "dietary_restrictions": "vegan, gluten-free",
  "allergens": "peanuts, shellfish"
}
```

**Response**:
```json
{
  "success": true,
  "query_id": 1,
  "park": "Magic Kingdom",
  "plan": "MAGIC KINGDOM - ADVENTURELAND...",
  "dietary_restrictions": ["vegan", "gluten-free"],
  "allergens": ["peanuts", "shellfish"]
}
```

### `GET /api/query/<query_id>`
Retrieve a previously generated plan

### `GET /results/<query_id>`
View results page for a query

## 📝 Environment Variables

```bash
# Azure OpenAI
AZURE_OPENAI_API_KEY       # Your Azure OpenAI API key
AZURE_OPENAI_ENDPOINT      # Your Azure OpenAI endpoint
AZURE_DEPLOYMENT_NAME      # Model deployment name (default: gpt-35-turbo)
AZURE_API_VERSION          # API version (default: 2024-02-01)

# Flask
FLASK_ENV                  # development or production
DEBUG                      # True or False

# Database
DATABASE_PATH              # Path to SQLite database (default: ./data/app.db)
```

## 🔐 Security Notes

- **Never commit `.env`** file to GitHub - it contains sensitive credentials
- `.env.example` shows the required variables without values
- Users should create their own `.env` with their Azure credentials
- Store API keys securely and rotate regularly

## 🚧 Next Steps - Phase 2

1. **Create Disability Agent**
   - Analyze ride accessibility policies
   - Map disabilities to accommodations
   - Include in output alongside dietary info

2. **Integrate Foundry IQ MCP Server**
   - Connect to real-time theme park data
   - Reduce hallucination with verified sources
   - Improve accuracy of recommendations

3. **Multi-Agent Orchestration**
   - Coordinate between dietary and disability agents
   - Unified output format

## 🐛 Troubleshooting

### "Azure OpenAI credentials not found"
- Check `.env` file exists in project root
- Verify `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` are set
- Check for typos in environment variable names

### "Failed to generate plan"
- Verify Azure OpenAI API is accessible
- Check API key is still valid
- Ensure model deployment exists
- Check Azure quota/capacity

### "Database error"
- Verify `data/` directory has write permissions
- Check `DATABASE_PATH` is correctly set

## 📚 Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [OpenAI Python Client](https://github.com/openai/openai-python)

## 👥 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT License - Feel free to use for learning and hackathons

---

**Made with ❤️ for theme park accessibility** 
