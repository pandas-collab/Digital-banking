# GET /api/transfers Endpoint Documentation

## Overview
This endpoint retrieves paginated transfer history for authenticated users.

## Endpoint Details
- **Path**: `/api/transfers`
- **Method**: GET
- **Authentication**: Bearer token required in Authorization header
- **Content-Type**: application/json

## Query Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 0 | Zero-based page number |
| `size` | int | 10 | Items per page (max: 100) |

## Request Headers
