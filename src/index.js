/**
 * Age of Empires II API - Cloudflare Worker
 * Provides data about civilizations, units, structures, and technologies
 */

// Base URL for fetching JSON files (configure to your GitHub Pages or static host)
const BASE_URL = 'https://aoe2api.teamrespawntv.com/data';

// Resource types with their JSON file names
const RESOURCES = {
  civilizations: 'civilizations.json',
  units: 'units.json',
  structures: 'structures.json',
  technologies: 'technologies.json'
};

/**
 * Normalize a name for lookup (handle underscores, hyphens, case-insensitivity)
 * Converts "chu_ko_nu" or "chu-ko-nu" or "Chu Ko Nu" to "chu ko nu"
 */
function normalizeName(name) {
  return name.toLowerCase().replace(/_/g, ' ').replace(/-/g, ' ').trim();
}

/**
 * Fetch and parse a resource JSON file
 */
async function fetchResource(resource) {
  const filename = RESOURCES[resource];
  if (!filename) {
    throw new Error(`Invalid resource: ${resource}`);
  }

  const url = `${BASE_URL}/${filename}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch ${resource}: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

/**
 * Find an item by ID (numeric) or name (string)
 * Supports underscores, hyphens, and case-insensitive name matching
 */
function findItem(items, identifier) {
  // Check if identifier is numeric (ID lookup)
  if (/^\d+$/.test(identifier)) {
    const id = parseInt(identifier, 10);
    // 1-based indexing: ID 1 = array index 0
    if (id > 0 && id <= items.length) {
      return { id: id, ...items[id - 1] };
    }
    return null;
  }

  // Name lookup with normalization
  const normalizedSearch = normalizeName(identifier);
  const index = items.findIndex(item =>
    normalizeName(item.name) === normalizedSearch
  );

  if (index !== -1) {
    return { id: index + 1, ...items[index] };
  }

  return null;
}

/**
 * Add IDs to all items in an array (1-based indexing)
 */
function addIdsToItems(items) {
  return items.map((item, index) => ({
    id: index + 1,
    ...item
  }));
}

/**
 * Create CORS headers
 */
function createCORSHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };
}

/**
 * Handle OPTIONS request for CORS preflight
 */
function handleOptions() {
  return new Response(null, {
    status: 204,
    headers: createCORSHeaders()
  });
}

/**
 * Create error response
 */
function createErrorResponse(message, status = 400) {
  return new Response(
    JSON.stringify({ error: message }, null, 2),
    {
      status: status,
      headers: createCORSHeaders()
    }
  );
}

/**
 * Create success response
 */
function createSuccessResponse(data) {
  return new Response(
    JSON.stringify(data, null, 2),
    {
      status: 200,
      headers: createCORSHeaders()
    }
  );
}

/**
 * Main request handler
 */
export default {
  async fetch(request) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return handleOptions();
    }

    // Only allow GET requests
    if (request.method !== 'GET') {
      return createErrorResponse('Method not allowed. Only GET requests are supported.', 405);
    }

    try {
      const url = new URL(request.url);
      const path = url.pathname;

      // Remove trailing slash for consistent matching
      const cleanPath = path.endsWith('/') && path !== '/' ? path.slice(0, -1) : path;

      // Route: GET / - API info
      if (cleanPath === '/' || cleanPath === '') {
        return createSuccessResponse({
          name: 'Age of Empires II API',
          version: '1.0.0',
          description: 'Free API for Age of Empires II data',
          endpoints: {
            '/civilizations': 'List all civilizations',
            '/civilization/:id': 'Get civilization by ID or name',
            '/units': 'List all units',
            '/unit/:id': 'Get unit by ID or name',
            '/structures': 'List all structures',
            '/structure/:id': 'Get structure by ID or name',
            '/technologies': 'List all technologies',
            '/technology/:id': 'Get technology by ID or name'
          },
          examples: {
            byId: '/civilization/1',
            byName: '/civilization/britons',
            withUnderscore: '/unit/chu_ko_nu',
            withHyphen: '/technology/thumb-ring'
          }
        });
      }

      // Route: GET /civilizations - List all civilizations
      if (cleanPath === '/civilizations') {
        const data = await fetchResource('civilizations');
        return createSuccessResponse({
          civilizations: addIdsToItems(data)
        });
      }

      // Route: GET /civilization/:id - Single civilization
      const civMatch = cleanPath.match(/^\/civilization\/(.+)$/);
      if (civMatch) {
        const data = await fetchResource('civilizations');
        const item = findItem(data, civMatch[1]);
        if (item) {
          return createSuccessResponse(item);
        }
        return createErrorResponse('Civilization not found', 404);
      }

      // Route: GET /units - List all units
      if (cleanPath === '/units') {
        const data = await fetchResource('units');
        return createSuccessResponse({
          units: addIdsToItems(data)
        });
      }

      // Route: GET /unit/:id - Single unit
      const unitMatch = cleanPath.match(/^\/unit\/(.+)$/);
      if (unitMatch) {
        const data = await fetchResource('units');
        const item = findItem(data, unitMatch[1]);
        if (item) {
          return createSuccessResponse(item);
        }
        return createErrorResponse('Unit not found', 404);
      }

      // Route: GET /structures - List all structures
      if (cleanPath === '/structures') {
        const data = await fetchResource('structures');
        return createSuccessResponse({
          structures: addIdsToItems(data)
        });
      }

      // Route: GET /structure/:id - Single structure
      const structMatch = cleanPath.match(/^\/structure\/(.+)$/);
      if (structMatch) {
        const data = await fetchResource('structures');
        const item = findItem(data, structMatch[1]);
        if (item) {
          return createSuccessResponse(item);
        }
        return createErrorResponse('Structure not found', 404);
      }

      // Route: GET /technologies - List all technologies
      if (cleanPath === '/technologies') {
        const data = await fetchResource('technologies');
        return createSuccessResponse({
          technologies: addIdsToItems(data)
        });
      }

      // Route: GET /technology/:id - Single technology
      const techMatch = cleanPath.match(/^\/technology\/(.+)$/);
      if (techMatch) {
        const data = await fetchResource('technologies');
        const item = findItem(data, techMatch[1]);
        if (item) {
          return createSuccessResponse(item);
        }
        return createErrorResponse('Technology not found', 404);
      }

      // 404 for unknown paths
      return createErrorResponse(
        'Not found. Available endpoints: /civilizations, /units, /structures, /technologies',
        404
      );

    } catch (error) {
      console.error('Error:', error);
      return createErrorResponse(error.message || 'Internal server error', 500);
    }
  }
};
