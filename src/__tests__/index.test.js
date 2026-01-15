import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock civilization data
const mockCivilizations = [
  {
    name: 'Aztecs',
    expansion: 'The Conquerors',
    army_type: 'Infantry and Monk',
    unique_unit: 'Jaguar Warrior',
    unique_tech: 'Garland Wars',
    team_bonus: 'Relics generate +33% gold',
    civilization_bonus: ['Villagers carry +5', 'Military units created 15% faster']
  },
  {
    name: 'Britons',
    expansion: 'Age of Kings',
    army_type: 'Foot Archer',
    unique_unit: 'Longbowman',
    unique_tech: 'Yeomen',
    team_bonus: 'Archery Ranges work 20% faster',
    civilization_bonus: ['Town Centers cost -50% wood upon reaching the Castle Age']
  },
  {
    name: 'Chu Ko Nu Masters',
    expansion: 'Test',
    army_type: 'Test',
    unique_unit: 'Test',
    unique_tech: 'Test',
    team_bonus: 'Test',
    civilization_bonus: ['Test']
  }
];

// Mock unit data
const mockUnits = [
  {
    name: 'Archer',
    description: 'Quick and light',
    expansion: 'Age of Kings',
    age: 'Feudal',
    created_in: 'Archery Range',
    cost: { Wood: 25, Gold: 45 },
    hit_points: 30,
    attack: 4
  },
  {
    name: 'Chu Ko Nu',
    description: 'Chinese unique unit',
    expansion: 'Age of Kings',
    age: 'Castle',
    created_in: 'Castle',
    cost: { Wood: 40, Gold: 35 },
    hit_points: 45,
    attack: 8
  },
  {
    name: 'Teutonic Knight',
    description: 'Teuton unique unit',
    expansion: 'Age of Kings',
    age: 'Castle',
    created_in: 'Castle',
    cost: { Food: 85, Gold: 40 },
    hit_points: 100,
    attack: 17
  }
];

// Mock structure data
const mockStructures = [
  {
    name: 'Barracks',
    expansion: 'Age of Kings',
    age: 'Dark',
    cost: { Wood: 175 },
    hit_points: 1200
  },
  {
    name: 'Town Center',
    expansion: 'Age of Kings',
    age: 'Dark',
    cost: { Wood: 275, Stone: 100 },
    hit_points: 2400
  }
];

// Mock technology data
const mockTechnologies = [
  {
    name: 'Loom',
    expansion: 'Age of Kings',
    age: 'Dark',
    develops_in: 'Town Center',
    cost: { Gold: 50 },
    description: 'Villagers +15 hit points'
  },
  {
    name: 'Thumb Ring',
    expansion: 'Age of Kings',
    age: 'Castle',
    develops_in: 'Archery Range',
    cost: { Food: 300, Wood: 250 },
    description: 'Faster reload time and 100% accuracy'
  }
];

// Mock fetch globally
global.fetch = vi.fn();

// Import the worker after setting up mocks
let worker;

describe('Age of Empires II API', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    return import('../index.js').then(module => {
      worker = module.default;
    });
  });

  describe('CORS Headers', () => {
    it('should handle OPTIONS requests with CORS headers', async () => {
      const request = new Request('https://api.example.com/civilizations', {
        method: 'OPTIONS',
      });

      const response = await worker.fetch(request);

      expect(response.status).toBe(204);
      expect(response.headers.get('Access-Control-Allow-Origin')).toBe('*');
      expect(response.headers.get('Access-Control-Allow-Methods')).toBe('GET, OPTIONS');
      expect(response.headers.get('Access-Control-Allow-Headers')).toBe('Content-Type');
    });

    it('should include CORS headers in all responses', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);

      expect(response.headers.get('Access-Control-Allow-Origin')).toBe('*');
      expect(response.headers.get('Content-Type')).toBe('application/json');
    });
  });

  describe('Method Validation', () => {
    it('should reject POST requests', async () => {
      const request = new Request('https://api.example.com/civilizations', {
        method: 'POST',
      });

      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(405);
      expect(data.error).toContain('Method not allowed');
    });

    it('should reject PUT requests', async () => {
      const request = new Request('https://api.example.com/civilizations', {
        method: 'PUT',
      });

      const response = await worker.fetch(request);
      expect(response.status).toBe(405);
    });

    it('should reject DELETE requests', async () => {
      const request = new Request('https://api.example.com/civilizations', {
        method: 'DELETE',
      });

      const response = await worker.fetch(request);
      expect(response.status).toBe(405);
    });
  });

  describe('Root Endpoint (/)', () => {
    it('should return API information', async () => {
      const request = new Request('https://api.example.com/');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Age of Empires II API');
      expect(data.version).toBe('1.0.0');
      expect(data.endpoints).toBeDefined();
      expect(data.endpoints).toHaveProperty('/civilizations');
      expect(data.endpoints).toHaveProperty('/units');
      expect(data.endpoints).toHaveProperty('/structures');
      expect(data.endpoints).toHaveProperty('/technologies');
    });

    it('should include examples in response', async () => {
      const request = new Request('https://api.example.com/');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(data.examples).toBeDefined();
      expect(data.examples.byId).toBeDefined();
      expect(data.examples.byName).toBeDefined();
    });
  });

  describe('Civilizations Endpoints', () => {
    it('should return all civilizations with IDs', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.civilizations).toBeDefined();
      expect(data.civilizations.length).toBe(3);
      expect(data.civilizations[0].id).toBe(1);
      expect(data.civilizations[0].name).toBe('Aztecs');
    });

    it('should find civilization by numeric ID', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/1');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.id).toBe(1);
      expect(data.name).toBe('Aztecs');
    });

    it('should find civilization by name (case insensitive)', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/britons');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.id).toBe(2);
      expect(data.name).toBe('Britons');
    });

    it('should find civilization by name with uppercase', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/BRITONS');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Britons');
    });

    it('should return 404 for non-existent civilization', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/nonexistent');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(404);
      expect(data.error).toContain('not found');
    });

    it('should return 404 for out-of-range ID', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/999');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(404);
    });

    it('should handle trailing slash', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilizations/');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.civilizations).toBeDefined();
    });
  });

  describe('Units Endpoints', () => {
    it('should return all units with IDs', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockUnits,
        });
      });

      const request = new Request('https://api.example.com/units');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.units).toBeDefined();
      expect(data.units.length).toBe(3);
      expect(data.units[0].id).toBe(1);
    });

    it('should find unit by name with underscores', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockUnits,
        });
      });

      const request = new Request('https://api.example.com/unit/chu_ko_nu');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Chu Ko Nu');
    });

    it('should find unit by name with hyphens', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockUnits,
        });
      });

      const request = new Request('https://api.example.com/unit/teutonic-knight');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Teutonic Knight');
    });

    it('should find unit by numeric ID', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockUnits,
        });
      });

      const request = new Request('https://api.example.com/unit/1');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.id).toBe(1);
      expect(data.name).toBe('Archer');
    });
  });

  describe('Structures Endpoints', () => {
    it('should return all structures with IDs', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockStructures,
        });
      });

      const request = new Request('https://api.example.com/structures');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.structures).toBeDefined();
      expect(data.structures.length).toBe(2);
    });

    it('should find structure by name', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockStructures,
        });
      });

      const request = new Request('https://api.example.com/structure/barracks');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Barracks');
    });

    it('should find structure by name with spaces (underscore format)', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockStructures,
        });
      });

      const request = new Request('https://api.example.com/structure/town_center');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Town Center');
    });
  });

  describe('Technologies Endpoints', () => {
    it('should return all technologies with IDs', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockTechnologies,
        });
      });

      const request = new Request('https://api.example.com/technologies');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.technologies).toBeDefined();
      expect(data.technologies.length).toBe(2);
    });

    it('should find technology by name', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockTechnologies,
        });
      });

      const request = new Request('https://api.example.com/technology/loom');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Loom');
    });

    it('should find technology by name with hyphen', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockTechnologies,
        });
      });

      const request = new Request('https://api.example.com/technology/thumb-ring');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.name).toBe('Thumb Ring');
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for unknown paths', async () => {
      const request = new Request('https://api.example.com/unknown');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(404);
      expect(data.error).toContain('Not found');
    });

    it('should handle fetch errors gracefully', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toBeDefined();
    });

    it('should handle 404 from data file fetch', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      });

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toContain('Failed to fetch');
    });

    it('should handle invalid JSON response', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => {
            throw new Error('Invalid JSON');
          },
        });
      });

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toBeDefined();
    });

    it('should return 404 for ID 0', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/0');
      const response = await worker.fetch(request);

      expect(response.status).toBe(404);
    });
  });

  describe('Response Format', () => {
    it('should return properly formatted JSON', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilization/1');
      const response = await worker.fetch(request);
      const data = await response.json();

      expect(data).toMatchObject({
        id: expect.any(Number),
        name: expect.any(String),
        expansion: expect.any(String),
      });
    });

    it('should return formatted JSON with indentation', async () => {
      global.fetch.mockImplementation(() => {
        return Promise.resolve({
          ok: true,
          json: async () => mockCivilizations,
        });
      });

      const request = new Request('https://api.example.com/civilizations');
      const response = await worker.fetch(request);
      const text = await response.text();

      // Check that it's valid JSON
      const data = JSON.parse(text);
      expect(data.civilizations).toBeDefined();

      // Check that it's formatted (contains newlines from indentation)
      expect(text).toContain('\n');
    });
  });
});
