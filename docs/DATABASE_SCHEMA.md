# Database Schema and Indexes

## URL Document Schema

The `urls` collection in MongoDB stores shortened URL information with the following structure:

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | ObjectId | Yes | MongoDB auto-generated unique identifier |
| `url_hash` | String | Yes | Unique hash for the shortened URL (indexed, unique) |
| `actual_url` | String | Yes | The original long URL |
| `user_id` | Integer | Yes | ID of the user who created the URL (indexed) |
| `user_name` | String | Yes | Name of the user who created the URL (indexed) |
| `user_role` | String | Yes | Role of the user |
| `group_guid` | String | Yes | Group identifier for the URL |
| `created_at` | String | Yes | Timestamp when URL was created (indexed) |
| `updated_at` | String | Yes | Timestamp when URL was last updated |
| `last_redirected_at` | String | Optional | Timestamp when URL was last redirected (indexed) |
| `hits` | Integer | Yes | Number of times the URL was redirected (default: 0, indexed) |
| `has_custom_domain` | Boolean | Yes | Whether URL has a custom domain (default: false) |
| `custom_domain` | String | Optional | Custom domain if applicable |

## Indexes

The following indexes are created automatically when the application starts or can be created manually using the migration script.

### Single Field Indexes

1. **url_hash_idx** (Unique)
   - Fields: `url_hash` (ascending)
   - Purpose: Fast lookups by URL hash
   - Unique: Yes

2. **user_id_idx**
   - Fields: `user_id` (ascending)
   - Purpose: Filter queries by user ID

3. **user_name_idx**
   - Fields: `user_name` (ascending)
   - Purpose: Filter queries by user name

4. **created_at_idx**
   - Fields: `created_at` (descending)
   - Purpose: Sort by latest shortened URLs

5. **last_redirected_at_idx**
   - Fields: `last_redirected_at` (descending)
   - Purpose: Sort by latest redirected URLs

6. **hits_idx**
   - Fields: `hits` (descending)
   - Purpose: Sort by redirect count (most popular first)

### Compound Indexes

These compound indexes optimize common query patterns that filter by user and sort by different fields:

7. **user_id_hits_idx**
   - Fields: `user_id` (ascending), `hits` (descending)
   - Purpose: Filter by user_id and sort by redirect count

8. **user_name_hits_idx**
   - Fields: `user_name` (ascending), `hits` (descending)
   - Purpose: Filter by user_name and sort by redirect count

9. **user_id_created_at_idx**
   - Fields: `user_id` (ascending), `created_at` (descending)
   - Purpose: Filter by user_id and sort by creation date

10. **user_name_created_at_idx**
    - Fields: `user_name` (ascending), `created_at` (descending)
    - Purpose: Filter by user_name and sort by creation date

11. **user_id_last_redirected_at_idx**
    - Fields: `user_id` (ascending), `last_redirected_at` (descending)
    - Purpose: Filter by user_id and sort by last redirect time

12. **user_name_last_redirected_at_idx**
    - Fields: `user_name` (ascending), `last_redirected_at` (descending)
    - Purpose: Filter by user_name and sort by last redirect time

## Index Creation

### Automatic Creation

Indexes are automatically created when the `DatabaseManager` is initialized (on application startup).

### Manual Creation

To manually create indexes, run the migration script:

```bash
python migerations/create_indexes.py
```

### Viewing Indexes

You can view all indexes using MongoDB shell:

```javascript
db.urls.getIndexes()
```

Or programmatically:

```python
from config import config
indexes = config.backend.get_index_info()
print(indexes)
```

## Query Optimization

The indexes are designed to optimize the following query patterns:

1. **Lookup by hash**: Uses `url_hash_idx` (unique index)
2. **Filter by user + sort by hits**: Uses compound indexes `user_id_hits_idx` or `user_name_hits_idx`
3. **Filter by user + sort by created_at**: Uses compound indexes `user_id_created_at_idx` or `user_name_created_at_idx`
4. **Filter by user + sort by last_redirected_at**: Uses compound indexes `user_id_last_redirected_at_idx` or `user_name_last_redirected_at_idx`
5. **Sort by hits (all users)**: Uses `hits_idx`
6. **Sort by created_at (all users)**: Uses `created_at_idx`
7. **Sort by last_redirected_at (all users)**: Uses `last_redirected_at_idx`

## Performance Considerations

- All indexes are created with `background=True` to avoid blocking database operations
- Compound indexes follow the rule: equality filters first, then sort fields
- The `url_hash` index is unique to prevent duplicate shortened URLs
- Indexes are checked on startup and only created if they don't already exist

