# Age of Empires II API

A free API for Age of Empires II game data, providing information about civilizations, units, structures, and technologies.

Built with Cloudflare Workers for fast, serverless delivery.

## Base URL

```
https://aoe2api.teamrespawntv.com
```

## Endpoints

### Root
```
GET /
```
Returns API information and available endpoints.

### Civilizations

```
GET /civilizations
```
Returns a list of all civilizations.

```
GET /civilization/:id
```
Returns a single civilization. The `:id` parameter can be:
- A numeric ID (1-33)
- A civilization name (case-insensitive, underscores or hyphens accepted)

**Examples:**
- `/civilization/1`
- `/civilization/britons`
- `/civilization/byzantines`

### Units

```
GET /units
```
Returns a list of all units.

```
GET /unit/:id
```
Returns a single unit by ID or name.

**Examples:**
- `/unit/1`
- `/unit/archer`
- `/unit/chu_ko_nu`
- `/unit/teutonic-knight`

### Structures

```
GET /structures
```
Returns a list of all structures.

```
GET /structure/:id
```
Returns a single structure by ID or name.

**Examples:**
- `/structure/1`
- `/structure/barracks`
- `/structure/town_center`

### Technologies

```
GET /technologies
```
Returns a list of all technologies.

```
GET /technology/:id
```
Returns a single technology by ID or name.

**Examples:**
- `/technology/1`
- `/technology/loom`
- `/technology/thumb-ring`

## Response Format

All responses are JSON with pretty-printing enabled.

### List Response
```json
{
  "civilizations": [
    {
      "id": 1,
      "name": "Aztecs",
      "expansion": "The Conquerors",
      "army_type": "Infantry and Monk",
      "unique_unit": "Jaguar Warrior",
      "unique_tech": "Garland Wars",
      "team_bonus": "Relics generate +33% gold",
      "civilization_bonus": [
        "Villagers carry +5",
        "Military units created 15% faster",
        "+5 Monk hit points for each Monastery technology",
        "Loom free"
      ]
    }
  ]
}
```

### Single Item Response
```json
{
  "id": 2,
  "name": "Britons",
  "expansion": "Age of Kings",
  "army_type": "Foot Archer",
  "unique_unit": "Longbowman",
  "unique_tech": "Yeomen",
  "team_bonus": "Archery Ranges work 20% faster",
  "civilization_bonus": [
    "Town Centers cost -50% wood upon reaching the Castle Age",
    "Foot archers (excluding Skirmishers) have +1 range in Castle Age and +1 in Imperial Age (for +2 total)",
    "Shepherds work 25% faster"
  ]
}
```

### Error Response
```json
{
  "error": "Civilization not found"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `405` - Method Not Allowed
- `500` - Internal Server Error

## Data Models

### Civilization
- `id` - Unique identifier
- `name` - Civilization name
- `expansion` - Game expansion
- `army_type` - Primary army focus
- `unique_unit` - Unique unit(s)
- `unique_tech` - Unique technology/technologies
- `team_bonus` - Team bonus
- `civilization_bonus` - List of civilization bonuses

### Unit
- `id` - Unique identifier
- `name` - Unit name
- `description` - Unit description
- `expansion` - Game expansion
- `age` - Available in age (Dark, Feudal, Castle, Imperial)
- `created_in` - Building that creates the unit
- `cost` - Resource cost object
- `build_time` - Build time in seconds
- `reload_time` - Attack reload time
- `attack_delay` - Attack delay
- `movement_rate` - Movement speed
- `line_of_sight` - Vision range
- `hit_points` - Health
- `range` - Attack range
- `attack` - Attack damage
- `armor` - Armor values (melee/pierce)
- `attack_bonus` - Attack bonuses
- `armor_bonus` - Armor bonuses
- `search_radius` - Search radius
- `accuracy` - Attack accuracy
- `blast_radius` - Splash damage radius

### Structure
- `id` - Unique identifier
- `name` - Structure name
- `expansion` - Game expansion
- `age` - Available in age
- `cost` - Resource cost object
- `build_time` - Build time in seconds
- `hit_points` - Health
- `line_of_sight` - Vision range
- `armor` - Armor values (melee/pierce)
- `range` - Attack range (if applicable)
- `reload_time` - Attack reload time (if applicable)
- `attack` - Attack damage (if applicable)
- `special` - Special properties

### Technology
- `id` - Unique identifier
- `name` - Technology name
- `expansion` - Game expansion
- `age` - Required age
- `develops_in` - Building that researches the tech
- `cost` - Resource cost object
- `build_time` - Research time in seconds
- `applies_to` - Affected units/buildings
- `description` - Technology effect

## Development

### Prerequisites
- Node.js
- Cloudflare account (for deployment)

### Setup
```bash
npm install
```

### Local Development
```bash
npm run dev
```
The API will be available at `http://localhost:8787`

### Testing
```bash
npm test
```

### Deployment
```bash
npx wrangler login
npm run deploy
```

## License

MIT
