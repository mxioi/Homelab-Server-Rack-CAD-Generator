# Adjustment Examples

## 1) Move U-mounted devices to true front plane

Pattern:
- Compute front mount plane once.
- Translate UDM/RPS/patch panel using that plane.
- Keep ear geometry and standoffs co-located.

Pseudo-pattern:

```python
front_face = -RACK["outer_width"] / 2
udm = udm.translate((0, front_face + depth / 2, z))
```

## 2) Fix bottom shelf collisions

Order of operations:
1. Place tallest item first (NAS or Time Capsule)
2. Place laptop last
3. Rotate laptop footprint by 90 degrees if needed
4. Push deep items rearward until clear

## 3) Reduce clutter collisions on upper shelf

Use a left-to-right map and place each object with small spacing margins:
- Joy-Cons
- Switch dock
- Sky box
- Mini PC
- Hue bridge
- Wii and Wii PSU

Recommended spacing:
- 5 to 15 mm side clearance between envelope boxes

## 4) Keep visual mount realism

When users say equipment "looks in the air":
- add standoff blocks at ear positions
- add visible U-hole marker geometry if requested
- confirm patch panel and 1U devices share front mount plane
