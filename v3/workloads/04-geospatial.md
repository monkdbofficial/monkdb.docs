# Geospatial Workloads

MonkDB supports `geo_point` and `geo_shape` for location search and spatial filtering.

## Create tables

```sql
CREATE TABLE IF NOT EXISTS doc.geo_points (
  id INT PRIMARY KEY,
  location GEO_POINT
);

CREATE TABLE IF NOT EXISTS doc.geo_shapes (
  id INT PRIMARY KEY,
  region GEO_SHAPE
);
```

## Insert sample data

```sql
INSERT INTO doc.geo_points (id, location) VALUES
  (1, [5.0, 5.0]),
  (2, [-8.0, -8.0]),
  (3, [15.0, 15.0]),
  (4, [-12.0, 5.0]);

INSERT INTO doc.geo_shapes (id, region) VALUES
  (1, 'POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10))');

REFRESH TABLE doc.geo_points, doc.geo_shapes;
```

## Find points within polygon

```sql
SELECT p.id, p.location
FROM doc.geo_points p,
     doc.geo_shapes s
WHERE s.id = 1
  AND within(p.location, s.region)
ORDER BY p.id;
```

## Distance sort from a reference point

```sql
SELECT id,
       distance(location, [0.0, 0.0]) AS dist_m
FROM doc.geo_points
ORDER BY dist_m ASC;
```

## 3D + WKB context

For WKB and Z-value retention behavior, see [Geospatial WKB and 3D Retention](../features/geospatial-wkb-3d.md).

